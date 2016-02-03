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
    from ext_pylib.files import Section
    from ext_pylib.prompt import prompt, prompt_str
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from ww import settings as s
from ww_file import WWFile


class HtaccessSection(Section, WWFile):
    def __str__(self):
        pass


# Htaccess()
#   A class that describes an Apache htaccess file.
#   This is primarily a wrapper for htaccess managment.
#
#   methods:
#       verify()
class Htaccess(WWFile):

    def __init__(self, atts):
        """TODO:"""
        super(Htaccess, self).__init__(atts)
        self.sections = []
        if 'hta' in atts:
            for hta in atts['hta']:
                htaccess = HtaccessSection(hta)
                self.data = htaccess.apply_to(self.read())
                self.sections.append(htaccess)

    def verify(self, repair):
        """TODO:"""
        result = super(Htaccess, self).verify(repair)
        save = False

        for htaccess in self.sections:
            print 'Checking htaccess for ' + str(htaccess) + ' section...',
            if not htaccess.has_section(self.read()):
                if repair:
                    self.data = htaccess.apply_to(self.read())
                    save = True
                else:
                    print '[FAIL]'
                    return false
            print '[OK]'
            if not htaccess.is_applied(self.read()):
                print '[!] htaccess has 5g section, but it is an old' + \
                        'version, or it has been altered.'

        if repair and save:
            result = result and self.write()

        return result
