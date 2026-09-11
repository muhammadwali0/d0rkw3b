"""Local OSINT query generation. Importing this package performs no I/O."""
__version__ = "1.0.0"


def investigate(value, **options):
    """Build an offline investigation plan; see docs/API.md."""
    from .investigation import investigate as build_plan
    return build_plan(value, **options)


def providers():
    """Return validated bundled query definitions. Performs no network access."""
    from .core.registry import load_registry
    result, errors = load_registry()
    if errors:
        raise ValueError('; '.join(errors))
    return result
