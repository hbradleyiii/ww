#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             vhost.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2015
#
#                   TODO: add SSL capabilities

"""
ww.vhost
~~~~~~~~

A class to create Apache vhost configurations.
It extends WWFile.
"""

from __future__ import absolute_import, print_function

import subprocess

try:
    from ext_pylib.files import Parsable, Template
    from ext_pylib.input import prompt, prompt_str
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from . import settings as s
from .ww_file import WWFile


def run_command(command):
    """A function to run os commands."""
    try:
        retcode = subprocess.call(command, shell=True)
        if retcode > 0:
            print("Command was terminated by signal ", -retcode)
            return False
        else:
            print("Command completed successfully.")
            return True
    except OSError as error:
        print("Command: '" + command + "' failed: ", error)


class VhostTemplate(Template, WWFile):
    """A Vhost template File."""


class Vhost(Parsable, WWFile):
    """A class that describes an Apache vhost configuration.
    This is primarily a wrapper for vhost managment.
    """

    def __init__(self, domain, atts):
        """Initializes a Vhost file."""
        self.domain = domain
        self.template = VhostTemplate({'path' : s.VHOST_TEMPLATE})
        super(Vhost, self).__init__(atts)
        self.regexes = {'htdocs'     : ('DocumentRoot ["]?([^"\n]*)',
                                        'DocumentRoot {0}'),
                        'error_log'  : ('ErrorLog ["]?([^"\n]*)',
                                        'ErrorLog {0}'),
                        'access_log' : ('CustomLog ["]?([^"\n]*)',
                                        'CustomLog {0}'),}
        self.setup_parsing()

    def create(self, data=''):
        """Creates a vhost file replacing placeholders with data if they exist."""
        # pylint: disable=attribute-defined-outside-init,redefined-variable-type
        if data:
            self.data = data
        elif getattr(self, 'placeholders', None):
            self.data = self.template.apply_using(self.placeholders)  # pylint: disable=no-member
        else:
            self.data = self.template.read()
        super(Vhost, self).create()
        self.enable()

    def parse(self):
        """Parses an existing vhost file (or the contents of memory).
        Prompts when an attribute can't be found."""
        self.read()

        for attribute in ['htdocs', 'error_log', 'access_log']:
            if not getattr(self, attribute, None):
                print('Could not parse "' + attribute + '".')
                setattr(self, attribute, prompt_str('What is the htdocs path?'))

        return {'htdocs'     : {'path' : getattr(self, 'htdocs')},
                'access_log' : {'path' : getattr(self, 'access_log')},
                'error_log'  : {'path' : getattr(self, 'error_log')},
                'log'        : {'path' : getattr(self, 'access_log').rsplit('/', 1)[0]}}

    def verify(self, repair=False):
        """Verifies that the vhost file exists and is enabled."""
        result = super(Vhost, self).verify(repair)
        if not self.is_enabled():
            print('Vhost configuration file for ' + self.domain + ' is not enabled.')
            if not repair:
                return False
            else:
                self.enable(False)
        print('Vhost for ' + self.domain + ' is enabled.')
        return result

    def is_enabled(self):
        """Checks if apache is serving this vhost."""
        cmd = s.CMD_CHECK_IF_ENABLED.format(self.domain)
        try:
            if subprocess.check_output(cmd, shell=True) == '':
                return False
            return True
        except subprocess.CalledProcessError:
            return False

    def enable(self, ask=True):
        """Enables vhost and restarts apache server."""
        if not ask or prompt('Enable ' + self.domain + ' in apache?'):
            print('Enabling ' + self.domain + ' vhost...')
            return run_command(s.CMD_ENABLE_CONFIG + self.domain) and \
                run_command(s.CMD_RESTART_APACHE)

    def disable(self, ask=True):
        """Disable vhost and restarts apache server."""
        if not ask or prompt('Disable ' + self.domain + ' in apache?'):
            print('Disabling ' + self.domain + ' vhost...')
            return run_command(s.CMD_DISABLE_CONFIG + self.domain) and \
                run_command(s.CMD_RESTART_APACHE)
