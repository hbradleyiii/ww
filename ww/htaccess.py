#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             htaccess.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/23/2016
#

"""
ww.htaccess
~~~~~~~~~~~

A class to create Apache htaccess files.
It extends WWFile.
"""

from __future__ import absolute_import, print_function

try:
    from ext_pylib.files import SectionFile
    from ext_pylib.input import prompt
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

from .ww_file import WWFile


class HtaccessSection(SectionFile):
    """Htaccess section file."""
    def __str__(self):
        return getattr(self, 'name', None)


class Htaccess(WWFile):
    """A class that describes an Apache htaccess file.
    This is primarily a wrapper for htaccess managment.
    """

    def __init__(self, atts):
        """Initialize an Htaccess class."""
        super(Htaccess, self).__init__(atts)

        self.sections = []
        if 'sections' in atts:
            for sfile in atts['sections']:
                section = HtaccessSection(sfile)
                self.sections.append(section)

        if not self.exists() or not prompt('Use existing htaccess file?'):
            for section in self.sections:
                self.data = section.apply_to(self.read())

    def verify(self, repair=False):
        """Verifies the htaccess file and contents.
        This checks to make sure sections exist. It does"""
        result = super(Htaccess, self).verify(repair)
        save = False

        for section in self.sections:
            print('Checking htaccess for ' + section.name + ' section...', end=' ')
            if not section.is_in(self.read()):
                if repair:
                    self.data = section.apply_to(self.read())
                    save = True
                else:
                    print('[FAIL]')
                    return False
            print('[OK]')

            if not section.is_applied(self.read()):
                print('[!] htaccess has ' + section.name + ' section, but it is an old' + \
                        'version, or it has been altered.')
                if repair and prompt('Apply template to old/altered version?'):
                    self.data = section.apply_to(self.read(), overwrite=True)
                    save = True

        if repair and save:
            result = result and self.write()

        return result
