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
    from ext_pylib.files import File, Parsable, Section, Template
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

from ww import settings as s


SALT_REGEXES = {
    'auth_key'         : ("define\('AUTH_KEY',[ ]*'([^']*)'\);",
                            "define\('AUTH_KEY',[ ]*'{}'\);"),
    'secure_auth_key'  : ("define\('SECURE_AUTH_KEY',[ ]*'([^']*)'\);",
                            "define\('SECURE_AUTH_KEY',[ ]*'{}'\);"),
    'logged_in_key'    : ("define\('LOGGED_IN_KEY',[ ]*'([^']*)'\);",
                            "define\('LOGGED_IN_KEY',[ ]*'{}'\);"),
    'nonce_key'        : ("define\('NONCE_KEY',[ ]*'([^']*)'\);",
                            "define\('NONCE_KEY',[ ]*'{}'\);"),
    'auth_salt'        : ("define\('AUTH_SALT',[ ]*'([^']*)'\);",
                            "define\('AUTH_SALT',[ ]*'{}'\);"),
    'secure_auth_salt' : ("define\('SECURE_AUTH_SALT',[ ]*'([^']*)'\);",
                            "define\('SECURE_AUTH_SALT',[ ]*'{}'\);"),
    'logged_in_salt'   : ("define\('LOGGED_IN_SALT',[ ]*'([^']*)'\);",
                            "define\('LOGGED_IN_SALT',[ ]*'{}'\);"),
    'nonce_salt'       : ("define\('NONCE_SALT',[ ]*'([^']*)'\);",
                            "define\('NONCE_SALT',[ ]*'{}'\);"),
}

WP_CONF_REGEXES = dict(SALT_REGEXES, **{
    'debug'        : ("define\('WP_DEBUG', (.*)\);",
                      "define\('WP_DEBUG', {}\);"),
    'db_name'      : ("define\('DB_NAME', '(.*)'\);",
                      "define\('DB_NAME', '{}'\);"),
    'db_user'      : ("define\('DB_USER', '(.*)'\);",
                      "define\('DB_USER', '{}'\);"),
    'db_password'  : ("define\('DB_PASSWORD', '(.*)'\);",
                      "define\('DB_PASSWORD', '{}'\);"),
    'db_hostname'  : ("define\('DB_HOSTNAME', '(.*)'\);",
                      "define\('DB_HOSTNAME', '{}'\);"),
    'table_prefix' : ("$table_prefix[ ]*=[ ]*['\"](.*)['\"];",
                      "$table_prefix = '{}';"),
})


class WPConfigTemplate(Template, File): pass

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
class WPConfig(Parsable, File):
    regexes = WP_CONF_REGEXES

    def __init__(self, atts):
        self.setup_parsing()  # Do this FIRST, before initializing attributes
        super(WPConfig, self).__init__(atts)
        if self.exists() and prompt('Parse existing wp_config.php?'):
            atts = self.parse()
        else:  # Otherwise, apply the template
            self.template = WPConfigTemplate({'path' : s.WP_CONFIG_TEMPLATE}).read()
            self.data = self.template

        self.salt = WPSalt()
        for key, value in self.salt.secrets():
            setattr(self, key, value)

        self.table_prefix = atts['wp']['table_prefix']
        self.debug = atts['wp']['debug']
        self.db_name = atts['wp']['db_name']
        self.db_user = atts['wp']['db_user']
        self.db_password = atts['wp']['db_password']
        self.db_hostname = atts['wp']['db_hostname']

    def parse(self):
        """This does not return the salts. They will be changed every time."""
        if self.debug == []:
            print 'Could not parse debug mode.'
            if prompt('Turn debug mode on?'):
                self.debug = 'true'
            else:
                self.debug = 'false'
        else:
            self.debug = self.debug[0]

        if self.table_prefix == []:
            print 'Could not parse WordPress database table_prefix.'
            self.table_prefix = prompt_str('What is the WordPress database table_prefix?')
        else:
            self.table_prefix = self.table_prefix[0]

        if self.db_name == []:
            print 'Could not parse WordPress database name.'
            self.db_name = prompt_str('What is the WordPress database name?')
        else:
            self.db_name = self.db_name[0]

        if self.db_user == []:
            print 'Could not parse WordPress database user.'
            self.db_user = prompt_str('What is the WordPress database user?')
        else:
            self.db_user = self.db_user[0]

        if self.db_password == []:
            print 'Could not parse WordPress database password.'
            self.db_password = prompt_str('What is the WordPress database password?')
        else:
            self.db_password = self.db_password[0]

        if self.db_hostname == []:
            print 'Could not parse WordPress database hostname.'
            self.db_hostname = prompt_str('What is the WordPress database hostname?')
        else:
            self.db_hostname = self.db_hostname[0]

        return { 'debug'        : self.htdocs,
                 'table_prefix' : self.db_name,
                 'db_name'      : self.db_name,
                 'db_user'      : self.db_user,
                 'db_password'  : self.db_password,
                 'db_hostname'  : self.db_hostname, }

    def verify(self):
        # [WARN] debug is set True ... etc.
        pass
