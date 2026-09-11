# Contributing

Provider improvements, reproducible bug reports, documentation and tests are welcome.
Use Python 3.10+ and install with `python -m pip install -e .`.

For providers, follow [the schema](docs/providers.md). Most additions only need
JSON, not Python. Include the source of the URL, applicable target types, login
requirements, and known limitations. Do not claim live verification without it.
Keep deprecated definitions with honest metadata instead of silently dropping them.

Run `python -m unittest discover -s tests -v` and `d0rkw3b validate-providers`.
For Python changes, include tests for changed behavior, especially encoding,
privacy defaults, detection and malformed community input. Avoid target network
requests in tests. Describe the problem, changes and commands run in your PR.
Do not include personal target data or secrets in issues or fixtures.

The original migration is reproducible through `tools/migrate_providers.py` against
baseline commit `9e49913`. This is an archival migration tool, not a routine update
command: rerunning it overwrites the migrated registry and inventory. The coverage
test checks every legacy link; update expected coverage deliberately when adding
new entries, while retaining the migration subset and equivalence checks.
