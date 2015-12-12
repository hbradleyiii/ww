#!/usr/bin/env python
#
# name:             test_vhost.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      A unit test for ww module's Vhost class and methods.
#

from ww import Vhost
import pytest


init_args = [
    ({ 'htdocs' : None, 'assets' : None, 'logs' : None, 'vhost_conf' : None, 'htaccess' : None, }, None),
]
@pytest.mark.parametrize(("atts", "expected"), init_args)
def test_vhost_create(atts, expected):
    """Test initialize Vhost."""
    #vhost = Vhost(atts)
    #assert str(vhost) == expected
    pass

def test_vhost_remove():
    """TODO:"""
    pass

def test_vhost_verify():
    """TODO:"""
    pass

def test_vhost_parse():
    """TODO:"""
    pass
