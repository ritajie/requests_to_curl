# RequestsToCurl
Convert python requests object to cURL command.

This repository is improved based on [curlify](https://github.com/ofw/curlify). Since curlify does not seem to be updated anymore, no one responded to the PR I provided, so this repository was created.

## Installation
```sh
pip install requests_to_curl
```

## Usage

```py
>>> import curl
>>> import requests
>>> response = requests.get("https://lulaolu.com")
>>> curl.parse(response)
curl -X GET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.27.1' https://lulaolu.com:443/
```

you can also use `r2c` or `requests_to_curl` instead of `curl`
```python3
>>> import r2c
>>> r2c.parse(response)  # ok!
>>>
>>> import requests_to_curl
>>> requests_to_curl.parse(response)  # ok!
```
