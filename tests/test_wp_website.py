#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_wp_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's WPWebsite class and methods.
#

import pytest
from ww import WPWebsite


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_wp_website_initialize(atts, expected):
    """Test initialize WPWebsite."""
    #wp_website = WPWebsite(atts)
    #assert str(wp_website) == expected
    pass

def test_wp_website_verify():
    """TODO:"""
    pass
