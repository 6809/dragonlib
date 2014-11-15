#!/usr/bin/env python
# encoding:utf8

"""
    dragonlib
    =========

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import logging
import struct

from dragonlib.utils.logging_utils import log_bytes


log = logging.getLogger(__name__)


class BinaryFile(object):
    def __init__(self):
        self.load_address = None
        self.length = None
        self.exec_address = None
        self.data = None

    def load_DragonDosBinary(self, bin, strip_padding=True):
        """
        Dragon DOS Binary Format

        http://dragon32.info/info/binformt.html

        Offset:  Type:   Value:
          0       byte    $55           Constant
          1       byte    Filetype
          2:3     word    Load Address
          4:5     word    Length
          6:7     word    Exec Address
          8       byte    $AA           Constant
          9-xxx   byte[]  Data
        """
        log.debug("Load Dragon DOS Binary Format.")

        meta_data = struct.unpack(">BBHHHBB", bin[:10])

        machine_type = meta_data[0]
        if machine_type != 0x55:
            log.error("ERROR: Machine type wrong: is $%02X but should be $55!", machine_type)

        self.file_type = meta_data[1]
        self.load_address = meta_data[2]
        self.length = meta_data[3]
        self.exec_address = meta_data[4]
        terminator = meta_data[5]
        if terminator != 0xAA:
            log.error("ERROR: Terminator byte is $%02X but should be $AA!", terminator)

        if strip_padding:
            self.data = bin[9:self.length + 7]
        else:
            self.data = bin[9:]

        log.debug(
            "File type: $%02X Load Address: $%04X Exec Address: $%04X Length: %iBytes",
            self.file_type, self.load_address, self.exec_address, self.length
        )
        if self.length != len(self.data):
            log.error("ERROR: Wrong data size: should be: %i Bytes but is %i Bytes!", self.length, len(self.data))

        log_bytes(self.data, "data in hex: %s", level=logging.DEBUG)

    def load_from_bin(self, bin):
        """
        convert binary files to a ASCII basic string.
        Supported are:
            * Dragon DOS Binary Format
            * CoCo DECB (Disk Extended Color BASIC) Format

        see:
        http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=348&p=10139#p10139
        """
        machine_type = struct.unpack("B", bin[0])[0]
        if machine_type == 0x55:
            # Dragon DOS Binary Format
            self.load_DragonDosBinary(bin)
        elif machine_type == 0x00:
            raise NotImplementedError("CoCo DECB (Disk Extended Color BASIC) Format not supported, yet.")
        else:
            raise NotImplementedError("ERROR: Format $%02X unknown." % machine_type)