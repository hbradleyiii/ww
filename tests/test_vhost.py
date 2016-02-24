#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_vhost.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# pylint:           disable=no-member

"""
Unit tests for ww module's Vhost methods. Most of Vhost's methods are
difficult to unit test because they are tightly coupled to an apache system.
"""

from mock import patch

from ww import Vhost
from ww.vhost import run_command


_INPUT = 'ext_pylib.input.prompts.INPUT'

VHOST_DATA = """This is a sample vhost file.
DocumentRoot /the/root/dir
ErrorLog "/the/error/log"
CustomLog "/the/access/log"
"""

DEFAULT_ARGS = {'path' : '/tmp/path', 'domain' : 'example.com'}

@patch('subprocess.call', return_value=0)
def test_run_command(mock_call):
    """Tests run_command function."""
    assert run_command('the command')
    mock_call.assert_called_once_with('the command', shell=True)

@patch('subprocess.call', return_value=1)
def test_run_command_failed(mock_call):
    """Tests run_command function."""
    assert not run_command('the command')
    mock_call.assert_called_once_with('the command', shell=True)

def test_vhost_init():
    """Tests vhost init method."""
    vhost = Vhost(DEFAULT_ARGS)
    vhost.data = VHOST_DATA
    assert vhost.domain == 'example.com'
    assert vhost.htdocs == '/the/root/dir'
    assert vhost.access_log == '/the/access/log'
    assert vhost.error_log == '/the/error/log'

@patch('ext_pylib.files.File.create')
@patch('ww.vhost.Vhost.enable')
def test_vhost_create(mock_enable, mock_create):
    """Tests vhost create method."""
    vhost = Vhost(DEFAULT_ARGS)
    vhost.template.data = """#WEBSITE#
#HTDOCS#
#EMAIL#
#ACCESS_LOG#"""
    expected_data = """example.com
/the/docs/
email@example.com
/the/logs"""
    vhost.placeholders = {
        '#WEBSITE#'    : 'example.com',
        '#HTDOCS#'     : '/the/docs/',
        '#EMAIL#'      : 'email@example.com',
        '#ACCESS_LOG#' : '/the/logs',
    }
    vhost.create()
    assert vhost.read() == expected_data
    mock_create.assert_called_once_with()
    mock_enable.assert_called_once_with()

def test_vhost_parse():
    """Tests vhost parse method."""
    vhost = Vhost(DEFAULT_ARGS)
    vhost.data = VHOST_DATA
    assert vhost.parse() == {'htdocs'     : {'path' : '/the/root/dir'},
                             'access_log' : {'path' : '/the/access/log'},
                             'error_log'  : {'path' : '/the/error/log'},
                             'log'        : {'path' : '/the/access'}}

def test_vhost_parse_with_prompts():
    """Tests vhost parse method with prompts."""
    vhost = Vhost(DEFAULT_ARGS)
    vhost.data = ''
    with patch(_INPUT, return_value='/a/sample/dir'):
        assert vhost.parse() == {'htdocs'     : {'path' : '/a/sample/dir'},
                                 'access_log' : {'path' : '/a/sample/dir'},
                                 'error_log'  : {'path' : '/a/sample/dir'},
                                 'log'        : {'path' : '/a/sample'}}
    assert vhost.htdocs == '/a/sample/dir'
    assert vhost.access_log == '/a/sample/dir'
    assert vhost.error_log == '/a/sample/dir'

@patch('ext_pylib.files.File.verify', return_value=True)
@patch('ww.vhost.Vhost.is_enabled', return_value=True)
def test_vhost_verify(mock_enabled, mock_file_verify):
    """Tests vhost verify method."""
    vhost = Vhost(DEFAULT_ARGS)
    assert vhost.verify()
    mock_enabled.return_value = False
    assert not vhost.verify()
    mock_enabled.return_value = True
    mock_file_verify.return_value = False
    assert not vhost.verify()

@patch('ww.vhost.run_command', return_value=True)
def test_vhost_enable(_):
    """Test vhost enable method."""
    vhost = Vhost(DEFAULT_ARGS)
    assert vhost.enable(False)

@patch('ww.vhost.run_command', return_value=True)
def test_vhost_disable(_):
    """Tests vhost disble method."""
    vhost = Vhost(DEFAULT_ARGS)
    assert vhost.disable(False)
