#!/usr/bin/env python
#
# name:             vhost.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2014
#
# description:      A class to create Apache vhost configurations.
#
#                   TODO: add SSL capabilities

from ext_pylib.files import File, Parsable, Template
from ext_pylib.prompt import prompt, prompt_str
import os
import shutil

DEFAULT_VHOST_DIR = '/etc/apache2/sites-available/'
VHOST_TEMPLATE = os.path.dirname(os.path.realpath(__file__)) + 'vhost.template'

# OS commands
RESTART_APACHE = 'sudo service apache2 restart'
ENABLE_CONFIG = 'sudo a2ensite '
DISABLE_CONFIG = 'sudo a2dissite '

class VhostTemplate(Template, File): pass

# Vhost()
#   A class that describes an Apache vhost configuration.
#   This is primarily a wrapper for vhost managment.
#
#   methods:
#       create()
#       parse()
#       verify()
#       repair()
#       is_enabled()
#       enable(ask)
#       disable(ask)
class Vhost(Parsable, File):

    def __init__(self, domain, atts):
        self.domain = domain
        self.template = VhostTemplate({'path' : VHOST_TEMPLATE})
        super(Vhost, self).__init__(atts)

    def create(self, placeholders):
        data = self.template.apply_using(placeholders)
        super(Vhost, self).create(data)
        self.enable()

    def parse(self):
        regexes = { 'htdocs'  : 'DocumentRoot ["]?([^"\n]*)',
                  'error_log' :     'ErrorLog ["]?([^"\n]*)',
                 'access_log' :    'CustomLog ["]?([^"\n]*)', }
        super(Vhost, self).parse(regexes)

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

    def get_parsed(self):
        self.parse()
        return { 'htdocs' : { 'path' : self.htdocs },
             'access_log' : { 'path' : self.access_log },
              'error_log' : { 'path' : self.error_log },
                   'logs' : { 'path' : self.access_log.rsplit('/', 1)[0] } }

    def verify(self, repair=False):
        if not super(Vhost, self).verify(repair):
            return False
        if not self.is_enabled():
            print 'Vhost configuration file for ' + self.domain + \
                    ' is not enabled.'
            if not repair:
                return False
            else:
                self.enable(False)
        print 'Vhost for ' + self.domain + ' is enabled.'
        return True

    def repair(self):
        self.verify(True)

    def is_enabled(self):
        apache_list = os.popen("apache2ctl -S | grep ' namevhost " + self.domain + " '").read()
        if apache_list == '':
            return False
        return True

    def enable(self, ask=True):
        if not ask or prompt('Enable ' + self.domain + ' in apache?'):
            print 'Enabling ' + self.domain + ' vhost...'
            os.system(ENABLE_CONFIG + self.domain)
            os.system(RESTART_APACHE)

    def disable(self, ask=True):
        if not ask or prompt('Disable ' + self.domain + ' in apache?'):
            print 'Disabling ' + self.domain + ' vhost...'
            os.system(DISABLE_CONFIG + self.domain)
            os.system(RESTART_APACHE)
