# coding: utf-8
import sys
from copy import deepcopy

import requests

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote


def parse(request_or_response, compressed=False, verify=True):
    """
    Args:
        request_or_response: requests.models.Request|requests.models.Response

    Print:
        curl command
    """
    if isinstance(request_or_response, requests.models.Response):
        request = deepcopy(request_or_response.request)
        connection_pool = request_or_response.connection.get_connection(request.url)
        http_scheme = connection_pool.scheme
        if http_scheme not in ('http', 'https'):
            http_scheme = 'http'
        request.url = '{scheme}://{host}:{port}{path_url}'.format(
            scheme=http_scheme, host=connection_pool.host, port=connection_pool.port, path_url=request.path_url
        )
    elif isinstance(request_or_response, (requests.models.Request, requests.models.PreparedRequest)):
        request = deepcopy(request_or_response)
    else:
        raise Exception("`parse` needs a request or response, not {}".format(type(request_or_response)))

    print(_parse_request(request=request, compressed=compressed, verify=verify))


def _parse_request(request, compressed=False, verify=True):
    parts = [('curl', None), ('-X', request.method)]
    for k, v in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]
    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-d', body)]
    if compressed:
        parts += [('--compressed', None)]
    if not verify:
        parts += [('--insecure', None)]
    parts += [(None, request.url)]
    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))
    return ' '.join(flat_parts)
