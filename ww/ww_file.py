#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             ww_file.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/06/2016
#

"""
ww.ww_file
~~~~~~~~~~

An abstract class from which to inherit for ww files.
Extends ext_pylib.files.File.
"""

try:
    from ext_pylib.files import File
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')


class WWFile(File):
    """An abstract class intended to be exteneded by ww File classes.
    This is primarily a wrapper for preventing code duplication and
    consistency.
    """
    def repair(self):
        """Repair runs verify with a repair set to true."""
        return self.verify(True)
