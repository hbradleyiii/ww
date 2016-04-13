#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# date:             11/11/2015
#
# pylint:           disable=line-too-long

"""
ww.website
~~~~~~~~~~

A class to manage websites
"""

from __future__ import absolute_import, print_function

from subprocess import check_output, CalledProcessError

try:
    from ext_pylib.files import Dir, File, TemplateFile
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
        print('Adding temporary host entry.')
        remove_entry = True
        cmd = "echo '127.0.0.1 " + self.domain + "' | cat >> /etc/hosts"
        try:
            check_output(cmd, shell=True)
        except CalledProcessError:
            print('[WARN] Error adding temporary host entry')
            remove_entry = False

        result = function(self, *args, **kwargs)

        if remove_entry:
            print('Removing temporary host entry.')
            cmd = "sed -i '/^127\.0\.0\.1 " + self.domain + "$/d' /etc/hosts"  # pylint: disable=anomalous-backslash-in-string
            if check_output(cmd, shell=True) != 0:
                print('[WARN] Error removing temporary host entry.')

        return result

    return function_wrapper


def merge_atts(atts, new_atts):
    """Merges two dictionaries with the second overwriting the corresponding
    values of the first and returns the result."""
    if not atts:
        return new_atts
    if not new_atts:
        return atts
    for k, _ in new_atts.iteritems():
        if (k in atts and isinstance(atts[k], dict)
                and isinstance(new_atts[k], dict)):
            atts[k] = merge_atts(atts[k], new_atts[k])
        else:
            atts[k] = new_atts[k]
    return atts


class Website(object):  # pylint: disable=too-many-instance-attributes
    """A class that describes a generic website with the following properties:
        domain      Website domain
        htdocs      Website root directory
        assets      Website assets directory
        log         Website log directory
        access_log  Website access log file
        error_log   Website error log file
        vhost       Apache vhost config file
        htaccess    Website root htaccess file
    """

    def __init__(self, domain, atts=None):
        """Initializes a new Website instance."""
        atts = atts or {}

        print('[*] SSL not yet implemented in Website class.')

        self.domain = WebsiteDomain(domain)
        self.dirs = {}
        self.files = {}

        default_atts = {
            'root' : {
                'path'  : s.WWW_DIR + self.domain,
                'perms' : 0775,
                'owner' : s.WWW_ADMIN,
                'group' : s.WWW_ADMIN,
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
            'log' : {
                'path'  : s.WWW_DIR + self.domain + '/log/',
                'perms' : 0770,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'access_log' : {
                'path'  : s.WWW_DIR + self.domain + '/log/access_log',
                'perms' : 0750,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'error_log' : {
                'path'  : s.WWW_DIR + self.domain + '/log/error_log',
                'perms' : 0750,
                'owner' : 'root',
                'group' : s.WWW_ADMIN,
            },
            'vhost' : {
                'path'  : s.VHOST_PATH + self.domain + '.conf',
                'perms' : 0644,
                'owner' : 'root',
                'group' : 'root',
                'domain': self.domain,
            },
            'htaccess' : {
                'path'  : s.WWW_DIR + self.domain + '/htdocs/.htaccess',
                'perms' : 0664,
                'owner' : s.WWW_USR,
                'group' : s.WWW_USR,
                'sections' : [
                    {'identifier' : 'h5g', 'path' : s.HTA_5G_TEMPLATE},
                ]
            },
        }

        atts = merge_atts(default_atts, atts)

        # Initialize Vhost first, in order to possibly parse atts from it
        self.vhost = Vhost(atts['vhost'])
        if self.vhost.exists() and prompt(str(self.vhost) + ' already exists.\n' + \
            'Use existing vhost configuration for htdocs directory and log file location?'):
            atts = merge_atts(atts, self.vhost.parse())
        else:  # Otherwise, use the template
            self.vhost.data = TemplateFile({'path' : s.VHOST_TEMPLATE}).apply_using({
                '#DOMAIN#'     : self.domain.name,
                '#HTDOCS#'     : s.WWW_DIR + self.domain + '/htdocs/',
                '#EMAIL#'      : s.SITE_ADMIN_EMAIL,
                '#ACCESS_LOG#' : s.WWW_DIR + self.domain + '/log/access_log',
                '#ERROR_LOG#'  : s.WWW_DIR + self.domain + '/log/error_log',
            })

        # Initialize Directories
        self.root = Dir(atts['root'])
        self.htdocs = Dir(atts['htdocs'])
        self.assets = Dir(atts['assets'])
        self.log = Dir(atts['log'])

        # Initialize Files
        self.htaccess = Htaccess(atts['htaccess'])
        self.access_log = File(atts['access_log'])
        self.error_log = File(atts['error_log'])

    def __str__(self):
        """Returns a string with relevant instance information."""
        string = '\n\n----------------------------------------------------------'
        string += '\n                        - Website -'
        string += '\n----------------------------------------------------------'
        string += '\n  domain:           ' + str(self.domain)
        string += '\n  vhost config:     ' + str(self.vhost)
        string += '\n  htdocs directory: ' + str(self.htdocs)
        string += '\n  assets:           ' + str(self.assets)
        string += '\n  log:              ' + str(self.log)
        string += '\n----------------------------------------------------------\n'
        return string

    def __repr__(self):
        """Returns a python string that evaluates to the object instance."""
        return self.__class__.__name__ + "('" + \
            self.domain.name + "', {" + \
            "'htdocs' : " + str(self.htdocs.get_atts()) + \
            ", 'assets' : " + str(self.assets.get_atts()) + \
            ", 'log' : " + str(self.log.get_atts()) + \
            ", 'access_log' : " + str(self.access_log.get_atts()) + \
            ", 'error_log' : " + str(self.error_log.get_atts()) + \
            ", 'htaccess' : " + str(self.htaccess.get_atts()) + \
            ", 'vhost' : " + str(self.vhost.get_atts()) + "})"

    def install(self):
        """Installs website to server"""
        # Check if domain is already installed
        if self.is_installed():
            print(self.domain + ' is already installed.')

        self.create_directories()
        self.create_files()
        self.vhost.create()
        self.domain.set_ip()

        print(str(self))
        print('Installation complete.')

    def create_directories(self):
        """Creates website directories."""
        self.root.create()
        self.htdocs.create()
        self.assets.create()
        self.log.create()

    def create_files(self):
        """Creates website log files and htaccess file."""
        self.access_log.create()
        self.error_log.create()
        self.htaccess.create()

    def remove(self, ask=True):
        """Removes website from server"""
        self.vhost.disable(ask)

        self.vhost.remove(ask)
        self.access_log.remove(ask)
        self.error_log.remove(ask)
        self.htaccess.remove(ask)
        self.log.remove(ask)
        self.htdocs.remove(ask)
        self.assets.remove(ask)
        self.root.remove(ask)

        self.domain.set_ip()

    def pack(self, tarball=None):
        """Packs the htdocs, assets, and vhost files into a tarball."""
        import tarfile

        if not tarball:
            tarball = '/tmp/packed-' + self.domain.name + '.tar.gz'
        with tarfile.open(tarball, 'w:gz') as tar:
            tar.add(self.htdocs.path, arcname='htdocs')
            tar.add(self.assets.path, arcname='assets')
            tar.add(self.vhost.path, arcname='vhost.conf')

    def unpack(self, tarball=None, location=None, use_vhost=True):
        """Unpacks the previously packed htdocs, assets, and vhost files."""
        import tarfile

        if not tarball:
            tarball = '/tmp/packed-' + self.domain.name + '.tar.gz'
        if not location:
            location = '/tmp/unpacked-' + self.domain.name
        with tarfile.open(tarball, 'r') as tar:
            tar.extractall(location)

        if use_vhost:
            self.create_directories()
            self.create_files()
            self.vhost.create(File({'path' : location + '/vhost.conf'}).read())
        else:
            self.install()
        self.htdocs.fill(Dir({'path' : location + '/htdocs/'}))
        self.assets.fill(Dir({'path' : location + '/assets/'}))

    def migrate(self, new_domain):
        """Migrates a website from one domain to another.
        This is essentially making an exact copy of the website using a
        different domain."""

        self.domain.name = new_domain
        # if not old_website:
        #     old_website = self.existing
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
                      self.log.verify(repair),
                      self.htdocs.verify(repair),
                      self.assets.verify(repair),
                      self.root.verify(repair),
                      self.domain.verify(repair)])
        print(self)
        return result

    def repair(self):
        """Repairs website installation"""
        print('Repairing ' + self.domain + '...')
        if self.verify(True):
            print('[OK] Repair completed successfully.')
        else:
            print('[ERROR] Repair resulted in errors.')

    def is_installed(self):
        """Returns true if vhost is enabled"""
        return self.vhost.is_enabled()
