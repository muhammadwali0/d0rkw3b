# Provider verification and recommendations

`d0rkw3b providers health` explicitly contacts at most 10 unique public provider
hosts. Select IDs with repeated `--provider`, and set `--max-requests` (1–100),
`--timeout` (socket seconds, default 5, maximum 30) or `--delay` (minimum 0.25,
default 0.5). `--format json` emits a report suitable for shell redirection.

The checker uses sequential HEAD requests to origin homepages, never an
investigation query. It sends an identifying User-Agent, rejects non-public IPs,
pins resolved addresses, verifies TLS, and ignores environment proxies. It never
follows redirects, sends cookies or credentials, reads response bodies, retries,
or probes Tor. DNS resolution follows the operating system's resolver timeout;
this is not a hard overall process deadline. CI additionally limits job duration.

A report separates `structurally_valid`, `template_valid`, `reachable`, and
`semantic_status`. HTTP 2xx produces health `healthy`, meaning **homepage
reachability only**. It never sets semantic verification. 3xx is `redirect`, 401
is `auth-required`, 403/405 require manual verification, 429 is `rate-limited`,
and other HTTP errors are `degraded`. DNS, TLS, connection and timeout failures
have separate outcomes. No response is equated with target existence.

Skipped definitions have null `last_checked`. Disabled/keyed/authenticated
providers require manual verification. Tor is `tor-unchecked`. The request budget
can leave entries `unknown`. A repeated host reuses its exact checked URL/result,
including Retry-After; no additional request is made to that host. `failure_count`
is the number of failed network attempts for that host **in this run** (0 or 1),
not a historical failure streak. Reports do not modify registry files or dates.
Only an actual semantic review should set registry `last_verified` and optional
`verification: {method, confidence, notes}` metadata. Confidence is qualitative.

A separate scheduled/manual workflow generates a bounded health artifact. Provider
429s and outages do not fail normal tests or modify the registry. Structural errors
still produce a nonzero command exit. No automatic issues are created.

## Transparent ranking

`quality: {priority, reason}` supplies an editorial priority from 0 to 5, scored
as priority × 10. Additional components: no API key +3, auth none +2, unknown 0,
may_require −2, required −4, disabled −100, broken/deprecated/disabled status −50.
Stable IDs break ties. These are visible judgments, not scientific reliability,
privacy or speed estimates. No inferred health/freshness bonus is applied.

Text queries show the top 10 by default, with an additional-count notice on stderr.
`--all` exposes every matching result. Explicit `--provider` selection and existing
JSON/CSV/Markdown formats remain complete. Machine output keeps the v1 row schema
but is now ranked instead of alphabetical. `providers list` aliases `providers`;
`dev validate-providers` aliases the old validation command; `dev registry-stats`
prints counts from the current registry.

Protocol basis: [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html) and
[Python HTTP client](https://docs.python.org/3/library/http.client.html).
