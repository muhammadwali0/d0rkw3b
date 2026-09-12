# Local cases, evidence, and exports

```sh
d0rkw3b case new acme
d0rkw3b case add acme example.com
d0rkw3b case add acme alice@example.com
d0rkw3b case note acme "Review certificate history"
d0rkw3b investigate example.com --recipe domain-footprint --case acme
d0rkw3b case list
d0rkw3b case show acme
d0rkw3b evidence add acme ./report.txt
d0rkw3b case export acme --format jsonl
d0rkw3b case graph acme --format graphml
d0rkw3b case graph acme --format gexf
d0rkw3b case timeline acme --format csv
```

All commands above are local. Cases are created only by `case new`; saving a run
requires an existing case. Normal query/investigate commands do not persist data.
`case add` generates and saves the default investigation plan, including its
selected generated queries. Case JSON records keep `generated_query` distinct
from observed evidence. Repeated runs retain separate observations and provenance,
even when they refer to the same normalized entity. Raw run input is also retained.

Storage defaults:

- Linux: `$XDG_DATA_HOME/d0rkw3b` or `~/.local/share/d0rkw3b`.
- macOS: `~/Library/Application Support/D0RKW3B`.
- Windows: `%LOCALAPPDATA%\D0RKW3B`.

An explicit `D0RKW3B_DATA_DIR` override supports testing or alternate local storage.
Paths inside a Git repository are refused. Case names are SQL values, never paths.
Database/evidence names are generated; path traversal and symbolic-link evidence
storage are rejected. New directories request owner-only permissions and new
SQLite files request mode 0600; Windows access control follows OS/user settings.
Local data is not encrypted by D0RKW3B. Protect backups and exported files.

## Evidence

`evidence add` explicitly copies a regular file byte-for-byte to a generated name.
It records original filename/path, stored relative path, MIME (signature when
recognized, otherwise extension guess), size, SHA-256, import timestamp, file
entity and provenance. Source files are not modified or uploaded. Copying streams
through a temporary file and flushes it before atomic rename; a database failure
removes the new copy. A process crash between rename and database commit may leave
an unreferenced copy; it does not corrupt existing evidence. Back up the entire
data directory with the application closed. Do not edit acquired copies.

The helper checks source size/mtime/inode before and after reading and rejects
observed changes; an immutable source copy is best for strict acquisition needs.
File MIME/metadata is not proof of authenticity. Symbolic-link inputs are resolved
only when explicitly supplied, and the resolved original path is recorded.

## Database evolution

SQLite schema 1 contains cases, per-case entities, runs, relationships,
observations, notes and evidence. Foreign keys are enforced, including same-case
entity/run/relationship references. Writes use transactions. JSON columns contain
variable provenance/metadata, while identity and join fields have SQL constraints
and indexes. Timestamps are timezone-bearing ISO strings; timeline sorting parses
them as dates rather than relying on lexical offsets.

An empty version-0 database initializes atomically. Unknown nonempty databases
and newer schema versions are refused without rewriting their contents. Future
migrations must back up before upgrade, increment `user_version` in the same
transaction, and test preservation/rollback. Initial-schema rollback means
restoring a backup, not silently dropping user tables. Readers never initialize
missing storage. Concurrent SQLite writers use a five-second busy timeout.

## Exports and time

JSON preserves the complete case schema. JSONL emits typed records; CSV includes
record type, timestamp kind and JSON payload so nested provenance is retained.
Markdown provides a table of these records. GraphML and GEXF include entities and
only provenance-backed relationships, with full record JSON on each node/edge.
Generated URLs never create speculative profile edges. Repeated observations of
the same relationship retain separate run edges.

Timeline distinguishes created, observed and collected timestamps. A generated
query timestamp is creation, not observation of a remote account. Provenance
collection time is a separate event even when equal to observed time. Filesystem
mtime and ctime remain labeled file metadata; ctime is OS-dependent, not assumed
to be a document's creation time. STIX and a graphical UI are not implemented.
