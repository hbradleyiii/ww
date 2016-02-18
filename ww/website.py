#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# date:             11/11/2015
#

"""
ww.website
~~~~~~~~~~

A class to manage websites
"""

import os
import tarfile

try:
    from ext_pylib.files import Dir, File
    from ext_pylib.input import prompt
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from . import settings as s
from .htaccess import Htaccess
from .vhost import Vhost
from .website_domain import WebsiteDomain


def localhost(function):
    """A python decorator that creates a temporary host entry before
    the function is called and removes it after it is completed."""
    def function_wrapper(self, *args, **kwargs):
        """Adds a hostentry for self.domain to resolve to localhost."""
        print 'Adding temporary host entry.'
        os.system("echo '127.0.0.1 " + self.domain + "' | cat >> /etc/hosts")
        function(self, *args, **kwargs)
        print 'Removing temporary host entry.'
        os.system("sed -i '/^127\.0\.0\.1 " + self.domain + "$/d' /etc/hosts")
    return function_wrapper


def merge_atts(atts, new_atts):
    """Merges two dictionaries with the second overwriting the corresponding
    values of the first and returns the result."""
    for k, _ in new_atts.iteritems():
        if (k in atts and isinstance(atts[k], dict)
                and isinstance(new_atts[k], dict)):
            atts[k] = merge_atts(atts[k], new_atts[k])
        else:
            atts[k] = new_atts[k]
    return atts


class Website(object):
    """A class that describes a generic website with the following properties:
        domain      Website domain
        htdocs      Website root directory
        assets      Website assets directory
        logs        Website log directory
        access_log  Website access log file
        error_log   Website error log file
        vhost       Apache vhost config file
        htaccess    Website root htaccess file
    """

    def __init__(self, domain, atts=None):
        """Initializes a new Website instance."""
        atts = atts or {}

        print '[*] SSL not yet implemented in Website class.'

        self.domain = WebsiteDomain(domain)
        self.dirs = {}
        self.files = {}

        default_atts = {
            'root' : {
                'path'  : s.WWW_DIR + self.domain,
                'perms' : 0775,
                'owner' : s.WWW_USR,
                'group' : s.WWW_USR,
            },
            'htdocs' : {
                'path'  : s.WWW_DIR + self.domain + '/htdocs/',
                'perms' : 0775,
                'owner' : s.WWW_USR,
                'group' : s.WWW_USR,
            },
            'assets' : {
                'path'  : s.WWW_DIR + self.domain + '/assets/',
                'perms' : 0775,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'logs' : {
                'path'  : s.WWW_DIR + self.domain + '/log/',
                'perms' : 0770,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'access_log' : {
                'path'  : None,
                'perms' : 0750,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'error_log' : {
                'path'  : None,
                'perms' : 0750,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'vhost' : {
                'path'  : s.VHOST_PATH + self.domain + '.conf',
                'perms' : 0644,
                'owner' : 'root',
                'group' : 'root',
            },
            'htaccess' : {
                'path'  : None,
                'perms' : 0664,
                'owner' : s.WWW_USR,
                'group' : s.WWW_USR,
                'sections' : [
                    {'name' : 'h5g', 'path' : s.HTA_5G_TEMPLATE},
                ]
            },
        }

        atts = merge_atts(default_atts, atts)

        self.vhost = Vhost(self.domain.name, atts['vhost'])

        # If an apache vhost config already exists, try to parse it
        if self.vhost.exists():
            print str(self.vhost) + ' already exists.'
            if prompt('Parse existing vhost configuration?'):
                atts = merge_atts(atts, self.vhost.parse())
        # TODO: Convert...or migrate?

        self.root = Dir(atts['root'])
        self.htdocs = Dir(atts['htdocs'])
        self.assets = Dir(atts['assets'])
        self.logs = Dir(atts['logs'])

        # Set path of htaccess, access_log, and error_log after htdocs is set.
        if not atts['htaccess']['path']:
            atts['htaccess']['path'] = self.htdocs.path + '.htaccess'
        if not atts['access_log']['path']:
            atts['access_log']['path'] = self.logs.path + s.SITE_ACCESS_LOG
        if not atts['error_log']['path']:
            atts['error_log']['path'] = self.logs.path + s.SITE_ERROR_LOG

        self.htaccess = Htaccess(atts['htaccess'])
        self.access_log = File(atts['access_log'])
        self.error_log = File(atts['error_log'])

        # Setup vhost placeholders after attributes have been defined
        self.vhost.placeholders = {
            '#WEBSITE#'    : self.domain.name,
            '#HTDOCS#'     : self.htdocs.path,
            '#EMAIL#'      : s.SITE_ADMIN_EMAIL,
            '#ACCESS_LOG#' : self.access_log.path,
            '#ERROR_LOG#'  : self.error_log.path
        }


    def __str__(self):
        """Returns a string with relevant instance information."""
        string = '\n\n----------------------------------------------------------'
        string += '\n                        - Website -'
        string += '\n----------------------------------------------------------'
        string += '\n  domain:           ' + str(self.domain)
        string += '\n  vhost config:     ' + str(self.vhost)
        string += '\n  htdocs directory: ' + str(self.htdocs)
        string += '\n  assets:           ' + str(self.assets)
        string += '\n  logs:             ' + str(self.logs)
        string += '\n----------------------------------------------------------\n'
        return string

    def __repr__(self):
        """Returns a python string that evaluates to the object instance."""
        return "{0}('{1}', {'htdocs' : {2}, 'assets' : {3}, 'logs' : {4}, " + \
               "'access_log' : {5}, 'error_log' : {6}, 'htaccess' : {7}, " + \
               "'vhost' : {8}})".format(
                   self.__class__.__name__,
                   self.domain,
                   self.htdocs.get_atts(),
                   self.assets.get_atts(),
                   self.logs.get_atts(),
                   self.access_log.get_atts(),
                   self.error_log.get_atts(),
                   self.htaccess.get_atts(),
                   self.vhost.get_atts()
               )

    def install(self):
        """Installs website to server"""
        # Check if domain is already installed
        if self.is_installed():
            print self.domain + ' is already installed.'

        self.root.create()
        self.htdocs.create()
        self.assets.create()
        self.logs.create()
        self.access_log.create()
        self.error_log.create()
        self.htaccess.create()

        self.vhost.create()

        self.domain.set_ip()

        print str(self)
        print 'Installation complete.'

    def remove(self, ask=True):
        """Removes website from server"""
        self.vhost.disable(ask)

        self.vhost.remove(ask)
        self.access_log.remove(ask)
        self.error_log.remove(ask)
        self.htaccess.remove(ask)
        self.logs.remove(ask)
        self.htdocs.remove(ask)
        self.assets.remove(ask)
        self.root.remove(ask)

        self.domain.set_ip()

    def pack(self):
        """Todo:"""
        pass

    def unpack(self):
        """Todo:"""
        pass

    def migrate(self, old_website=None):
        """Todo:"""
        if not old_website:
            old_website = self.existing
        # make sure there's nothing conflicting
        # install() new
        # this overwrites vhostconf...
        # for dirs and files in old copy
        # this includes vhost...

    def verify(self, repair=False):
        """Verifies website installation"""
        result = all([self.vhost.verify(repair),
                      self.access_log.verify(repair),
                      self.error_log.verify(repair),
                      self.htaccess.verify(repair),
                      self.logs.verify(repair),
                      self.htdocs.verify(repair),
                      self.assets.verify(repair),
                      self.root.verify(repair),
                      self.domain.verify(repair)])
        print self
        return result

    def repair(self):
        """Repairs website installation"""
        print 'Repairing ' + self.domain + '...'
        if self.verify(True):
            print '[OK] Repair completed successfully.'
        else:
            print '[ERROR] Repair resulted in errors.'

    def is_installed(self):
        """Returns true if vhost is enabled"""
        return self.vhost.is_enabled()
