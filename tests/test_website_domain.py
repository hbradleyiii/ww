#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_website_domain.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015

"""
A unit test for ww.website_domain's create_domain factory function.
"""

from mock import patch

from ww.website_domain import create_domain, WebsiteDomain


_INPUT = 'ext_pylib.input.prompts.INPUT'

def test_create_domain():
    """Tests WebsiteDomain factory function."""
    domain = WebsiteDomain('example.com')
    assert domain == create_domain('example.com')

def test_create_domain_by_prompt():
    """Tests WebsiteDomain factory function using prompt."""
    domain = WebsiteDomain('example.com')
    assert domain == create_domain('example.com')

    with patch(_INPUT, return_value='example.com'):
        assert domain == create_domain()
