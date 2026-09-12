# Connector plugin API v1

Static query providers and recipes are JSON data and never require Python.
Executable connectors are separately installed Python distributions. They have
full Python privileges when explicitly invoked; capability metadata is **not a
sandbox**. Review code and distribution provenance before installing a plugin.
Installing a Python package can itself execute build code, outside D0RKW3B.

A plugin declares an entry point in group `d0rkw3b.connectors`, named for its
connector ID. It must also package exactly one file named `d0rkw3b-plugin.json`.
Normal query/investigate commands do not even discover plugins. `connectors`
discovers distribution metadata and reads static JSON, without importing plugin
code. Only `--connector ID` or `--with ID` loads that entry point, after disclosure.
Malformed manifests, duplicate/reserved IDs and unsupported API versions are rejected.

Packaging example (illustrative, not a claimed published package):

```toml
[project.entry-points."d0rkw3b.connectors"]
my-local-connector = "my_connector:collect"

[tool.setuptools.package-data]
my_connector = ["d0rkw3b-plugin.json"]
```

The JSON document contains `api_version: 1` and `connectors`, an object keyed by
entry-point name. Each value has the Manifest fields shown by `d0rkw3b connectors`:
`id`, `name`, `accepted_types`, `produced_types`, `capabilities`, `description`,
`rate_limit_notes`, `timeout_seconds`, `required_keys`, `optional_keys`, `api_version`.
Capabilities contain `network` (destination descriptions), `filesystem_read`
(boolean), and `subprocess` (boolean). Credential fields name environment variables,
never key values. The manifest must be <=64 KiB and match its entry-point ID.

Lifecycle: the entry point is a callable `collect(entity, *, timeout)` returning
a `Collection`. It must perform only declared work, honor the timeout, bound
responses/subprocesses, respect rate limits, and return typed entities,
provenance-backed relationships and observations. Each output must reference known
entities/relationships and preserve the input entity. Plugins must not persist case
data themselves; the core saves an accepted collection only with explicit --case.

The SDK types are `Entity`, `Provenance`, `Relationship`, `Observation` from
`d0rkw3b.core.entities`, and `Collection`, `Capabilities`, `Manifest` from
`d0rkw3b.connectors.models`. These named types are the version-1 connector contract;
other internal modules are not a supported plugin API. Exceptions become concise
errors. Plugin exception text is suppressed in normal output to avoid secret leaks.

Tests must use mocked network/subprocess boundaries, assert provenance and
capabilities, handle missing tools and malformed responses, and confirm no code
loads during discovery. The core suite includes one internal test plugin with a
static manifest and load spy. No fake external plugin packages are shipped.
