#!/usr/bin/env python
# name:             test_wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's WPWebsite class and methods.
#

import pytest
from ww import WPWebsite


INIT_ARGS = [
    ({'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None,}, None),
]
@pytest.mark.parametrize(("atts", "expected"), INIT_ARGS)
def test_wp_website_initialize(atts, expected):
    """Test initialize WPWebsite."""
    #wp_website = WPWebsite(atts)
    #assert str(wp_website) == expected

def test_wp_website_verify():
    """TODO:"""
    pass

def test_wp_website_install_verify_remove():
    """TODO:"""
    pass

def test_wp_website_pack_remove_unpack_verify_remove():
    """TODO:"""
    pass
