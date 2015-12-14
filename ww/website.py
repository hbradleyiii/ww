#!/usr/bin/env python
#
# name:             website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# date:             11/11/2015
#
# description:      A class to manage websites
#


from ext_pylib.files import Dir, File
from ext_pylib.prompt import prompt, prompt_str, warn_prompt
import os
import re
import requests
import tarfile
import time
from vhost import Vhost
from website_domain import Website_Domain


# localhost(function)
#   a python decorator that creates a temporary host entry before
#   the function is called and removes it after it is completed.
def localhost(function):
    def function_wrapper(self, *args, **kwargs):
        print 'Adding temporary host entry.'
        os.system("echo '127.0.0.1 " + self.domain + "' | cat >> /etc/hosts")
        function(self, *args, **kwargs)
        print 'Removing temporary host entry.'
        os.system("sed -i '/^127\.0\.0\.1 " + self.domain + "$/d' /etc/hosts")
    return function_wrapper


# Website(website)
#   a class that describes a generic website with the following properties:
#       domain              Website domain
#       dirs['htdocs']      Website root directory
#       dirs['assets']      Website assets directory
#       dirs['logs']        Website log directory
#       files['vhost_conf'] Apache vhost config file.
#       files['htaccess']   Website root htaccess file.
#   primary methods:
#       install()
#       uninstall()
#       verify()
class Website(object):

    def __init__(self, domain, atts = { 'htdocs'     : None,
                                        'assets'     : None,
                                        'logs'       : None,
                                        'vhost_conf' : None,
                                        'htaccess'   : None,
                                       }):
        """Initializes a new Website instance."""

        print '[*] SSL not yet implemented in Website class.'

        self.domain = Website_Domain(domain)
        self.dirs = {}
        self.files = {}

        self.files['vhost_conf'] = Vhost({
            'path'  : '/etc/apache2/sites-available/' + self.domain + '.conf',
            'perms' : 0644,
            'owner' : 'root',
            'group' : 'root',
        } if not atts['vhost_conf'] else atts['vhost_conf'])

        # If an apache vhost config already exists, try to parse it
        if self.files['vhost_conf'].exists():
            print self.files['vhost_conf'] + ' already exists. Parsing file...'
            parsed_atts = self.files['vhost_conf'].parse()
            if parsed_atts:
                print 'Using parsed data.'
                atts = parsed_atts

        # Convert...
        # or migrate?



        # Website htdocs directory
        self.dirs['htdocs'] = Dir({
            'path'  : '/var/www/' + self.domain + '/htdocs/',
            'perms' : 0775,
            'owner' : 'www-data',
            'group' : 'www-data',
        } if not atts['htdocs'] else atts['htdocs'])

        # Website assets directory
        self.dirs['assets'] = Dir({
            'path'  : '/var/www/' + self.domain + '/assets/',
            'perms' : 0775,
            'owner' : 'root',
            'group' : 'mm_admin', # TODO: Setup a user setting
        } if not atts['assets'] else atts['assets'])

        # Website Log Directory
        self.dirs['logs'] = Dir({
            'path'  : '/var/www/' + self.domain + '/logs/',
            'perms' : 0775,
            'owner' : 'root',
            'group' : 'mm_admin',
        } if not atts['logs'] else atts['logs'])

        self.files['htaccess']  = File({
            'path'  : self.dirs['htdocs'] + '.htaccess',
            'perms' : 0664,
            'owner' : 'www-data',
            'group' : 'www-data',
        } if not atts['htaccess'] else atts['htaccess'])


    def __str__(self):
        """Returns a string with relevant instance information."""
        string =  '\n  domain:           ' + self.domain
        string += '\n  vhost config:     ' + self.files['vhost_conf']
        string += '\n  htdocs directory: ' + self.dirs['htdocs']
        string += '\n  assets:           ' + self.dirs['assets']
        string += '\n  logs:             ' + self.dirs['logs']
        return string

    def __repr__(self):
        return self.__str__()


    ################
    # Public Methods

    def install(self):
        """Installs website to server"""
        # Check if domain is already installed
        if self.is_installed():
            print self.domain + ' is already installed.'

        # Create dirs
        for dir in self.dirs:
            dir.create()

        # Create Files
        for file in self.files:
            file.create()

        self.domain.set_ip()

    def uninstall(self):
        """Removes website from server"""
        # Remove Files
        for file in self.files:
            file.remove()

        # Remove dirs
        for dir in self.dirs:
            dir.remove()

        self.domain.set_ip()

    def verify(self, repair = False):
        """Verifies website's installation"""
        print self

        # Verify Domain
        result = self.domain.verify()

        # Verify Files
        for file in self.files:
            result = result and file.verify(repair)

        # Remove dirs
        for dir in self.dirs:
            result = result and dir.verify(repair)
        #todo: check if website is enabled
        #todo: check if apache is started
        # Check for index.html or php
        return result

    def repair(self):
        print 'Repairing ' + self.domain + '...'
        if self.verify(True):
            print 'Repair completed successfully. [OK]'
        else:
            print 'Repair resulted in errors. [ERROR]'

    def pack(self):
        pass

    def unpack(self):
        pass

    def migrate(self, old_website = None):
        if not old_website:
            old_website = self.existing
        # make sure there's nothing conflicting
        # install() new
        # this overwrites vhostconf...
        # for dirs and files in old copy
        # this includes vhost...

    def is_installed(self):
        apache_list = os.popen("apache2ctl -S | grep ' namevhost " + self.domain + " '").read()
        if apache_list == '':
            return false
        return true

    def enable(self, ask = True):
        if not ask or prompt('Enable ' + self.domain + ' in apache?'):
            self.files['vhost_conf'].enable()

    def disable(self, ask = True):
        if not ask or prompt('Disable ' + self.domain + ' in apache?'):
            self.files['vhost_conf'].disable()

    def restart(self, ask = True):
        if not ask or prompt('Restart Apache?'):
            os.system(RESTART_APACHE)
