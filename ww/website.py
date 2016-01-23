#!/usr/bin/env python
#
# name:             website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# date:             11/11/2015
#
# description:      A class to manage websites
#

try:
    from ext_pylib.files import Dir, File
    from ext_pylib.prompt import prompt, prompt_str, warn_prompt
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

import os
import tarfile
from vhost import Vhost
from website_domain import WebsiteDomain
from ww import settings as s


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
#       domain      Website domain
#       htdocs      Website root directory
#       assets      Website assets directory
#       logs        Website log directory
#       access_log  Website access log file
#       error_log   Website error log file
#       vhost       Apache vhost config file
#       htaccess    Website root htaccess file
#   methods:
#       install()  - installs a new website
#       remove()  - removes an existing website
#       pack  - packs an existing website
#       unpack  - unpacks an existing packed website into current server
#       migrate  - migrates a website from existing settings to default
#                  settings
#       verify()  - verifies a website installation
#       repair()  - verifies website forcing repairs
class Website(object):

    def __init__(self, domain, atts = {}):
        """Initializes a new Website instance."""

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
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : s.WWW_ADMIN,
                },
                'access_log' : {
                    'path'  : None,
                    'perms' : 0775,
                    'owner' : 'root',
                    'group' : s.WWW_ADMIN,
                },
                'error_log' : {
                    'path'  : None,
                    'perms' : 0775,
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
                },
            }

        atts = merge_atts(default_atts, atts)

        self.vhost = Vhost(self.domain, atts['vhost'])

        # If an apache vhost config already exists, try to parse it
        if self.vhost.exists():
            print self.files['vhost'] + ' already exists.'
            if prompt('Parse existing vhost configuration?'):
                atts = merge_atts(atts, self.vhost.get_parsed())
        # TODO: Convert...or migrate?

        self.root   = Dir(atts['root'])
        self.htdocs = Dir(atts['htdocs'])
        self.assets = Dir(atts['assets'])
        self.logs   = Dir(atts['logs'])

        # Set path of htaccess, access_log, and error_log after htdocs is set.
        if not atts['htaccess']['path']:
            atts['htaccess']['path'] = self.htdocs.path + '.htaccess'
        if not atts['access_log']['path']:
            atts['access_log']['path'] = self.logs.path + s.SITE_ACCESS_LOG
        if not atts['error_log']['path']:
            atts['error_log']['path'] = self.logs.path + s.SITE_ERROR_LOG

        self.htaccess  = File(atts['htaccess'])
        self.access_log = File(atts['access_log'])
        self.error_log = File(atts['error_log'])


    def __str__(self):
        """Returns a string with relevant instance information."""
        string =  '\n  domain:           ' + self.domain
        string += '\n  vhost config:     ' + self.vhost
        string += '\n  htdocs directory: ' + self.htdocs
        string += '\n  assets:           ' + self.assets
        string += '\n  logs:             ' + self.logs
        return string

    def __repr__(self):
        """Returns a python string that evaluates to the object instance."""
        return "%s('%s', {'htdocs' : %s, 'assets' : %s, 'logs' : %s, " + \
               "'access_log' : %s, 'error_log' : %s, 'htaccess' : %s, 'vhost' : %s})" % (
            self.__class__.__name__,
            self.domain,
            self.dirs['htdocs']._atts_(),
            self.dirs['assets']._atts_(),
            self.dirs['logs']._atts_(),
            self.dirs['access_log']._atts_(),
            self.dirs['error_log']._atts_(),
            self.files['htaccess']._atts_(),
            self.files['vhost']._atts_()
            )


    ################
    # Public Methods

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

        self.vhost.create({
                '#WEBSITE#'    : self.domain.domain,
                '#HTDOCS#'     : self.htdocs.path,
                '#EMAIL#'      : s.SITE_ADMIN_EMAIL,
                '#ACCESS_LOG#' : self.access_log.path,
                '#ERROR_LOG#'  : self.error_log.path
            })

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

    def verify(self, repair = False):
        """Verifies website installation"""
        print self
        return self.domain.verify() and \
               self.vhost.verify(repair) and \
               self.access_log.verify(repair) and \
               self.error_log.verify(repair) and \
               self.htaccess.verify(repair) and \
               self.logs.verify(repair) and \
               self.htdocs.verify(repair) and \
               self.assets.verify(repair) and \
               self.root.verify(repair)

    def repair(self):
        """Repairs website installation"""
        print 'Repairing ' + self.domain + '...'
        if self.verify(True):
            print 'Repair completed successfully. [OK]'
        else:
            print 'Repair resulted in errors. [ERROR]'

    def is_installed(self):
        """Returns true if website is installed"""
        return False
