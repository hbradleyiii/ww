#!/usr/bin/env python
#
# name:             site_domain.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2014
#
# description:      A class to describe and manage a domain name and
#                   corresponding ip address.
#
#                   TODO: add DNS API capabilities

from ext_pylib.domain import Domain
import re
import requests
import socket


# Site_Domain(domain)
#   A class to describe and manage a domain name and corresponding ip address.
#
#   methods:
#       verify()
#       repair()
class Site_Domain(Domain):

    def verify(self, repair = False):
        """Verifies that the domain is pointed at the server."""
        print 'Server IP: ' + self.server_ip
        print 'Current site IP: ' + self.ip
        if not self.server_ip == self.ip:
            print '[!] Site IP is not the same as this server\'s ip'
            print '[*] DNS API not yet implemented.'
            return False
        print 'Domain is correctly pointed at this server.'
        return True

    def repair(self):
        """Repairs domain -- not yet implemented."""
        print '[*] DNS API not yet implemented.'
        self.verify()
