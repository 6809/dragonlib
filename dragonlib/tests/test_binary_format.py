#!/usr/bin/env python
# encoding:utf8

"""
    unittests for BASIC parser
    ==========================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import logging
import sys
import unittest

from dragonlib.core.binary_files import BinaryFile
from dragonlib.utils.unittest_utils import TextTestRunner2


log = logging.getLogger(__name__)


class TestBinaryFile(unittest.TestCase):
    def setUp(self):
        self.binary = BinaryFile()

    def test_load_from_bin(self):
        tokenised_dump = (
            b"\x1e\x07" # load address
            b"\x00\x0a" # line number == 10
            b"\x87" # PRINT
            b"\x00" # line end
            b"\x00\x00" # listing end
        )
        log_bytes(tokenised_dump, msg="tokenised: %s")
        self.binary.load_tokenised_dump(tokenised_dump,
            load_address=0x1234, exec_address=0x5678
        )

        header = (
            b"\x55" # head byte
            b"\x01" # filetype $01==.BAS
            b"\x12\x34" # load address
            b"\x00\x08" # length
            b"\x56\x78" # exec address
            b"\xAA" # terminator
        )
        self.assertEqual(self.binary.get_header(), header)

        dragon_bin = self.binary.dump_DragonDosBinary()
        log_bytes(dragon_bin, msg="DragonDOS: %s")

        self.assertEqual(dragon_bin, header + tokenised_dump)

    def test_load_from_bin2(self):
        tokenised_dump = (
            b"\x1e\x07\x00\x0a\xa0\x00"
            b"\x1e\x1a\x00\x14\x80\x20\x49\x20\xcb\x20\x30\x20\xbc\x20\x32\x35\x35\x3a\x00"
            b"\x1e\x2d\x00\x1e\x93\x20\x31\x30\x32\x34\xc3\x28\x49\xc5\x32\x29\x2c\x49\x00"
            b"\x1e\x35\x00\x28\x8b\x20\x49\x00"
            b"\x1e\x4e\x00\x32\x49\x24\x20\xcb\x20\xff\x9a\x3a\x85\x20\x49\x24\xcb\x22\x22\x20\xbf\x20\x35\x30\x00"
            b"\x00\x00"
        )
        # Listing from test_api.Dragon32BASIC_HighLevel_ApiTest:
        # 10 CLS
        # 20 FOR I = 0 TO 255:
        # 30 POKE 1024+(I*2),I
        # 40 NEXT I
        # 50 I$ = INKEY$:IF I$="" THEN 50

        log_bytes(tokenised_dump, msg="tokenised: %s")
        self.binary.load_tokenised_dump(tokenised_dump,
            load_address=0x1234, exec_address=0x5678
        )

        header = (
            b"\x55" # head byte
            b"\x01" # filetype $01==.BAS
            b"\x12\x34" # load address
            b"\x00\x4f" # length
            b"\x56\x78" # exec address
            b"\xAA" # terminator
        )
        self.assertEqual(self.binary.get_header(), header)

        dragon_bin = self.binary.dump_DragonDosBinary()
        log_bytes(dragon_bin, msg="DragonDOS: %s")

        self.assertEqual(dragon_bin, header + tokenised_dump)


if __name__ == "__main__":
    from dragonlib.utils.logging_utils import setup_logging, log_bytes

    setup_logging(
        # level=1 # hardcore debug ;)
        level=10  # DEBUG
        # level=20  # INFO
        # level=30  # WARNING
        # level=40 # ERROR
        # level=50 # CRITICAL/FATAL
    )

    unittest.main(
        argv=(
            sys.argv[0],
            # "TestBASICParser.test_spaces_after_line_no",
        ),
        testRunner=TextTestRunner2,
        # verbosity=1,
        verbosity=2,
        # failfast=True,
    )
    print(" --- END --- ")
