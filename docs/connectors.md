# Explicit collection

Query providers generate URLs offline. Connectors deliberately collect observations.
Nothing runs because it appears in a recipe or provider registry. These commands
explicitly grant the chosen connector its declared capabilities:

```sh
d0rkw3b connectors
d0rkw3b collect domain example.com --connector dns
d0rkw3b investigate example.com --with rdap
d0rkw3b collect ip 1.1.1.1 --connector rdap
d0rkw3b file ./document.pdf
d0rkw3b file ./photo.jpg --with exiftool
d0rkw3b collect domain example.com --connector dns --case acme
```

The CLI prints connector, target, destinations/capabilities, required credential
variable names, expected output and limitations on stderr before execution. JSON
stdout remains structured. Use `--timeout` on collect/file for a bounded override
(up to 60 seconds). Multiple connectors run sequentially, maximum five distinct
IDs per command. Missing cases fail before collection. Result observations,
relationships and provenance can be explicitly saved to an existing case.

| Connector | Capability and result |
|---|---|
| dns | System resolver A/AAAA lookup in an isolated child Python process; produces observed resolves_to edges |
| rdap | GET IANA bootstrap and selected HTTPS RDAP registry; validates returned domain/IP object and records registration metadata, plus domain nameserver edges |
| local-file | Stream a regular local file for SHA-256 and bounded header/text inspection; produces a file_hash entity and has_hash edge |
| exiftool | Optional installed ExifTool subprocess, fixed read-only tags, no user ExifTool config, no file writes or upload |

DNS child execution has a hard process timeout. DNS resolver infrastructure,
caching and retries follow OS configuration. DNS output is not proof of ownership
or DNSSEC validation. RDAP HTTP requests use the public-address-pinned transport,
TLS validation, per-socket timeouts, 1 MiB response limits, no credentials,
redirects or retries. Bootstrap requests contain no target. The selected registry
receives the requested domain/IP. OS DNS resolution follows system timeout policy.
Some RDAP deployments redirect: these return a useful error rather than following
an undeclared destination. 401/403/429 are not bypassed. Registration records can
be redacted, stale or incomplete and are not attribution.

Local-file inspection hashes the entire file; header/text parsing is capped at
1 MiB. PNG/GIF and common JPEG headers provide dimensions. MIME can be a signature
or extension guess, explicitly labeled. UTF-8 text references are bounded candidates,
not verified entities. Parsing checks its time budget between read chunks; an OS
file read itself may block. Source changes observed while reading are rejected.
ExifTool optionally provides image EXIF/GPS/device/timestamps and document author,
title/producer/page counts where the installed tool supports the file. Metadata
is untrusted and can be forged. Extracted file timestamps keep their source labels.

No CT or Wayback scraper was added: those remain query paths. No social-platform
scrapers, CAPTCHA bypass, credential collection or speculative ownership edges.

## External tools

`d0rkw3b integrations` detects Sherlock, Maigret, ExifTool, theHarvester and Amass
on PATH without executing them. Only ExifTool currently has an execution adapter;
the others are explicitly `detection-only`, not claimed integrations. None is
vendored or required by the base package. Install optional tools independently
under their own licenses. ExifTool is distributed by its authors under the same
terms as Perl; D0RKW3B invokes its installed CLI without copying its code.

The adapter has deterministic mocked JSON/argument tests; the repository's unit
suite does not require or claim a live installed ExifTool run. Network connectors
are tested with mocked public responses, not invasive live checks.

Sources: [RDAP query format](https://www.rfc-editor.org/rfc/rfc9082.html),
[IANA bootstrap registries](https://data.iana.org/rdap/),
[ExifTool documentation and license](https://exiftool.org/).
