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


# Defaults
SITE_ADMIN_EMAIL = 'hosting@mediamarketers.com'
SITE_ERROR_LOG = 'error.log'
SITE_ACCESS_LOG = 'access.log'



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


# merge_atts(atts, new_atts)
#   Merges two dictionaries with the second overwriting the corresponding
#   values of the first and returns the result.
def merge_atts(atts, new_atts):
    for k, v in new_atts.iteritems():
        if (k in atts and isinstance(atts[k], dict)
                and isinstance(new_atts[k], dict)):
            atts[k] = merge_atts(atts[k], new_atts[k])
        else:
            atts[k] = new_atts[k]
    return atts


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

    def __init__(self, domain, atts = {}):
        """Initializes a new Website instance."""

        print '[*] SSL not yet implemented in Website class.'

        self.domain = Website_Domain(domain)
        self.dirs = {}
        self.files = {}

        default_atts = {
                'root' : {
                    'path'  : '/var/www/' + self.domain,
                    'perms' : 0775,
                    'owner' : 'www-data',
                    'group' : 'www-data',
                },
                'htdocs' : {
                    'path'  : '/var/www/' + self.domain + '/htdocs/',
                    'perms' : 0775,
                    'owner' : 'www-data',
                    'group' : 'www-data',
                },
                'assets' : {
                    'path'  : '/var/www/' + self.domain + '/assets/',
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : 'mm_admin', # TODO: Setup a user setting
                },
                'logs' : {
                    'path'  : '/var/www/' + self.domain + '/logs/',
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : 'mm_admin',
                },
                'access_log' : {
                    'path'  : '/var/www/' + self.domain + '/logs/access_log',
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : 'mm_admin',
                },
                'error_log' : {
                    'path'  : '/var/www/' + self.domain + '/logs/error_log',
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : 'mm_admin',
                },
                'vhost_conf' : {
                    'path'  : '/etc/apache2/sites-available/' + self.domain + '.conf',
                    'perms' : 0644,
                    'owner' : 'root',
                    'group' : 'root',
                },
                'htaccess' : {
                    'perms' : 0664,
                    'owner' : 'www-data', # TODO: Make this a setting
                    'group' : 'www-data',
                },
            }

        atts = merge_atts(default_atts, atts)

        self.vhost = Vhost(self.domain, atts['vhost_conf'])

        # If an apache vhost config already exists, try to parse it
        if self.vhost.exists():
            print self.files['vhost_conf'] + ' already exists.'
            if prompt('Parse existing vhost configuration?'):
                atts = merge_atts(atts, self.vhost.get_parsed())
        # Convert...or migrate?

        self.root = Dir(atts['root'])
        self.dirs['htdocs'] = Dir(atts['htdocs'])
        self.dirs['assets'] = Dir(atts['assets'])
        self.dirs['logs'] = Dir(atts['logs'])

        # Set path of htaccess after htdocs has been set.
        atts['htaccess']['path'] = self.dirs['htdocs'].path + '.htaccess'
        self.files['htaccess']  = File(atts['htaccess']) # May need to re-orient htaccess to path...


    def __str__(self):
        """Returns a string with relevant instance information."""
        string =  '\n  domain:           ' + self.domain
        string += '\n  vhost config:     ' + self.files['vhost_conf']
        string += '\n  htdocs directory: ' + self.dirs['htdocs']
        string += '\n  assets:           ' + self.dirs['assets']
        string += '\n  logs:             ' + self.dirs['logs']
        return string

    def __repr__(self):
        """Returns a python string that evaluates to the object instance."""
        return "%s('%s', {'htdocs' : %s, 'assets' : %s, 'logs' : %s, 'htaccess' : %s, 'vhost_conf' : %s})" % (
            self.__class__.__name__,
            self.domain,
            self.dirs['htdocs']._atts_(),
            self.dirs['assets']._atts_(),
            self.dirs['logs']._atts_(),
            self.files['htaccess']._atts_(),
            self.files['vhost_conf']._atts_()
            )


    ################
    # Public Methods

    def new(self):
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

        vhost_template = TemplateFile({'path' : '/template/path'})
        self.vhost.create({
                '#WEBSITE#'    : self.domain,
                '#HTDOCS#'     : self.htdocs.path,
                '#EMAIL#'      : SITE_ADMIN_EMAIL,
                '#ACCESS_LOG#' : self.log.path + SITE_ACCESS_LOG,
                '#ERROR_LOG#'  : self.log.path + SITE_ERROR_LOG,
            })

        self.domain.set_ip()

    def remove(self):
        """Removes website from server"""
        self.files['vhost'].disable()

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

        result and self.root.verify()

        result = result and is_apache_running(repair)

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
