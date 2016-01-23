#!/usr/bin/env python
#
# name:             wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
#
# description:      A class to manage WordPress websites; extends Website.
#

try:
    from ext_pylib.prompt import prompt, prompt_str, warn_prompt
    from ext_pylib.password import generate_pw
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

try:
    import MySQLdb
except ImportError:
    raise ImportError('Python module mysqldb must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

import os
import re
from shutil import *
import tarfile
import time
from website import Website, localhost


WP_LATEST      = 'http://wordpress.org/latest.tar.gz'
WP_TARBALL     = '/tmp/' + time.strftime("%d-%m-%Y") +  '-wp.tar.gz'
WP_EXTRACTED   = '/tmp/' + time.strftime("%d-%m-%Y") +  '-wp/'
WP_SETUP_URL   = '/wp-admin/setup-config.php?step=2'
WP_INSTALL_URL = '/wp-admin/install.php?step=2'


class WPWebsite(Website):

    def __init__(self, domain, htdocs, mysql={}, is_new_website=False):
        """Initializes a new WPWebsite instance."""

        super(WPWebsite, self).__init__(domain)

        # Setup MySQL connection
        self.mysql = MySQLdb.connect(
                host   = mysql['host'],
                user   = mysql['user'],
                passwd = mysql['password']
                )
        self.cur = self.mysql.cursor()
        self.query = self.cur.execute # Used for SQL queries

        self.db = {'name' : '', 'user' : '', 'password' : ''}
        if is_new_website:

            # Initialize Wordpress database vars
            name = re.sub('[^A-Za-z0-9_]', '_', 'wp_' + domain)
            while True:
                if self.query("SELECT schema_name FROM information_schema.schemata WHERE schema_name = '" + name + "'"):
                    print '[!] Database "' + name + '" already exists.'
                    name = prompt_str('Choose another MySQL database name:')
                else:
                    break
            self.db['name'] = name

            user = re.sub('[^A-Za-z0-9_]', '_', 'usr_' + domain)
            if len(user) > 10:
                user = user[:10]
            while True:
                if self.query("SELECT user FROM mysql.user WHERE user = '" + user + "'"):
                    print '[!] MySQL user "' + user + '" already exists.'
                    user = prompt_str('Choose another MySQL username:')
                else:
                    break
            self.db['user'] = user
            self.db['password'] = generate_pw()

        else: # Current website; use wp_config
            self.parse_wp_config()

    def __str__(self):
        """Returns a string with relevant instance information."""
        string = '\n----------------------------------------------------------'
        string += '\n                   - Wordpress Website -'
        string += super(WPWebsite, self).__str__()
        string += '\n  Database:         ' + self.db['name']
        string += '\n  MySQL User:       ' + self.db['user']
        string += '\n  MySQL Password:   ' + self.db['password']
        string += '\n----------------------------------------------------------\n\n'
        return string

    ################
    # Public Methods

    def install(self):
        """Copies WordPress to htdocs, sets up a new database, then runs the 5 min setup."""
        super(WPWebsite, self).install()
        self.download_wordpress()
        self.untar_wordpress()
        self.create_wordpress_db()

    def uninstall(self, no_prompt=False):
        """Uninstalls WordPress."""
        if no_prompt or prompt('Remove WordPress website database "' + self.db['name'] + '"?'):
            self.remove_wordpress_db()
        if no_prompt or prompt('Remove WordPress website directory "' + self.htdocs + '"?'):
            self.remove_wordpress_files()
        super(WPWebsite, self).uninstall()

    def verify(self):
        """Verifies WordPress installation."""
        super(WPWebsite, self).verify()

    @localhost
    def setup_wordpress(self):
        """Runs the WordPress 5 min setup."""
        wordpress_config_setup()
        wordpress_install()

    def import_db(self, mysql_dump):
        """Imports a mysql database into WordPress database."""
        print 'Importing mysql database...'

        # find/replace in sql database if necessary
        raw_input('find and replace not yet implemented... Press enter to continue.')

        # TODO: error handling
        os.system(
            'mysql ' +
            '-u ' + self.mysql['user'] +
            ' -p' + self.mysql['password'] + ' ' + self.domain +
            ' < ' + mysql_dump
            )
        print 'Import complete.'

    def import_wp_content(self, import_dir):
        """Imports wp-content into WordPress."""
        print 'Importing wp-content...'
        wp_content = self.htdocs + 'wp-content'
        if os.path.exists(wp_content):
            shutil.rmtree(wp_content)
        shutil.copytree(import_dir, wp_content)
        # need perms of wp-content to be correct.
        os.system('chown -R www-data ' + self.htdocs)


    ###################
    # Private Methods

    def download_wordpress(self):
        """Downloads a fresh WordPress tarball."""
        if not os.path.exists(WP_TARBALL):
            print 'Downloading Wordpress...'
            with open(WP_TARBALL, 'wb') as tarball:
                tarball.write(requests.get(WP_LATEST).content)
            print 'Download Complete.'
        else:
            print 'Already downloaded wordpress today. Using existing tarball.'

    def untar_wordpress(self):
        """Untars WordPress to htdocs."""
        if not os.path.exists(WP_EXTRACTED + 'wordpress/'):
            print 'Uncompressing files...'
            tarball = tarfile.open(WP_TARBALL)
            tarball.extractall(WP_EXTRACTED)
            tarball.close()
            print 'Extraction complete.'
        print 'Moving files to "' + self.htdocs + '"...'
        move(WP_EXTRACTED + 'wordpress/', self.htdocs)
        rmtree(self.htdocs + 'wordpress') # Get rid of the 'wordpress' root directory
        os.system('chown -R www-data ' + self.htdocs)
        print 'Move complete.'

    def remove_wordpress_files(self):
        """Removes WordPress website files."""
        print 'Removing Wordpress website files...'
        # TODO: error handling
        rmtree(self.htdocs)
        print 'Website files removed.'

    def create_wordpress_db(self):
        """Creates WordPress MySQL database."""
        print 'Setting up WordPress database "' + self.db['name'] + '"...'
        # TODO: error handling
        self.query("CREATE DATABASE " + self.db['name'])
        self.query("CREATE USER " + self.db['user'] + "@localhost IDENTIFIED BY '" + self.db['password']  + "'")
        self.query("GRANT ALL PRIVILEGES ON " + self.db['name'] + ".* TO " + self.db['user'] + "@localhost")
        self.query("FLUSH PRIVILEGES")
        print 'Database ready.'

    def remove_wordpress_db(self):
        """Removes WordPress MySQL database."""
        print 'Removing Wordpress database "' + self.db['name'] + '"...'
        # TODO: error handling
        self.query("DROP DATABASE " + self.db['name'])
        print 'Removing Wordpress user "' + self.db['user'] + '"...'
        self.query("DROP USER " + self.db['user'] + "@localhost")
        self.query("FLUSH PRIVILEGES")
        print 'Database removed.'

    def wordpress_config_setup(self):
        payload = {
                'dbname' : self.db['name'],
                'uname'  : self.db['user'],
                'pwd'    : self.db['password'],
                'dbhost' : 'localhost',
                'prefix' : 'wp_'
                }

        # TODO: error handling
        print 'Running setup config...'
        r = requests.post('http://' + self.domain + WP_SETUP_URL, data=payload)
        print r.text
        print 'Config setup complete'

    def wordpress_install(self):
        public = '1' if prompt("Allow search engines to index?") else '0'
        user = prompt_str('What is the WordPress admin username?', 'admin')
        password = prompt_str('What is the password for this account?', 'password123')
        email = prompt_str('What is the email for this account?', 'email@google.com')
        title = raw_input("What is the website's title? ")

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

        print 'Running install...'
        r = requests.post('http://' + self.domain + WP_INSTALL_URL, data=payload)
        print r.text
        print 'Installation complete'


    def parse_wp_config(self):
        self.db['user'] = user
        self.db['password'] = generate_pw()
        self.db['name'] = ''
