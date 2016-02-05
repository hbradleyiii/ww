#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016
#
# description:      Unit tests for ww module's Htaccess class.
#

import pytest
from ww.ww import Htaccess

HTACCESS_DATA = """This is a sample htaccess file.
DocumentRoot /the/root/dir
ErrorLog "/the/error/log"
CustomLog "/the/access/log"
"""

def txest_htaccess_init():
    """TODO: Test htaccess init method."""
    htaccess = Htaccess('domain.com', {'path' : '/tmp/path'})
    htaccess.data = HTACCESS_DATA
    # assert htaccess.htdocs == '/the/root/dir'
    # assert htaccess.access_log == '/the/access/log'
    # assert htaccess.error_log == '/the/error/log'

def test_vhost_verify():
    """TODO: Test vhost get_parsed method."""
    pass
