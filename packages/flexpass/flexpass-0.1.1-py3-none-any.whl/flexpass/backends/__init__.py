from __future__ import annotations

import os
import pkgutil
from importlib import import_module

_loading = False

def ensure_included_backends_loaded():
    """
    Load all backends in the current package.
    """
    global _loading

    if _loading:
        return
    _loading = True

    for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        import_module(f'{__name__}.{name}')
