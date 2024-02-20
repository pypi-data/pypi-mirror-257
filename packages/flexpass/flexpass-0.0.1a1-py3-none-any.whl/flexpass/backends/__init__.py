from __future__ import annotations

import os
import pkgutil
from importlib import import_module


def load_included_backends():
    """
    Load all backends in the current package.
    """
    for _, name, _ in pkgutil.iter_modules([os.path.dirname(__file__)]):
        import_module(f'{__name__}.{name}')
