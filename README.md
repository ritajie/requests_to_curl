# requests_to_curl - convert python requests request object to cURL command

## Installation
```sh
pip install requests_to_curl
```

## Usage

```py
import requests_to_curl
import requests

response = requests.get("http://google.ru")
print(requests_to_curl.parse(response.request))
# curl -X 'GET' -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.18.4' 'http://www.google.ru/'
```
