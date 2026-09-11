# Changelog

## 1.1.0

- Position D0RKW3B as a local OSINT workbench, retaining all 425 legacy query definitions.
- Add explicit conservative provider-health reports, editorial ranking, logical
  packs, validated local registry snapshots with SHA-256 and rollback.
- Add typed entities, provenance, observations, relationships, seven declarative
  recipes, offline `investigate`, typed expressions and a public Python API.
- Add explicit local SQLite cases, notes, repeated runs, byte-preserving evidence
  import, SHA-256, JSONL/CSV/Markdown exports, timelines, GraphML and GEXF.
- Add explicit DNS, RDAP and local-file connectors, optional read-only ExifTool
  adapter, installed-tool detection, static capability manifests and plugin API v1.
- Add validated local preferences and stderr diagnostics without automatic target
  persistence, network activity, telemetry, or plugin imports during planning.
- Expand offline tests, platform/Python CI, wheel-install checks, checksums, SPDX
  runtime SBOM, release-build/attestation preparation and security workflows.
- Add workbench, privacy, plugin, packaging, translation and future interface docs.

Compatibility: human query output now shows 10 ranked recommendations by default;
use `--all` for full text output. Legacy JSON/CSV/Markdown query rows remain complete
but are ranked. New investigation CSV explicitly labels generated queries. No
providers were removed. No GitHub or PyPI publication is performed by this change.

## 1.0.0

- Installable src-layout package with console/module entry points and no runtime dependencies.
- Declarative registry preserving 425 legacy links, target detection, central
  encoding, guided menus, text/JSON/CSV/Markdown and browser/Tor safeguards.
- Retain questionable endpoints disabled and unverified. Remove the bundled API
  key and copied image query parameters; fix exclusive X year boundaries.
- Add offline regression tests, migration inventory and community documentation.
