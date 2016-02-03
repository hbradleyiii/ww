#!/usr/bin/env python
#
# name:             website_domain.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2015
#
# description:      A class to describe and manage a domain name and
#                   corresponding ip address.
#
#                   TODO: add DNS API capabilities

try:
    from ext_pylib.domain import Domain, SERVER_IP
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

try:
    import requests
except ImportError:
    raise ImportError('requests must be installed to run ww')

import re
import socket


# WebsiteDomain(domain)
#   A class to describe and manage a domain name and corresponding ip address.
#
#   methods:
#       verify()
#       repair()
class WebsiteDomain(Domain):

    def verify(self, repair = False):
        """Verifies that the domain is pointed at the server."""
        print 'Server IP: ' + SERVER_IP
        print 'Current website IP: ' + self.ip
        if not SERVER_IP == self.ip:
            print '[!] Website IP is not the same as this server\'s ip'
            print '[*] DNS API not yet implemented.'
            return False
        print 'Domain is correctly pointed at this server.'
        return True

    def repair(self):
        """Repairs domain -- not yet implemented."""
        print '[*] DNS API not yet implemented.'
        self.verify()
