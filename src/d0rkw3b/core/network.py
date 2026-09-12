"""Explicit, bounded public HTTP access. Importing this module sends nothing."""

import http.client
import ipaddress
import socket
import ssl
from urllib.parse import urlsplit


class NetworkPolicyError(ValueError):
    """Destination is outside the public HTTP capability."""


def request(url, *, method="HEAD", timeout=5, max_bytes=1_048_576):
    """One request, no redirects, cookies, proxies, retries, or implicit credentials.

    Resolve once and pin the validated public address to prevent DNS rebinding.
    Socket operations are timed out; DNS resolution uses the OS resolver policy.
    """
    parts = urlsplit(url)
    host = parts.hostname
    if (
        parts.scheme not in ("http", "https")
        or not host
        or parts.username is not None
        or parts.password is not None
        or host.lower().rstrip(".").endswith(".onion")
        or any(c.isspace() or ord(c) < 32 for c in url)
    ):
        raise NetworkPolicyError(
            "only public HTTP(S) destinations without credentials are allowed"
        )
    port = parts.port or (443 if parts.scheme == "https" else 80)
    if port not in (80, 443):
        raise NetworkPolicyError("only public HTTP ports 80 and 443 are allowed")
    host = host.encode("idna").decode("ascii")
    addresses = socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
    if not addresses or any(
        not ipaddress.ip_address(a[4][0]).is_global for a in addresses
    ):
        raise NetworkPolicyError("destination resolves to a non-public address")
    family, socktype, protocol, _, address = addresses[0]
    connection = http.client.HTTPConnection(host, port, timeout=timeout)
    transport = socket.socket(family, socktype, protocol)
    try:
        transport.settimeout(timeout)
        transport.connect(address)
        if parts.scheme == "https":
            transport = ssl.create_default_context().wrap_socket(
                transport, server_hostname=host
            )
        connection.sock = transport
        path = parts.path or "/"
        if parts.query:
            path += "?" + parts.query
        connection.request(
            method,
            path,
            headers={
                "User-Agent": "D0RKW3B/1.1 (+https://github.com/muhammadwali0/d0rkw3b)",
                "Accept": "application/json, */*;q=0.1",
                "Connection": "close",
            },
        )
        response = connection.getresponse()
        headers = dict(response.getheaders())
        body = b"" if method == "HEAD" else response.read(max_bytes + 1)
        if len(body) > max_bytes:
            raise NetworkPolicyError("response exceeds size limit")
        return response.status, headers, body
    finally:
        connection.close()
        transport.close()
