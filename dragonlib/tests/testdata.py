# encoding:utf8

"""
    DragonLib unittests
    ===================

    contains some shared test data

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

LISTING_01= ('10 PRINT',)
LISTING_01_BIN = ( # program address: $1234 !
    b"\x12\x3a" # load address
    b"\x00\x0a" # line number == 10
    b"\x87" # PRINT
    b"\x00" # line end
    b"\x00\x00" # listing end
)
LISTING_01_DOS_HEADER = ( # Dragon DOS Binary Format header
    b"\x55" # head byte
    b"\x01" # filetype $01==.BAS
    b"\x12\x34" # load address
    b"\x00\x08" # length
    b"\x56\x78" # exec address
    b"\xAA" # terminator
)
LISTING_01_DOS_DUMP = LISTING_01_DOS_HEADER + LISTING_01_BIN

#--------------------------------------------------------------------------------------------

LISTING_02 = (
    '10 CLS',
    '20 FOR I = 0 TO 255:',
    '30 POKE 1024+(I*2),I',
    '40 NEXT I',
    '50 I$ = INKEY$:IF I$="" THEN 50'
)
LISTING_02_BIN = ( # program address: $abcd !
    b"\xab\xd3\x00\x0a\xa0\x00"
    b"\xab\xe6\x00\x14\x80\x20\x49\x20\xcb\x20\x30\x20\xbc\x20\x32\x35\x35\x3a\x00"
    b"\xab\xf9\x00\x1e\x93\x20\x31\x30\x32\x34\xc3\x28\x49\xc5\x32\x29\x2c\x49\x00"
    b"\xac\x01\x00\x28\x8b\x20\x49\x00"
    b"\xac\x1a\x00\x32\x49\x24\x20\xcb\x20\xff\x9a\x3a\x85\x20\x49\x24\xcb\x22\x22\x20\xbf\x20\x35\x30\x00"
    b"\x00\x00"
)
LISTING_02_DOS_HEADER = ( # Dragon DOS Binary Format header
    b"\x55" # head byte
    b"\x01" # filetype $01==.BAS
    b"\xab\xcd" # load address
    b"\x00\x4f" # length
    b"\xdc\xba" # exec address
    b"\xAA" # terminator
)
LISTING_02_DOS_DUMP = LISTING_02_DOS_HEADER + LISTING_02_BIN

