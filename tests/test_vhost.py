#!/usr/bin/env python
#
# name:             test_vhost.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# description:      Unit tests for ww module's Vhost methods.
#                   Most of Vhost's methods are difficult to unit test because
#                   they are tightly coupled to an apache system.
#

import pytest
from ww.ww import Vhost


def test_vhost_init():
    """TODO: Test vhost init method."""
    pass

def test_vhost_create():
    """TODO: Test vhost create method."""
    pass

# Monkey Patch function for read() method
def read():
    return """This is a sample vhost file.
DocumentRoot /the/root/dir
ErrorLog "/the/error/log"
CustomLog "/the/access/log"
"""

def test_vhost_setup_parse():
    """Test vhost parse method."""
    vhost = Vhost('domain.com', {'path' : '/tmp/path'})
    vhost.read = read
    assert vhost.htdocs == '/the/root/dir'
    assert vhost.access_log == '/the/access/log'
    assert vhost.error_log == '/the/error/log'

def test_vhost_get_parsed():
    """TODO: Test vhost get_parsed method."""
    pass

def test_vhost_verify():
    """TODO: Test vhost get_parsed method."""
    pass

def test_vhost_repair():
    """TODO: Test vhost get_parsed method."""
    pass
