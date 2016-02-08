#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_ww_file.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016

"""
Unit tests for ww module's WWFile abstract class.
"""

from mock import patch
from ww import WWFile


@patch('ext_pylib.files.node.Node.verify', return_value=True)
def test_ww_file_repair(mock_verify):
    """Test WWFile repair method."""
    assert WWFile().repair()
    mock_verify.assert_called_once_with(True)
