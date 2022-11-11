# coding: utf-8
from requests_to_curl import parse
import re
import unittest

import requests


class Test(unittest.TestCase):
    def test_empty_data(self):
        r = requests.post(
            "http://google.ru",
            headers={"user-agent": "mytest"},
        )
        self.assertEqual(
            parse(r.request, return_it=True, print_it=False),
            (
                "curl -X POST "
                "-H 'Accept: */*' "
                "-H 'Accept-Encoding: gzip, deflate' "
                "-H 'Connection: keep-alive' "
                "-H 'user-agent: mytest' "
                "http://google.ru/"
            )
        )
    
    def test_response(self):
        r = requests.post(
            "http://google.ru",
            headers={"user-agent": "mytest"},
        )
        self.assertEqual(
            parse(r, return_it=True, print_it=False),
            (
                "curl -X POST "
                "-H 'Accept: */*' "
                "-H 'Accept-Encoding: gzip, deflate' "
                "-H 'Connection: keep-alive' "
                "-H 'user-agent: mytest' "
                "http://google.ru:80/"
            )
        )


    def test_ok(self):
        r = requests.get(
            "http://google.ru",
            data={"a": "b"},
            cookies={"foo": "bar"},
            headers={"user-agent": "mytest"},
        )
        self.assertEqual(
            parse(r.request, return_it=True, print_it=False),
            (
                "curl -X GET "
                "-H 'Accept: */*' "
                "-H 'Accept-Encoding: gzip, deflate' "
                "-H 'Connection: keep-alive' "
                "-H 'Content-Type: application/x-www-form-urlencoded' "
                "-H 'Cookie: foo=bar' "
                "-H 'user-agent: mytest' "
                "-d a=b http://google.ru/"
            )
        )


    def test_prepare_request(self):
        request = requests.Request(
            'GET', "http://google.ru",
            headers={"user-agent": "UA"},
        )

        self.assertEqual(
            parse(request.prepare(), return_it=True, print_it=False),
            (
                "curl -X GET "
                "-H 'user-agent: UA' "
                "http://google.ru/"
            )
        )


    def test_compressed(self):
        request = requests.Request(
            'GET', "http://google.ru",
            headers={"user-agent": "UA"},
        )
        self.assertEqual(
            parse(request.prepare(), compressed=True, return_it=True, print_it=False),
            "curl -X GET -H 'user-agent: UA' --compressed http://google.ru/",
        )


    def test_verify(self):
        request = requests.Request(
            'GET', "http://google.ru",
            headers={"user-agent": "UA"},
        )
        self.assertEqual(
            parse(request.prepare(), verify=False, return_it=True, print_it=False),
            "curl -X GET -H 'user-agent: UA' --insecure http://google.ru/",
        )


    def test_post_json(self):
        data = {'foo': 'bar'}
        url = 'https://httpbin.org/post'

        r = requests.Request('POST', url, json=data)
        curlified = parse(r.prepare(), return_it=True, print_it=False)

        self.assertEqual(curlified, (
            "curl -X POST "
            "-H 'Content-Type: application/json' "
            "-d '{\"foo\": \"bar\"}' https://httpbin.org/post"
        ))


    def test_post_csv_file(self):
        r = requests.Request(
            method='POST',
            url='https://httpbin.org/post',
            files={'file': open('data.csv', 'r')},
            headers={'User-agent': 'UA'}
        )

        curlified = parse(r.prepare(), return_it=True, print_it=False)
        boundary = re.search(r'boundary=(\w+)', curlified).group(1)
        expected = (
            'curl -X POST'
            f' -H \'Content-Type: multipart/form-data; boundary={boundary}\''
            ' -H \'User-agent: UA\''
            f' -d \'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="data.csv"\r\n\r\n'
            '"Id";"Title";"Content"\n'
            '1;"Simple Test";"Ici un test d\'"\'"\'échappement de simple quote"\n'
            '2;"UTF-8 Test";"ăѣ𝔠ծềſģȟᎥ𝒋ǩľḿꞑȯ𝘱𝑞𝗋𝘴ȶ𝞄𝜈ψ𝒙𝘆𝚣1234567890!@#$%^&*()-_=+;:\'"\'"\'",[]{}<.>/?~𝘈Ḇ𝖢𝕯٤ḞԍНǏ𝙅ƘԸⲘ𝙉০Ρ𝗤Ɍ𝓢ȚЦ𝒱Ѡ𝓧ƳȤѧᖯć𝗱ễ𝑓𝙜Ⴙ𝞲𝑗𝒌ļṃŉо𝞎𝒒ᵲꜱ𝙩ừ𝗏ŵ𝒙𝒚ź"'
            f'\r\n--{boundary}--\r\n\''
            ' https://httpbin.org/post'
        )
        self.assertEqual(curlified, expected)


unittest.main()
