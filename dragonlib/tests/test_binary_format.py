#!/usr/bin/env python
# encoding:utf8

"""
    unittests for BASIC parser
    ==========================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014-2015 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import logging
import sys
import unittest

from dragonlib.core.binary_files import BinaryFile
from dragonlib.tests import testdata
from dragonlib.tests.test_base import BaseTestCase
from dragonlib.utils.byte_word_values import bin2hexline
from dragonlib.utils.logging_utils import log_bytes

log = logging.getLogger(__name__)


class TestBinaryFile(BaseTestCase):
    def setUp(self):
        self.binary = BinaryFile()

    def test_load_from_bin1(self):
        """ test with one line listing: testdata.LISTING_01 """
        # log_bytes(testdata.LISTING_01_BIN, msg="tokenised: %s")
        self.binary.load_tokenised_dump(testdata.LISTING_01_BIN,
            load_address=0x1234, exec_address=0x5678
        )
        # self.binary.debug2log(level=logging.CRITICAL)

        self.assertBinEqual(self.binary.get_header(), testdata.LISTING_01_DOS_HEADER)

        dragon_bin = self.binary.dump_DragonDosBinary()
        # log_bytes(dragon_bin, msg="DragonDOS1: %s",level=logging.CRITICAL)
        # log_bytes(testdata.LISTING_01_DOS_DUMP, msg="DragonDOS2: %s",level=logging.CRITICAL)

        self.assertBinEqual(dragon_bin, testdata.LISTING_01_DOS_DUMP)
        
    def test_load_from_bin2(self):
        """ test with bigger testdata.LISTING_02 """
        # log_bytes(testdata.LISTING_02_BIN, msg="tokenised: %s")
        self.binary.load_tokenised_dump(testdata.LISTING_02_BIN,
            load_address=0xabcd, exec_address=0xdcba
        )
        # self.binary.debug2log(level=logging.CRITICAL)

        self.assertBinEqual(self.binary.get_header(), testdata.LISTING_02_DOS_HEADER)

        dragon_bin = self.binary.dump_DragonDosBinary()
        # log_bytes(dragon_bin, msg="DragonDOS: %s")

        self.assertBinEqual(dragon_bin, testdata.LISTING_02_DOS_DUMP)

