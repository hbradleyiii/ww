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
__copyright__ = 'Copyright (c) 2015-2016 Harold Bradley III'
__license__ = 'MIT'


from ext_pylib.prompt import prompt, prompt_str, warn_prompt
import platform
import sys
from ww import Website, Website_Domain, Vhost, WP_Website


def help():
    """Displays script help."""
    print 'Help not yet implemented.'

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

    if command not in ['install', 'uninstall', 'pack', 'unpack', 'verify', 'repair']:
        print 'ERROR: Command "' + command + '" not understood.'
        return 1

    wp = False
    if sys.argv and sys.argv[0] == 'wp':
        sys.argv.pop(0)
        wp = True

    domain = ''
    if sys.argv:
        domain = sys.argv.pop(0)

    website = WP_Website(domain) if wp else Website(domain)

    getattr(website, command)()


if __name__ == '__main__':
    sys.exit(main())
