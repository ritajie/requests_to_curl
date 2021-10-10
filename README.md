# RequestsToCurl
Convert python requests object to cURL command.

This repository is improved based on [curlify](https://github.com/ofw/curlify). Since curlify does not seem to be updated anymore, no one responded to the PR I provided, so this repository was created.

## Installation
```sh
pip install requests_to_curl
```

## Usage

```py
>>> import requests_to_curl
>>> import requests
>>> response = requests.get("https://lulaolu.com")
>>> requests_to_curl.parse(response)
"curl -X GET -H 'Accept: */*' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'User-Agent: python-requests/2.26.0' https://lulaolu.com:443/"
```

For convenience, you can also use `r2c` or `curl` instead of `requests_to_curl`
```python3
>>> import r2c
>>> r2c.parse(response)  # ok!
>>>
>>> import curl
>>> curl.parse(response)  # ok!
```
