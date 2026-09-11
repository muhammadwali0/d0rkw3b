# Explicit registry snapshots and packs

The bundled registry always works offline. There is no remote update endpoint,
automatic update check, account or telemetry. For reviewed local updates:

```sh
d0rkw3b providers update /path/to/providers.json --sha256 EXPECTED_FILE_SHA256
d0rkw3b providers rollback
```

The input is a complete JSON provider array (maximum 10 MiB). Obtain its expected
SHA-256 through a trusted independent channel. A checksum establishes byte
integrity, not publisher authenticity or safety of destinations. Every definition
is validated before activation. Existing bundled IDs, target coverage, category
and network must be preserved. Duplicate IDs and removal of bundled definitions
are refused. Disabled/deprecated metadata is the way to retain obsolete coverage.

Activation writes a normalized snapshot and its checksum atomically under the
application-data directory's `registry/`. A previous validated snapshot supports
one-level rollback; further rollback restores the bundled registry. Corrupt active
snapshots produce a diagnostic and fall back to bundled data. If active state is
corrupt, rollback before installing another snapshot. Nothing uploads targets.
No Python or plugin code can be supplied through registry snapshots.

Use `providers list --network all --include-disabled --format json` to export the
effective complete registry for review. The bundled source remains available in
the installed package. `--provider-file` continues to add unique community entries.
For eventual remote delivery, a caller can fetch a separately authenticated
snapshot and feed these same validation/activation APIs. No update infrastructure
or signature authority is invented here.

## Logical packs

```sh
d0rkw3b packs list
d0rkw3b providers list --pack infrastructure
d0rkw3b investigate example.com --pack infrastructure
d0rkw3b search "example" --pack darkweb --network tor
```

Packs group existing metadata without copying or splitting definitions: core,
social, infrastructure, development, documents, media, email and darkweb.
Counts are computed from the effective registry. Contributors may add a `packs`
array to definitions. `--network` remains independent: choosing darkweb does not
silently enable Tor. Use `dev registry-stats` for current coverage/status counts.
