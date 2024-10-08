#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging

from dragonlib.CoCo.basic_tokens import COCO_BASIC_TOKENS
from dragonlib.core.basic import BasicLine, BasicListing, BasicTokenUtil, RenumTool
from dragonlib.core.basic_parser import BASICParser
from dragonlib.core.binary_files import BinaryFile
from dragonlib.dragon32.basic_tokens import DRAGON32_BASIC_TOKENS
from dragonlib.utils.logging_utils import log_bytes


log = logging.getLogger(__name__)


DRAGON32 = "Dragon32"
COCO2B = "CoCo"


class BaseAPI:
    RENUM_REGEX = r"""
        (?P<statement> GOTO|GOSUB|THEN|ELSE ) (?P<space>\s*) (?P<no>[\d*,\s*]+)
    """

    def __init__(self):
        self.listing = BasicListing(self.BASIC_TOKENS)
        self.renum_tool = RenumTool(self.RENUM_REGEX)
        self.token_util = BasicTokenUtil(self.BASIC_TOKENS)

    def program_dump2ascii_lines(self, dump, program_start=None):
        """
        convert a memory dump of a tokensized BASIC listing into
        ASCII listing list.
        """
        dump = bytearray(dump)
        # assert isinstance(dump, bytearray)

        if program_start is None:
            program_start = self.DEFAULT_PROGRAM_START
        return self.listing.program_dump2ascii_lines(dump, program_start)

    def parse_ascii_listing(self, basic_program_ascii):
        parser = BASICParser()
        parsed_lines = parser.parse(basic_program_ascii)
        if not parsed_lines:
            log.critical("No parsed lines {} from {} ?!?".format(repr(parsed_lines), repr(basic_program_ascii)))
        log.debug("Parsed BASIC: %s", repr(parsed_lines))
        return parsed_lines

    def ascii_listing2basic_lines(self, basic_program_ascii, program_start):
        parsed_lines = self.parse_ascii_listing(basic_program_ascii)

        basic_lines = []
        for line_no, code_objects in sorted(parsed_lines.items()):
            basic_line = BasicLine(self.token_util)
            basic_line.code_objects_load(line_no, code_objects)
            basic_lines.append(basic_line)

        return basic_lines

    def ascii_listing2program_dump(self, basic_program_ascii, program_start=None):
        """
        convert a ASCII BASIC program listing into tokens.
        This tokens list can be used to insert it into the
        Emulator RAM.
        """
        if program_start is None:
            program_start = self.DEFAULT_PROGRAM_START

        basic_lines = self.ascii_listing2basic_lines(basic_program_ascii, program_start)

        program_dump = self.listing.basic_lines2program_dump(basic_lines, program_start)
        assert isinstance(program_dump, bytearray), "is type: {} and not bytearray: {}".format(
            type(program_dump), repr(program_dump)
        )
        return program_dump

    def pformat_tokens(self, tokens):
        """
        format a tokenized BASIC program line. Useful for debugging.
        returns a list of formated string lines.
        """
        return self.listing.token_util.pformat_tokens(tokens)

    def pformat_program_dump(self, program_dump, program_start=None):
        """
        format a BASIC program dump. Useful for debugging.
        returns a list of formated string lines.
        """
        assert isinstance(program_dump, bytearray)

        if program_start is None:
            program_start = self.DEFAULT_PROGRAM_START
        return self.listing.pformat_program_dump(program_dump, program_start)

    def renum_ascii_listing(self, content):
        return self.renum_tool.renum(content)

    def reformat_ascii_listing(self, basic_program_ascii):

        parsed_lines = self.parse_ascii_listing(basic_program_ascii)

        ascii_lines = []
        for line_no, code_objects in sorted(parsed_lines.items()):
            print()
            print(line_no, code_objects)
            basic_line = BasicLine(self.token_util)
            basic_line.code_objects_load(line_no, code_objects)

            print(basic_line)
            basic_line.reformat()
            new_line = basic_line.get_content()
            print(new_line)
            ascii_lines.append(new_line)

        return "\n".join(ascii_lines)

    def bas2bin(self, basic_program_ascii, load_address=None, exec_address=None):

        # FIXME: load_address/exec_address == program_start ?!?!
        if load_address is None:
            load_address = self.DEFAULT_PROGRAM_START

        if exec_address is None:
            exec_address = self.DEFAULT_PROGRAM_START

        tokenised_dump = self.ascii_listing2program_dump(basic_program_ascii, load_address)
        log.debug(type(tokenised_dump))
        log.debug(repr(tokenised_dump))
        log_bytes(tokenised_dump, msg="tokenised: %s")

        binary_file = BinaryFile()
        binary_file.load_tokenised_dump(
            tokenised_dump,
            load_address=load_address,
            exec_address=exec_address,
        )
        binary_file.debug2log(level=logging.CRITICAL)
        data = binary_file.dump_DragonDosBinary()
        return data

    def bin2bas(self, data):
        """
        convert binary files to a ASCII basic string.
        Supported are:
            * Dragon DOS Binary Format
            * TODO: CoCo DECB (Disk Extended Color BASIC) Format

        see:
        http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=348&p=10139#p10139
        """
        data = bytearray(data)

        binary_file = BinaryFile()
        binary_file.load_from_bin(data)

        if binary_file.file_type != 0x01:
            log.error("ERROR: file type $%02X is not $01 (tokenised BASIC)!", binary_file.file_type)

        ascii_lines = self.program_dump2ascii_lines(
            dump=binary_file.data,
            # FIXME:
            # program_start=bin.exec_address
            program_start=binary_file.load_address,
        )
        return "\n".join(ascii_lines)


class Dragon32API(BaseAPI):
    CONFIG_NAME = DRAGON32
    MACHINE_NAME = "Dragon 32"
    BASIC_TOKENS = DRAGON32_BASIC_TOKENS

    PROGRAM_START_ADDR = 0x0019
    VARIABLES_START_ADDR = 0x001B
    ARRAY_START_ADDR = 0x001D
    FREE_SPACE_START_ADDR = 0x001F

    # Default memory location of BASIC listing start
    DEFAULT_PROGRAM_START = 0x1E01


class CoCoAPI(Dragon32API):
    """
    http://sourceforge.net/p/toolshed/code/ci/default/tree/cocoroms/dragon_equivs.asm
    """

    CONFIG_NAME = COCO2B
    MACHINE_NAME = "CoCo"
    BASIC_TOKENS = COCO_BASIC_TOKENS


def example_renum_ascii_listing():
    api = Dragon32API()

    ascii_listing = "\n".join(
        [
            '1 PRINT "LINE 10"',
            '2 PRINT "LINE 20"',
            '3 GOTO 1',
        ]
    )
    print(api.renum_ascii_listing(ascii_listing))


def test_bin2bas():
    api = Dragon32API()

    with open(os.path.expanduser("~/DragonEnvPy3/DwRoot/AUTOLOAD.DWL"), "rb") as f:
        data1 = f.read()

    ascii_listing = api.bin2bas(data1)
    print(ascii_listing)

    data2 = api.bas2bin(ascii_listing, load_address=0x1E01, exec_address=0x1E01)

    log_bytes(data1, "data1: %s", level=logging.CRITICAL)
    log_bytes(data2, "data2: %s", level=logging.CRITICAL)


if __name__ == '__main__':
    import os

    from dragonlib.utils.logging_utils import setup_logging

    setup_logging(
        #         level=1 # hardcore debug ;)
        #         level=10  # DEBUG
        #         level=20  # INFO
        level=30  # WARNING
        #         level=40 # ERROR
        #         level=50 # CRITICAL/FATAL
        #         level=99
    )

    # example_renum_ascii_listing()
    test_bin2bas()
