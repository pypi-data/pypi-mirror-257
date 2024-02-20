from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .backends import load_included_backends
from .errors import BackendNotAvailable, BackendNotFound

if TYPE_CHECKING:
    from . import Backend

logger = logging.getLogger(__name__)

class Config:
    @classmethod
    def singleton(cls):
        try:
            return cls._singleton
        except AttributeError:
            pass
        cls._singleton = cls()
        return cls._singleton
    
    _loaded = False

    @classmethod
    def ensure_backends_loaded(cls):
        if not cls._loaded:
            cls._loaded = True
            load_included_backends()
    
    def __init__(self):
        self._backend_classes_by_name: dict[str,type[Backend]] = {}
        self._backend_classes_by_priority: dict[int,list[type[Backend]]] = {}
        self._backend_instances: dict[type[Backend],Backend|Exception] = {}
        self._backend_instances_ordered: list[Backend] = None

    def register_backend_class(self, backend: str|type, name: str|list[str] = None, priority: int = None):
        self.ensure_backends_loaded()

        backend_cls = self.get_backend_class(backend)
            
        # update backend names
        backend_cls.aka = _get_list(backend_cls.aka, str, label='name')
        for name in _get_list(name, str, label='name'):
            if name != backend_cls.name and not name in backend_cls.aka:
                if not backend_cls.name:
                    backend_cls.name = name
                else:
                    backend_cls.aka.append(name)
        
        if not backend_cls.name:
            basename = backend_cls.__name__
            if basename.endswith('Backend') and len(basename) > len('Backend'):
                basename = basename[:-len('Backend')].lower()
            backend_cls.name = basename

        # update backend priority
        if priority is not None:
            if not isinstance(priority, int):
                raise TypeError(f"Invalid type for priority {priority} ({type(priority)}): expected int")
            backend_cls.priority = priority
        elif backend_cls.priority is not None:
            if not isinstance(backend_cls.priority, int):
                raise TypeError(f"Invalid type for {backend_cls.__name__}.priority {priority} ({type(priority)}): expected int")
        else:
            backend_cls.priority = 1

        # will have to be rebuild with the updated priority
        self._backend_instances_ordered = None

        # remove if priority is 0
        if backend_cls.priority == 0:
            logger.debug("Unregister backend %s.%s: name=%s, aka=%s, priority=%s", backend_cls.__name__, backend_cls.__qualname__, backend_cls.name, backend_cls.aka, backend_cls.priority)

            for name in [backend_cls.name, *backend_cls.aka]:
                self._backend_classes_by_name.pop(name, None)
                    
            for backend_cls_list in self._backend_classes_by_priority.values():
                while backend_cls in backend_cls_list:
                    backend_cls_list.remove(backend_cls)

        else:
            # update _backend_classes_by... attributes
            logger.debug("Register backend %s.%s: name=%s, aka=%s, priority=%s", backend_cls.__name__, backend_cls.__qualname__, backend_cls.name, backend_cls.aka, backend_cls.priority)
            
            for name in [backend_cls.name, *backend_cls.aka]:
                if name in self._backend_classes_by_name and self._backend_classes_by_name[name] != backend_cls:
                    logger.warning(f"Backend name \"{name}\": {self._backend_classes_by_name[name]} replaced by {backend_cls}")
                self._backend_classes_by_name[name] = backend_cls
            
            # append to current priority
            if backend_cls.priority in self._backend_classes_by_priority:
                current_list = self._backend_classes_by_priority[backend_cls.priority]
            else:
                current_list = []
                self._backend_classes_by_priority[backend_cls.priority] = current_list
            if not backend_cls in current_list:
                current_list.append(backend_cls)

            # remove from other priorities
            for priority, backend_cls_list in self._backend_classes_by_priority.items():
                if priority != backend_cls.priority:
                    while backend_cls in backend_cls_list:
                        backend_cls_list.remove(backend_cls)

    def get_backend_classes(self):
        self.ensure_backends_loaded()
        
        backends: list[type[Backend]] = []
        for priority in sorted(self._backend_classes_by_priority.keys(), reverse=True):
            for backend in self._backend_classes_by_priority[priority]:
                backends.append(backend)

        return backends

    def get_backend_class(self, name_or_cls: str|type) -> type:        
        self.ensure_backends_loaded()

        if isinstance(name_or_cls, type):
            return name_or_cls
        elif isinstance(name_or_cls, str):
            name = name_or_cls
        else:
            raise TypeError(f"name_or_cls: {name_or_cls}")

        if not name in self._backend_classes_by_name:
            raise BackendNotFound(name)
        
        return self._backend_classes_by_name[name]
    
    def get_backend(self, name_or_cls: str|type):
        cls = self.get_backend_class(name_or_cls)
        
        if cls in self._backend_instances:
            instance = self._backend_instances[cls]
        else:
            try:
                logger.debug("Instanciate backend %s.%s", cls.__name__, cls.__qualname__)
                instance = cls()
            except Exception as err:
                instance = err
            self._backend_instances[cls] = instance

        if isinstance(instance, Exception):
            raise instance
        else:
            return instance
                 
    def get_backends(self):
        if self._backend_instances_ordered is None:
            self._backend_instances_ordered = []
            for cls in self.get_backend_classes():
                try:
                    instance = self.get_backend(cls)
                    self._backend_instances_ordered.append(instance)
                except BackendNotAvailable as err:
                    logger.debug(err)
                except Exception as err:
                    logger.exception("Cannot instanciate backend %s: %s", cls, err)

        return self._backend_instances_ordered


def _get_list(input, enforce_type: type|tuple[type] = None, *, label: str = None):
    def check_value(value):
        if enforce_type and not isinstance(value, enforce_type):
            raise TypeError(f"Invalid type for{f' {label}' if label else ''} {value} ({type(value)}): expected {enforce_type}")

    if input is None:
        return []
    
    elif isinstance(input, list):
        if enforce_type:
            for value in input:
                check_value(value)
        return input
    
    else:
        values = []
        if isinstance(input, (tuple,set)):
            for value in input:
                check_value(value)
                values.append(value)
        else:
            check_value(input)
            values.append(input)
        return values
