#!/usr/bin/env python
#
# name:             test_wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's WP_Website class and methods.
#

from ww import WP_Website
import pytest


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_wp_website_initialize(atts, expected):
    """Test initialize WP_Website."""
    #wp_website = WP_Website(atts)
    #assert str(wp_website) == expected
    pass

def test_wp_website_verify():
    """TODO:"""
    pass
