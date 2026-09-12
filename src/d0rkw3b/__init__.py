"""Local OSINT query generation. Importing this package performs no I/O."""

__version__ = "1.1.0"


def investigate(value, **options):
    """Build an offline investigation plan; see docs/API.md."""
    from .investigation import investigate as build_plan

    return build_plan(value, **options)


def providers(*, bundled=False):
    """Return query definitions; bundled=True bypasses local snapshots/preferences."""
    from .core.registry import load_bundled_registry, load_registry

    result, errors = load_bundled_registry() if bundled else load_registry()
    fatal = [
        error for error in errors if not error.startswith("active registry ignored;")
    ]
    if fatal:
        raise ValueError("; ".join(fatal))
    return result
