from __future__ import annotations
import re

import subprocess
from datetime import datetime
from pathlib import Path
from shutil import which
from tempfile import NamedTemporaryFile

from .. import (Backend, BackendError, BackendNotAvailable, PasswordInfo,
                register_backend)


@register_backend(priority=80)
class GpgBackend(Backend):
    """
    GPG encrypted files following the layout defined by `pass`, the _standard unix password manager_.

    See: https://www.passwordstore.org
    """
    def __init__(self, store: str|Path = '~/.password-store', key: str|Path = None, **kwargs):
        super().__init__(**kwargs)

        self._tmpkeyring = None
        self.gpg_exe = which('gpg')
        if not self.gpg_exe:
            raise BackendNotAvailable(self, f"GPG executable not found")
        self.logger.debug("GPG executable: %s", self.gpg_exe)

        if not isinstance(store, Path):
            store = Path(store)
        self.store = store.expanduser()
    
        if not self.store.exists():
            raise BackendNotAvailable(self, f"GPG password store not found: {self.store}")
    
        if key:
            self.key_id = None
            if isinstance(key, Path):
                pass
            elif key.lower().endswith(('.gpg','.asc','.key')):
                # key is supposed to be a path
                key = Path(key)
            else:
                # key is supposed to be an id
                self.key_id = key

            if self.key_id:
                self.logger.debug("GPG key id: %s", self.key_id)
                self._verify_key_id()
            else:
                self._tmpkeyring = NamedTemporaryFile(prefix=f"{re.sub(r'[^a-zA-Z0-9]', '', self.name)}-", suffix='.gpg')
                self.logger.debug(f"Create temporary keyring {self._tmpkeyring.name} and import {key}")
                cp = self._run_gpg(['--import', key])
                
                m = re.match(r'^gpg:.*([0-9A-F]{16})', cp.stderr)
                if not m:
                    self.logger.error(f"unexpected gpg stderr:\n{cp.stderr}")
                    raise BackendError(self, f"Cannot determine GPG key id for {key}")                
                self.key_id = m[1]
                self.logger.debug("GPG key id: %s", self.key_id)
        else:
            key_id_path = self.store.joinpath('.gpg-id')
            if not key_id_path.exists():
                raise BackendNotAvailable(self, f"GPG id definition file not found: {key_id_path}")
            self.key_id = key_id_path.read_text().strip()
        
            self.logger.debug("GPG key id: %s", self.key_id)
            self._verify_key_id()
    

    def close(self):
        super().close()
        if self._tmpkeyring:
            self._tmpkeyring.close()
            self._tmpkeyring = None


    def _verify_key_id(self):
        cp = self._run_gpg(['--list-secret-keys', self.key_id], accept_returncode={0,2})
        if cp.returncode == 2:
            raise BackendError(self, f"No secret key found for GPG id: {self.key_id}")


    def get_password(self, name: str) -> str|None:
        path = self._get_password_path(name)

        if not path.exists():
            self.logger.debug("File not found: %s", path)
            return None
        
        self.logger.debug("Decrypt %s", path)
        cp = self._run_gpg(['--decrypt', path])
        self.logger.info("Password %s retrieved from backend %s", name, self.name)
        return cp.stdout

    def set_password(self, name: str, password: str, **options) -> bool:
        path = self._get_password_path(name)
        prev = None
        if path.exists():
            prev = path.with_name(f"{path.name}~")
            self.logger.debug("Move existing %s to %s", path, prev)
            if prev.exists():
                prev.unlink()
            path.rename(prev)
            created = False
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            created = True
        
        try:
            self.logger.debug("Create encrypted %s", path)
            self._run_gpg(['--output', path, '--encrypt', '--trust-model', 'always', '--recipient', self.key_id], input=password)

            if prev:
                self.logger.debug("Remove previous %s", prev)
                prev.unlink()

            self.logger.info("Password %s %s in backend %s", name, 'created' if created else 'updated', self.name)
            return created
        except:
            if prev:
                self.logger.debug("Restore previous %s to %s", prev, path)
                prev.rename(path)
            raise

    def delete_password(self, name: str) -> bool:
        path = self._get_password_path(name)

        if not path.exists():
            self.logger.debug("File not found: %s", path)
            return False
        
        def remove_empty_dir(dir: Path):
            if dir == self.store:
                return
            
            is_empty = not any(dir.iterdir())
            if not is_empty:
                return
            
            self.logger.debug("Delete empty directory %s", dir)
            dir.rmdir()

            remove_empty_dir(dir.parent)

        self.logger.debug("Delete file %s", path)
        self.logger.info("Password %s deleted from backend %s", name, self.name)
        path.unlink()
        remove_empty_dir(path.parent)
        return True

    def list_passwords(self) -> list[PasswordInfo]:
        passwords = []

        def recurse(dir: Path):
            for path in sorted(dir.iterdir()):
                if path.is_dir():
                    recurse(path)
                else:
                    relative_pathname = str(path.relative_to(self.store).as_posix())
                    if relative_pathname.endswith('.gpg'):
                        password_name = relative_pathname[:-len('.gpg')]
                        password = PasswordInfo(password_name)
                        password.add_backend_info(self, {
                            'mtime': datetime.fromtimestamp(path.stat().st_mtime).astimezone(),
                        })
                        passwords.append(password)

        recurse(self.store)
        return passwords
    
    def _get_password_path(self, name: str) -> Path:
        return self.store.joinpath(f"{name}.gpg")
    
    def _run_gpg(self, args: list, input: str = None, env: dict[str,str] = None, accept_returncode: int|list[int] = 0) -> subprocess.CompletedProcess[str]:
        if not isinstance(accept_returncode, (list,tuple,set)):
            accept_returncode = [accept_returncode]

        if self._tmpkeyring:
            args = [self.gpg_exe, '--keyring', self._tmpkeyring.name, '--no-default-keyring', *args]
        else:
            args = [self.gpg_exe, *args]
        
        cp = subprocess.run(args, input=input, env=env, capture_output=True, text=True, encoding='utf-8') # NOTE: gpg uses utf-8 also on Windows
        cp.stdout = cp.stdout.rstrip()
        cp.stderr = cp.stderr.rstrip()

        if not cp.returncode in accept_returncode:
            message = f"GPG returned code {cp.returncode}"
            if cp.stderr:
                message += f"\n{cp.stderr}"
            if cp.stdout:
                message += f"\n{cp.stdout}"
            raise subprocess.SubprocessError(message)
        
        return cp
