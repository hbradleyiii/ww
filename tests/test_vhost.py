#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
from ww import Vhost

VHOST_DATA = """This is a sample vhost file.
DocumentRoot /the/root/dir
ErrorLog "/the/error/log"
CustomLog "/the/access/log"
"""

def test_vhost_init():
    """TODO: Test vhost init method."""
    vhost = Vhost('domain.com', {'path' : '/tmp/path'})
    vhost.data = VHOST_DATA
    assert vhost.htdocs == '/the/root/dir'
    assert vhost.access_log == '/the/access/log'
    assert vhost.error_log == '/the/error/log'

def test_vhost_create():
    """TODO: Test vhost create method."""
    pass

def test_vhost_parse():
    """Test vhost parse method."""
    pass

def test_vhost_verify():
    """TODO: Test vhost get_parsed method."""
    pass

def test_vhost_repair():
    """TODO: Test vhost get_parsed method."""
    pass
