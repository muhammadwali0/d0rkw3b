# Entities, observations and provenance

An entity has a stable ID derived from type and normalized value, plus raw input,
actual creation time and metadata. Types with current consumers are search,
username, email, domain, IPv4, IPv6, URL, document query, video ID, phone, user ID,
location ID, list ID, repository, company, hostname, file and SHA-256 file hash.
These are typed indicators, not inferred people or identities. Username casing
and email local-part casing are preserved to avoid platform-dependent merging.

A query provider renders a URL. Its observation is `generated_query`, unverified,
and has no confirmed output entity or relationship. A connector deliberately
collects information and returns `observed` records. Imports and manual records
have distinct schema kinds. Provenance records source, method, reference,
collection time, optional source URL and notes. A confidence label is qualitative,
not a probability or proof of authenticity.

Automatic relationships currently produced:

- Email `uses_domain`: syntactic parsing only, no existence check.
- Domain/hostname `resolves_to` IP: explicit system-resolver observation.
- Domain `uses_nameserver` hostname: explicit RDAP registration record.
- File `has_hash` SHA-256: explicit local byte inspection.

The schema also permits evidence-backed `belongs_to`, `has_profile`, `owns` and
`references` predicates for connectors/manual data. They are never guessed from
names or URLs. Relationship kinds distinguish observed, inferred and manually-added.
Every edge must refer to known entities and carry provenance; case foreign keys
also enforce case/run boundaries. No invisible AI attribution is used.

Run timestamps, observation times, provenance collection times, evidence import
times and document/file timestamps are different concepts. Timelines label their
origin. IDs and ordering are deterministic; newly acquired timestamps intentionally
reflect actual activity. Cases retain repeated runs instead of overwriting history.
