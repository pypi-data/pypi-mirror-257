"""
A simple yet flexible library (and command-line application) to access passwords from various backends (GPG/pass, Linux SecretService, Windows Credentials Manager, etc).
"""
from __future__ import annotations
import logging
from typing import Any
from .backends import ensure_included_backends_loaded as _ensure_included_backends_loaded
from .errors import BackendNotFound, BackendError, BackendNotAvailable

_logger = logging.getLogger(__name__)


#region Access to passwords

def get_password(name: str) -> str|None:
    any_backend = False

    for backend in get_backends():
        any_backend = True
        password = backend.get_password(name)
        if password is not None:
            return password
        
    if any_backend:        
        _logger.warning("Password %s not found", name)
        return None
    else:
        raise BackendNotAvailable("No backend available")


def set_password(name: str, password: str, **options) -> None:
    for backend in get_backends():
        if not backend.readonly:
            backend.set_password(name, password, **options)
            return
        
    raise BackendNotAvailable("No writable backend available")


def delete_password(name: str) -> bool:
    any_writable = False
    deleted = False
    
    for backend in get_backends():
        if not backend.readonly:
            any_writable = True
            if backend.delete_password(name):
                deleted = True
        
    if not any_writable:
        raise BackendNotAvailable("No writable backend available")
    
    if not deleted:        
        _logger.warning("Password %s not found", name)
    return deleted


def list_passwords() -> list[PasswordInfo]:
    passwords_by_name: dict[str,PasswordInfo] = {}
    for backend in get_backends():
        for p in backend.list_passwords():
            if not p.name in passwords_by_name:
                passwords_by_name[p.name] = PasswordInfo(p.name)
            passwords_by_name[p.name].add_backend_info(backend, p.backend_info[backend])

    return [passwords_by_name[name] for name in sorted(passwords_by_name.keys())]


class PasswordInfo:
    def __init__(self, name: str):
        self.name = name
        self.backends: list[Backend] = []  # sorted by decreasing priority
        self.backend_info: dict[Backend,dict[str,Any]] = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
    def add_backend_info(self, backend: Backend, info: dict[str,Any]):
        self.backends.append(backend)
        self.backends.sort(key=lambda backend: backend.priority, reverse=True)
        self.backend_info[backend] = info

#endregion


#region Access to backends

def get_backend(name_or_cls: str|type[Backend]) -> Backend:
    """
    Get instanciated backend by name (or by subclasss of Backend if only one backend is registered for this subclass).
    """
    definition = get_backend_definition(name_or_cls)
    return definition.get_instance()


def get_backends() -> list[Backend]:
    """
    Get all instanciated backends.
    """
    global _ordered_backends

    if _ordered_backends is None:
        _ordered_backends = []
        for definition in get_backend_definitions():
            try:
                instance = get_backend(definition.name)
                _ordered_backends.append(instance)
            except BackendNotAvailable as err:
                _logger.debug(err)
            except Exception as err:
                _logger.exception("Cannot instanciate backend %s (class %s.%s): %s", definition.name, definition.backend_cls.__name__, definition.backend_cls.__qualname__, err)

    return _ordered_backends


class Backend:
    # Class attributes
    readonly = False

    ## Instance attributes
    name: str
    priority: int
    options: dict[str,Any]

    def __init__(self, *, name: str, priority: int, **options):
        self.name = name
        self.priority = priority
        self.options = options
        self.logger = logging.getLogger(f'flexpass.backend.{name}')

    def close(self):
        pass

    def get_password(self, name: str) -> str|None:
        raise NotImplementedError(f"{self.__class__} does not implement get_password() method.")

    def set_password(self, name: str, password: str, **options) -> bool:
        raise NotImplementedError(f"{self.__class__} does not implement set_password() method.")

    def delete_password(self, name: str) -> bool:
        raise NotImplementedError(f"{self.__class__} does not implement delete_password() method.")

    def list_passwords(self) -> list[PasswordInfo]:
        raise NotImplementedError(f"{self.__class__} does not implement list_passwords() method.")

#endregion
        

#region Backend definition

_definitions_by_name: dict[str,BackendDefinition] = {}
_definitions_by_priority: dict[int,list[BackendDefinition]] = {}
_ordered_backends = None

def get_backend_definition(name_or_cls: str|type[Backend]) -> BackendDefinition:
    """
    Get registered backend definition by name (or by subclasss of Backend if only one backend is registered for this subclass).
    """
    _ensure_included_backends_loaded()

    if isinstance(name_or_cls, type):
        found_definition = None
        for definition in _definitions_by_name.values():
            if definition.backend_cls == name_or_cls:
                if found_definition:
                    if found_definition != definition:
                        raise ValueError(f"Several backends are registered for class {name_or_cls.__name__}: please provide the backend name to identify a registered backend uniquely.")
                else:
                    found_definition = definition
        if not found_definition:
            raise BackendNotFound(name_or_cls)
        return found_definition
    elif isinstance(name_or_cls, str):
        if not name_or_cls in _definitions_by_name:
            raise BackendNotFound(name_or_cls)
        return _definitions_by_name[name_or_cls]
    else:
        raise TypeError(f"name_or_cls: {name_or_cls}")


def get_backend_definitions() -> list[BackendDefinition]:
    """
    Get all registered backend definitions.
    """
    _ensure_included_backends_loaded()
    
    definitions: list[BackendDefinition] = []
    for priority in sorted(_definitions_by_priority.keys(), reverse=True):
        for definition in _definitions_by_priority[priority]:
            definitions.append(definition)

    return definitions


def register_backend(backend_cls: type[Backend] = None, name: str = None, priority: int = 1, **options) -> BackendDefinition:
    """
    Register a subclass of `Backend`.

    May be used as a normal function or as a decorator of the subclass.
    """
    global _ordered_backends

    if backend_cls is None: # decorator used with arguments, for example `@register_backend(name=...)` or `@register_backend()`
        def decorator(backend: type[Backend]):
            register_backend(backend, name=name, priority=priority, **options)
            return backend
        return decorator

    if not isinstance(backend_cls, type):
        raise TypeError(f"backend_cls: expected type, got {type(backend_cls).__name__}")

    if not name:
        basename = backend_cls.__name__
        if basename.endswith('Backend') and len(basename) > len('Backend'):
            basename = basename[:-len('Backend')].lower()
        name = basename
    elif not isinstance(name, str):
        raise TypeError(f"name: expected str, got {type(name).__name__}")
        
    if not isinstance(priority, int):
        raise TypeError(f"priority: expected int, got {type(priority).__name__}")

    _ensure_included_backends_loaded()
    
    if _logger.isEnabledFor(logging.DEBUG):
        options_log = f", options: {', '.join(f'{key}={value}' for key, value in options.items())}" if options else ''
        _logger.debug("Register backend %s (class %s.%s): priority=%s%s", name, backend_cls.__name__, backend_cls.__qualname__, priority, options_log)

    if name in _definitions_by_name:
        raise ValueError(f"A backend with name {name} has already been registered")
    
    definition = BackendDefinition(backend_cls=backend_cls, name=name, priority=priority, **options)
    
    _ordered_backends = None # will have to be rebuilt by get_backends() with the updated backend definitions
    _definitions_by_name[name] = definition
    if not priority in _definitions_by_priority:
        _definitions_by_priority[priority] = []
    _definitions_by_priority[priority].append(definition)

    return definition


def unregister_backend(name_or_cls: str|type[Backend], if_exists = False):
    global _ordered_backends

    _ensure_included_backends_loaded()

    try:
        definition = get_backend_definition(name_or_cls)
    except BackendNotFound:
        if if_exists:
            _logger.debug("Unregistration of backend %s: does not exist")
            return
        raise

    _logger.debug("Unregister backend %s (class %s.%s)", definition.name, definition.backend_cls.__name__, definition.backend_cls.__qualname__)

    if definition.instance:
        definition.instance.close()

    _ordered_backends = None # will have to be rebuilt by get_backends() with the updated backend definitions
    _definitions_by_name.pop(definition.name)
    _definitions_by_priority[definition.priority].remove(definition)


class BackendDefinition:
    backend_cls: type[Backend]
    instance: Backend|Exception
    name: str
    priority: int
    options: dict[str,Any]
    
    def __init__(self, *, backend_cls, name, priority, **options):
        self.backend_cls = backend_cls
        self.name = name
        self.priority = priority
        self.options = options
        self.instance = None
        self.exception = None
        self.logger = logging.getLogger(f'flexpass.backend.{name}')

    def __str__(self):
        return f"{self.name} (class {self.backend_cls.__module__}.{self.backend_cls.__qualname__})"
    
    def get_instance(self) -> Backend:
        if not self.instance and not self.exception:
            try:
                self.logger.debug("Instanciate backend %s (class %s.%s)", self.name, self.backend_cls.__name__, self.backend_cls.__qualname__)
                self.instance = self.backend_cls(name=self.name, priority=self.priority, **self.options)
            except Exception as err:
                self.exception = err

        if self.exception:
            raise self.exception
        else:
            return self.instance

# endregion


#region Version information

__prog__ = 'flexpass'

try:
    # generated by setuptools_scm during build
    from ._version import __version__, __version_tuple__
except ImportError:
    __version__ = None
    __version_tuple__ = None

#endregion


__all__ = (
    'BackendNotFound', 'BackendError', 'BackendNotAvailable',
    'get_password', 'set_password', 'delete_password', 'list_passwords', 'PasswordInfo',
    'get_backend', 'get_backends', 'get_backend_definitions', 'Backend', 'BackendDefinition',
    'register_backend',
)
