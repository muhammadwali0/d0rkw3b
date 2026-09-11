# Future local UI and browser integration contract (not implemented)

The supported Python `investigate` API and explicit `CaseStore`/connector models
provide a foundation for an optional local UI. No HTTP service, UI command or
browser extension is currently shipped. This avoids duplicating the CLI's
investigation logic before the interface is proven.

A future adapter should expose versioned operations mirroring the core:

| Proposed operation | Boundary |
|---|---|
| POST /v1/plans | Typed selected text/current URL to the offline investigation API |
| GET /v1/providers and /v1/recipes | Read-only validated metadata |
| POST /v1/cases/{id}/entities | Explicit case addition with provenance |
| POST /v1/collections | Explicit connector ID and capability approval |
| POST /v1/cases/{id}/evidence | Explicit local import; never an arbitrary URL fetch |

Requirements before implementing this adapter: loopback-only binding by default,
an unguessable per-session authorization token, strict Origin/Host checks, CSRF
protection for mutations, bounded request bodies, no wildcard CORS, no credentials
in URLs, and no unreviewed file paths from a browser extension. The extension must
pair explicitly with the local instance and obtain user intent for case writes
and collection. Browser-selected text remains input data, not executable commands.
Do not expose an unauthenticated local API to external interfaces. UI dependencies
would be optional; no JS toolchain, cloud account or remote storage is required by
the current architecture. These are design requirements, not claims of a service.
