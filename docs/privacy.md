# Privacy and Tor

No telemetry, usage analytics, crash uploads, startup checks, silent search
history, remote case storage or listening server. Query and recipe processing
stays local. Snapshots are local files activated explicitly, not background updates.

Explicit actions cross boundaries:

- `--open`: sends one generated query through your browser. Provider cookies,
  login, tracking and retention are outside D0RKW3B.
- `providers health`: public homepage HEAD requests without investigation targets.
- DNS/RDAP connectors: disclosed DNS/registration lookups for your chosen entity.
- Local-file/ExifTool: local file reads and, when chosen, a subprocess; no upload.
- Case/evidence commands: intentional persistence under platform-local storage.
- Plugins: explicitly invoked trusted Python code with declared capabilities,
  not an enforced sandbox. Review code before installing or enabling it.

Health never contacts `.onion` providers. Query generation includes them only with
`--network tor` or `all`. `--pack darkweb` does not override that requirement.
D0RKW3B does not start Tor, infer proxy configuration, route clearnet requests via
Tor, or open onion URLs in the default browser. Copy selected Tor links into a
separately configured Tor Browser. Clearnet onion indexes remain clearnet sites.

Local data is not encrypted by the application. Exports, terminal scrollback,
case files and evidence may contain sensitive information. Protect them with your
OS access controls and backups. Do not post private data or credentials in issues.
No account is required to use the core; optional plugins may require independently
managed credential environment variables. API-key values do not belong in config.
