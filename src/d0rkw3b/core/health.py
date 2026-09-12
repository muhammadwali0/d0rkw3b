"""Conservative homepage reachability reports, never semantic verification."""

import http.client
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit

from .network import NetworkPolicyError, request
from .registry import validate_provider

OUTCOMES = frozenset(
    (
        "healthy",
        "degraded",
        "auth-required",
        "rate-limited",
        "redirect",
        "unreachable",
        "dns-failure",
        "tls-failure",
        "timeout",
        "manual-verification-required",
        "tor-unchecked",
        "deprecated",
        "unknown",
    )
)
FAILURES = frozenset(("unreachable", "dns-failure", "tls-failure", "timeout"))


def interpret_status(status):
    if 200 <= status < 300:
        return "healthy"
    if 300 <= status < 400:
        return "redirect"
    if status == 401:
        return "auth-required"
    if status in (403, 405):
        return "manual-verification-required"
    if status == 429:
        return "rate-limited"
    if status >= 400:
        return "degraded"
    return "unknown"


def check_providers(
    providers, *, max_requests=10, timeout=5, delay=0.5, probe=request, sleep=time.sleep
):
    """Sequential checks bounded by unique host count. No investigation inputs.

    Cache each host result within this run, including rate limits. Do not follow
    redirects or retry 429/503. A homepage response does not validate templates.
    Report-only: registry files and verification dates are never changed.
    """
    if not 1 <= max_requests <= 100 or not 0 < timeout <= 30 or not 0.25 <= delay <= 60:
        raise ValueError(
            "use 1–100 requests, timeout >0 and <=30 seconds, delay 0.25–60 seconds"
        )
    results, cache, requests = [], {}, 0
    for provider in sorted(providers, key=lambda p: str(p.get("id", ""))):
        row = {
            "id": provider.get("id"),
            "structurally_valid": True,
            "template_valid": True,
            "reachable": None,
            "health": "unknown",
            "semantic_status": "unverified",
            "last_checked": None,
            "last_verified": provider.get("last_verified"),
            "verification_method": None,
            "failure_count": 0,
            "http_status": None,
            "checked_url": None,
            "retry_after": None,
            "note": "",
        }
        try:
            validate_provider(provider)
        except (ValueError, TypeError, KeyError) as exc:
            row.update(structurally_valid=False, template_valid=False, note=str(exc))
            results.append(row)
            continue
        if provider["network"] == "tor":
            row.update(
                health="tor-unchecked",
                note="Tor probing is not supported; no request made.",
            )
        elif provider["status"] == "deprecated":
            row.update(
                health="deprecated", note="Deprecated definition; no request made."
            )
        elif (
            not provider["enabled"]
            or provider["requires_api_key"]
            or provider["auth"] == "required"
        ):
            row.update(
                health="manual-verification-required",
                note="Disabled, keyed or authenticated definition; no request made.",
            )
        else:
            parts = urlsplit(provider["homepage"])
            # Only the origin root is probed; no copied query/session/target data.
            endpoint = f"{parts.scheme}://{parts.netloc}/"
            host = parts.hostname.lower()
            if host in cache:
                row.update(cache[host])
            elif requests >= max_requests:
                row["note"] = "Request budget exhausted; no request made."
            else:
                if requests:
                    sleep(delay)
                requests += 1
                outcome = {
                    "last_checked": datetime.now(timezone.utc).isoformat(),
                    "checked_url": endpoint,
                    "verification_method": "HEAD origin homepage",
                    "note": "Homepage reachability only; query semantics remain unverified.",
                }
                try:
                    status, headers, _ = probe(endpoint, method="HEAD", timeout=timeout)
                    outcome.update(
                        health=interpret_status(status),
                        reachable=True,
                        http_status=status,
                        retry_after=next(
                            (
                                v
                                for k, v in headers.items()
                                if k.lower() == "retry-after"
                            ),
                            None,
                        ),
                    )
                except ssl.SSLError:
                    outcome.update(health="tls-failure", reachable=False)
                except socket.gaierror:
                    outcome.update(health="dns-failure", reachable=False)
                except (TimeoutError, socket.timeout):
                    outcome.update(health="timeout", reachable=False)
                except NetworkPolicyError as exc:
                    outcome.update(
                        health="manual-verification-required",
                        reachable=None,
                        note=str(exc),
                    )
                except (OSError, http.client.HTTPException):
                    outcome.update(health="unreachable", reachable=False)
                outcome["failure_count"] = int(outcome["health"] in FAILURES)
                cache[host] = outcome
                row.update(outcome)
        results.append(row)
    return {"schema_version": 1, "request_count": requests, "results": results}
