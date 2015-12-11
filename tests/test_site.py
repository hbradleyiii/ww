#!/usr/bin/env python
#
# name:             test_site.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's Site class and methods.
#

from ww import Site
import pytest


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_site_initialization(atts, expected):
    """Test initialize Site."""
    #site = Site(atts)
    #assert str(site) == expected
    pass

def test_site_install():
    """TODO:"""
    pass

def test_site_unintstall():
    """TODO:"""
    pass

def test_site_verify():
    """TODO:"""
    pass

def test_site_repair():
    """TODO:"""
    pass

def test_site_pack():
    """TODO:"""
    pass

def test_site_unpack():
    """TODO:"""
    pass

def test_site_migrate():
    """TODO:"""
    pass

def test_site_isinstalled():
    """TODO:"""
    pass
