from __future__ import annotations

import os
from datetime import datetime

from .. import (Backend, BackendError, BackendNotAvailable, PasswordInfo,
                register_backend)

try:
    from secretstorage import Collection, Item, dbus_init, get_all_collections, get_default_collection
    from secretstorage.exceptions import SecretStorageException
except ImportError:
    dbus_init = None

@register_backend(priority=60)
class SecretServiceBackend(Backend):
    """
    Secret Service D-Bus API, a FreeDesktop.org standard usually accessed through libsecret and its frontends (secret-tool, Gnome Keyring, KDE Wallet Manager or KeePassXC).

    See: https://www.freedesktop.org/wiki/Specifications/secret-storage-spec/
    - libsecret: https://wiki.gnome.org/Projects/Libsecret
    - secret-tool: https://manpages.debian.org/bookworm/libsecret-tools/secret-tool.1.en.html
    - Gnome Keyring: https://wiki.gnome.org/Projects/GnomeKeyring
    - KDE Wallet Manager: https://apps.kde.org/fr/kwalletmanager5/
    - KeyPassXC: https://keepassxc.org/
    """
    def __init__(self, collection: str = None, application: str = 'flexpass', **kwargs):
        super().__init__(**kwargs)

        if not dbus_init:
            raise BackendNotAvailable(self, "package secretstorage missing")
        
        if not 'DBUS_SESSION_BUS_ADDRESS' in os.environ:
            raise BackendNotAvailable(self, "environment variable DBUS_SESSION_BUS_ADDRESS missing")
    
        self._collection_arg = collection
        self._application = application
        self._connection = None
        self._name_attribute = None


    def close(self):
        super().close()
        if self._connection:
            self._connection.close()
            self._connection = None


    @property
    def collection(self):
        try:
            return self._collection
        except:
            pass

        # Open the collection
        self._connection = dbus_init()
        try:
            if self._collection_arg:
                if '/' in self._collection_arg: # it is a path
                    self.collection = Collection(self._connection, self._collection_arg)
                else: # it is a label
                    self._collection = None
                    for collection in get_all_collections(self._connection):
                        if collection.get_label() == self._collection_arg:
                            if self._collection:
                                raise BackendError(self, f"several collection found with label \"{self._collection_arg}\"")
                            self._collection = collection
                    if not self._collection:
                        raise BackendError(self, f"no collection found with label \"{self._collection_arg}\"")
            else:
                self._collection = get_default_collection(self._connection)
        except SecretStorageException as err:
            raise BackendError(self, "failed to initiate collection: %s." % err)

        # Unlock the collection if necessary
        if self._collection.is_locked():
            self._collection.unlock()
            if self._collection.is_locked():  # User dismissed the prompt
                raise BackendError(self, "failed to unlock collection")
            
        # Determine the name attribute
        if 'keepass' in self._collection.collection_path.lower():
            self._name_attribute = 'Title'
        elif not self._collection.collection_path.startswith('/org/freedesktop/secrets/aliases/'):
            self._name_attribute = 'service'
        else:
            iterator = self._collection.get_all_items()
            try:
                an_item = next(iterator)
                if 'Title' in an_item.get_attributes():
                    self._name_attribute = 'Title'
                else:
                    self._name_attribute = 'service'
            except StopIteration:
                self._name_attribute = 'service'

        self.logger.debug("Use collection %s, path=%s, name_attribute=%s", self._collection.get_label(), self._collection.collection_path, self._name_attribute)
        return self._collection


    def _unlock(self, item):
        if hasattr(item, 'unlock'):
            item.unlock()
        if item.is_locked():  # User dismissed the prompt
            raise BackendError(self, 'failed to unlock item')


    def _get_password_item(self, name: str):
        iterator = self.collection.search_items({self._name_attribute: name})
        try:
            item = next(iterator)
        except StopIteration:
            return None

        try:
            other_item = next(iterator)
            raise BackendError(self, f"several passwords found with name {self.name}")
        except StopIteration:
            pass

        return item


    def get_password(self, name: str) -> str|None:
        item = self._get_password_item(name)
        if item is None:
            return None

        self._unlock(item)
        self.logger.info("Password %s retrieved from backend %s", name, self.name)
        return item.get_secret().decode('utf-8')


    def set_password(self, name: str, password: str, **options) -> bool:
        item = self._get_password_item(name)
        
        if item is not None:
            created = False
            item.set_secret(password)
        else:
            created = True
            self.collection.create_item(name, {self._name_attribute: name, 'application': self._application}, password)

        self.logger.info("Password %s %s in backend %s", name, 'created' if created else 'updated', self.name)
        return created


    def delete_password(self, name: str) -> bool:
        item = self._get_password_item(name)

        if item is None:
            return False
        
        item.delete()
        self.logger.info("Password %s deleted from backend %s", name, self.name)
        return True


    def list_passwords(self) -> list[PasswordInfo]:
        passwords: list[PasswordInfo] = []

        def add_item(item: Item, *, current_collection: bool):
            attributes = item.get_attributes()

            if current_collection:
                name = attributes.pop(self._name_attribute, None)
            else:
                name = None
            
            password = PasswordInfo(name)

            mtime = datetime.fromtimestamp(item.get_modified()).astimezone()
            application = attributes.pop('application', None)
            
            info = {
                'mtime': mtime,
                'collection': current_collection_label,
                'label': item.get_label(),
                'application': application,
            }

            for key, value in attributes.items():
                if value is None or value == '':
                    continue
                if key in info:
                    key = f'attr:{key}'
                info[key] = value

            password.add_backend_info(self, info)
            passwords.append(password)

        # Get passwords from current collection
        current_collection_label = self.collection.get_label()
        for item in self.collection.get_all_items():
            add_item(item, current_collection=True)

        # Get passwords for other collections
        for collection in get_all_collections(self.collection.connection):
            if collection.get_label() == current_collection_label:
                continue
            add_item(item, current_collection=False)

        # remove label and/or path if they all have their expected value
        keep_label = False
        keep_path = False
        for password in passwords:
            info = password.backend_info[self]
            if info['label'] != password.name:
                keep_label = True
            if 'Path' in info and info['Path'] != f'/{password.name}':
                keep_path = True

        if not keep_label or not keep_path:
            for password in passwords:
                info = password.backend_info[self]
                if not keep_label:
                    info.pop('label')
                if not keep_path:
                    info.pop('Path', None)

        return passwords
    