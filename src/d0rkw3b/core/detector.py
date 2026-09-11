import ipaddress
from .validation import clean, domain_name, validate


def detect(value):
    value = clean(value)
    if '://' in value:
        return validate(value, 'url')
    if value.startswith('@'):
        return validate(value, 'username')
    if '@' in value and ' ' not in value:
        return validate(value, 'email')
    try:
        ipaddress.ip_address(value)
    except ValueError:
        pass
    else:
        return validate(value, 'ip')
    try:
        domain_name(value)
    except (ValueError, UnicodeError):
        return validate(value, 'search')
    return validate(value, 'domain')
