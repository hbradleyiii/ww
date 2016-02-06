#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             settings.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#
# description:      The settings file for ww
#

import os
import time


TEMPLATE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/../templates/'


## Change these settings to your hearts content ##

# Site Settings
SITE_ADMIN_EMAIL = 'email@mail.com'
SITE_ERROR_LOG = 'error.log'
SITE_ACCESS_LOG = 'access.log'

WWW_DIR = '/var/www/'
WWW_USR = 'www-data'
WWW_ADMIN = 'admin_usr'

GITIGNORE_TEMPLATE = TEMPLATE_PATH + 'gitignore.template'

HTA_5G_TEMPLATE = TEMPLATE_PATH + '5g-htaccess.template'

VHOST_PATH = '/etc/apache2/sites-available/'
VHOST_TEMPLATE = TEMPLATE_PATH + 'vhost.template'
VHOST_SSL_TEMPLATE = TEMPLATE_PATH + 'vhost-ssl.template'

MYSQL = {
    'host'     : 'localhost',
    'user'     : 'username',
    'password' : 'password123',
}

# WordPress Settings
WP_LATEST      = 'http://wordpress.org/latest.tar.gz'
WP_SETUP_URL   = '/wp-admin/setup-config.php?step=2'
WP_INSTALL_URL = '/wp-admin/install.php?step=2'

WP_HTA_TEMPLATE = TEMPLATE_PATH + 'wordpress-htaccess.template'
WP_HTA_HARDENED_TEMPLATE = TEMPLATE_PATH + 'hardened-wordpress-htaccess.template'
WP_CONFIG_TEMPLATE = TEMPLATE_PATH + 'wp-config.php.template'

WP_ADMIN_USER  = 'admin'
WP_ADMIN_EMAIL = 'admin@wp.com'
WP_ADMIN_PW    = 'password123' # Please change this.

WP_SALT_URL = 'https://api.wordpress.org/secret-key/1.1/salt/'

# Apache commands
CMD_RESTART_APACHE = 'sudo service apache2 restart'
CMD_ENABLE_CONFIG  = 'sudo a2ensite '  # run as: {command} domain
CMD_DISABLE_CONFIG = 'sudo a2dissite ' # run as: {command} domain


# Try to import local settings. This is a temporary work-around for now.
try:
    from .settings_local import *
except ImportError:
    print "Can't find settings_local. Using default settings."
