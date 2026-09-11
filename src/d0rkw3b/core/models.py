from dataclasses import dataclass

TARGET_TYPES = frozenset(('search', 'username', 'email', 'domain', 'ipv4', 'ipv6',
                          'url', 'document', 'video_id', 'phone', 'user_id',
                          'location_id', 'list_id', 'repository', 'company'))
VARIABLES = frozenset(('query', 'username', 'username2', 'email', 'domain', 'ip',
                       'url', 'video_id', 'phone', 'user_id', 'location_id',
                       'list_id', 'repository', 'company', 'year', 'next_year'))


@dataclass(frozen=True)
class Target:
    type: str
    value: str

    @property
    def variable(self):
        return {'search': 'query', 'document': 'query', 'ipv4': 'ip',
                'ipv6': 'ip'}.get(self.type, self.type)
