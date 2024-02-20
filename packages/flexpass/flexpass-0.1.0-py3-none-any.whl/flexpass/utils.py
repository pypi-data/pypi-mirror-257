from __future__ import annotations

import ctypes
import locale
import logging
import logging.config
import os
import sys
from configparser import RawConfigParser
from contextlib import nullcontext
from datetime import datetime
from io import TextIOBase
from pathlib import Path

logger = logging.getLogger(__name__)


def tabulate(data: list[list], headers: list[str] = None, *, out: TextIOBase|str|Path = None, title=None):
    today = datetime.today().date()

    locale.setlocale(locale.LC_ALL, '')
    csv_separator = ';' if locale.localeconv()["decimal_point"] == ',' else '.'
    csv_quotechar = '"'
    
    csv = False
    if out == 'stdout' or not out:
        out = sys.stdout
    elif out == 'stderr':
        out = sys.stderr
    elif isinstance(out, (str,Path)):
        csv = True
        if title:
            logger.info(f"Export {title} to {out}")
            
        dirpath = os.path.dirname(out)
        if dirpath:
            os.makedirs(dirpath, exist_ok=True)
        
    with open(out, 'w', encoding='utf-8-sig') if csv else nullcontext(out) as fp:        
        def escape(value):
            if not isinstance(value, str):
                value = str(value)

            need_escape = False
            result = ''
            for c in value:
                if value == '\r':
                    continue # ignore
                elif value == '\n':
                    if csv:
                        result += c
                        need_escape = True
                    else:
                        result += ' '
                elif value == '\n' or value == csv_separator:
                    result += c
                    if csv:
                        need_escape = True
                elif value == csv_quotechar:
                    if csv:
                        result += f'{c}{c}'
                        need_escape = True
                    else:
                        result += c
                elif value == '\t':
                    if csv:
                        result += c
                    else:
                        result += ' '
                else:
                    result += c

            if need_escape:
                return f'{csv_quotechar}{result}{csv_quotechar}'
            else:
                return result

        def convert(value):
            if value is None:
                return '\"\"' if csv else ''
            
            if isinstance(value, datetime):
                if value.tzinfo:
                    value = value.astimezone()
                    if csv:
                        return escape(value.replace(tzinfo=None).strftime('%Y-%m-%d %H:%M:%S')) # for display in Excel (does not support timezones)
                    else:
                        return escape(value.strftime('%H:%M:%S') if value.date() == today else value.strftime('%Y-%m-%d'))
                else:
                    return escape(value.replace(microsecond=0))
            
            return escape(value)
        
        if csv:
            for i, header in enumerate(headers):
                if i > 0:
                    fp.write(csv_separator)
                fp.write(convert(header))

            for n, row in enumerate(data):
                fp.write('\n')
                if n % 100 == 0:
                    fp.flush()
                
                for i, value in enumerate(row):
                    if i > 0:
                        fp.write(csv_separator)
                    fp.write(convert(value))
                    
            fp.flush()

        else:
            # convert everything to str
            if headers:
                headers = [convert(header) for header in headers]
            data = [[convert(value) for value in row] for row in data]

            # determine max widths
            maxwidths = [len(header) for header in headers] if headers else []
            for row in data:
                for i, value in enumerate(row):
                    value_len = len(value)
                    if len(maxwidths) <= i:
                        maxwidths.append(value_len)
                    else:
                        if value_len > maxwidths[i]:
                            maxwidths[i] = value_len

            # display headers
            if headers:
                separator_row = ''
                for i, header in enumerate(headers):
                    if i > 0:
                        fp.write(' | ')
                        separator_row += ' | '
                    fp.write(header.ljust(maxwidths[i]))
                    separator_row += '-'.ljust(maxwidths[i], '-')
                fp.write('\n')

                fp.write(separator_row)
                fp.write('\n')

            for n, row in enumerate(data):
                for i, value in enumerate(row):
                    if i > 0:
                        fp.write(' | ')
                    fp.write(value.ljust(maxwidths[i]))
                
                fp.write('\n')
                if n % 100 == 0:
                    fp.flush()
                    
            fp.flush()


def configure_logging(level: str|int = None):
    if level is None:
        level = os.environ.get('LOG_LEVEL', '').upper() or 'INFO'
    elif isinstance(level, str):
        level = level.upper()

    logging.config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'color': {
                '()': ColorFormatter.__module__ + '.' + ColorFormatter.__qualname__,
                'format': '%(levelcolor)s%(levelname)s%(reset)s %(gray)s[%(name)s]%(reset)s %(messagecolor)s%(message)s%(reset)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'color',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': level,
        },
    })


def _convert_str_to_boolean(value: str):
    value = value.lower()
    if value not in RawConfigParser.BOOLEAN_STATES:
        raise ValueError('Not a boolean: %s' % value)
    return RawConfigParser.BOOLEAN_STATES[value.lower()]


class Colors:
    RESET = '\033[0m'
    BLACK = '\033[0;30m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[0;33m'
    BLUE = '\033[0;34m'
    PURPLE = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    GRAY = '\033[0;90m'
    BOLD_RED = '\033[0;1;31m'

    # Disable coloring if environment variable DISABLE_COLORS is set to 1
    DISABLED = False
    if _convert_str_to_boolean(os.environ.get('DISABLE_COLORS') or '0'):
        DISABLED = True
        for _ in dir():
            if isinstance(_, str) and _[0] != '_' and _ not in ['DISABLED']:
                locals()[_] = ''

    # Set Windows console in VT mode
    if not DISABLED and sys.platform == 'win32':
        _kernel32 = ctypes.windll.kernel32
        _kernel32.SetConsoleMode(_kernel32.GetStdHandle(-11), 7)
        del _kernel32


class ColorFormatter(logging.Formatter):
    def formatMessage(self, record: logging.LogRecord) -> str:
        """Format a message from a record object."""
        wrapper = ColoredRecord(record)
        message = super().formatMessage(wrapper)
        return message


class ColoredRecord:
    LEVELCOLORS = {
        logging.DEBUG:     Colors.GRAY,
        logging.INFO:      Colors.CYAN,
        logging.WARNING:   Colors.YELLOW,
        logging.ERROR:     Colors.RED,
        logging.CRITICAL:  Colors.BOLD_RED,
    }

    MESSAGECOLORS = {
        logging.INFO:      '',
    }

    def __init__(self, record: logging.LogRecord):
        # The internal dict is used by Python logging library when formatting the message
        # (inspired from library "colorlog")
        levelcolor = self.LEVELCOLORS.get(record.levelno, '')
        self.__dict__.update(record.__dict__)
        self.__dict__.update({
            'levelcolor': levelcolor,
            'messagecolor': self.MESSAGECOLORS.get(record.levelno, levelcolor),
            'red': Colors.RED,
            'green': Colors.GREEN,
            'yellow': Colors.YELLOW,
            'cyan': Colors.CYAN,
            'gray': Colors.GRAY,
            'bold_red': Colors.BOLD_RED,
            'reset': Colors.RESET,
        })
