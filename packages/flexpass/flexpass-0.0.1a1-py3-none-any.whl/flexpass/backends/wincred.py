from __future__ import annotations

from .. import Backend, BackendNotAvailable, register_backend_class

try:
    import pywintypes
    import win32cred
except ImportError:
    win32cred = None


@register_backend_class(priority=5)
class WincredBackend(Backend):
    def __init__(self):
        super().__init__()

        if not win32cred:
            raise BackendNotAvailable(self.__class__, "package win32cred missing")
