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
    from ext_pylib.files import File, Template
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('Python module ext_pylib must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('Python module requests must be installed to run ww')

from ww import settings as s


class WPConfigTemplate(Template, File): pass

class WPSalt(Section, Parsable):

    def __init__(self):
        self.regexes = {
            'auth_key'         : "define('AUTH_KEY',[ ]*'([^']*)'\);",
            'secure_auth_key'  : "define('SECURE_AUTH_KEY',[ ]*'([^']*)'\);",
            'logged_in_key'    : "define('LOGGED_IN_KEY',[ ]*'([^']*)'\);",
            'nonce_key'        : "define('NONCE_KEY',[ ]*'([^']*)'\);",
            'auth_salt'        : "define('AUTH_SALT',[ ]*'([^']*)'\);",
            'secure_auth_salt' : "define('SECURE_AUTH_SALT',[ ]*'([^']*)'\);",
            'logged_in_salt'   : "define('LOGGED_IN_SALT',[ ]*'([^']*)'\);",
            'nonce_salt'       : "define('NONCE_SALT',[ ]*'([^']*)'\);",
        }
        self.setup_parsing()

    def read(self):
        try:
            self.data
        except AttributeError:
            self.data = requests.get(s.WP_SALT_URL).text
        return self.data

    def get_secrets(self):
        secrets = {}
        for key, regex in self.regexes.iteritems():
            secrets[key] = getattr(self, key)
        return secrets

# define:('WP_DEBUG'
# self.wp_debug
# database name
# mysql domain
# username
# password
# charset
# table_prefix


# WPConfig()
#   A class that describes a WordPress wp_config.php file.
#   This is primarily a wrapper for wp_config managment.
#
#   methods:
#       create()
#       verify()
class WPConfig(Parsable, File):
    def __init__(self):
        pass

    def create(self, data):
        # take the data and set it up
        pass

    def verify(self):
        # [WARN] debug is set True ... etc.
        pass
