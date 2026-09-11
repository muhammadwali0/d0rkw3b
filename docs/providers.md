# Provider definitions

Bundled providers live in `src/d0rkw3b/providers/*.json`. Each file contains an
array of objects. JSON keeps the core free of runtime dependencies; IDs must be
unique across bundled and additional files. Load community files with
`--provider-file path.json` or `--provider-file directory` (repeatable).
Invalid entries are skipped with source/index diagnostics on stderr; valid entries
still work. `validate-providers` exits 1 if any entries fail. Duplicate IDs do not
override an earlier definition. Additional files are data, never executed Python.

Required fields:

| Field | Meaning |
|---|---|
| id | Lowercase letters/digits with hyphen separators; globally unique |
| name, description, category | Nonempty display/selection metadata |
| template | HTTP(S) URL with simple `{variable}` fields |
| target_types | Nonempty list of supported target types |
| parameters | Nonempty list of recognized input variables |
| tags | List of strings |
| network | `clearnet` or `tor`, consistent with hostname |
| auth | `none`, `unknown`, `may_require`, or `required` |
| requires_api_key, enabled | JSON booleans |
| homepage | HTTP(S) provider home URL, same network |
| status | `active`, `unverified`, `deprecated`, `broken`, or `disabled` |
| last_verified | Null, or an actual verification date as YYYY-MM-DD |
| notes | Nonempty limitations, verification context, or usage notes |
| source | Nonempty provenance, e.g. original function or contribution source |

Types: `search`, `username`, `email`, `domain`, `ipv4`, `ipv6`, `url`, `document`,
`video_id`, `phone`, `user_id`, `location_id`, `list_id`, `repository`, `company`.
`ip` is a CLI alias that selects IPv4 or IPv6 after validation.

Variables: `query`, `username`, `username2`, `email`, `domain`, `ip`, `url`,
`video_id`, `phone`, `user_id`, `location_id`, `list_id`, `repository`, `company`,
`year`, `next_year`. Search/document supply `query`; IPv4/IPv6 supply `ip`.
Other types supply their matching variable. `next_year` derives from `year`.
Supply additional inputs through `--param NAME=VALUE`.

All substituted values are percent-encoded with `urllib.parse.quote(safe='')`.
Spaces use `%20`, literal plus signs use `%2B`, and nested target URLs are encoded
as a value. Static search operators belong in the template, already URL-encoded
where needed. Literal braces must be doubled (`{{` and `}}`). No Python field
access, conversions, or format specifications are allowed. Variables in hostname
positions must contain a valid single DNS label. Do not encode a placeholder twice.

Copy a relevant existing entry, use a new ID and real source URL, then validate.
Use `unverified` and null dates until actual verification. Describe login/API-key
requirements honestly. Retain broken/deprecated links disabled with an explanation.
Do not submit credentials, copied session tokens, tracking parameters, or claims
of health based only on successful URL generation.
