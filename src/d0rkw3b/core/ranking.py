"""Transparent editorial ordering, not a scientific measure of provider quality."""


def ranking(provider):
    quality = provider.get('quality', {})
    parts = {'editorial_priority': quality.get('priority', 0) * 10,
             'no_api_key': 0 if provider['requires_api_key'] else 3,
             'auth_friction': {'none': 2, 'unknown': 0, 'may_require': -2, 'required': -4}[provider['auth']],
             'enabled': 0 if provider['enabled'] else -100,
             'status': -50 if provider['status'] in ('broken', 'disabled', 'deprecated') else 0}
    return {'score': sum(parts.values()), 'components': parts,
            'basis': quality.get('reason', 'No editorial priority assigned; availability is not inferred.')}


def rank_providers(providers):
    return sorted(providers, key=lambda p: (-ranking(p)['score'], p['id']))
