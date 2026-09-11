# Pre-migration audit

Audited baseline: `9e49913`. All 15 root Python files, README, license,
ignore rules, tracked tree and menu call sites were inspected before code changes.
The five existing screenshots describe the legacy UI, not the new application.
There are no packaging files, tests, workflows, or repository agent instructions.
The MIT license and copyright must remain intact.

## Existing behavior and migration requirements

`main.py` prints a banner on import and implements 14 menu categories. Provider
modules return dictionaries of URLs; `search_links` returns clearnet and Tor
dictionaries. No module fetches targets or opens a browser. The unused `requests`
import in LinkedIn contradicts the README's standard-library-only installation.
Most modules use quote_plus, while several interpolate raw input or replace
whitespace with plus signs. Path segments and nested URLs need central encoding.
There is no validation, EOF handling, scripting interface, or structured output.

All 35 provider functions must be inventoried by source function and dictionary
key, including the unreachable-in-menu GitHub general search. Preserve Facebook
phone/user/location IDs, X IDs/lists/year filters/real names, Instagram paired
usernames and username-plus-term searches, LinkedIn companies/post URLs, GitHub
repository searches, image URLs, video IDs and all document filetype queries.
Generic URL input should expose existing reverse-image and post-URL launchers.
Ambiguous text should be a search, not a guessed username.

## Findings

- LinkedIn repeats the `Profile` dictionary key, overwriting its encoded variant.
- Google image queries carry copied tracking/session parameters and an unrelated
  apple query. Preserve the image search intent and remove those parameters.
- YouTube metadata embeds an API key. Remove it from maintained files; retain the
  endpoint disabled with `requires_api_key`, without providing a replacement key.
  The credential remains in git history and should be revoked by its owner.
- Instagram GraphQL links rely on undocumented query hashes and authentication;
  retain disabled and unverified. Do not fetch followers automatically.
- X year queries use an exclusive end date of December 31, omitting that day;
  render January 1 of the following year instead.
- Archive URLs include fixed historical dates. Preserve these as historical
  snapshots, not claims of current archives or availability.
- IPAddress.com has an IPv4-only route. Restrict that definition to IPv4.
- WiGLE SSID/postal links in the IP module are semantically questionable; retain
  disabled with notes. Port scan, traceroute and SSL-test launchers may initiate
  remote activity when visited; keep disabled by default and describe this.
- Tor addresses and other providers have not been network-verified. Metadata must
  say unverified with no invented last-verified date. Tor links require explicit
  selection and must never open through an ordinary browser automatically.
- README overstates GitHub and IP coverage and references unavailable features.
  Replace claims with behavior backed by the registry and CLI.

## Architecture decisions

Use JSON provider files: the existing zero-runtime-dependency design is a concrete
reason to use the standard-library parser instead of adding YAML. Each definition
has stable ID, provenance, target types, category, URL template and honest status.
Keep a machine-readable complete inventory before replacing any legacy module.
Centralize validation/rendering and use argparse, ipaddress, urllib.parse,
importlib.resources and unittest. No runtime networking, telemetry, account,
API-key requirement, persisted target history, or server. Browser launch is opt-in.
EOF and interruption must exit cleanly; JSON output must remain deterministic.
