#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_website.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       12/11/2015
#
# pylint:           disable=invalid-name,unused-argument

"""
Integration and unit tests for ww module's Website class and methods.
"""

from __future__ import absolute_import, print_function

import os
from mock import patch
import pytest
from ext_pylib.files import File

from ww import Website, WebsiteDomain
from ww import settings as s
from ww.website import merge_atts, localhost


def test_superuser():
    """Tests to ensure tests are run as superuser."""
    if os.getuid() != 0:
        assert False, "You must be a superuser to run these tests."

_INPUT = 'ext_pylib.input.prompts.INPUT'

TEST_DOMAIN = 'example.com'
TEST_ATTS = {
    'root' : {
        'path'  : '/www/example.com/',
        'perms' : 0775,
        'owner' : 'www-data',
        'group' : 'www-data',
    },
    'htdocs' : {'path' : '/www/htdocs/', },
    'log' : {'path' : '/www/log/', },
    'access_log' : {'path' : '/www/log/access_log', },
    'vhost' : {'path' : '/etc/apache2/the_example.com.conf', },
    'htaccess' : {
        'path' : '/www/htdocs/.htaccess',
        'sections' : [{'identifier' : 'h5g', 'path' : s.HTA_5G_TEMPLATE}, ]
    },
}

def test_localhost_decorator():
    """Integration test for localhost() decorator.

    This sets up a domain that does not point to this server.
    Then it wraps a function with the localhost decorator that tests if the
    domain points to this server. At this point it should. After the function
    is called, however, the domain should again no longer point to this server.
    """
    test_domain = WebsiteDomain(TEST_DOMAIN)

    print('test_domain should not point to this server to begin with.')
    assert not test_domain.verify(), \
            "Make sure there is *not* a host entry for example.com before running the test!"

    @localhost
    def decorator_test(test_domain):
        """Function stub for testing localhost() decorator"""
        print('test_domain *should* point to this server inside the decorated function.')

        return test_domain.verify()

    assert decorator_test(test_domain)

    print('test_domain should *not* point to this server after the decorated function has run.')
    assert not test_domain.verify()

MERGE_ATTS_ARGS = [
    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/new/path'}},
     {'htdocs' : {'path' : '/new/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    (None,
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),

    ({'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'},
     None,
     {'htdocs' : {'path' : '/default/path', 'perms' : 0700}, 'other' : 'default_value'}),
]
@pytest.mark.parametrize(("atts", "new_atts", "expected"), MERGE_ATTS_ARGS)
def test_merge_atts(atts, new_atts, expected):
    """Tests merge_atts function."""
    assert merge_atts(atts, new_atts) == expected

def test_website_initialization():
    """Test initialize Website."""
    website = Website(TEST_DOMAIN, TEST_ATTS)
    assert website.domain == TEST_DOMAIN
    assert website.root.path == TEST_ATTS['root']['path']
    assert website.root.perms == TEST_ATTS['root']['perms']
    assert website.root.owner == TEST_ATTS['root']['owner']
    assert website.root.group == TEST_ATTS['root']['group']
    assert website.htdocs.path == TEST_ATTS['htdocs']['path']
    assert website.log.path == TEST_ATTS['log']['path']
    assert website.access_log.path == TEST_ATTS['access_log']['path']
    assert website.vhost.path == TEST_ATTS['vhost']['path']
    assert website.htaccess.path == TEST_ATTS['htaccess']['path']

@patch('ww.website.Vhost.exists', return_value=True)
@patch('ww.website.Vhost.parse', return_value={})
def test_website_init_existing_vhost(mock_exists, *args):
    """Test initialize Website."""
    with patch(_INPUT, return_value='y'):
        Website(TEST_DOMAIN, TEST_ATTS)
    mock_exists.assert_called_once_with()

@patch('ww.website.Website.verify', return_value=True)
def test_website_repair(mock_verify):
    """Tests Website class verify method."""
    website = Website(TEST_DOMAIN, TEST_ATTS)
    website.repair()
    mock_verify.assert_called_once_with(True)

def test_website_install_verify_remove():
    """Integration test: initializes, installs, verifies, and removes website."""
    with patch(_INPUT, return_value='y'):
        website = Website('example.com')

    assert not website.is_installed(), "Website 'example.com' should not exist on this server."
    assert not website.verify(), "Verification on a non-existing website should fail."

    with patch(_INPUT, return_value='y'):
        website.install()

    @localhost
    def installed_website_tests(website):
        """Function testing installed website. Wrapped by localhost() decorator."""
        print('test_domain *should* point to this server inside the decorated function.')
        assert website.is_installed()
        assert website.verify(), "Freshly installed website should verify as true."

    installed_website_tests(website)

    website.remove(ask=False)
    assert not website.is_installed()
    assert not website.verify(), "Verification on a non-existing website should fail."

    # Repeat the test for good measure:
    with patch(_INPUT, return_value='y'):
        website.install()

    installed_website_tests(website)

    website.remove(ask=False)
    assert not website.is_installed()
    assert not website.verify(), "Verification on a non-existing website should fail."

def test_website_pack_unpack():
    """Integration test: initializes, installs, verifies, packs, removes,
    unpacks and removes website."""
    with patch(_INPUT, return_value='y'):
        website = Website('example.com')

    assert not website.is_installed(), "Website 'example.com' should not exist on this server."
    assert not website.verify(), "Verification on a non-existing website should fail."

    with patch(_INPUT, return_value='y'):
        website.install()

    # Create a test file in htdocs
    the_file = File({'path' : website.htdocs + '/index.html'})
    the_file.data = 'Test file.'
    the_file.create()

    # Pack the site
    website.pack()

    website.remove(ask=False)
    assert not website.is_installed()
    assert not website.verify(), "Verification on a non-existing website should fail."
    assert not the_file.exists()

    with patch(_INPUT, return_value='y'):
        website.unpack()

    assert website.is_installed()
    def verify(website):
        """Verify function to wrap with localhost decorator."""
        assert website.verify()
    localhost(verify)(website)
    assert the_file.exists()

    # Remove and check again for good measure
    website.remove(ask=False)
    assert not website.is_installed()
    assert not website.verify(), "Verification on a non-existing website should fail."
    assert not the_file.exists()

def test_website_migrate():
    """TODO:"""
    pass
