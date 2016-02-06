#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             wp_config.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#

"""
ww.wp_config
~~~~~~~~~~~~

A class to create WordPress wp_config.php files.
Extends WWFile.
"""

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

try:
    from ext_pylib.files import Parsable, Section, Template
    from ext_pylib.input import prompt, prompt_str
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

from . import settings as s
from .ww_file import WWFile


SALT_REGEXES = {
    'auth_key'         : ("define\('AUTH_KEY',[ ]*'([^']*)'\);",
                            "define('AUTH_KEY',         '{0}');"),
    'secure_auth_key'  : ("define\('SECURE_AUTH_KEY',[ ]*'([^']*)'\);",
                            "define('SECURE_AUTH_KEY',  '{0}');"),
    'logged_in_key'    : ("define\('LOGGED_IN_KEY',[ ]*'([^']*)'\);",
                            "define('LOGGED_IN_KEY',    '{0}');"),
    'nonce_key'        : ("define\('NONCE_KEY',[ ]*'([^']*)'\);",
                            "define('NONCE_KEY',        '{0}');"),
    'auth_salt'        : ("define\('AUTH_SALT',[ ]*'([^']*)'\);",
                            "define('AUTH_SALT',        '{0}');"),
    'secure_auth_salt' : ("define\('SECURE_AUTH_SALT',[ ]*'([^']*)'\);",
                            "define('SECURE_AUTH_SALT', '{0}');"),
    'logged_in_salt'   : ("define\('LOGGED_IN_SALT',[ ]*'([^']*)'\);",
                            "define('LOGGED_IN_SALT',   '{0}');"),
    'nonce_salt'       : ("define\('NONCE_SALT',[ ]*'([^']*)'\);",
                            "define('NONCE_SALT',       '{0}');"),
}

WP_CONF_REGEXES = dict(SALT_REGEXES, **{
    'debug'        : ("define\('WP_DEBUG', ([^ \n]*)\);",
                      "define('WP_DEBUG', {0});"),
    'db_name'      : ("define\('DB_NAME', '([^ \n]*)'\);",
                      "define('DB_NAME', '{0}');"),
    'db_user'      : ("define\('DB_USER', '(.*)'\);",
                      "define('DB_USER', '{0}');"),
    'db_password'  : ("define\('DB_PASSWORD', '(.*)'\);",
                      "define('DB_PASSWORD', '{0}');"),
    'db_host'      : ("define\('DB_HOST', '(.*)'\);",
                      "define('DB_HOST', '{0}');"),
    'table_prefix' : ("\$table_prefix[ ]*=[ ]*['\"](.*)['\"];",
                      "$table_prefix = '{0}';"),
    'disallow_edit': ("define\('DISALLOW_FILE_EDIT', (.*)\);",
                      "define('DISALLOW_FILE_EDIT', {0});"),
    'fs_method'    : ("define\('FS_METHOD', '(.*)'\);",
                      "define('FS_METHOD', '{0}');"),
})


class WPConfigTemplate(Template, WWFile):
    """A WordPress configuration template file."""


class WPSalt(Section, Parsable):
    """A class that describes a WordPress wp_config.php Salt section."""

    regexes = SALT_REGEXES

    def __init__(self):
        """WPSalt init."""
        self.data = requests.get(s.WP_SALT_URL).text
        self.setup_parsing()

    def read(self):
        """Overrides the parent method, merely returning self.data.
        The data is set in __init__. This prevents excessive network calls."""
        return self.data

    def secrets(self):
        """A generator that yields a tuple of key and salt value."""
        secrets = {}
        for key, regex in self.regexes.iteritems():
            yield (key, getattr(self, key))


class WPConfig(Parsable, WWFile):
    """A class that describes a WordPress wp_config.php file.
    This is primarily a wrapper for wp_config managment.
    """

    regexes = WP_CONF_REGEXES  # The regexes guarantee that the class will have
                               # necessary attributes, even if set to None.

    def __init__(self, atts):
        """Initializes WPConfig."""
        self.setup_parsing()  # Do this first, before initializing attributes

        super(WPConfig, self).__init__(atts)
        self.default_atts = atts

        if self.exists() and prompt('Parse existing wp_config.php?'):
            atts['wp'] = self.parse(True)
        else:  # Otherwise, apply the template and create salts
            self.template = WPConfigTemplate({'path' : s.WP_CONFIG_TEMPLATE}).read()
            self.data = self.template
            for key, value in WPSalt().secrets():
                setattr(self, key, value)

        if 'wp' in atts:
            for att, value in atts['wp'].iteritems():
                setattr(self, att, value)


    def parse(self, parse_from_disk=False):
        """Returns a dict of attributes. Passing in True as an arguement will
           force reading from disk."""

        if parse_from_disk:
            """Prompting is necessary (but hopefully unusual) if file on disk
               cannot be parsed."""

            self.read(True)  # Force read() clearing memory

            if not self.debug:
                print 'Could not parse debug mode.'
                if prompt('Turn debug mode on?'):
                    self.debug = 'true'
                else:
                    self.debug = 'false'

            if not self.table_prefix:
                print 'Could not parse WordPress database table_prefix.'
                self.table_prefix = prompt_str('What is the WordPress database table_prefix?')

            if not self.db_name:
                print 'Could not parse WordPress database name.'
                self.db_name = prompt_str('What is the WordPress database name?')

            if not self.db_user:
                print 'Could not parse WordPress database user.'
                self.db_user = prompt_str('What is the WordPress database user?')

            if not self.db_password:
                print 'Could not parse WordPress database password.'
                self.db_password = prompt_str('What is the WordPress database password?')

            if not self.db_host:
                print 'Could not parse WordPress database hostname.'
                self.db_host = prompt_str('What is the WordPress database hostname?')

            if not self.disallow_edit:
                print 'Could not parse DISALLOW_EDIT.'
                if prompt('Set DISALLOW_EDIT to "true"?'):
                    self.disallow_edit = 'true'
                else:
                    self.disallow_edit = 'false'

            if not self.fs_method:
                print 'Could not parse fs_method.'
                self.fs_method = prompt_str('What should we set fs_method?', 'direct')

            if not self.auth_key or \
               not self.secure_auth_key or \
               not self.logged_in_key or \
               not self.nonce_key or \
               not self.auth_salt or \
               not self.secure_auth_salt or \
               not self.logged_in_salt or \
               not self.nonce_salt:
                print 'Salts not parsable. Recreating new salts...'
                for key, value in WPSalt().secrets():
                    setattr(self, key, value)

        else:
            self.read()  # At least make sure contents are already read into
                         # memory.

        return { 'debug'            : self.debug,
                 'table_prefix'     : self.table_prefix,
                 'db_name'          : self.db_name,
                 'db_user'          : self.db_user,
                 'db_password'      : self.db_password,
                 'db_host'          : self.db_host,
                 'disallow_edit'    : self.disallow_edit,
                 'fs_method'        : self.fs_method,
                 'auth_key'         : self.auth_key,
                 'secure_auth_key'  : self.secure_auth_key,
                 'logged_in_key'    : self.logged_in_key,
                 'nonce_key'        : self.nonce_key,
                 'auth_salt'        : self.auth_salt,
                 'secure_auth_salt' : self.secure_auth_salt,
                 'logged_in_salt'   : self.logged_in_salt,
                 'nonce_salt'       : self.nonce_salt }

    def verify(self, repair=False, use_default_atts=False):
        """Verifies the attributes of WPConfig instance. Unless you pass in
           use_default_atts as True, this assumes the in-memory values are the
           correct values."""
        result = True  # Assume the best :)
        save = False

        if use_default_atts:
            correct_values = self.default_atts
        else:
            correct_values = self.parse()  # Retrieve values in memory (and hold
                                           # for comparison and/or repair)

        self.read(True)  # Force reading values in from disk

        verify_items = {
            'debug'         : '[!] Debug is incorrectly set to: ',
            'table_prefix'  : '[!] WordPress table prefix is incorrectly set to: ',
            'db_name'       : '[!] WordPress database name is incorrectly set to: ',
            'db_user'       : '[!] WordPress database username is incorrectly set to: ',
            'db_password'   : '[!] WordPress database password is incorrectly set to: ',
            'db_host'       : '[!] Databse hostname is incorrectly set to: ',
            'disallow_edit' : '[!] DISALLOW_EDIT is incorrectly set to: ',
            'fs_method'     : '[!] FS_METHOD is incorrectly set to: ',
        }

        for attribute, error_message in verify_items.iteritems():
            correct_value = correct_values[attribute]
            current_value = getattr(self, attribute)
            if not current_value == correct_value:
                print error_message + str(current_value)
                if repair:
                    print 'Setting "' + attribute + '" to: "' + \
                        correct_value + '"...'
                    setattr(self, attribute, correct_value)
                    save = True
                else:
                    result = False

        if repair and save:
            if prompt('Create new salts?'):
                print 'Creating new salts...'
                for key, value in WPSalt().secrets():
                    setattr(self, key, value)
            self.write(append=False)

        if self.debug == 'true':
            print '\n    -------------------------------------'
            print '    [WARN] WordPress Debug mode is on.'
            print '           Be sure to turn this off in'
            print '           a production environment!'
            print '    -------------------------------------\n'

        return result
