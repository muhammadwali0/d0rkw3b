# Migration completion evidence

Scope is the supplied attachment (10,751 bytes), which ends mid-sentence in
section 7. No absent later requirements are assumed.

| Requirement | Implementation and verification |
|---|---|
| Audit before replacement | AUDIT.md records baseline structure, all modules/menu paths, dependencies, metadata and defects; inventory was generated before legacy removal |
| Preserve all provider knowledge | migration-inventory.json maps all 425 returned URLs across 35 functions; test_inventory_coverage compares every ID and URL, allowing only documented corrections |
| Local-first product | No runtime HTTP client; socket/browser-denial tests cover example commands; browser opening requires explicit single-provider selection |
| Modern installation | pyproject.toml, src layout, version 1.0.0, MIT license; wheel and source distribution built, isolated wheel installation exercised |
| Both entry points | Console script registry validation and python -m version/query smoke tests |
| Interactive and scripts | Guided category/action menus and CLI prompt; tests cover guided domain lookup, malformed command recovery and EOF; deterministic JSON/text/CSV/Markdown |
| Registry validation | 425 valid definitions; tests cover malformed JSON, duplicate IDs, missing fields, types, schemes, variables, malformed templates and graceful continuation |
| Honest provider metadata | Every migrated endpoint unverified with null verification date; Tor, authentication uncertainty and disabled reference endpoints recorded |
| Central rendering | All URLs rendered through one quote-based renderer; tests exercise spaces, +, &, Unicode, @, #, slashes, nested URLs and query strings |
| Target types and detection | All supplied examples tested; IPv4/IPv6, IDNA domains, URLs, email, usernames, search plus legacy IDs, companies, repositories, documents/video and paired inputs |
| Existing special behavior | Every function has a guided menu action; X year boundaries corrected; disabled GraphQL/API-key/probe references retained; IPv4-only provider excluded for IPv6 |
| Community readiness | README, changelog, contributing, security, conduct, schema docs, issue/PR templates and Linux/macOS/Windows CI matrix |

Local checks run on Linux with Python 3.14. The cross-platform CI configuration
is supplied; remote CI jobs and live provider availability have not been claimed
as verified. No screenshots, releases, download counts or health claims invented.

The original API key is absent from maintained definitions and source. Revoking
that historical credential requires its owner; history is intentionally preserved.
