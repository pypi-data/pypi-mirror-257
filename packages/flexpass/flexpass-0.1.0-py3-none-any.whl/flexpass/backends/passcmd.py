from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from shutil import which

from .. import (Backend, BackendError, BackendNotAvailable, PasswordInfo,
                register_backend_class)


@register_backend_class(name=['pass', 'gpg'], priority=80)
class PassBackend(Backend):
    """
    Backend for the `pass` command-line password manager, the "standard unix password manager".

    See https://www.passwordstore.org.

    NOTE: the `pass` executable is actually not required, only `gpg` is required.
    """
    def __init__(self):
        super().__init__()

        self.gpg_exe = which('gpg')
        if not self.gpg_exe:
            raise BackendNotAvailable(self.__class__, f"GPG executable not found")
        self.logger.debug("GPG executable: %s", self.gpg_exe)

        self.store_root = Path('~/.password-store').expanduser()
        gpg_id_path = self.store_root.joinpath('.gpg-id')
        if not gpg_id_path.exists():
            raise BackendNotAvailable(self.__class__, f"GPG id definition file not found: {gpg_id_path}")
        self.gpg_id = gpg_id_path.read_text().strip()
        self.logger.debug("GPG id: %s", self.gpg_id)

        cp = self._run_gpg(['--list-secret-keys', self.gpg_id], accept_returncode={0,2})
        if cp.returncode == 2:
            raise BackendError(self.__class__, f"No secret key found for GPG id: {self.gpg_id}")
    
    def get_password(self, name: str) -> str|None:
        path = self._get_service_path(name)

        if not path.exists():
            self.logger.debug("File not found: %s", path)
            return None
        
        self.logger.debug("Decrypt %s", path)
        cp = self._run_gpg(['--decrypt', path])
        self.logger.info("Password %s retrieved from backend %s", name, self.__class__.name)
        return cp.stdout

    def set_password(self, name: str, password: str, **options) -> bool:
        path = self._get_service_path(name)
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
            self._run_gpg(['--output', path, '--encrypt', '--recipient', self.gpg_id], input=password)

            if prev:
                self.logger.debug("Remove previous %s", prev)
                prev.unlink()

            self.logger.info("Password %s %s in backend %s", name, 'created' if created else 'updated', self.__class__.name)
            return created
        except:
            if prev:
                self.logger.debug("Restore previous %s to %s", prev, path)
                prev.rename(path)
            raise

    def delete_password(self, name: str) -> bool:
        path = self._get_service_path(name)

        if not path.exists():
            self.logger.debug("File not found: %s", path)
            return False
        
        def remove_empty_dir(dir: Path):
            if dir == self.store_root:
                return
            
            is_empty = not any(dir.iterdir())
            if not is_empty:
                return
            
            self.logger.debug("Delete empty directory %s", dir)
            dir.rmdir()

            remove_empty_dir(dir.parent)

        self.logger.debug("Delete file %s", path)
        self.logger.info("Password %s deleted from backend %s", name, self.__class__.name)
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
                    relative_pathname = str(path.relative_to(self.store_root).as_posix())
                    if relative_pathname.endswith('.gpg'):
                        password_name = relative_pathname[:-len('.gpg')]
                        password = PasswordInfo(password_name)
                        password.add_backend_info(self.__class__, {
                            'mtime': datetime.fromtimestamp(path.stat().st_mtime).astimezone(),
                        })
                        passwords.append(password)

        recurse(self.store_root)
        return passwords
    
    def _get_service_path(self, service: str) -> Path:
        return self.store_root.joinpath(f"{service}.gpg")
    
    def _run_gpg(self, args: list, input: str = None, accept_returncode: int|list[int] = 0) -> subprocess.CompletedProcess[str]:
        if not isinstance(accept_returncode, (list,tuple,set)):
            accept_returncode = [accept_returncode]
        
        cp = subprocess.run([self.gpg_exe, *args], input=input, capture_output=True, text=True, encoding='utf-8') # NOTE: gpg uses utf-8 also on Windows
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
