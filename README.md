# D0RKW3B

**The Local OSINT Workbench**

Turn domains, usernames, emails, IP addresses, URLs and local files into structured
investigation paths. Search, pivot and organize research while keeping your case
data on your own machine.

Normal queries and investigation plans are offline. Active collection is explicit.
Generated links are **queries, not findings**. No accounts, mandatory API keys,
telemetry, server or base runtime dependencies.

## Install

Python 3.10+; version **1.1.0**. From this checkout:

```sh
pipx install .
# Or: uv tool install .
# Or, inside a virtual environment: python -m pip install .
d0rkw3b --version
```

`python -m d0rkw3b` is equivalent after installation. These commands install the
checkout; they do not assume a PyPI release or community package exists.
See [Getting started](docs/getting-started.md) for Windows/macOS/Linux instructions.

## A 30-second start

```sh
d0rkw3b investigate example.com --recipe domain-footprint
d0rkw3b investigate alice --type username
d0rkw3b user@example.com --format json
d0rkw3b recipes list
```

The domain recipe produces certificate, registration, history and reputation
query paths. It does not contact those providers or claim any result was found.
Use `--all` for every matching query, or `--pack infrastructure` to focus a plan.
Legacy commands such as `d0rkw3b domain example.com`, `search "Acme Corporation"`,
and `interactive` remain available.

## Save a local case

```sh
d0rkw3b case new acme
d0rkw3b investigate example.com --case acme
d0rkw3b case add acme alice@example.com
d0rkw3b case note acme "Review certificate history"
d0rkw3b evidence add acme ./report.pdf
d0rkw3b case timeline acme --format csv
d0rkw3b case graph acme --format graphml
```

Cases use local SQLite with entities, relationships, runs, observations, notes and
evidence provenance. Evidence imports preserve bytes and record SHA-256. No case
or search history is saved unless you explicitly use a case.

## Query providers versus connectors

| Action | What happens |
|---|---|
| `investigate example.com` | Builds a local plan with ranked generated queries |
| `domain example.com --format json` | Emits a complete array of generated URLs |
| `collect domain example.com --connector dns` | Explicitly resolves through your system DNS resolver |
| `investigate example.com --with rdap` | Explicitly queries IANA bootstrap and the selected RDAP registry |
| `file ./photo.jpg` | Reads local bytes for hashes and bounded metadata |
| `file ./photo.jpg --with exiftool` | Explicitly runs an optional installed ExifTool adapter |

Connector capabilities and destinations are disclosed before execution. Optional
Python plugins use static manifests and explicit entry-point activation; they
are trusted code, not sandboxed code. `integrations` distinguishes a working
adapter contract from tools that are only detected on PATH.

## Provider trust and privacy

The bundled registry retains **425 providers** across **14 categories**: **13 Tor**,
**10 disabled**, and **425 semantically unverified**. These are definitions, not
verified services. No live provider health results are claimed.

```sh
d0rkw3b dev registry-stats
d0rkw3b providers health --help
d0rkw3b packs list
```

`providers health` is an explicit, bounded homepage reachability check. HTTP 200
never establishes semantic correctness. Normal startup does not run health checks.
Editorial ranking is transparent and does not pretend to measure reliability.

No hidden network calls, target uploads, file uploads or remote case storage.
Explicit browser opening sends the selected target to its provider. Tor links
require `--network tor` or `all`; D0RKW3B never opens them in your ordinary browser
or configures Tor automatically. Case exports and terminal output may contain
sensitive data. Review destinations and protect local files.

## Learn and contribute

- [Documentation index](docs/index.md): CLI, concepts, investigations, providers,
  recipes, cases, evidence, connectors, plugins, privacy, Tor and troubleshooting.
- [Python API](docs/API.md): `from d0rkw3b import investigate, providers`.
- [Contributing](CONTRIBUTING.md): providers, fixes, recipes, plugins, translations.
- [Release and packaging](docs/releasing.md): builds, checksums, SBOM and limitations.

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check .
python -m build
```

Use public information responsibly and respect authorization, access controls and
other people's privacy. D0RKW3B does not provide credential attacks, login/CAPTCHA
bypass, exploit deployment or speculative attribution. See [SECURITY.md](SECURITY.md)
and the [MIT license](LICENSE). Existing screenshots show the legacy v1 menu, not
new workbench functionality.
