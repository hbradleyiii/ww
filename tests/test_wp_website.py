#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# pylint:           disable=no-member,invalid-name,unused-argument

"""
A unit test for ww module's WPWebsite class and methods.
"""

from __future__ import absolute_import

from mock import patch

from ww import WPConfig, WPWebsite
from ww import settings as s


_INPUT = 'ext_pylib.input.prompts.INPUT'

TEST_DOMAIN = 'wordpress.example.com'
TEST_ATTS = {
    'root' : {
        'path'  : '/www/example.com/',
        'perms' : 0775,
        'owner' : 'www-data',
        'group' : 'www-data',
    },
    'htdocs' : {'path' : '/www/htdocs/', },
    'log' : {'path' : '/www/log/', },
    'access_log' : {'path' : '/www/log/access_log', },
    'vhost' : {'path' : '/etc/apache2/the_example.com.conf', },
    'htaccess' : {
        'path' : '/www/htdocs/.htaccess',
        'sections' : [{'identifier' : 'h5g', 'path' : s.HTA_5G_TEMPLATE}, ]
    },
}

CUSTOM_ATTS = {
    'wp' : {
        'db_name'      : 'database',
        'db_user'      : 'user',
        'db_password'  : 'password',
        'table_prefix' : 'prefix_',
        'debug'        : 'true',
        'disallow_edit': 'false',
    },
}

def test_wp_website_default_initialize():
    """Test initialize WPWebsite."""
    website = WPWebsite(TEST_DOMAIN, TEST_ATTS)
    assert website.domain == 'wordpress.example.com'
    assert website.config.path == '/www/htdocs/wp-config.php'
    assert website.config.perms == 0440
    assert website.config.db_name == 'wp_wordpress_example_com'
    assert website.config.db_user == 'usr_wordpr'

def test_wp_website_initialize_custom_atts():
    """Test initialize WPWebsite with custom atts."""
    website = WPWebsite(TEST_DOMAIN, CUSTOM_ATTS)
    assert website.config.db_name == 'database'
    assert website.config.db_user == 'user'
    assert website.config.db_password == 'password'
    assert website.config.table_prefix == 'prefix_'
    assert website.config.debug == 'true'
    assert website.config.disallow_edit == 'false'

@patch('ww.WPConfig.exists', return_value=True)
def test_wp_website_initialize_existing_config(*args):
    """Test initialize WPWebsite with existing config (will use defaults
    answering [y] to parse() questions)."""
    def read(self, *args):
        """Mock read function"""
        return self.data
    WPConfig.read = read  # Monkey patch 'read' method
    WPConfig.data = '_'

    with patch(_INPUT, return_value='y'):
        website = WPWebsite(TEST_DOMAIN, TEST_ATTS)
    assert website.domain == 'wordpress.example.com'
    assert website.config.path == '/www/htdocs/wp-config.php'
    assert website.config.perms == 0440

    # Input given was 'y' any time it was needed
    assert website.config.db_name == 'y'
    assert website.config.db_user == 'y'
    assert website.config.db_password == 'y'
    assert website.config.db_host == 'y'
    assert website.config.table_prefix == 'y'

    website.config.table_prefix = 'database'
    assert website.config.table_prefix == 'database'
    website.config.db_host = 'hostname'
    assert website.config.db_host == 'hostname'

def test_wp_website_install_verify_remove():
    """TODO:"""
    pass

def test_wp_website_pack_remove_unpack_verify_remove():
    """TODO:"""
    pass
