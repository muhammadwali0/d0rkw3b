# Contributing to D0RKW3B

Contributions can improve providers, fix URLs, add investigation recipes, build
connector plugins, document integrations, translate pages or improve tests.

Start from a feature branch. Keep commits focused and use pull requests; never
force push or rewrite shared history to resolve a conflict.

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check .
ruff format --check .
d0rkw3b dev validate-providers
d0rkw3b dev validate-recipes
```

## Static providers: one data-file change

Copy a relevant JSON entry in `src/d0rkw3b/providers/`, give it a unique ID and real
source/homepage, choose appropriate targets, and run validation/tests. Most
provider contributions require no Python. See [the schema](docs/providers.md).
Never submit credentials, copied session tokens, target data or invented health
claims. Use unverified/null dates unless actual semantic review supports them.
Keep broken/deprecated providers as disabled definitions with explanatory notes.

The migration inventory protects all 425 original URLs. New providers should be
added to the coverage test's extension expectations without deleting the baseline
subset checks. The one-time migration tool targets historical commit 9e49913 and
must not be rerun as a routine update: it overwrites current registry edits.

## Recipes and executable extensions

Recipes are JSON methodology with real existing provider IDs and compatible types;
see [investigations](docs/investigations.md). No arbitrary code or silent connectors.
For executable extensions, follow [plugin API v1](docs/plugins.md): static capability
manifest, explicit invocation, bounded collection, provenance, deterministic mocked
tests and useful unavailable-tool errors. Do not vendor another project's code or
call detection an integration. No CAPTCHA/login bypass or speculative attribution.

## Documentation and review

English is canonical; see [translation guidance](docs/translations/README.md).
Keep source commands, privacy guarantees and verification status accurate. Do not
claim future work as delivered or use screenshots from another version as evidence.

Suggested issue labels (maintainers may create them): broken-provider, new-provider,
recipe, connector, integration, translation, good-first-issue and help-wanted.
Templates prompt for the necessary evidence; CI validates provider and recipe data.
Include sanitized reproduction steps and exact validation commands in PRs. Use
nonsensitive fixture targets. See [SECURITY.md](SECURITY.md) for vulnerability reports.
