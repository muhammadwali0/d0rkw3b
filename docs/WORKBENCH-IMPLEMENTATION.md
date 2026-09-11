# Workbench implementation inventory

## Audit before changes

Baseline `827efe6`, v1.0.0, clean main synchronized with origin. All executable
modules, tests, workflow, package metadata, provider files, migration inventory,
README and development/security documentation inspected. No local/remote tags.
The legacy wrapper imports the installed CLI; there is no supported Python API.
The registry is JSON, 425 definitions, 14 categories, 15 target types, 412 clearnet
and 13 Tor, all unverified; 415 enabled and 10 disabled. Auth: 333 unknown, 92
may_require. Existing 11 offline unittest checks pass. Runtime dependencies: none.

The CLI is a single argparse dispatcher: query generation, provider listing,
validation, guided prompts, four formats and guarded single-provider browser open.
There is no health checking, ranking, entities, relationships, observations,
recipes, cases, evidence, active connectors, integrations, plugins or graph/timeline.
The current verification document describes v1 only and must not be treated as
proof of workbench capabilities. No TODO implementations found. CI currently
runs unit tests and provider validation on Python 3.10/3.13 across three OSes;
no lint, wheel-install, release, or health workflow. Provider preservation tests
currently require exact equality and will need to allow deliberate additions.

## Ordered implementation and acceptance inventory

- P0 trust: separate reachability/semantic records; bounded explicit health command,
  no target queries, no Tor probes, status tests and separate scheduled report CI.
  Transparent editorial ranking, complete --all and machine-output compatibility.
- P0 investigation: typed deterministic entities, provenance-bearing relationships,
  observations that distinguish generated_query from observations; validated JSON
  recipes; investigate, export, minimal query expressions and API-level tests.
- P1 storage: platform-local SQLite schema/versioning/FKs/transactions, explicit
  cases and notes, observations/relationships/runs, evidence copies and hashes,
  timeline, GraphML/GEXF and structured exports with provenance.
- P1 collection: explicit capability manifests, bounded network operations,
  low-risk DNS/RDAP/local-file connectors as supported, integration discovery
  and a tested local ExifTool adapter; no social scrapers or automatic execution.
- P2 ecosystem: entry-point plugins with explicit activation, validated local
  registry update/rollback abstraction without invented remote infrastructure,
  logical provider packs, stable public Python API and contribution/translation docs.
- P2 release: expanded deterministic tests/lint/build/install/pip-check CI;
  conservative scheduled health artifacts; release build/checksums/SBOM/security
  workflows, packaging guidance with no claimed nonexistent distribution channels.
- P3 architecture only: document authenticated loopback API/browser-extension
  contract; no UI, server or extension until core is complete. STIX remains future
  rather than arbitrary JSON. No publishing, force pushes or remote history rewrite.
- Completion: full requirement audit, provider before/after counts, all specified
  CLI/build/lint/install gates, entire diff review, reviewable local commits and
  final factual report. The original 57-section attachment remains the full scope.

## Design constraints

Preserve v1 query commands and machine-readable row structure. Keep ordinary
startup offline with no persistent target state. Health checks write reports only
on explicit request; reachability never implies semantic correctness. Query plan
objects use deterministic IDs and optional timestamps; saved runs attach actual
collection/creation times. Use stdlib SQLite, urllib and package entry points;
optional integrations must declare capabilities and handle absence honestly.

## Progress: trust and ranking

Implemented explicit health reports, public-address-pinned HTTP transport,
conservative classification/budgets, optional quality/verification schema metadata,
editorial recommendations, complete --all/machine outputs, provider/dev aliases,
stats and separate scheduled health artifacts. 19 offline unittest checks pass.
Baseline provider coverage remains 425/14 categories/15 types/13 Tor, all unverified.
No live checks or semantic claims made. No external release exists in the GitHub
release listing inspected during audit. Remaining P0/P1/P2/P3 items above are open.

## Progress: structured P0 investigations

Added validated Entity/Relationship/Provenance/Observation models, stable typed
identity, offline investigation API, seven validated recipes, investigate and
recipes command groups, clean structured exports and interactive routing.
Generated queries cannot carry a confirmed output entity/relationship. The email
pivot is explicitly syntactic, not an inferred account or ownership claim.
26 offline unittest checks pass, including all seven recipe executions and API
network-denial tests. P1 storage/collection and P2/release/adoption work remain open.
