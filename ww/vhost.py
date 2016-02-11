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

import os

try:
    from ext_pylib.files import Parsable, Template
    from ext_pylib.input import prompt, prompt_str
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from . import settings as s
from .ww_file import WWFile


class VhostTemplate(Template, WWFile):
    """A Vhost template File."""

def run_command(command):
    """A function to run os commands."""
    try:
        retcode = call(command, shell=True)
        if retcode < 0:
            print("Command was terminated by signal ", -retcode)
            return False
        else:
            print("Command completed successfully.")
    except OSError as error:
        print("Command: '" + command + "' failed: ", error)

class Vhost(Parsable, WWFile):
    """A class that describes an Apache vhost configuration.
    This is primarily a wrapper for vhost managment.
    """

    def __init__(self, domain, atts):
        """TODO:"""
        self.domain = domain
        self.template = VhostTemplate({'path' : s.VHOST_TEMPLATE})
        super(Vhost, self).__init__(atts)
        self.regexes = {'htdocs'     : 'DocumentRoot ["]?([^"\n]*)',
                        'error_log'  :     'ErrorLog ["]?([^"\n]*)',
                        'access_log' :    'CustomLog ["]?([^"\n]*)',}
        self.setup_parsing()

    def create(self, data=''):
        """TODO:"""
        if getattr(self, 'placeholders', None):
            data = self.template.apply_using(self.placeholders)  # pylint: disable=no-member
        super(Vhost, self).create(data)
        self.enable()

    def parse(self):
        """TODO:"""
        for attribute in ['htdocs', 'error_log', 'access_log']:
            if not getattr(self, attribute, None):
                print('Could not parse "' + attribute + '".')
                setattr(self, attribute, prompt_str('What is the htdocs path?'))

        return {'htdocs'     : {'path' : getattr(self, 'htdocs')},
                'access_log' : {'path' : getattr(self, 'access_log')},
                'error_log'  : {'path' : getattr(self, 'error_log')},
                'log'        : {'path' : getattr(self, 'access_log').rsplit('/', 1)[0]}}

    def verify(self, repair=False):
        """TODO:"""
        result = super(Vhost, self).verify(repair)
        if not self.is_enabled():
            print 'Vhost configuration file for ' + self.domain + \
                    ' is not enabled.'
            if not repair:
                return False
            else:
                self.enable(False)
        print 'Vhost for ' + self.domain + ' is enabled.'
        return result

    def is_enabled(self):
        """TODO:"""
        cmd = s.CMD_CHECK_IF_ENABLED.format(self.domain)
        try:
            if check_output(cmd, shell=True) == '':
                return False
            return True
        except CalledProcessError:
            return False

    def enable(self, ask=True):
        """TODO:"""
        if not ask or prompt('Enable ' + self.domain + ' in apache?'):
            print('Enabling ' + self.domain + ' vhost...')
            run_command(s.CMD_ENABLE_CONFIG + self.domain)
            run_command(s.CMD_RESTART_APACHE)

    def disable(self, ask=True):
        """TODO:"""
        if not ask or prompt('Disable ' + self.domain + ' in apache?'):
            print('Disabling ' + self.domain + ' vhost...')
            run_command(s.CMD_DISABLE_CONFIG + self.domain)
            run_command(s.CMD_RESTART_APACHE)
