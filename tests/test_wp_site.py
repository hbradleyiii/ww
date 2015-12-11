#!/usr/bin/env python
#
# name:             test_wp_site.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's WP_Site class and methods.
#

from ww import WP_Site
import pytest


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_wp_site_initialize(atts, expected):
    """Test initialize WP_Site."""
    #wp_site = WP_Site(atts)
    #assert str(wp_site) == expected
    pass

def test_wp_site_verify():
    """TODO:"""
    pass
