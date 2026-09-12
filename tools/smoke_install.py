"""Run against an installed wheel from a temporary directory, never source imports."""

import importlib.metadata
import json
import os
import subprocess
import sys
import sysconfig
import tempfile
from pathlib import Path


def smoke():
    import d0rkw3b

    assert d0rkw3b.__version__ == importlib.metadata.version("d0rkw3b")
    assert len(d0rkw3b.providers(bundled=True)) >= 425
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        env = os.environ | {
            "D0RKW3B_DATA_DIR": str(root / "data"),
            "D0RKW3B_CONFIG": str(root / "config.json"),
        }
        env.pop("PYTHONPATH", None)

        def run(*args, as_json=False):
            result = subprocess.run(
                [sys.executable, "-m", "d0rkw3b", *args],
                cwd=root,
                env=env,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            )
            return json.loads(result.stdout) if as_json else result.stdout

        run("--help")
        run("providers", "list", "--format", "json", as_json=True)
        run("providers", "health", "--help")
        run("dev", "validate-providers")
        run("dev", "validate-recipes")
        run("recipes", "list")
        run("investigate", "example.com")
        run("investigate", "alice", "--type", "username")
        run("search", "open source intelligence")
        assert run("domain", "example.com", "--format", "json", as_json=True)
        assert not (root / "data").exists()
        run("case", "new", "test-case")
        run("case", "add", "test-case", "example.com")
        assert run("case", "show", "test-case", as_json=True)["entities"]
        path = root / "local document.txt"
        path.write_text("Example https://example.com", encoding="utf-8")
        run("file", str(path), as_json=True)
        run("evidence", "add", "test-case", str(path), as_json=True)
        run("case", "graph", "test-case", "--format", "graphml")
        executable = Path(sysconfig.get_path("scripts")) / (
            "d0rkw3b.exe" if os.name == "nt" else "d0rkw3b"
        )
        subprocess.run(
            [str(executable), "--version"],
            cwd=root,
            env=env,
            check=True,
            capture_output=True,
        )
    print("Installed-wheel smoke checks passed; temporary cases and files removed.")


if __name__ == "__main__":
    smoke()
