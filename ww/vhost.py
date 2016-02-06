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
                        'access_log' :    'CustomLog ["]?([^"\n]*)', }
        self.setup_parsing()

    def create(self, data=''):
        """TODO:"""
        if self.placeholders:
            data = self.template.apply_using(self.placeholders)
        super(Vhost, self).create(data)
        self.enable()

    def parse(self):
        """TODO:"""
        if self.htdocs == []:
            print 'Could not parse htdocs.'
            self.htdocs = prompt_str('What is the htdocs path?')
        else:
            self.htdocs = self.htdocs[0]

        if self.error_log == []:
            print 'Could not parse path for error log.'
            self.error_log = prompt_str('What is the error log path?')
        else:
            self.error_log = self.error_log[0]

        if self.access_log == []:
            print 'Could not parse path for access log.'
            self.access_log = prompt_str('What is the access log path?')
        else:
            self.access_log = self.access_log[0]

        return { 'htdocs' : { 'path' : self.htdocs },
             'access_log' : { 'path' : self.access_log },
              'error_log' : { 'path' : self.error_log },
                   'logs' : { 'path' : self.access_log.rsplit('/', 1)[0] } }

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
        apache_list = os.popen("apache2ctl -S | grep ' namevhost " + \
                               self.domain + " '").read()
        if apache_list == '':
            return False
        return True

    def enable(self, ask=True):
        """TODO:"""
        if not ask or prompt('Enable ' + self.domain + ' in apache?'):
            print 'Enabling ' + self.domain + ' vhost...'
            os.system(s.CMD_ENABLE_CONFIG + self.domain)
            os.system(s.CMD_RESTART_APACHE)

    def disable(self, ask=True):
        """TODO:"""
        if not ask or prompt('Disable ' + self.domain + ' in apache?'):
            print 'Disabling ' + self.domain + ' vhost...'
            # TODO: Change to subprocess
            os.system(s.CMD_DISABLE_CONFIG + self.domain)
            os.system(s.CMD_RESTART_APACHE)
