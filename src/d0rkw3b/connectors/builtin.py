"""Low-risk built-in connectors. Every runner requires explicit invocation."""
import ipaddress
import json
import sys
from urllib.parse import quote, urlsplit

from ..core.entities import Entity, Observation, Provenance, Relationship, identifier, now
from ..core.errors import ConnectorUnavailableError
from ..core.network import request
from ..localfiles import inspect_file
from .models import Capabilities, Collection, Manifest
from .process import run_json

MANIFESTS = {
    'dns': Manifest('dns', 'System DNS resolution', ('domain', 'hostname'), ('ipv4', 'ipv6'),
        Capabilities(network=('system-configured DNS resolver',), subprocess=True),
        'Resolve A/AAAA addresses through the OS resolver in an isolated child Python process.',
        'One resolver lookup per invocation; OS DNS caching/retries apply.', 10),
    'rdap': Manifest('rdap', 'RDAP registration lookup', ('domain', 'ipv4', 'ipv6'), ('hostname',),
        Capabilities(network=('data.iana.org', 'HTTPS RDAP registry selected from IANA bootstrap')),
        'Read public registration metadata; domain nameservers are registry observations, not ownership attribution.',
        'Two bounded GET requests; no redirects or retries; 429/403 require manual follow-up.', 10),
    'local-file': Manifest('local-file', 'Local file metadata and SHA-256', ('file',), ('file_hash',),
        Capabilities(filesystem_read=True),
        'Hash a regular local file and inspect bounded header/text metadata; no upload.',
        'One file streamed locally; parsing uses the first 1 MiB. Runtime scales with file size.', 10),
}


def observation(entity, source, method, metadata, *, output=None, relationship=None, source_url=None, collected=None):
    collected = collected or now()
    ref = identifier('acquisition', source, entity.entity_id, collected)
    provenance = Provenance(source, method, ref, collected, source_url=source_url)
    return Observation(identifier('observation', ref, metadata), 'observed', source, method,
                       entity.entity_id, collected, provenance,
                       output.entity_id if output else None,
                       relationship.relationship_id if relationship else None,
                       confidence='high', metadata=metadata)


def dns(entity, *, timeout=10):
    script = ('import json,socket,sys; '
              'print(json.dumps(sorted({x[4][0] for x in socket.getaddrinfo(sys.argv[1], None, type=socket.SOCK_STREAM)})))')
    values = run_json([sys.executable, '-I', '-c', script, entity.normalized_value], timeout=timeout)
    if not isinstance(values, list) or len(values) > 1024 or any(not isinstance(v, str) for v in values):
        raise ConnectorUnavailableError('DNS resolver returned an invalid result')
    entities, relations, observations = [entity], [], []
    collected = now()
    for value in sorted(set(values)):
        output = Entity.create(value, 'ip', created_at=collected)
        provenance = Provenance('dns', 'OS getaddrinfo A/AAAA', identifier('dns', entity.entity_id, value, collected), collected,
                                notes='Resolver answer at collection time; not a claim of ownership or DNSSEC validation.')
        relation = Relationship.create(entity, 'resolves_to', output, provenance=provenance)
        entities.append(output)
        relations.append(relation)
        observations.append(Observation(identifier('observation', provenance.reference), 'observed', 'dns', provenance.method,
            entity.entity_id, collected, provenance, output.entity_id, relation.relationship_id, 'high'))
    return Collection(entity, entities, relations, observations)


def rdap_base(bootstrap, entity):
    services = bootstrap.get('services') if isinstance(bootstrap, dict) else None
    if not isinstance(services, list):
        raise ConnectorUnavailableError('invalid IANA bootstrap response')
    candidates = []
    for service in services:
        if not isinstance(service, list) or len(service) != 2:
            raise ConnectorUnavailableError('invalid bootstrap service')
        suffixes, endpoints = service
        if not isinstance(suffixes, list) or not isinstance(endpoints, list):
            raise ConnectorUnavailableError('invalid bootstrap service fields')
        for suffix in suffixes:
            if not isinstance(suffix, str):
                continue
            if entity.type == 'domain':
                match = entity.normalized_value == suffix or entity.normalized_value.endswith('.' + suffix)
                specificity = len(suffix)
            else:
                try:
                    subnet = ipaddress.ip_network(suffix)
                    match = ipaddress.ip_address(entity.normalized_value) in subnet
                    specificity = subnet.prefixlen
                except ValueError:
                    continue
            if match:
                for endpoint in endpoints:
                    if isinstance(endpoint, str) and urlsplit(endpoint).scheme == 'https':
                        candidates.append((specificity, endpoint))
    if not candidates:
        raise ConnectorUnavailableError('no matching HTTPS RDAP service in IANA bootstrap')
    return sorted(candidates, key=lambda item: (-item[0], item[1]))[0][1].rstrip('/') + '/'


def get_json(url, timeout):
    status, _, body = request(url, method='GET', timeout=timeout)
    if status != 200:
        raise ConnectorUnavailableError(f'RDAP request returned HTTP {status}; no redirect, retry or bypass attempted')
    try:
        result = json.loads(body)
    except (ValueError, UnicodeError) as exc:
        raise ConnectorUnavailableError('RDAP service returned invalid JSON') from exc
    if not isinstance(result, dict):
        raise ConnectorUnavailableError('RDAP JSON must be an object')
    return result


def rdap(entity, *, timeout=10):
    table = 'dns' if entity.type == 'domain' else entity.type
    bootstrap = get_json(f'https://data.iana.org/rdap/{table}.json', timeout)
    base = rdap_base(bootstrap, entity)
    endpoint = base + ('domain/' if entity.type == 'domain' else 'ip/') + quote(entity.normalized_value, safe='')
    data = get_json(endpoint, timeout)
    expected = 'domain' if entity.type == 'domain' else 'ip network'
    if data.get('objectClassName') != expected:
        raise ConnectorUnavailableError('RDAP response does not match the requested object class')
    # Check that the returned object is the requested domain/network before linking.
    if entity.type == 'domain':
        name = data.get('ldhName', data.get('unicodeName'))
        if not isinstance(name, str) or Entity.create(name, 'domain').entity_id != entity.entity_id:
            raise ConnectorUnavailableError('RDAP returned a different domain')
    else:
        try:
            address = ipaddress.ip_address(entity.normalized_value)
            if not ipaddress.ip_address(data['startAddress']) <= address <= ipaddress.ip_address(data['endAddress']):
                raise ValueError('address not covered')
        except (KeyError, TypeError, ValueError) as exc:
            raise ConnectorUnavailableError('RDAP response does not cover the requested IP') from exc
    collected = now()
    entities, relations = [entity], []
    observations = [observation(entity, 'rdap', 'public RDAP GET', data, source_url=endpoint, collected=collected)]
    diagnostics = []
    if entity.type == 'domain':
        nameservers = data.get('nameservers', [])
        if not isinstance(nameservers, list):
            raise ConnectorUnavailableError('malformed RDAP nameservers')
        seen = set()
        for ns in nameservers[:100]:
            try:
                output = Entity.create(ns['ldhName'], 'hostname', created_at=collected)
            except (KeyError, TypeError, ValueError):
                diagnostics.append('Skipped malformed RDAP nameserver')
                continue
            if output.entity_id in seen:
                continue
            seen.add(output.entity_id)
            provenance = Provenance('rdap', 'RDAP nameservers field', endpoint, collected, source_url=endpoint,
                                    notes='Registration-service record, not a DNS resolution or ownership claim.')
            relation = Relationship.create(entity, 'uses_nameserver', output, provenance=provenance)
            entities.append(output)
            relations.append(relation)
    return Collection(entity, entities, relations, observations, diagnostics)


def local_file(entity, *, timeout=10):
    data = inspect_file(entity.normalized_value, timeout=timeout)
    collected = now()
    output = Entity.create('sha256:' + data['sha256'], 'file_hash', created_at=collected)
    provenance = Provenance('local-file', 'streamed SHA-256', entity.normalized_value, collected,
                            notes='Local bytes read explicitly; file not uploaded.')
    relation = Relationship.create(entity, 'has_hash', output, provenance=provenance)
    observed = Observation(identifier('observation', provenance.reference, collected), 'observed', 'local-file',
        provenance.method, entity.entity_id, collected, provenance, output.entity_id,
        relation.relationship_id, 'high', data)
    return Collection(entity, [entity, output], [relation], [observed])


RUNNERS = {'dns': dns, 'rdap': rdap, 'local-file': local_file}
