# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2022 Matthias Klumpp <matthias@tenstral.net>
#
# Licensed under the GNU Lesser General Public License Version 3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the license, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import os
import re
import sys

from .env import unicode_allowed
from .misc import safe_copy


def console_supports_color():
    '''
    Returns True if the running system's terminal supports color, and False
    otherwise.
    '''

    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    return 'ANSICON' in os.environ or is_a_tty


def print_textbox(title, tl, hline, tr, vline, bl, br):
    def write_utf8(s):
        sys.stdout.buffer.write(s.encode('utf-8'))

    tlen = len(title)
    write_utf8('\n{}'.format(tl))
    write_utf8(hline * (10 + tlen))
    write_utf8('{}\n'.format(tr))

    write_utf8('{}  {}'.format(vline, title))
    write_utf8(' ' * 8)
    write_utf8('{}\n'.format(vline))

    write_utf8(bl)
    write_utf8(hline * (10 + tlen))
    write_utf8('{}\n'.format(br))

    sys.stdout.flush()


def print_header(title):
    if unicode_allowed():
        print_textbox(title, '╔', '═', '╗', '║', '╚', '╝')
    else:
        print_textbox(title, '+', '═', '+', '|', '+', '+')


def print_section(title):
    if unicode_allowed():
        print_textbox(title, '┌', '─', '┐', '│', '└', '┘')
    else:
        print_textbox(title, '+', '-', '+', '|', '+', '+')


def print_info(*arg):
    '''
    Prints an information message and ensures that it shows up on
    stdout immediately.
    '''
    print(*arg)
    sys.stdout.flush()


def print_warn(*arg):
    '''
    Prints an information message and ensures that it shows up on
    stdout immediately.
    '''
    if console_supports_color():
        print('\033[93m/!\\\033[0m', *arg)
    else:
        print('/!\\', *arg)
    sys.stdout.flush()


def print_error(*arg):
    '''
    Prints an information message and ensures that it shows up on
    stdout immediately.
    '''
    if console_supports_color():
        print('\033[91mERROR:\033[0m', *arg, file=sys.stderr)
    else:
        print('ERROR:', *arg, file=sys.stderr)
    sys.stderr.flush()


def print_bullet(*arg, large: bool = False, indent: int = 0):
    '''
    Prints a bullet point to the console, with a set
    indentation and style.
    '''
    if unicode_allowed():
        b = '●' if large else '•'
    else:
        b = '*'
    print((' ' * indent) + b, *arg)


def print_bool_item(prefix: str, b: bool, text_true: str = 'yes', text_false: str = 'no'):
    '''
    Prints a (colored, if possible) boolean item with a given prefix.
    '''
    if console_supports_color():
        s = '\033[92m{}\033[0m'.format(text_true) if b else '\033[91m{}\033[0m'.format(text_false)
    else:
        s = text_true if b else text_false
    if prefix:
        print(prefix, s)
    else:
        print(prefix)
    sys.stdout.flush()


def input_bool(question_text, default=False) -> bool:
    """As user a Yes/No question."""
    if default:
        default_info = '[Y/n]'
    else:
        default_info = '[y/N]'
    while True:
        try:
            in_str = input('{} {}:'.format(question_text, default_info))
        except EOFError:
            return default
        if in_str == 'y' or in_str == 'Y':
            return True
        elif in_str == 'n' or in_str == 'N':
            return False
        elif not in_str:
            return default


class TwoStreamLogger:
    '''
    Permits logging messages to stdout/stderr as well as to a file.
    '''

    class Buffer:
        def __init__(self, fstream, cstream):
            self._fstream = fstream
            self._cstream = cstream

        def write(self, message):
            self._fstream.write(str(message, 'utf-8', 'replace'))
            self._cstream.buffer.write(message)

    def __init__(self, fstream, cstream, fflush_always=False):
        self._fstream = fstream
        self._cstream = cstream
        self._fflush_always = fflush_always
        self._colorsub = re.compile('\x1b\\[(K|.*?m)')
        self.buffer = TwoStreamLogger.Buffer(fstream, cstream)

    def write(self, message):
        # write message to console
        self._cstream.write(message)
        if self._fflush_always:
            self.flush()

        # write message to file, stripping ANSI colors
        self._fstream.write(self._colorsub.sub('', message))

    def flush(self):
        self._cstream.flush()
        self._fstream.flush()

    def copy_to(self, fname):
        self.flush()
        safe_copy(self._fstream.name, fname, preserve_mtime=False)

    def isatty(self):
        return self._cstream.isatty()


def capture_console_output():
    '''
    Direct console output to a file as well
    as to the original stdout/stderr terminal.
    '''
    from tempfile import NamedTemporaryFile

    logfile = NamedTemporaryFile(mode='a', prefix='ds_', suffix='.log')
    nstdout = TwoStreamLogger(logfile, sys.stdout)
    nstderr = TwoStreamLogger(logfile, sys.stderr, True)

    sys.stdout = nstdout
    sys.stderr = nstderr


def save_captured_console_output(fname):
    from .env import get_owner_uid_gid

    if hasattr(sys.stdout, 'copy_to'):
        o_uid, o_gid = get_owner_uid_gid()
        sys.stdout.copy_to(fname)
        os.chown(fname, o_uid, o_gid)
