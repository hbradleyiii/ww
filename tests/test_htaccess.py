#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016

"""
Unit tests for ww module's Htaccess class.
"""
# pylint: disable = no-member

from mock import patch
import pytest

from ww import Htaccess
from ww import settings as s
from ww.htaccess import HtaccessSection


_INPUT = 'ext_pylib.input.prompts.INPUT'

HTACCESS_DATA = """This is a sample htaccess file.
DocumentRoot /the/root/dir
ErrorLog "/the/error/log"
CustomLog "/the/access/log"
"""

DEFAULT_ATTS = {
    'path'  : '/the/htaccess/path',
    'sections' : [{'name' : 'h5g', 'path' : s.HTA_5G_TEMPLATE}]
}

def test_htaccess_section_name():
    """Tests htaccess section name."""
    section = HtaccessSection({'name' : 'h5g', 'path' : s.HTA_5G_TEMPLATE})
    assert section.name == 'h5g'
    assert str(section) == 'h5g'

def test_htaccess_init():
    """Tests htaccess init method."""
    htaccess = Htaccess(DEFAULT_ATTS)
    htaccess.data = HTACCESS_DATA
    assert htaccess.path == '/the/htaccess/path'
    with patch(_INPUT, return_value='y'):
        pass

@patch('ext_pylib.files.node.Node.verify', return_value=True)
def test_vhost_verify(_):
    """Tests htaccess verify method."""
    pass
