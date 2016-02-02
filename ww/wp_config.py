#!/usr/bin/env python
#
# name:             wp_config.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#
# description:      A class to create WordPress wp_config.php files.
#

try:
    from ext_pylib.files import Parsable, Section, Template
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

from ww import settings as s
from ww_file import WWFile


SALT_REGEXES = {
    'auth_key'         : ("define\('AUTH_KEY',[ ]*'([^']*)'\);",
                            "define('AUTH_KEY', '{}');"),
    'secure_auth_key'  : ("define\('SECURE_AUTH_KEY',[ ]*'([^']*)'\);",
                            "define('SECURE_AUTH_KEY', '{}');"),
    'logged_in_key'    : ("define\('LOGGED_IN_KEY',[ ]*'([^']*)'\);",
                            "define('LOGGED_IN_KEY', '{}');"),
    'nonce_key'        : ("define\('NONCE_KEY',[ ]*'([^']*)'\);",
                            "define('NONCE_KEY', '{}');"),
    'auth_salt'        : ("define\('AUTH_SALT',[ ]*'([^']*)'\);",
                            "define('AUTH_SALT', '{}');"),
    'secure_auth_salt' : ("define\('SECURE_AUTH_SALT',[ ]*'([^']*)'\);",
                            "define('SECURE_AUTH_SALT', '{}');"),
    'logged_in_salt'   : ("define\('LOGGED_IN_SALT',[ ]*'([^']*)'\);",
                            "define('LOGGED_IN_SALT', '{}');"),
    'nonce_salt'       : ("define\('NONCE_SALT',[ ]*'([^']*)'\);",
                            "define('NONCE_SALT', '{}');"),
}

WP_CONF_REGEXES = dict(SALT_REGEXES, **{
    'debug'        : ("define\('WP_DEBUG', ([^ \n]*)\);",
                      "define('WP_DEBUG', {});"),
    'db_name'      : ("define\('DB_NAME', '([^ \n]*)'\);",
                      "define('DB_NAME', '{}');"),
    'db_user'      : ("define\('DB_USER', '(.*)'\);",
                      "define('DB_USER', '{}');"),
    'db_password'  : ("define\('DB_PASSWORD', '(.*)'\);",
                      "define('DB_PASSWORD', '{}');"),
    'db_host'      : ("define\('DB_HOST', '(.*)'\);",
                      "define('DB_HOST', '{}');"),
    'table_prefix' : ("\$table_prefix[ ]*=[ ]*['\"](.*)['\"];",
                      "$table_prefix = '{}';"),
    'disallow_edit': ("define\('DISALLOW_FILE_EDIT', (.*)\);",
                      "define('DISALLOW_FILE_EDIT', {});"),
    'fs_method'    : ("define\('FS_METHOD', '(.*)'\);",
                      "define('FS_METHOD', '{}');"),
})


class WPConfigTemplate(Template, WWFile): pass

class WPSalt(Section, Parsable):
    regexes = SALT_REGEXES

    def __init__(self):
        self.data = requests.get(s.WP_SALT_URL).text
        self.setup_parsing()

    def read(self):
        return self.data

    def secrets(self):
        """A generator that yields a tuple of key and salt value."""
        secrets = {}
        for key, regex in self.regexes.iteritems():
            yield (key, getattr(self, key))


# WPConfig()
#   A class that describes a WordPress wp_config.php file.
#   This is primarily a wrapper for wp_config managment.
#
#   methods:
#       create()
#       verify()
class WPConfig(Parsable, WWFile):
    regexes = WP_CONF_REGEXES

    def __init__(self, atts):
        self.setup_parsing()  # Do this first, before initializing attributes

        super(WPConfig, self).__init__(atts)
        if self.exists() and prompt('Parse existing wp_config.php?'):
            atts['wp'] = self.parse(True)
        else:  # Otherwise, apply the template
            self.template = WPConfigTemplate({'path' : s.WP_CONFIG_TEMPLATE}).read()
            self.data = self.template

        self.salt = WPSalt()
        for key, value in self.salt.secrets():
            setattr(self, key, value)

        if 'wp' in atts:
            for att, value in atts['wp'].iteritems():
                setattr(self, att, value)


    def parse(self, parse_from_disk=False):
        """Returns a dict of attributes.  This does not return the salts. They
           will be changed every time.  Passing in True as an arguement will
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

        else:
            self.read()  # At least make sure contents are already read into
                         # memory.

        return { 'debug'        : self.debug,
                 'table_prefix' : self.table_prefix,
                 'db_name'      : self.db_name,
                 'db_user'      : self.db_user,
                 'db_password'  : self.db_password,
                 'db_host'      : self.db_host,
                 'disallow_edit': self.disallow_edit,
                 'fs_method'    : self.fs_method, }

    def verify(self, repair=False):
        """This assumes the in-memory values are the correct values."""
        result = True  # Assume the best :)

        correct_values = self.parse()  # Retrieve values in memory (and hold
                                       # for comparison and/or repair)
        self.read(True)  # Read values in from disk

        if not self.debug == correct_values['debug']:
            print '[!] Debug is incorrectly set to: ' + self.debug
            if repair:
                print 'Setting debug to: ' + correct_values['debug']
                self.debug = correct_values['debug']
            else:
                result = False

        if not self.table_prefix == correct_values['table_prefix']:
            print '[!] WordPress table prefix is incorrectly set to: ' + self.table_prefix
            if repair:
                print 'Setting table prefix to: ' + correct_values['table_prefix']
                self.table_prefix = correct_values['table_prefix']
            else:
                result = False

        if not self.db_name == correct_values['db_name']:
            print '[!] WordPress database is incorrectly set to: ' + self.db_name
            if repair:
                print 'Setting database name to: ' + correct_values['db_name']
                self.db_name = correct_values['db_name']
            else:
                result = False

        if not self.db_user == correct_values['db_user']:
            print '[!] WordPress database username is incorrectly set to: ' + self.db_user
            if repair:
                print 'Setting database user to: ' + correct_values['db_user']
                self.db_user = correct_values['db_user']
            else:
                result = False

        if not self.db_password == correct_values['db_password']:
            print '[!] WordPress database password is incorrectly set to: ' + self.db_password
            if repair:
                print 'Setting database password to: ' + correct_values['db_password']
                self.db_password = correct_values['db_password']
            else:
                result = False

        if not self.db_host == correct_values['db_host']:
            print '[!] Databse hostname is incorrectly set to: ' + self.db_host
            if repair:
                print 'Setting database host to: ' + correct_values['db_host']
                self.db_host = correct_values['db_host']
            else:
                result = False

        if not self.disallow_edit == correct_values['disallow_edit']:
            print '[!] DISALLOW_EDIT is incorrectly set to: ' + self.disallow_edit
            if repair:
                print 'Setting disallow_edit to: ' + correct_values['disallow_edit']
                self.disallow_edit = correct_values['disallow_edit']
            else:
                result = False

        if not self.fs_method == correct_values['fs_method']:
            print '[!] FS_METHOD is incorrectly set to: ' + self.fs_method
            if repair:
                print 'Setting fs_method to: ' + correct_values['fs_method']
                self.fs_method = correct_values['fs_method']
            else:
                result = False

        if self.debug == 'true':
            print '-------------------------------------'
            print '[WARN] WordPress Debug mode is on.'
            print '       Be sure to turn this off in'
            print '       a production environement!'
            print '-------------------------------------'

        return result
