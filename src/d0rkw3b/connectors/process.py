"""Bounded subprocess output and time; no shell evaluation."""
import json
import os
import subprocess
import tempfile
import time

from ..core.errors import ConnectorUnavailableError


def run_json(argv, *, timeout=10, max_bytes=2_097_152):
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        try:
            process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=stdout, stderr=stderr, shell=False)
        except OSError as exc:
            raise ConnectorUnavailableError('external executable could not start') from exc
        deadline = time.monotonic() + timeout
        try:
            while True:
                if os.fstat(stdout.fileno()).st_size + os.fstat(stderr.fileno()).st_size > max_bytes:
                    raise ConnectorUnavailableError('external output exceeded the size limit')
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise ConnectorUnavailableError('external tool timed out')
                try:
                    code = process.wait(timeout=min(remaining, 0.05))
                    break
                except subprocess.TimeoutExpired:
                    continue
            if code:
                raise ConnectorUnavailableError(f'external tool exited with status {code}; no result accepted')
            stdout.seek(0)
            raw = stdout.read(max_bytes + 1)
            if len(raw) > max_bytes:
                raise ConnectorUnavailableError('external output exceeded the size limit')
            return json.loads(raw)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ConnectorUnavailableError('external tool returned malformed JSON') from exc
        finally:
            if process.poll() is None:
                process.kill()
            process.wait()
