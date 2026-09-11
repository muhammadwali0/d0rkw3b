# Development, releases and community packaging

Version 1.1.0 extends the v1 query interface. Default human output is ranked and
shortened; `--all` preserves complete text coverage and legacy machine rows remain
complete. The public Python API and plugin API are introduced at this version.
All 425 legacy definitions remain. No GitHub/PyPI release is published by this work.

```sh
python -m pip install -e ".[dev]"
python -m pytest -q
ruff check .
ruff format --check .
d0rkw3b dev validate-providers
d0rkw3b dev validate-recipes
python -m build
python tools/release_manifest.py dist
```

Use a clean output directory containing one wheel and one source archive. The
manifest tool validates archive paths, wheel RECORD hashes, bundled data, package
identity and absence of base runtime dependencies. It generates SHA256SUMS and a
minimal SPDX 2.3 runtime-distribution SBOM for the built artifacts. This describes
the dependency-free runtime distribution, not a complete SBOM of build tools or
optional plugins installed elsewhere.

Install the built wheel into a fresh virtual environment, run `pip check`, then
run `python tools/smoke_install.py` with that environment's Python. The smoke tool
executes CLI checks from a temporary directory without PYTHONPATH, verifies both
entry points, creates temporary cases/evidence and cleans them up. It never probes
live providers. Source unit tests mock DNS/RDAP/tool responses and plugin loading.

## Workflows

Normal CI uses Python 3.10–3.14 on Linux and 3.13 on Windows/macOS. It checks tests,
lint/format, provider/recipe validation, builds, artifact integrity, wheel install,
pip check and CLI smoke behavior. A separate weekly/manual health job checks at
most 20 public origins and uploads a report without rewriting provider definitions.
Security workflows prepare CodeQL and dependency review. Action versions are
pinned to verified upstream refs; Dependabot can propose bounded monthly updates.

The manual/tag-triggered release-build workflow produces artifacts/checksums/SBOM
and GitHub build provenance attestations. It does not create a release or publish
to PyPI. Platform features such as attestations, dependency review and secret
scanning require repository-host availability/settings; configuration alone does
not prove these services have run. Maintainers should enable host secret scanning
and push protection if available. No long-lived publishing credential is added.

Future PyPI publishing should use Trusted Publishing with an explicitly approved
GitHub environment and the minimal id-token permission, following PyPI's current
setup instructions. Actual publishing, tags and release creation require separate
authorization. Do not force push or bypass branch protection; work through PRs.

## Distribution readiness

Local installation supports pip in virtualenvs, pipx and uv tool via the standard
wheel/console-entry-point mechanism. No runtime service or API key is required.
Optional ExifTool remains an independently installed executable.

Community packagers can use tagged source archives and checksummed wheels once a
release is actually published. There are no Homebrew, AUR, Scoop, WinGet, Kali or
BlackArch packages claimed or created here.

- **Homebrew:** a Python virtualenv-style formula can install the wheel; generate
  actual URL/version/checksum from a published artifact and test on macOS.
- **AUR:** a PKGBUILD should build from source with the distribution Python build
  backend and run the offline suite; do not write user case data during packaging.
- **Scoop/WinGet:** use a tested Python application installation strategy and
  platform-appropriate entry point; no standalone Windows executable is supplied.
- **Kali/BlackArch:** follow the distribution's Python package policy, retain the
  MIT license and registry data, and keep ExifTool optional.

These are maintainer guidance, not placeholder manifests. Docker is omitted:
local files, browsers and case directories fit a normal local Python installation.
