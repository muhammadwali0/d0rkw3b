# D0RKW3B

D0RKW3B is a privacy-first, local OSINT query engine and investigation launcher.
Turn a username, email, domain, IP, URL or search term into links to public
providers. It generates queries; it does not fetch results, scrape profiles,
crawl sites, or collect target data.

Version 1.0.0 requires Python 3.10 or newer. There are no runtime dependencies,
telemetry, mandatory accounts, API keys, or servers. Generating links performs no
network requests. Output contains your target: handle redirected files accordingly.

## Install

From a local checkout:

```sh
pipx install .
```

Or install in a virtual environment:

```sh
python -m venv .venv
# Linux/macOS
. .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install .
d0rkw3b --version
```

These instructions install the checkout; they do not assume a PyPI release exists.
`python -m d0rkw3b` provides the same interface after installation.

## Generate queries

```sh
d0rkw3b username muhammadwali0
d0rkw3b email example@example.com
d0rkw3b domain example.com
d0rkw3b ip 1.1.1.1
d0rkw3b url https://example.com/page
d0rkw3b search "Acme Corporation"

d0rkw3b example@example.com
d0rkw3b example.com
d0rkw3b 8.8.8.8
d0rkw3b 2001:4860:4860::8888
d0rkw3b @username
d0rkw3b wali --type username
```

Plain ambiguous text is a search. Domains normalize through IDNA; IP addresses
normalize through Python's IP parser. Explicit types validate inputs without DNS
lookups. Email validation accepts common addresses, not every RFC mailbox syntax.

```sh
d0rkw3b example.com --format json > queries.json
d0rkw3b document "annual report" --format markdown
d0rkw3b providers --format json
d0rkw3b validate-providers
d0rkw3b --help
```

`--category documents` applies to the `document` target type:

```sh
d0rkw3b document "Acme Corporation" --category documents --format csv
```

JSON is an array ordered by stable provider ID, with `id`, `name`, `category`,
`network`, `status`, and `url`. It includes no timestamps or random fields.
CSV has the same columns; Markdown and text support human review. Diagnostics go
to stderr. Exit codes: 0 success, 1 failed registry validation, 2 usage/input/no
matching providers, 130 interrupted. Redirect output using your shell; existing
files are subject to your shell's normal overwrite behavior.

## Categories and advanced targets

The registry preserves 425 legacy links across 14 categories: `search_links`,
`facebook`, `x`, `linkedin`, `instagram`, `github`, `communities`, `emailaddresses`,
`usernames`, `documents`, `images`, `videos`, `ipaddresses`, and `domain`.

Additional explicit types are `document`, `video_id` (YouTube), `phone` (Facebook
number route), `user_id`, `location_id`, `list_id`, `repository`, and `company`.
Use `--category` to select the platform for IDs. A URL target offers the existing
reverse-image and LinkedIn post timestamp launchers; choose the relevant category.
A generated link does not imply the target exists or matches the provider.

```sh
d0rkw3b username someone --category x --param year=2024
d0rkw3b username someone --category instagram --param query="search terms"
d0rkw3b username someone --category instagram --param username2=other
d0rkw3b repository d0rkw3b --category github
d0rkw3b company acme --category linkedin
d0rkw3b user_id 12345 --category facebook
d0rkw3b video_id dQw4w9WgXcQ --category videos
```

Providers needing additional parameters are omitted until those parameters are
supplied. Selecting one explicitly with `--provider ID` instead reports missing
parameters. Use repeatable `--provider` flags for precise selection. IDs and
parameter names are listed by `providers --format json`.

## Interactive use and opening links

```sh
d0rkw3b interactive
```

Choose a numbered category and action for guided prompts, preserving all legacy
menu actions. The terminal prompt also accepts the same commands (without the `d0rkw3b` prefix),
including category filters and structured formats. Enter `help`, `providers`,
or `quit`. EOF and Ctrl-C exit cleanly. Scripts should use direct commands.

Nothing opens by default. To send a target to one provider through your browser,
select its exact ID and add `--open`:

```sh
d0rkw3b search "Acme Corporation" --provider search-links-generate-links-clearnet-google --open
```

The browser and destination service may store queries, use cookies, require login,
or perform their own collection. Review provider notes before visiting a link.

## Tor and provider status

Use `--network tor` or `--network all` to include `.onion` links. D0RKW3B does not
start Tor, configure a proxy, or verify that Tor is running. It refuses automatic
opening of Tor links. Copy a selected link into a separately configured Tor Browser.
Clearnet indexes of onion content remain clearnet providers.

All migrated endpoints are **unverified**; none were live-probed during migration.
`enabled` means eligible for local query generation, not a health claim. Providers
may be unavailable, outdated, authentication-dependent, or geographically limited.
`--include-disabled` exposes retained reference definitions, including undocumented
Instagram queries, questionable WiGLE mappings, remote-probe launchers, and the
YouTube metadata endpoint requiring an API key. These cannot be opened with
`--open`. No API-key execution feature is supplied.

## Development and contributions

```sh
python -m pip install -e .
python -m unittest discover -s tests -v
d0rkw3b validate-providers
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [provider schema](docs/providers.md),
[pre-migration audit](docs/AUDIT.md), and the complete
[migration inventory](docs/migration-inventory.json). Adding most providers only
requires a JSON entry. Existing screenshots in `screenshots/` show the legacy UI.
The MIT [license](LICENSE) is unchanged. See [SECURITY.md](SECURITY.md) for reporting.
