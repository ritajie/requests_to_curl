# coding: utf-8

from copy import deepcopy
import requests

# Use `shlex.quote` for Python 3, and `pipes.quote` for Python 2
try:
    from shlex import quote
except ImportError:
    from pipes import quote


HEADER_BLOCKLIST = {
    "Content-Length",
}


def parse(request_or_response, compressed=False, verify=True, return_it=False, print_it=True):
    """
    Args:
        request_or_response: requests.models.Request | requests.models.Response
        return_it: bool - If True, return the generated curl string; otherwise, return None.
        print_it: bool - If True, print the generated curl string to stdout.

    Returns:
        str or None: The generated curl command if return_it is True; otherwise, None.

    Prints:
        The generated curl command if print_it is True.
    """

    def _build_url(connection_pool, request):
        scheme = connection_pool.scheme if connection_pool.scheme in ("http", "https") else "http"
        host = f"[{connection_pool.host}]" if ":" in connection_pool.host else connection_pool.host
        return f"{scheme}://{host}:{connection_pool.port}{request.path_url}"

    if isinstance(request_or_response, requests.models.Response):
        request = deepcopy(request_or_response.request)
        connection_pool = request_or_response.connection.get_connection_with_tls_context(request, verify)
        request.url = _build_url(connection_pool, request)
    elif isinstance(request_or_response, (requests.models.Request, requests.models.PreparedRequest)):
        request = deepcopy(request_or_response)
    else:
        raise TypeError(f"`parse` needs a request or response, not {type(request_or_response).__name__}")

    curl_string = _parse_request(request=request, compressed=compressed, verify=verify)

    if print_it:
        print(curl_string)
    if return_it:
        return curl_string


def _parse_request(request, compressed=False, verify=True):
    parts = [("curl", None), ("-X", request.method)]

    # Add headers, skipping blocklisted ones
    headers = [
        ("-H", f"{k}: {v}")
        for k, v in sorted(request.headers.items())
        if k not in HEADER_BLOCKLIST
    ]
    parts.extend(headers)

    # Add body if present
    if request.body:
        body = request.body.decode("utf-8") if isinstance(request.body, bytes) else request.body
        parts.append(("-d", body))

    # Add optional flags
    if compressed:
        parts.append(("--compressed", None))
    if not verify:
        parts.append(("--insecure", None))

    # Add the request URL
    parts.append((None, request.url))

    # Flatten parts and return the command string
    flat_parts = [quote(k) for k, v in parts if k] + [quote(v) for k, v in parts if v]

    return " ".join(flat_parts)
