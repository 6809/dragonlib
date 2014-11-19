# coding: utf-8

"""
    unitest utilities
    ~~~~~~~~~~~~~~~~~

    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import unittest
import sys


class TextTestResult2(unittest.TextTestResult):
    def startTest(self, test):
        sys.stdout.flush()
        sys.stderr.flush()

        if not self.showAll:
            super(TextTestResult2, self).startTest(test)
            return
        print()
        print("_" * 70)
        self.showAll = False
        print(self.getDescription(test), "...")
        super(TextTestResult2, self).startTest(test)
        self.showAll = True

        sys.stdout.flush()
        sys.stderr.flush()


class TextTestRunner2(unittest.TextTestRunner):
    resultclass = TextTestResult2