# Getting started

D0RKW3B 1.1.0 requires Python 3.10 or newer. Tests are configured for 3.10–3.14 on
Linux, plus Python 3.13 on Windows/macOS. Local verification results are recorded
separately; configured CI is not a claim that remote jobs already ran.

From a checkout, install with `pipx install .` or `uv tool install .`. To use a venv:

```sh
python -m venv .venv
# Linux/macOS:
. .venv/bin/activate
# Windows PowerShell instead:
# .venv\Scripts\Activate.ps1
python -m pip install .
d0rkw3b --help
```

No PyPI publication or OS package is assumed. `python -m d0rkw3b` uses the same CLI.
You need no service account or API key for queries, planning, cases or core
connectors. Optional tools such as ExifTool must be installed independently.

```sh
d0rkw3b investigate example.com --recipe domain-footprint
d0rkw3b username alice --format json
d0rkw3b interactive
```

These are offline. Use the numbered query categories or type complete workbench
commands at the interactive prompt. `help` shows commands; `quit`, EOF or Ctrl-C
exits. Scripts should use direct commands and structured output.

To explicitly collect, first inspect `d0rkw3b connectors`, then choose one with
`collect ... --connector ID` or `investigate ... --with ID`. A case is never
created implicitly. `case new NAME` creates one under platform-local storage.
