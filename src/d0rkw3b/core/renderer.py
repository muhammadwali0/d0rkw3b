import re
from string import Formatter
from urllib.parse import quote, urlsplit

from .validation import clean


def fields(template):
    result = set()
    for _, field, spec, conversion in Formatter().parse(template):
        if field is not None:
            if spec or conversion or not re.fullmatch('[a-z_][a-z_0-9]*', field):
                raise ValueError('template must use simple {variable} fields only')
            result.add(field)
    return result


def render(provider, target, extras=None):
    values = {target.variable: target.value}
    for key, value in (extras or {}).items():
        values[key] = clean(value)
    if 'year' in values:
        if not re.fullmatch(r'[0-9]{4}', values['year']) or not 1 <= int(values['year']) <= 9998:
            raise ValueError('year must be between 0001 and 9998')
        values['next_year'] = f'{int(values["year"]) + 1:04d}'
    needed = fields(provider['template'])
    missing = needed - values.keys()
    if missing:
        raise ValueError('missing parameters: ' + ', '.join(sorted(missing)))
    # Hosts cannot contain percent-encoded arbitrary input. This applies to the
    # legacy Tumblr username subdomain and to contributed host templates.
    host_template = urlsplit(provider['template']).netloc
    for field in fields(host_template):
        if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?', values[field]):
            raise ValueError(f'{field} is not a valid hostname label for this provider')
    return provider['template'].format_map({k: quote(v, safe='') for k, v in values.items()})
