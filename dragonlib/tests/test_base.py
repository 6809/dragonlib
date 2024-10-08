#!/usr/bin/env python

"""
    Dragon Lib unittests
    ~~~~~~~~~~~~~~~~~~~~

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

import textwrap

import unittest
from dragonlib.utils.byte_word_values import bin2hexline


class BaseTestCase(unittest.TestCase):
    """
    Only some special assertments.
    """

    maxDiff = 3000

    def assertHexList(self, first, second, msg=None):
        first = ["$%x" % value for value in first]
        second = ["$%x" % value for value in second]
        self.assertEqual(first, second, msg)

    def assertEqualHex(self, hex1, hex2, msg=None):
        first = "$%x" % hex1
        second = "$%x" % hex2
        if msg is None:
            msg = "{} != {}".format(first, second)
        self.assertEqual(first, second, msg)

    def assertIsByteRange(self, value):
        self.assertTrue(0x0 <= value, "Value (dez: %i - hex: %x) is negative!" % (value, value))
        self.assertTrue(0xFF >= value, "Value (dez: %i - hex: %x) is greater than 0xff!" % (value, value))

    def assertIsWordRange(self, value):
        self.assertTrue(0x0 <= value, "Value (dez: %i - hex: %x) is negative!" % (value, value))
        self.assertTrue(0xFFFF >= value, "Value (dez: %i - hex: %x) is greater than 0xffff!" % (value, value))

    def assertEqualHexByte(self, hex1, hex2, msg=None):
        self.assertIsByteRange(hex1)
        self.assertIsByteRange(hex2)
        first = "$%02x" % hex1
        second = "$%02x" % hex2
        if msg is None:
            msg = "{} != {}".format(first, second)
        self.assertEqual(first, second, msg)

    def assertEqualHexWord(self, hex1, hex2, msg=None):
        self.assertIsWordRange(hex1)
        self.assertIsWordRange(hex2)
        first = "$%04x" % hex1
        second = "$%04x" % hex2
        if msg is None:
            msg = "{} != {}".format(first, second)
        self.assertEqual(first, second, msg)

    def assertBinEqual(self, bin1, bin2, msg=None, width=16):
        # first = bin2hexline(bin1, width=width)
        # second = bin2hexline(bin2, width=width)
        # self.assertSequenceEqual(first, second, msg)

        first = "\n".join(bin2hexline(bin1, width=width))
        second = "\n".join(bin2hexline(bin2, width=width))
        self.assertMultiLineEqual(first, second, msg)

    def _dedent(self, txt):
        # Remove any common leading whitespace from every line
        txt = textwrap.dedent(txt)

        # strip whitespace at the end of every line
        txt = "\n".join([line.rstrip() for line in txt.splitlines()])
        txt = txt.strip()
        return txt

    def assertEqual_dedent(self, first, second, msg=None):
        first = self._dedent(first)
        second = self._dedent(second)
        try:
            self.assertEqual(first, second, msg)
        except AssertionError as err:
            # Py2 has a bad error message
            msg = (
                "%s\n"
                " ------------- [first] -------------\n"
                "%s\n"
                " ------------- [second] ------------\n"
                "%s\n"
                " -----------------------------------\n"
            ) % (err, first, second)
            raise AssertionError(msg)
