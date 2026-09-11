"""Expected domain errors; safe to render without a traceback."""


class WorkbenchError(ValueError):
    pass


class CaseNotFoundError(WorkbenchError):
    pass


class EvidenceError(WorkbenchError):
    pass


class StorageError(WorkbenchError):
    pass


class ConnectorUnavailableError(WorkbenchError):
    pass


class ConnectorPermissionError(WorkbenchError):
    pass
