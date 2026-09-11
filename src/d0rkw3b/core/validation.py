import ipaddress
import re
import unicodedata
from urllib.parse import urlsplit, urlunsplit

from .models import TARGET_TYPES, Target


def clean(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('target must not be empty')
    if len(value) > 8192 or any(unicodedata.category(c).startswith('C') for c in value):
        raise ValueError('input contains control characters or exceeds 8192 characters')
    return value.strip()


def domain_name(value):
    value = value.rstrip('.').encode('idna').decode('ascii').lower()
    labels = value.split('.')
    if len(value) > 253 or len(labels) < 2 or not all(
        re.fullmatch(r'[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?', label) for label in labels
    ) or labels[-1].isdigit():
        raise ValueError('invalid domain name')
    return value


def validate(value, kind):
    value = clean(value)
    if kind == 'ip':
        kind = f'ipv{ipaddress.ip_address(value).version}'
    if kind not in TARGET_TYPES:
        raise ValueError(f'unsupported target type: {kind}')
    if kind in ('ipv4', 'ipv6'):
        address = ipaddress.ip_address(value)
        if kind != f'ipv{address.version}' or '%' in value:
            raise ValueError(f'invalid {kind} address')
        value = str(address)
    elif kind == 'domain':
        value = domain_name(value)
    elif kind == 'email':
        if value.count('@') != 1:
            raise ValueError('invalid email address')
        local, host = value.split('@')
        if not local or len(local) > 64 or re.search(r'[\s<>"(),:;\\]', local):
            raise ValueError('invalid email local part')
        value = local + '@' + domain_name(host)
    elif kind == 'url':
        parts = urlsplit(value)
        if parts.scheme not in ('http', 'https') or not parts.hostname or parts.username is not None or parts.password is not None:
            raise ValueError('URL must use http(s), with a host and no embedded credentials')
        host = parts.hostname
        try:
            address = ipaddress.ip_address(host)
            host = f'[{address}]' if address.version == 6 else str(address)
        except ValueError:
            host = domain_name(host)
        port = parts.port  # validates port range
        value = urlunsplit((parts.scheme, host + (f':{port}' if port is not None else ''), parts.path, parts.query, parts.fragment))
    elif kind == 'username':
        value = value.removeprefix('@')
        if not value or re.search(r'[\s/@?#\\]', value):
            raise ValueError('username must not contain whitespace, slashes, @, ? or #')
    elif kind in ('user_id', 'location_id', 'list_id'):
        if not re.fullmatch(r'[0-9]+', value):
            raise ValueError(f'{kind} must contain digits only')
    elif kind == 'phone':
        if not re.fullmatch(r'\+?[0-9]{3,15}', value):
            raise ValueError('phone must contain 3–15 digits with an optional leading +')
    elif kind == 'video_id':
        if not re.fullmatch(r'[A-Za-z0-9_-]{11}', value):
            raise ValueError('YouTube video ID must contain 11 letters, digits, _ or -')
    return Target(kind, value)
