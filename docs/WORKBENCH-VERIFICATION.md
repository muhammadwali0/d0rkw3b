# Workbench 1.1.0 engineering report

This report covers the next-generation specification, sections 1–57. The initial
inventory is [WORKBENCH-IMPLEMENTATION.md](WORKBENCH-IMPLEMENTATION.md); the older
AUDIT.md and VERIFICATION.md describe the v1 migration only.

## Initial and final architecture

Baseline `827efe6` was an installable, dependency-free v1 query CLI with 11 tests,
425 JSON providers, 14 categories and 15 query target types. There were no cases,
connectors, recipes, structured entities or supported public Python entry points.

Version 1.1.0 retains that engine and adds typed entities, provenance-bearing
relationships and observations, ranked offline investigation plans, JSON recipes,
explicit capability-declaring connectors and entry-point plugins. SQLite stores
explicit cases, runs, notes, observations and evidence. Query providers remain
non-executable data. Local snapshot updates and preferences layer over bundled
providers. There is no server, LLM, telemetry or runtime dependency.

## Provider preservation and trust

A direct comparison against baseline JSON records confirms that all 425 records
are unchanged except added editorial `quality` metadata. No IDs, URLs, target
coverage, categories, Tor definitions or disabled states were removed or changed.
The migration inventory test also retains the original URL coverage check.

| Metric | Baseline | Final bundled registry |
|---|---:|---:|
| Providers | 425 | 425 |
| Categories | 14 | 14 |
| Query target types | 15 | 15 |
| Clearnet / Tor | 412 / 13 | 412 / 13 |
| Enabled / disabled | 415 / 10 | 415 / 10 |
| Semantically unverified | 425 | 425 |
| Deprecated | 0 | 0 |
| Auth unknown / may require | 333 / 92 | 333 / 92 |
| Auth explicitly required | 0 | 0 |
| Recorded healthy / degraded | 0 / 0 | 0 / 0 |

Zero recorded healthy/degraded means no live reachability assessment is claimed;
it does not mean providers are unavailable. Health reports are separate from the
registry and distinguish structure, template validity, reachability and semantics.
HTTP 200 never establishes semantic correctness. Tests mock status responses.

## Delivered interface and data

New groups: `investigate`, `recipes list/info/validate`, `providers health/update/rollback`,
`packs list`, `connectors`, `integrations`, `collect`, `file`, `case`, `evidence`, and
`dev validate-providers/validate-recipes/registry-stats`. Legacy query commands,
exports, interactive prompts and browser safeguards remain available.

Entity types: search, username, email, domain, ipv4, ipv6, url, document, video_id,
phone, user_id, location_id, list_id, repository, company, file, file_hash, hostname.
Types with no implemented consumer, such as Person and CIDR, were not invented.

Relationship vocabulary: uses_domain, resolves_to, uses_nameserver, belongs_to,
has_profile, owns, references, has_hash. Core producers currently emit the explicit
syntactic email uses_domain pivot, observed DNS resolves_to, RDAP uses_nameserver
and local-file has_hash. The remaining predicates are validated vocabulary for
explicit structured input/plugins, not claims of automatic enrichment. Relationship
kind and provenance distinguish observed, inferred and manually added records.

Seven recipes: document-provenance, domain-footprint, email-footprint,
image-provenance, organization-research, repository-investigation,
username-footprint. Recipes contain methodology and validated references, not code.

Connectors: DNS, IANA-bootstrap RDAP and local-file/hash. Optional ExifTool has a
read-only subprocess adapter with mocked argument/output tests. Sherlock, Maigret,
theHarvester and Amass have PATH detection only. Missing tools yield explicit errors.
No live installed ExifTool or third-party network validation is claimed.

Cases support create/list/show/add/note, explicit plan/collection saves, deduplicated
entities, separate runs, evidence byte copies/SHA-256, provenance, graphs and timelines.
Exports: legacy text/JSON/CSV/Markdown; structured cases additionally JSONL, GraphML
and GEXF. Graph edges preserve provenance; query URLs are generated queries, not
findings. Timeline distinguishes creation, observation and collection timestamps.

## Requirement-by-requirement evidence

The table maps every original section to implementation, checks or an explicitly
permitted design-only decision. Paths are relative to the repository.

| Section | Evidence and scope |
|---|---|
| 1 Audit | Initial inventory, baseline commit and direct provider comparison above |
| 2 Positioning | README first screen and docs/index.md use Local OSINT Workbench |
| 3 Query engine | core/renderer.py, cli.py; test_core offline/query/export/browser checks |
| 4 Trust | core/health.py and network.py; test_health covers statuses, skips, errors, limits and public destinations |
| 5 Health CI | Separate provider-health.yml, 20-origin report artifact, no registry mutation |
| 6 Ranking | core/ranking.py; test_ranking checks transparency, determinism, --all/machine completeness |
| 7 Registry updates | core/updates.py; checksum/schema/coverage validation, atomic activation, rollback/fallback; test_registry_updates including special-file rejection |
| 8 Entities | core/entities.py and validation.py; normalization/identity tests in test_investigations |
| 9 Relationships | Validated predicates, kind and required Provenance; syntactic email and observed connector tests |
| 10 Observations | Observation model rejects generated queries with output findings; collection boundary validates finite bounded JSON |
| 11 Investigate | investigation.py and workbench_cli.py; offline API/CLI, categories, recipes, explicit collection/case dispatch |
| 12 Recipes | Seven bundled JSON files; core/recipes.py strict validator and all-recipe execution tests |
| 13 Connectors | connectors/models.py, builtin.py and registry.py; DNS/RDAP mocks plus actual temporary local-file tests |
| 14 Permissions | Static capability manifests and stderr disclosure before explicit execution; no sandbox claim |
| 15 Integrations | integrations.py PATH discovery and optional ExifTool adapter; absence and fixed-argument tests |
| 16 Plugins | d0rkw3b.connectors entry points plus packaged static manifest; test plugin discovery/load/error tests; docs/plugins.md |
| 17 Cases | cases/store.py and cli.py; transactional persistence, isolation, explicit storage and CLI tests |
| 18 Evidence | cases/evidence.py; original bytes, SHA-256, stored path, provenance and symlink/nonregular rejection tests |
| 19 Local files | localfiles.py bounded signature/text parsing and streaming hash; optional ExifTool tags for richer metadata; test_evidence |
| 20 Graphs | cases/exports.py GraphML/GEXF; XML parsing and edge-provenance tests |
| 21 Timeline | Timestamp-aware timeline projection; test_case_exports verifies creation versus observation/collection |
| 22 Exports | Legacy export tests plus case projections; STIX explicitly future in docs/cases.md |
| 23 Python API | __init__.py exports investigate/providers; docs/API.md contract and offline fixed-clock API tests |
| 24 Expressions | core/expressions.py shlex grammar TYPE:VALUE plus optional category; rejection tests; no eval |
| 25 Packs | core/packs.py logical groups/filtering, derived counts; test_expressions_packs |
| 26 CLI UX | Group dispatch, help/examples, stderr diagnostics; CLI and machine-output tests |
| 27 Interactive | cli.interactive routes commands through main; category queries reuse engine; recovery/guided-menu tests |
| 28 UI | docs/local-interface.md architecture only; no optional UI needed in this phase |
| 29 Extension | Same document defines selected-text/URL/case operations, pairing, authentication, loopback and origin boundaries |
| 30 Release | pyproject.toml 1.1.0; real build, fresh wheel install, pip check and smoke tool |
| 31 Distribution | Standard wheel/console script; docs/releasing.md pip/pipx/uv and community packaging guidance; no fictitious manifests |
| 32 Supply chain | Pinned workflows, CodeQL/dependency review, artifact RECORD/path checks, checksums, SPDX SBOM and attestation workflow; no publishing credentials |
| 33 CI | tests.yml Linux 3.10–3.14 and Windows/macOS 3.13; unit/lint/validate/build/install/pip/smoke gates |
| 34 Tests | 54 tests in 11 logical files, live service responses mocked; local filesystem/subprocess tests use temporary inputs |
| 35 Docs site | docs/index.md topic navigation and relative Markdown links |
| 36 README | Real CLI examples, actual counts, install/privacy/cases/plugins/contribution/legal sections |
| 37 Community | CONTRIBUTING.md, provider schema and plugin/recipe guides, contribution issue template; CI schema validation |
| 38 Translation | docs/translations/README.md canonical English and community locale structure; no automatic translation claims |
| 39 No AI core | Deterministic Python/JSON implementation; no LLM clients or speculative attribution |
| 40 Privacy | Ordinary query execution has no network/storage dispatch; no telemetry/server; tests deny network and implicit storage |
| 41 Security | Explicit public-information/local-file connectors, no bypass/scrapers/credential collection |
| 42 Dependencies | dependencies=[]; build manifest verifies no base Requires-Dist; tools independently optional |
| 43 Performance | Sequential bounded collection; registry parse and indexed SQLite; local domain plan mean 0.039s over 10 runs (informational, hardware-specific) |
| 44 Database | cases/schema.py version 1, FK enforcement, composite keys/indexes; store transactions, foreign/future-schema refusal tests |
| 45 Errors | core/errors.py domain errors; dispatcher conversion; ordinary invalid-input tests avoid tracebacks |
| 46 Diagnostics | --verbose/--debug stderr only; no locals/secrets in debug frames; plugin error suppression and config tests |
| 47 Config | core/config.py bounded JSON preferences, platform dirs, explicit overrides; disable-provider/connector and format tests |
| 48 Dev tools | management.py and workbench_cli.py validation/stats commands; installed-wheel smoke executes validators |
| 49 Migration | Exact baseline comparison, original inventory tests and legacy wrappers retained; default human ranking documented |
| 50 Priority | Ordered implementation commits: trust, models/recipes, cases, collection/plugins, registry, release/docs |
| 51 Restraint | No cloud accounts, distributed scraping, fake integrations, UI toolchain or speculative enrichment |
| 52 Version | 1.1.0 in package/runtime metadata, CHANGELOG, README/docs; no tag/release/PyPI publication |
| 53 Acceptance | Core, preservation, trust, storage, explicit collection, privacy and packaging checks listed above and below |
| 54 Validation | Full pytest/Ruff/build/wheel/pip/smoke commands below; temporary cases/files cleaned by smoke harness |
| 55 Self-review | Baseline diff/provider comparison, network/subprocess call-site review, schema/path/metadata review; fixed special-file hangs and portable path assertions |
| 56 Git | Conventional commits on feat/local-osint-workbench, remote upstream, fast-forward push/pull; no history rewrite |
| 57 Report | This document records architecture, counts, interfaces, checks, limitations and commit history |

## Validation and limitations

Local validation at `c4ae190`: `python -m pytest -q` reports **54 passed in 4.83s**;
`ruff check .` reports **All checks passed!**. The named-pipe regression is POSIX-only
and skips on Windows, where that filesystem API is unavailable. CI run [34618931605](https://github.com/muhammadwali0/d0rkw3b/actions/runs/34618931605)
passed all seven jobs at `344b843`: Linux Python 3.10–3.14 and Windows/macOS
Python 3.13, including lint, validators, build, wheel installation, pip check and
installed-command smoke checks. The earlier CI failures were corrected: canonical
path expectations on macOS/Windows and sysconfig-based Windows script discovery.

The final local source build at `344b843` succeeded with `python -m build`, generating a
1.1.0 wheel and source archive. `tools/release_manifest.py` verified wheel RECORD
hashes and source members and generated checksums/SPDX. Fresh virtualenv wheel
installation succeeded; `pip check` reported **No broken requirements found.**
`tools/smoke_install.py` reported **Installed-wheel smoke checks passed; temporary
cases and files removed.** No source changes followed this final successful build; this report records the
verified state.

The smoke tool executes both entry points, help, provider listing/health help,
provider/recipe validation, recipe listing, domain/username investigations, search,
JSON domain queries, case new/add/show, local file inspection, evidence import and
graph export from a temporary directory. Tests separately exercise DNS/RDAP and
ExifTool with deterministic mock responses. No invasive live checks were run.

Deferred as allowed by the specification: active CT/Wayback adapters, executable
social integrations, remote registry hosting/signatures, installable packs,
STIX/HTML visualization, local HTTP/UI/extension implementations, localization and
actual distribution-channel publication. Architecture and contribution contracts
are documented without claiming these features exist.

Limits: plugins are trusted Python, not sandboxed. ExifTool is optional and tested
with mocks. Basic file parsing samples the first MiB; richer document/image tags
need ExifTool. HTTP DNS follows OS timeout policy; file reads can block despite
cooperative time budgets. Local SHA-256 snapshots verify integrity, not publisher
authenticity. Cases are not encrypted. A crash between evidence rename and database
commit can leave an unreferenced copied file. Health semantics remain unverified.
Host security/attestation services are configured, not claimed as executed releases.
The historical credential noted in SECURITY.md requires owner revocation; this
work adds no secret and does not rewrite history to conceal the earlier exposure.

No intentional breaking query-command changes. Human recommendations are ranked
and abbreviated; `--all` restores full human output. Legacy machine rows remain
complete. New API/plugin contracts begin at 1.1.0. No new runtime dependencies.

## Implementation commits

- `f998c84` provider health and ranking
- `ebf2a39` structured entities/observations and recipes
- `5f3a1b4` transactional cases and evidence
- `87f6e40` connectors, integrations and plugin API
- `04c1284` registry snapshots, packs and preferences
- `4243541` final code validation/export fixes and Ruff formatting
- `6b3623e` workbench documentation and release/security CI
- `c4ae190` special-file rejection, portable path assertions and command help
- `344b843` portable installed-command discovery in wheel smoke tests

The final report commit is identified by Git history and the completion response.
The feature branch tracks origin/feat/local-osint-workbench. Main remains at the
v1 baseline; merging and publishing are separate actions.
