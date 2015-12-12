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
