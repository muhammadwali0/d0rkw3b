"""Small explicit typed-query grammar; no operators or executable expressions."""
import shlex
from .models import TARGET_TYPES


def parse_expression(expression):
    words = shlex.split(expression)
    if not 1 <= len(words) <= 2:
        raise ValueError('expression syntax: TYPE:VALUE [category:NAME]; quote values with spaces')
    kind, separator, value = words[0].partition(':')
    if not separator or kind not in TARGET_TYPES | {'ip'} or not value:
        raise ValueError('expression requires a supported TYPE:VALUE')
    category = None
    if len(words) == 2:
        key, separator, category = words[1].partition(':')
        if key != 'category' or not separator or not category:
            raise ValueError('only an optional category:NAME filter is supported')
    return kind, value, category
