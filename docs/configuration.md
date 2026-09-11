# Local preferences and diagnostics

Core use needs no configuration. An optional JSON file can contain:

```json
{
  "default_format": "text",
  "disabled_providers": [],
  "disabled_connectors": []
}
```

Default location: Linux `$XDG_CONFIG_HOME/d0rkw3b/config.json` (or
`~/.config/d0rkw3b/config.json`), macOS
`~/Library/Application Support/D0RKW3B/config.json`, Windows
`%APPDATA%\D0RKW3B\config.json`. `D0RKW3B_CONFIG` explicitly overrides the file path.
No file is created automatically. Unknown settings and malformed files produce
errors rather than quietly ignoring policy. Maximum size is 64 KiB.

`default_format` applies to legacy query output. New structured case/collection
commands default to JSON independently. Disabled providers stay in the registry
but are ineligible for normal generation/opening; `--include-disabled` displays
reference definitions. Disabled connectors cannot execute, even if explicitly
selected. Credential values are not supported in this configuration. Plugins name
required environment variables and do not receive secrets through registry data.

`--verbose` adds dispatch diagnostics on stderr without targets or credentials.
`--debug` adds traceback frames for expected errors; it excludes frame locals and
chained plugin exception messages. JSON stdout stays parseable. Active collection
explicitly discloses its target on stderr as part of informed execution, not as a
background log. No log file, crash upload, or persistent search history is created.

## Small query expressions

```sh
d0rkw3b investigate 'domain:example.com category:domain' --expression
d0rkw3b investigate 'username:alice' --expression
d0rkw3b investigate 'search:"Acme Corporation"' --expression
```

Grammar: `TYPE:VALUE [category:NAME]`, parsed using shell-style quoting. Only known
entity types and an optional category filter are supported. Values may contain
colons (URLs/IPv6). Explicit filters must not conflict. There is no eval, boolean
operator language, nested expression grammar, or implicit collection. Ordinary
commands still accept literal targets without expression interpretation.
