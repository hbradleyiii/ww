#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             ww_file.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/01/2016
#
# description:      An abstract class for ww files. This is primarily to
#                   prevent code duplication and have consistency for ww File
#                   classes.
#

try:
    from ext_pylib.files import File
except ImportError:
    raise ImportError('ext_pylib must be installed to run ww')

# WWFile()
#   An abstract class intended to be exteneded by ww File classes.
#   This is primarily a wrapper for preventing code duplication and
#   consistency.
#
#   methods:
#       repair()
class WWFile(File):
    def repair(self):
        self.verify(True)
