# Troubleshooting

- **Command missing:** activate the environment used to install the checkout, or
  use its `python -m d0rkw3b`. For pipx/uv tool installs, check their bin directory
  is on PATH. Running root `main.py` also requires an installed package.
- **No matching providers:** check the explicit type, category, pack and network.
  Document dorks use `document`; video IDs use 11-character `video_id`. Use
  `providers list --network all --include-disabled --format json` to inspect data.
- **Only a few queries shown:** text defaults to 10 and investigation stages to 5.
  Use `--all`. A generated URL never proves that a profile or document exists.
- **Provider unavailable/login/CAPTCHA:** use metadata and manual review. Health
  is only homepage reachability. D0RKW3B does not bypass access controls or retry
  rate limits automatically. Unverified is not a claim of either health or death.
- **RDAP redirect/error:** the connector intentionally does not follow redirects;
  use the retained query providers or inspect the service manually. A 429/403 is
  not a definitive absence finding.
- **ExifTool missing:** `integrations` reports availability; install it separately
  if desired. Other detected tools currently have no execution adapter.
- **Case missing:** use `case new NAME` before saving. Check the platform data path
  or `D0RKW3B_DATA_DIR`. Storage inside a Git repository is deliberately refused.
- **Database newer than application:** use an application version supporting that
  schema or restore a compatible backup. Never delete case files to fix a version
  error. Back up the full data directory while the application is closed.
- **Registry integrity error:** bundled definitions remain usable. Run
  `providers rollback` to remove a corrupt active snapshot or restore a prior one.
- **Invalid config:** correct the named JSON file or point `D0RKW3B_CONFIG` at the
  intended configuration. Only documented settings are accepted.
- **Interrupted git pull/rebase:** inspect `git status`, resolve stated conflicts,
  and continue the pending operation. Do not force push or reset away local work.
  Use feature branches and pull requests when the repository requires them.

For reports, include Python/OS/package versions and a command using a nonsensitive
example. `--debug` adds traceback frames on stderr without frame locals. Review
all output before posting; do not share case contents or credentials.
