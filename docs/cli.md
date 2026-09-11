# CLI reference

Run `d0rkw3b --help` and each group's `--help` for accepted flags.

| Command | Purpose |
|---|---|
| `TARGET`, `TYPE TARGET` | Offline query generation with automatic detection or explicit type |
| `investigate TARGET` | Structured offline paths and provenance; optional explicit --with/--case |
| `recipes list`, `recipes info NAME` | Discover actual declarative methodologies |
| `providers`, `providers list` | Query registry definitions |
| `providers health` | Explicit bounded homepage checks, no semantic claims |
| `providers update FILE --sha256 HASH`, `providers rollback` | Explicit local snapshot activation/rollback |
| `packs list` | Logical provider groups |
| `connectors`, `integrations` | Capabilities and installed-tool availability |
| `collect [TYPE] TARGET --connector ID` | Explicit collection |
| `file PATH [--with exiftool]` | Local file inspection, never upload |
| `case new/list/show/add/note/export/graph/timeline` | Local investigation storage and projections |
| `evidence add CASE FILE` | Explicit byte-preserving acquisition |
| `dev validate-providers`, `dev validate-recipes`, `dev registry-stats` | Offline maintenance checks |
| `interactive` | Guided queries and the same workbench command APIs |

Query types retain search, username, email, domain, IPv4/IPv6 (`ip` alias), URL,
document, video_id, phone, user_id, location_id, list_id, repository and company.
File, file_hash and hostname entities support collection; they do not imply new
URL-provider coverage. Domain/hostname normalization uses IDNA without DNS lookup.
Ambiguous text is search; `@alice` is username; explicit overrides use `--type`.

Query options: `--category`, `--pack`, repeatable `--provider`, `--provider-file`,
`--param NAME=VALUE`, `--network`, `--include-disabled`, `--all`, `--format`, `--open`.
`--open` requires exactly one enabled nondeprecated clearnet provider and never
opens Tor or API-key reference definitions. Generated query JSON/CSV/Markdown keep
the legacy row structure; ranking changes ordering, not coverage. Text defaults
to 10 recommendations. `--all` expands it; explicit provider selection stays exact.

Investigation options add `--recipe`, `--recipe-file`, `--with`, `--case`,
`--expression`, `--category` and `--pack`. Plans show five queries per stage unless
`--all` is set. JSON retains entities/observations/provenance. Investigation CSV
adds a `kind` column (`generated_query`); Markdown labels the query projection.
Full active observations are in JSON and saved cases, not flattened query exports.

Legacy advanced examples:

```sh
d0rkw3b username alice --category x --param year=2024
d0rkw3b username alice --category instagram --param query="search terms"
d0rkw3b username alice --category instagram --param username2=bob
d0rkw3b repository project --category github
d0rkw3b company acme --category linkedin
d0rkw3b document "annual report"
d0rkw3b video_id dQw4w9WgXcQ
```

Global `--verbose`/`--debug` go to stderr. Use `--` before literal values that look
like flags. JSON stdout contains no banner or diagnostics. Ordinary error exits
are 2, validation failure is 1, interruption is 130, success is 0. Temporary
provider outages are report data, not a failing health command. Shell redirection
uses the shell's normal overwrite rules; D0RKW3B does not silently write exports.
