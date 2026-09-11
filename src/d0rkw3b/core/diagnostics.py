"""Opt-in diagnostic detail without changing machine-readable stdout."""
import sys
import traceback
from contextvars import ContextVar

DEBUG = ContextVar('d0rkw3b_debug', default=False)


def report_error(error):
    print(f'error: {error}', file=sys.stderr)
    if DEBUG.get():
        # Do not print chained plugin exceptions (which can contain credentials)
        # or frame locals. Traceback frames provide enough debugging context.
        traceback.print_tb(error.__traceback__, file=sys.stderr)
