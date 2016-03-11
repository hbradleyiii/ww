#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#

"""
ww.wp_website
~~~~~~~~~~~~~

A class to manage WordPress websites
Extends Website.
"""

from __future__ import absolute_import, print_function

import os
import re
import shutil
import tarfile
import time

try:
    import MySQLdb
except ImportError:
    raise ImportError('Python module mysqldb must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

try:
    from ext_pylib.files import TemplateFile
    from ext_pylib.input import prompt, prompt_str
    from ext_pylib.password import generate_pw
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

from . import settings as s
from .htaccess import Htaccess
from .website import Website, localhost, merge_atts
from .wp_config import WPConfig


def select_database(name):
    """Selects a specific mysql database and returns true if it exists."""
    return "SELECT schema_name FROM information_schema.schemata WHERE schema_name = '" + name + "'"

def select_user(user):
    """Selects a specific mysql user and returns true if it exists."""
    return "SELECT user FROM mysql.user WHERE user = '" + user + "'"

def download():
    """Downloads a fresh WordPress tarball, returns path of download"""
    wp_tarball = '/tmp/' + time.strftime("%d-%m-%Y") +  '-wp.tar.gz'
    if not os.path.exists(wp_tarball):
        print('Downloading Wordpress...')
        with open(wp_tarball, 'wb') as tarball:
            tarball.write(requests.get(s.WP_LATEST).content)
        print('Download Complete.')
    else:
        print('Already downloaded wordpress today. Using existing tarball.')
    return wp_tarball  # Return path to wordpress

def untar(tarball):
    """Untars WordPress to tmp dir, returns path of extracted files."""
    wp_extract_dir = '/tmp/' + time.strftime("%d-%m-%Y") +  '-wp/'
    wp_extracted = wp_extract_dir + 'wordpress/'
    if not os.path.exists(wp_extracted):
        print('Uncompressing files...')
        wp_tarfile = tarfile.open(tarball)
        wp_tarfile.extractall(wp_extract_dir)
        wp_tarfile.close()
        print('Extraction complete.')
    return wp_extracted  # Return path to extracted files


class WPWebsite(Website):
    """A WordPress website class and its associated attributes and methods."""

    def __init__(self, domain, atts, mysql=None):
        """Initializes a new WPWebsite instance."""
        if not mysql:
            mysql = s.MYSQL

        super(WPWebsite, self).__init__(domain, atts)

        # Setup MySQL connection
        self.query = MySQLdb.connect(
            host=mysql['host'],
            user=mysql['user'],
            passwd=mysql['password']
        ).cursor().execute

        db_name = re.sub('[^A-Za-z0-9_]', '_', 'wp_' + self.domain).lower()
        db_user = re.sub('[^A-Za-z0-9_]', '_', 'usr_' + self.domain).lower()
        if len(db_user) > 10:
            db_user = db_user[:10]

        default_atts = {
            'wp_config' : {
                'path'  : self.htdocs.path + 'wp-config.php',
                'perms' : 0775,
                'owner' : s.WWW_USR,
                'group' : s.WWW_USR,
            },
            'wp' : {
                'db_name'      : db_name,
                'db_host'      : 'localhost',
                'db_user'      : db_user,
                'db_password'  : generate_pw(),
                'table_prefix' : 'wp_',
                'debug'        : 'false',
                'disallow_edit': 'true',
                'fs_method'    : 'direct',
            },
        }

        atts = merge_atts(default_atts, atts)

        # Initialize config
        self.config = WPConfig(atts['wp_config'])
        if self.config.exists() and prompt(str(self.config) + ' already exists.\n' + \
            'Use existing wp_config.php configuration settings?'):
            atts = merge_atts(atts, self.config.parse())  # atts not used at this point (force flush/read())
        else:  # Otherwise, use the template
            self.config.data = TemplateFile({'path' : s.WP_CONFIG_TEMPLATE}).read()
            self.config.set(atts['wp'])

    def __str__(self):
        """Returns a string with relevant instance information."""
        string = '\n\n----------------------------------------------------------'
        string += '\n                   - Wordpress Website -'
        string += '\n----------------------------------------------------------'
        string += super(WPWebsite, self).__str__()[156:]
        string += '  Database:         ' + str(self.config.db_name)
        string += '\n  MySQL User:       ' + str(self.config.db_user)
        string += '\n  MySQL Password:   ' + str(self.config.db_password)
        string += '\n----------------------------------------------------------\n'
        return string

    def install(self):
        """Copies WordPress to htdocs, sets up a new database, then runs the 5 min setup."""
        super(WPWebsite, self).install()
        self.create_database()
        self.setup()

    def create_directories(self):
        """Creates website directories."""
        super(WPWebsite, self).create_directories()

    def create_files(self):
        """Creates website log files and htaccess file."""
        super(WPWebsite, self).create_files()
        self.config.create()
        self.htdocs.fill(untar(download()))

    def remove(self, no_prompt=False):
        """Uninstalls WordPress."""
        if no_prompt or prompt('Remove WordPress website database "' + self.db['name'] + '"?'):
            self.remove_wordpress_db()
        if no_prompt or prompt('Remove WordPress website directory "' + self.htdocs + '"?'):
            self.remove_wordpress_files()
        super(WPWebsite, self).uninstall()

    def pack(self, tarball=None):
        """Packs the htdocs, assets, and vhost files into a tarball."""

    def unpack(self, tarball=None, location=None, use_vhost=True):
        """Unpacks the previously packed htdocs, assets, and vhost files."""

    def migrate(self, old_website=None):
        """Todo:"""
        pass

    def verify(self):
        """Verifies WordPress installation."""
        super(WPWebsite, self).verify()

    @localhost
    def setup(self):
        """Runs the WordPress 5 min setup."""
        self.domain
        wordpress_config_setup()
        wordpress_install()

    def import_db(self, mysql_dump):
        """Imports a mysql database into WordPress database."""
        print('Importing mysql database...')

        # find/replace in sql database if necessary
        raw_input('find and replace not yet implemented... Press enter to continue.')

        # TODO: error handling
        os.system(
            'mysql ' +
            '-u ' + self.mysql['user'] +
            ' -p' + self.mysql['password'] + ' ' + self.domain +
            ' < ' + mysql_dump
            )
        print('Import complete.')

    def import_wp_content(self, import_dir):
        """Imports wp-content into WordPress."""
        print('Importing wp-content...')
        wp_content = self.htdocs + 'wp-content'
        if os.path.exists(wp_content):
            shutil.rmtree(wp_content)
        shutil.copytree(import_dir, wp_content)
        # need perms of wp-content to be correct.
        os.system('chown -R www-data ' + self.htdocs)

    def create_database(self):
        """Creates WordPress MySQL database."""
        print('Setting up WordPress database "' + self.db['name'] + '"...')
        # TODO: error handling
        while True:
            if self.query(select_user(user)):
                print('[!] MySQL user "' + user + '" already exists.')
                user = prompt_str('Choose another MySQL username:')
            else:
                break
        self.config.db_username
        self.query("CREATE DATABASE " + self.db['name'])

        while True:
            if self.query(select_database(name)):
                print('[!] Database "' + name + '" already exists.')
                name = prompt_str('Choose another MySQL database name:')
            else:
                break
        self.config.db_name = name
        self.query("CREATE USER " + self.db['user'] + "@localhost IDENTIFIED BY '" + self.db['password']  + "'")

        self.query("GRANT ALL PRIVILEGES ON " + self.db['name'] + ".* TO " + self.db['user'] + "@localhost")
        self.query("FLUSH PRIVILEGES")
        print('Database ready.')

    def remove_database(self):
        """Removes WordPress MySQL database."""
        print('Removing Wordpress database "' + self.db['name'] + '"...')
        # TODO: error handling
        self.query("DROP DATABASE " + self.db['name'])
        print('Removing Wordpress user "' + self.db['user'] + '"...')
        self.query("DROP USER " + self.db['user'] + "@localhost")
        self.query("FLUSH PRIVILEGES")
        print('Database removed.')

    def wordpress_install(self):
        """TODO:"""
        public = '1' if prompt('Allow search engines to index?') else '0'
        user = prompt_str('What is the WordPress admin username?', \
                          s.WP_ADMIN_USER)
        password = prompt_str('What is the password for this account?', \
                             s.WP_ADMIN_PW)
        email = prompt_str('What is the email for this account?', \
                          s.WP_ADMIN_EMAIL)
        title = prompt_sr('What is the website\'s title?')

        payload = {
            'blog_public'     : public,
            'user_name'       : user,
            'admin_password'  : password,
            'pass1-text'      : password,
            'admin_password2' : password,
            'admin_email'     : email,
            'weblog_title'    : title,
            'language'        : 'en_US'
        }

        print('Running install...')
        r = requests.post('http://' + self.domain + s.WP_INSTALL_URL, data=payload)
        print(r.text)
        print('Installation complete')
