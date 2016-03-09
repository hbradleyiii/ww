#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#

"""
Integration and unit tests for ww module's Website class and methods.
"""

from __future__ import absolute_import, print_function

import pytest
from ww import Website
from ww.website import merge_atts, localhost


def test_localhost_decorator():
    pass

MERGE_ATTS_ARGS = [
    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/new/path'}},
     {'htdocs' : {'path' : '/new/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    (None,
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     None,
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),
]
@pytest.mark.parametrize(("atts", "new_atts", "expected"), MERGE_ATTS_ARGS)
def test_merge_atts(atts, new_atts, expected):
    """Tests merge_atts function."""
    assert merge_atts(atts, new_atts) == expected

INIT_ARGS = [
    ({'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None,}, None),
]
@pytest.mark.parametrize(("atts", "expected"), INIT_ARGS)
def test_website_initialization(atts, expected):
    """Test initialize Website."""
    #website = Website(atts)
    #assert str(website) == expected
    pass

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
