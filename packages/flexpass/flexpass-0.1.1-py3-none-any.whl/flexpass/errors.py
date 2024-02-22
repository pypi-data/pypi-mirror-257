from __future__ import annotations


class BackendError(Exception):
    reason = 'error'

    def __init__(self, backend = None, details = None):
        from . import Backend
        
        if isinstance(backend, (Backend,type)):
            self.backend = backend.__name__ if isinstance(backend, type) else backend.name
            self.details = details
            message = f"Backend {self.backend}{f' {self.reason}' if self.reason else ''}{f': {self.details}' if self.details else ''}"
        elif isinstance(backend, str):
            self.backend = backend
            self.details = details
            message = f"Backend {backend}{f' {self.reason}' if self.reason else ''}{f': {self.details}' if self.details else ''}"
        else:
            self.backend = str(backend)
            self.details = details
            message = f"{self.backend}{f': {self.details}' if self.details else ''}"

        super().__init__(message)

class BackendNotFound(BackendError):
    reason = 'not found'

class BackendNotAvailable(BackendError):
    reason = 'not available'
