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

from dragonlib.utils import six
from dragonlib.utils.byte_word_values import bin2hexline
from dragonlib.utils.logging_utils import log_bytes


log = logging.getLogger(__name__)


class BinaryFile(object):
    def __init__(self):
        self.file_type = None # $01 == BAS | $02 == BIN
        self.load_address = None
        self.length = None
        self.exec_address = None
        self.data = None

    def debug2log(self, level=logging.DEBUG):
        def verbose_value(value, fmt="$%02x"):
            try:
                return fmt % value
            except TypeError:
                return repr(value)

        log.log(level, "File Type: %s", verbose_value(self.file_type))
        log.log(level, "Load Address: %s", verbose_value(self.load_address, fmt="$%04x"))
        if self.length is None:
            log.log(level, "Length: None")
        else:
            log.log(level, "Length: $%04x (dez.: %i Bytes)",
                self.length, self.length
            )
        log.log(level, "Exec Address: %s", verbose_value(self.exec_address, fmt="$%04x"))

        if not self.data:
            log.log(level, "Data: %s", repr(self.data))
        else:
            log.log(level, "Data:")
            for line in bin2hexline(self.data, width=16):
                log.log(level, line)

    def get_header(self):
        header = struct.pack(">BBHHHB",
            0x55,
            self.file_type,
            self.load_address,
            self.length,
            self.exec_address,
            0xAA,
        )
        log_bytes(header, "Dragon DOS binary header in hex: %s", level=logging.DEBUG)
        return header

    def dump_DragonDosBinary(self):
        # log_bytes(self.data, "data in hex: %s", level=logging.DEBUG)
        self.debug2log(level=logging.DEBUG)
        header = self.get_header()

        return header + self.data

    def load_DragonDosBinary(self, data, strip_padding=True):
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

        meta_data = struct.unpack(">BBHHHB", data[:9])

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

        # print("before strip:")
        # print("\n".join(bin2hexline(data, width=16)))
        if strip_padding:
            self.data = data[9:self.length + 9]
        else:
            self.data = data[9:]
        # print("after strip:")
        # print("\n".join(bin2hexline(self.data, width=16)))

        log.debug(
            "File type: $%02X Load Address: $%04X Exec Address: $%04X Length: %iBytes",
            self.file_type, self.load_address, self.exec_address, self.length
        )
        if self.length != len(self.data):
            log.error("ERROR: Wrong data size: should be: %i Bytes but is %i Bytes!", self.length, len(self.data))

        # log_bytes(self.data, "data in hex: %s", level=logging.DEBUG)
        self.debug2log(level=logging.DEBUG)

    def load_from_bin(self, data):
        """
        convert binary files to a ASCII basic string.
        Supported are:
            * Dragon DOS Binary Format
            * CoCo DECB (Disk Extended Color BASIC) Format

        see:
        http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=348&p=10139#p10139
        """
        machine_type = data[0]
        # machine_type = struct.unpack("B", bin[0])[0]
        if machine_type == 0x55:
            # Dragon DOS Binary Format
            self.load_DragonDosBinary(data)
        elif machine_type == 0x00:
            raise NotImplementedError("CoCo DECB (Disk Extended Color BASIC) Format not supported, yet.")
        else:
            raise NotImplementedError("ERROR: Format $%02X unknown." % machine_type)

    def load_tokenised_dump(self, tokenised_dump, load_address, exec_address):
        assert isinstance(tokenised_dump, six.binary_type), (
            "is type: %s and not bytes/str: %s" % (type(tokenised_dump), repr(tokenised_dump))
        )
        self.file_type = 0x01
        self.load_address = load_address
        self.length = len(tokenised_dump)
        self.exec_address = exec_address
        self.data = tokenised_dump