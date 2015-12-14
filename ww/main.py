#!/usr/bin/env python
#
# name:             main.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# date:             12/11/2015
#
# description:      A program for managing websites
#

__author__ = 'Harold Bradley III'
__copyright__ = 'Copyright (c) 2015 Harold Bradley III'
__license__ = 'MIT'


from ext_pylib.prompt import prompt, prompt_str, warn_prompt
import platform
import sys
from ww import Website, Website_Domain, Vhost, WP_Website


## Exceptions ##
class CommandNotFound(Exception): pass


def new():
    """Creates a new website."""
    print 'Not yet implemented.'

def remove():
    """Removes an existing website."""
    print 'Not yet implemented.'

def pack():
    """Packs a website."""
    print 'Not yet implemented.'

def unpack():
    """Unpacks a previously packed website."""
    print 'Not yet implemented.'

def verify(repair = False):
    """Verifies a website's installation."""
    print 'Not yet implemented.'

def repair():
    """Repairs website."""
    verify(True)

def help():
    """Displays script help."""
    print 'Not yet implemented.'

def main():
    """Main entry point for the script."""

    if platform.system() != 'Linux':
        raise SysError('ERROR: ww cannot be run from ' + platform.system() + '.')

    try:
        script = sys.argv.pop(0)
    except IndexError: # Unknown Error
        raise UnknownError('ERROR: sys.argv was not set in main()')

    try:
        command = sys.argv.pop(0)
    except IndexError: # No arguments given
        help() # If no argmuments are given, run help
        return

    domain = ''
    if sys.argv:
        domain = sys.argv.pop(0)

    website = Website(domain)

    try:
        execute[command](website)
    except KeyError:
        raise CommandNotFound('ERROR: Command "' + command + '" not understood')


# Command line arguments (MUST be declared after modules are defined)
execute = {
    'new'    : new,
    'remove' : remove,
    'pack'   : pack,
    'unpack' : unpack,
    'verify' : verify,
    'repair' : repair,
    'help'   : help,
}

if __name__ == '__main__':
    sys.exit(main())
