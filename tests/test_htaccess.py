#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016
#
# pylint:           disable = no-member,invalid-name,unused-argument

"""
Unit tests for ww.htaccess module's Htaccess class.
"""

from mock import patch

from ww import Htaccess
from ww import settings as s
from ww.htaccess import HtaccessSection


_INPUT = 'ext_pylib.input.prompts.INPUT'

HTACCESS_SECTION = """# BEGIN Test Section
This is a test htaccess section
# END Test Section
"""

HTACCESS_DATA = """This is a sample htaccess file.
# BEGIN Test Section
This is a test htaccess section
# END Test Section
It has the section.
"""

HTACCESS_DATA_NO_SECTION = """This is a sample htaccess file.
It does not have the section.
"""

HTACCESS_DATA_CHANGED = """This is a sample htaccess file.
# BEGIN Test Section
Outdated or changed
# END Test Section
It has the section, but it is changed.
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

def read():
    """A mock read function."""
    return HTACCESS_SECTION

TEST_SECTION = HtaccessSection({'name' : 'test_section'})
TEST_SECTION.read = read

@patch('ext_pylib.files.node.Node.verify', return_value=True)
def test_vhost_verify_is_in(*args):
    """Tests htaccess verify method."""
    htaccess = Htaccess(DEFAULT_ATTS)
    htaccess.data = HTACCESS_DATA
    htaccess.sections = [TEST_SECTION]
    assert htaccess.verify()

@patch('ext_pylib.files.File.write', return_value=True)
@patch('ext_pylib.files.node.Node.verify', return_value=True)
def test_vhost_verify_without_section(*args):
    """Tests htaccess verify method."""
    htaccess = Htaccess(DEFAULT_ATTS)
    htaccess.data = HTACCESS_DATA_NO_SECTION
    htaccess.sections = [TEST_SECTION]
    assert not htaccess.verify()
    assert htaccess.verify(True)  # Correct it.

@patch('ext_pylib.files.File.write', return_value=True)
@patch('ext_pylib.files.node.Node.verify', return_value=True)
def test_vhost_verify_with_altered_section(*args):
    """Tests htaccess verify method."""
    htaccess = Htaccess(DEFAULT_ATTS)
    htaccess.data = HTACCESS_DATA_CHANGED
    htaccess.sections = [TEST_SECTION]
    assert htaccess.verify()
    with patch(_INPUT, return_value='n'):
        assert htaccess.verify(True)
        assert htaccess.data == HTACCESS_DATA_CHANGED
    with patch(_INPUT, return_value='y'):
        assert htaccess.verify(True)
        assert htaccess.data != HTACCESS_DATA_CHANGED
        assert htaccess.sections[0].is_in(htaccess.data)
