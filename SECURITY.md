# Security

D0RKW3B generates URLs locally. It does not fetch target data or persist history.
Explicit browser opening sends the target to the destination service. Terminal
output and redirected files may contain sensitive indicators.

Report vulnerabilities through the repository host's private vulnerability
reporting feature if available. If unavailable, open an issue asking maintainers
for a private contact route without posting exploit details, secrets or personal
data. No dedicated security email or response-time commitment is established.

The legacy YouTube metadata URL contained an API key. The maintained application
removes that key and retains the endpoint disabled. Git history still contains
the original value; its owner should revoke it. D0RKW3B does not test or use it.

Contributed provider files must be treated as untrusted destinations. Review them
before opening generated links. A syntactically valid URL is not an endorsement.
