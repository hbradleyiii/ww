#!/usr/bin/env python
#
# name:             test_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's Website class and methods.
#

import pytest
from ww import Website
from ww.ww.website import merge_atts


merge_atts_args = [
    ({ 'htdocs' : { 'path' : '/default/path', 'perms' : 0700 }, 'other' : 'default_value' },
     { 'htdocs' : { 'path' : '/new/path' } },
     { 'htdocs' : { 'path' : '/new/path', 'perms' : 0700 }, 'other' : 'default_value' }),
    ({ 'htdocs' : { 'path' : '/default/path', 'perms' : 0700 }, 'other' : 'default_value' },
     { },
     { 'htdocs' : { 'path' : '/default/path', 'perms' : 0700 }, 'other' : 'default_value' }),
    ({ },
     { 'htdocs' : { 'path' : '/default/path', 'perms' : 0700 }, 'other' : 'default_value' },
     { 'htdocs' : { 'path' : '/default/path', 'perms' : 0700 }, 'other' : 'default_value' }),
]
@pytest.mark.parametrize(("atts", "new_atts", "expected"), merge_atts_args)
def test_merge_atts(atts, new_atts, expected):
    """Tests merge_atts function."""
    assert merge_atts(atts, new_atts) == expected

init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_website_initialization(atts, expected):
    """Test initialize Website."""
    #website = Website(atts)
    #assert str(website) == expected
    pass

# repr_args = [
#     ('domain.com',
#         {},
#         "Website('domain.com', {'htdocs' : {'perms': 509, 'path': '/var/www/domain.com/htdocs/', 'group': 'www-data', 'owner': 'www-data'}, 'assets' : {'perms': 509, 'path': '/var/www/domain.com/assets/', 'group': 'mm_admin', 'owner': 'root'}, 'logs' : {'perms': 509, 'path': '/var/www/domain.com/logs/', 'group': 'mm_admin', 'owner': 'root'}, 'htaccess' : {'perms': 436, 'path': '/var/www/domain.com/htdocs/.htaccess', 'group': 'www-data', 'owner': 'www-data'}, 'vhost_conf' : {'perms': 420, 'path': '/etc/apache2/sites-available/domain.com.conf', 'group': 'root', 'owner': 'root'}})"),
#     ('domain.com',
#         {'htdocs' : {'path' : '/the/new/path/'}, 'logs' : {'path' : '/the/logs/', 'perms' : 0700 } },
#     "Website('domain.com', {'htdocs' : {'perms': None, 'path': '/the/new/path/', 'group': None, 'owner': None}, 'assets' : {'perms': 509, 'path': '/var/www/domain.com/assets/', 'group': 'mm_admin', 'owner': 'root'}, 'logs' : {'perms': 448, 'path': '/the/logs/', 'group': None, 'owner': None}, 'htaccess' : {'perms': 436, 'path': '/the/new/path/.htaccess', 'group': 'www-data', 'owner': 'www-data'}, 'vhost_conf' : {'perms': 420, 'path': '/etc/apache2/sites-available/domain.com.conf', 'group': 'root', 'owner': 'root'}})"),
# ]
# @pytest.mark.parametrize(("domain", "atts", "expected"), repr_args)
# def test_website_repr(domain, atts, expected):
#     """Test Website repr."""
#     website = Website(domain, atts)
#     assert website.__repr__() == expected

def test_website_install():
    """TODO:"""
    pass

def test_website_remove():
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
