#!/usr/bin/env python
#
# name:             htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/31/2016
#
# description:      A class to create Apache htaccess files.
#

try:
    from ext_pylib.files import File, Section
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from htaccess import Htaccess, HtaccessSection
from ww import settings as s


# Htaccess()
#   A class that describes an Apache htaccess file.
#   This is primarily a wrapper for htaccess managment.
#
#   methods:
#       create()
#       verify()
class WPHtaccess(Htaccess):
    def __init__(self, atts):
        super(WPHtaccess, self).__init__(atts)
        if getattr(self, 'wp_htaccess', None):
            self.wp_htaccess = HtaccessSection({'path' : s.WP_HTA_TEMPLATE})
            self.data = self.wp_hardened.apply_to(self.read())
        if getattr(self, 'wp_hardened', None):
            self.wp_hardened = HtaccessSection({'path' : s.WP_HTA_HARDENED_TEMPLATE})
            self.data = self.wp_hardened.apply_to(self.read())

    def verify(self, repair):
        result = super(WPHtaccess, self).verify(repair)
        if self.exists() and self.wp_htaccess:  # Use wordpress htaccess template?
            print 'Checking htaccess for WordPress section...',
            if not self.wp_htaccess.has_section(self.read()):
                # TODO: do the repair if repair
                print '[FAIL]'
                return false
            print '[OK]'
            if not self.wp_htaccess.is_applied(self.read()):
                print '[!] htaccess has WordPress section, but it is an old' + \
                        'version, or it has been altered.'
        if self.exists() and self.wp_hardened:  # Use hardened wordpress htaccess template?
            print 'Checking htaccess for hardened WordPress section...',
            if not self.h5g.has_section(self.read()):
                # TODO: do the repair if repair
                print '[FAIL]'
                return false
            print '[OK]'
            if not self.h5g.is_applied(self.read()):
                print '[!] htaccess has hardened WordPress section, but it is an old' + \
                        'version, or it has been altered.'
        return result
