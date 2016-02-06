#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             website_domain.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2015
#
#                   TODO: add DNS API capabilities

"""
ww.website_domain
~~~~~~~~~~~~~~~~~

A class to describe and manage a domain name and corresponding ip address.
Extends ext_pylib.domain.Domain
"""

try:
    from ext_pylib.domain import Domain, get_server_ip
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('requests must be installed to run ww')

import re
import socket


def create_domain(name=None):
    """Factory function for Website Domain.
    Accepts nameLoops on invalid entry."""
    while True:
        try:
            if not name:
                name = prompt_str("What is the site name?", "example.com")
            return WebsiteDomain(name)
        except ValueError as msg:
            print msg


class WebsiteDomain(Domain):
    """A class to describe and manage a domain name and corresponding ip address."""

    def verify(self, repair = False):
        """Verifies that the domain is pointed at the server."""
        server_ip == get_server_ip()
        print 'Server IP: ' + server_ip
        print 'Current website IP: ' + self.ip
        if not server_ip == self.ip:
            print '\n    -----------------------------------------------------------'
            print '    [WARN] Website IP is not the same as this server\'s ip!'
            print '           DNS API not yet implemented.'
            print '           Please remember to change DNS settings manually.'
            print '    -----------------------------------------------------------\n'
            return False
        print 'Domain is correctly pointed at this server.'
        return True

    def repair(self):
        """Repairs domain -- not yet implemented."""
        print '[*] DNS API not yet implemented.'
        self.verify()
