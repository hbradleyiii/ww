#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             wp_config.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#
# pylint:           disable=attribute-defined-outside-init,too-many-branches

"""
ww.wp_config
~~~~~~~~~~~~

A class to create WordPress wp_config.php files.
Extends WWFile.
"""

from __future__ import absolute_import, print_function

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

try:
    from ext_pylib.files import Parsable, Section
    from ext_pylib.input import prompt, prompt_str
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

from . import settings as s
from .ww_file import WWFile


SALT_REGEXES = {
    'auth_key'         : (r"define\('AUTH_KEY',[ ]*'([^']*)'\);",
                          "define('AUTH_KEY',         '{0}');"),
    'secure_auth_key'  : (r"define\('SECURE_AUTH_KEY',[ ]*'([^']*)'\);",
                          "define('SECURE_AUTH_KEY',  '{0}');"),
    'logged_in_key'    : (r"define\('LOGGED_IN_KEY',[ ]*'([^']*)'\);",
                          "define('LOGGED_IN_KEY',    '{0}');"),
    'nonce_key'        : (r"define\('NONCE_KEY',[ ]*'([^']*)'\);",
                          "define('NONCE_KEY',        '{0}');"),
    'auth_salt'        : (r"define\('AUTH_SALT',[ ]*'([^']*)'\);",
                          "define('AUTH_SALT',        '{0}');"),
    'secure_auth_salt' : (r"define\('SECURE_AUTH_SALT',[ ]*'([^']*)'\);",
                          "define('SECURE_AUTH_SALT', '{0}');"),
    'logged_in_salt'   : (r"define\('LOGGED_IN_SALT',[ ]*'([^']*)'\);",
                          "define('LOGGED_IN_SALT',   '{0}');"),
    'nonce_salt'       : (r"define\('NONCE_SALT',[ ]*'([^']*)'\);",
                          "define('NONCE_SALT',       '{0}');"),
}

WP_CONF_REGEXES = dict(SALT_REGEXES, **{
    'db_name'      : (r"define\('DB_NAME', '([^ \n]*)'\);",
                      "define('DB_NAME', '{0}');"),
    'db_host'      : (r"define\('DB_HOST', '(.*)'\);",
                      "define('DB_HOST', '{0}');"),
    'db_user'      : (r"define\('DB_USER', '(.*)'\);",
                      "define('DB_USER', '{0}');"),
    'db_password'  : (r"define\('DB_PASSWORD', '(.*)'\);",
                      "define('DB_PASSWORD', '{0}');"),
    'table_prefix' : (r"\$table_prefix[ ]*=[ ]*['\"](.*)['\"];",
                      "$table_prefix = '{0}';"),
    'debug'        : (r"define\('WP_DEBUG', ([^ \n]*)\);",
                      "define('WP_DEBUG', {0});"),
    'disallow_edit': (r"define\('DISALLOW_FILE_EDIT', (.*)\);",
                      "define('DISALLOW_FILE_EDIT', {0});"),
    'fs_method'    : (r"define\('FS_METHOD', '(.*)'\);",
                      "define('FS_METHOD', '{0}');"),
})


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
        for key, _ in self.regexes.iteritems():
            yield (key, getattr(self, key))


class WPConfig(Parsable, WWFile):
    """A class that describes a WordPress wp_config.php file.
    This is primarily a wrapper for wp_config managment.
    """
    # pylint: disable=too-many-instance-attributes
    regexes = WP_CONF_REGEXES  # The regexes guarantee that the class will have
                               # necessary attributes, even if set to None.

    def __init__(self, atts):
        """Initializes WPConfig."""
        super(WPConfig, self).__init__(atts)
        self.setup_parsing()

    def create(self, data=''):
        """Creates a vhost file replacing placeholders with data if they exist."""
        # pylint: disable=attribute-defined-outside-init
        if data:
            self.data = data

        # (re)Create salts every time
        for key, value in WPSalt().secrets():
            setattr(self, key, value)

        super(WPConfig, self).create()

    def set(self, atts):
        """Takes a dict of atts and sets them on the object."""
        for att, value in atts.iteritems():
            setattr(self, att, value)

    def parse(self, flush_memory=False, ask=True):
        """Returns a dict of attributes. Passing in True as an arguement will
        force reading from disk."""

        # Make sure contents are already read into memory.
        self.read(flush_memory)

        # Prompting is necessary (but hopefully unusual) if file on disk
        # cannot be parsed.

        for attribute in ['debug', 'disallow_edit']:
            if not getattr(self, attribute, None):
                print('Could not parse WordPress attribute ' + attribute + '.')
                if ask:
                    if prompt('Set ' + attribute + ' to True?'):
                        self.debug = 'true'
                    else:
                        self.debug = 'false'

        for attribute in ['table_prefix', 'db_name', 'db_user',
                          'db_password', 'db_host',]:
            if not getattr(self, attribute, None):
                print('Could not parse WordPress ' + attribute + '.')
                if ask:
                    setattr(self, attribute,
                            prompt_str('What is the WordPress database table_prefix?'))

        if not getattr(self, 'fs_method', None):
            print('Could not parse fs_method.')
            if ask:
                self.fs_method = prompt_str('What should we set fs_method?', 'direct')

        for salt in ['auth_key', 'secure_auth_key', 'logged_in_key',
                     'nonce_key', 'auth_salt', 'secure_auth_salt',
                     'logged_in_salt', 'nonce_salt']:
            if not getattr(self, salt, None):
                print('Salts not parsable. Recreating new salts...')
                for key, value in WPSalt().secrets():
                    setattr(self, key, value)
                break

        return {'db_name'          : getattr(self, 'db_name', None),
                'db_host'          : getattr(self, 'db_host', None),
                'db_user'          : getattr(self, 'db_user', None),
                'db_password'      : getattr(self, 'db_password', None),
                'table_prefix'     : getattr(self, 'table_prefix', None),
                'debug'            : getattr(self, 'debug', None),
                'disallow_edit'    : getattr(self, 'disallow_edit', None),
                'fs_method'        : getattr(self, 'fs_method', None),
                'auth_key'         : getattr(self, 'auth_key', None),
                'secure_auth_key'  : getattr(self, 'secure_auth_key', None),
                'logged_in_key'    : getattr(self, 'logged_in_key', None),
                'nonce_key'        : getattr(self, 'nonce_key', None),
                'auth_salt'        : getattr(self, 'auth_salt', None),
                'secure_auth_salt' : getattr(self, 'secure_auth_salt', None),
                'logged_in_salt'   : getattr(self, 'logged_in_salt', None),
                'nonce_salt'       : getattr(self, 'nonce_salt', None)}

    def verify(self, repair=False, use_default_atts=False):
        """Verifies the attributes of WPConfig instance. Unless you pass in
           use_default_atts as True, this assumes the in-memory values are the
           correct values."""
        # pylint: disable=arguments-differ
        result = True  # Assume the best :)
        save = False

        if use_default_atts:
            correct_values = getattr(self, 'wp', None)
        else:
            correct_values = self.parse()  # Retrieve values in memory (and hold
                                           # for comparison and/or repair)

        self.read(True)  # Force reading values in from disk

        verify_items = {
            'db_name'       : '[!] WordPress database name is incorrectly set to: ',
            'db_host'       : '[!] Databse hostname is incorrectly set to: ',
            'db_user'       : '[!] WordPress database username is incorrectly set to: ',
            'db_password'   : '[!] WordPress database password is incorrectly set to: ',
            'table_prefix'  : '[!] WordPress table prefix is incorrectly set to: ',
            'debug'         : '[!] Debug is incorrectly set to: ',
            'disallow_edit' : '[!] DISALLOW_EDIT is incorrectly set to: ',
            'fs_method'     : '[!] FS_METHOD is incorrectly set to: ',
        }

        for attribute, error_message in verify_items.iteritems():
            correct_value = correct_values[attribute]
            current_value = getattr(self, attribute)
            if not current_value == correct_value:
                print(error_message + str(current_value))
                if repair:
                    print('Setting "' + attribute + '" to: "' + \
                        correct_value + '"...')
                    setattr(self, attribute, correct_value)
                    save = True
                else:
                    result = False

        if repair and save:
            if prompt('Create new salts?'):
                print('Creating new salts...')
                for key, value in WPSalt().secrets():
                    setattr(self, key, value)
            self.write(append=False)

        if self.debug == 'true':
            print('\n    -------------------------------------')
            print('    [WARN] WordPress Debug mode is on.')
            print('           Be sure to turn this off in')
            print('           a production environment!')
            print('    -------------------------------------\n')

        return result
