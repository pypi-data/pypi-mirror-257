from __future__ import annotations

import errno
import logging
from argparse import ArgumentParser
from getpass import getpass
from pathlib import Path

import flexpass

from . import (BackendError, __prog__, __version__, get_backend,
               get_backend_classes)
from .utils import Colors, configure_logging, tabulate

logger = logging.getLogger(__name__)

def main():
    configure_logging()

    parser = ArgumentParser(prog=__prog__, description="A simple yet flexible library (and command-line application) to access passwords.", add_help=False)

    parser.add_argument('name', nargs='?', metavar='NAME', help="Name of the password to get, set or delete.")
    parser.add_argument('password', nargs='?', metavar='PASSWORD', help="Value of the password to set. Use option -p (--prompt) instead to prompt for the password interactively.")

    group = parser.add_argument_group('command', description="The command to run. Defaults to --set if PASSWORD (or --prompt) is given, to --get if NAME is given, or to --list otherwise.")
    group = group.add_mutually_exclusive_group()
    group.add_argument('--list', action='store_const', const='list', dest='command', help="List available passwords.")
    group.add_argument('--get', action='store_const', const='get', dest='command', help="Get the password named NAME.")
    group.add_argument('--set', action='store_const', const='set', dest='command', help="Set the password named NAME.")
    group.add_argument('--delete', action='store_const', const='delete', dest='command', help="Delete the password named NAME.")
    group.add_argument('--backends', action='store_const', const='backends', dest='command', help="Show registered backends.")
    group.add_argument('-h', '--help', action='help', help="Show this help message.")
    group.add_argument('-v', '--version', action='version', version=f"{__prog__} {__version__ or ''}".strip(), help="Show program version.")

    group = parser.add_argument_group('options')
    group.add_argument('-b', '--backend', help=f"Use the given backend. Registered backends (in decreasing priority): {get_registered_backend_names()}.")
    group.add_argument('-p', '--prompt', action='store_true', help="Prompt for the password to set interactively.")
    group.add_argument('--full', action='store_true', help="Display full information for the --list command.")
    group.add_argument('--out', help="Export --list or --backends results to the given CSV file instead of stdout.")

    args = parser.parse_args()
    
    command = args.command
    if not command:
        if args.password or args.prompt:
            command = 'set'
        elif args.name:
            command = 'get'
        else:
            command = 'list'

    if command == 'get':
        BackendCommands(args.backend).get_password(args.name)
    elif command == 'set':
        BackendCommands(args.backend).set_password(args.name, args.password if args.password else None)
    elif command == 'delete':
        BackendCommands(args.backend).delete_password(args.name)
    elif command == 'list':
        BackendCommands(args.backend).list_passwords(args.out, args.full)
    elif command == 'backends':
        backends_command()
    else:
        logger.error(f"Unknown command: {command}")
        exit(errno.ENOENT)

class BackendCommands:
    def __init__(self, backend_name: str):
        try:
            self.target = get_backend(backend_name) if backend_name else flexpass
        except BackendError as err:
            logger.error(err)
            exit(errno.ESRCH)
        except Exception as err:
            logger.exception(err)
            exit(errno.EPERM)

    def list_passwords(self, out = None, full = False):
        passwords = self.target.list_passwords()
        csv = not (not out or out == 'stdout' or out == 'stderr' or not isinstance(out, (str,Path)))

        # Determine headers
        headers = ['name']
        if self.target == flexpass:
            headers.append('backend')

        main_headers = ['mtime']
        for password in passwords:
            for info in password.backend_info.values():
                for header in main_headers:
                    if not header in headers:
                        if header in info:
                            headers.append(header)
                
                if full:
                    for key in info:
                        if not key in headers:
                            headers.append(key)

        # Determine tabular data
        data = []
        for password in passwords:
            for backend in password.backends:
                if not csv and not full and len(password.name) > 40:
                    display_name = password.name[0:20] + ' … ' + password.name[-20:]
                else:
                    display_name = password.name

                row = [display_name]

                if self.target == flexpass:
                    row.append(backend.name)

                info = password.backend_info[backend]
                for header in headers:
                    if not header in ['name', 'backend']:
                        row.append(info.get(header))
                    
                data.append(row)

        # Export tabular data
        tabulate(data, headers, out=out, title='list of passwords')


    def get_password(self, name):
        password = self.target.get_password(name)
        if password is not None:
            print(password)
    
    def set_password(self, name, password = None):
        if password is None:
            try:
                password = getpass(f"Enter password {name} (will not be displayed): ")
            except KeyboardInterrupt:
                logger.error(f"Password prompt interrupted")
                exit(errno.EINTR)

        self.target.set_password(name, password)

    def delete_password(self, name):
        self.target.delete_password(name)

def backends_command(out = None):
    headers = ['name', 'aka', 'priority', 'readonly', 'available']
    data = []
    for backend in get_backend_classes():
        try:
            get_backend(backend)
            available = True
        except:
            available = False

        row = [backend.name, ', '.join(backend.aka), backend.priority, backend.readonly, available]
        data.append(row)
    
    tabulate(data, headers, out=out, title='list of backends')

def get_registered_backend_names():
    available_backend_names = None
    for backend_cls in get_backend_classes():
        available_backend_names = (f'{available_backend_names}, ' if available_backend_names else '') + f'{Colors.CYAN}{backend_cls.name}{Colors.RESET}'
        if backend_cls.aka:
            available_backend_names += f" (aka {', '.join(f'{Colors.CYAN}{name}{Colors.RESET}' for name in backend_cls.aka)})"

if __name__ == '__main__':
    main()
