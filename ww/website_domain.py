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
    from ext_pylib.domain import Domain, get_server_ip
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
