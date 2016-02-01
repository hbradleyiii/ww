#!/usr/bin/env python
#
# name:             htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#
# description:      A class to create Apache htaccess files.
#

try:
    from ext_pylib.files import File, Section
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from ww import settings as s


class HtaccessSection(Section, File): pass

# Htaccess()
#   A class that describes an Apache htaccess file.
#   This is primarily a wrapper for htaccess managment.
#
#   methods:
#       create()
#       verify()
class Htaccess(File):

    def __init__(self, atts):
        super(Htaccess, self).__init__(atts)
        if getattr(self, 'h5g', None):
            self.h5g = HtaccessSection({'path' : s.HTA_5G_TEMPLATE})
            self.data = self.h5g.apply_to(self.read())

    def verify(self, repair):
        result = super(Htaccess, self).verify(repair)
        if self.exists() and self.h5g: # Use 5g htaccess template?
            print 'Checking htaccess for 5g section...',
            if not self.h5g.has_section(self.read()):
                # TODO: do the repair if repair
                print '[FAIL]'
                return false
            print '[OK]'
            if not self.h5g.is_applied(self.read()):
                print '[!] htaccess has 5g section, but it is an old' + \
                        'version, or it has been altered.'
        return result
