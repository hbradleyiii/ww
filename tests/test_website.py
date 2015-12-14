#!/usr/bin/env python
#
# name:             test_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's Website class and methods.
#

from ww import Website
import pytest


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_website_initialization(atts, expected):
    """Test initialize Website."""
    #website = Website(atts)
    #assert str(website) == expected
    pass

repr_args = [
    ('domain.com',
        {},
        "Website('domain.com', {'htdocs' : {'path' : '/var/www/domain.com/htdocs/', 'perms' : 0775, 'owner' : 'www-data', 'group' : 'www-data'}, 'assets' : {'path' : '/var/www/domain.com/assets/', 'perms' : 0775, 'owner' : 'root', 'group' : 'mm_admin'}, 'logs' : {'path' : '/var/www/domain.com/logs/', 'perms' : 0775, 'owner' : 'root', 'group' : 'mm_admin'}, 'htaccess' : {'path' : '/var/www/domain.com/htdocs/.htaccess', 'perms' : 0664, 'owner' : 'www-data', 'group' : 'www-data'}, 'vhost_conf' : {'path' : '/etc/apache2/sites-available/domain.com.conf', 'perms' : 0644, 'owner' : 'root', 'group' : 'root'}})"),
    ('domain.com',
        {'htdocs' : {'path' : '/the/new/path/'}, 'logs' : {'path' : '/the/logs/', 'perms' : 0700 } },
        "Website('domain.com', {'htdocs' : {'path' : '/the/new/path/', 'perms' : None, 'owner' : None, 'group' : None}, 'assets' : {'path' : '/var/www/domain.com/assets/', 'perms' : 0775, 'owner' : 'root', 'group' : 'mm_admin'}, 'logs' : {'path' : '/the/logs/', 'perms' : 0700, 'owner' : None, 'group' : None}, 'htaccess' : {'path' : '/the/new/path/.htaccess', 'perms' : 0664, 'owner' : 'www-data', 'group' : 'www-data'}, 'vhost_conf' : {'path' : '/etc/apache2/sites-available/domain.com.conf', 'perms' : 0644, 'owner' : 'root', 'group' : 'root'}})"),
]
@pytest.mark.parametrize(("domain", "atts", "expected"), repr_args)
def test_website_repr(domain, atts, expected):
    """Test Website repr."""
    website = Website(domain, atts)
    assert website.__repr__() == expected

def test_website_install():
    """TODO:"""
    pass

def test_website_unintstall():
    """TODO:"""
    pass

def test_website_verify():
    """TODO:"""
    pass

def test_website_repair():
    """TODO:"""
    pass

def test_website_pack():
    """TODO:"""
    pass

def test_website_unpack():
    """TODO:"""
    pass

def test_website_migrate():
    """TODO:"""
    pass

def test_website_isinstalled():
    """TODO:"""
    pass
