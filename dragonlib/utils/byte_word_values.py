#!/usr/bin/env python

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    some code is borrowed from:
    XRoar emulator by Ciaran Anscomb (GPL license) more info, see README

    :copyleft: 2013-2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import string

import six


def signed5(x):
    """ convert to signed 5-bit """
    if x > 0xf: # 0xf == 2**4-1 == 15
        x = x - 0x20 # 0x20 == 2**5 == 32
    return x


def signed8(x):
    """ convert to signed 8-bit """
    if x > 0x7f: # 0x7f ==  2**7-1 == 127
        x = x - 0x100 # 0x100 == 2**8 == 256
    return x


def unsigned8(x):
    """ convert a signed 8-Bit value into a unsigned value """
    if x < 0:
        x = x + 0x0100 # 0x100 == 2**8 == 256
    return x


def signed16(x):
    """ convert to signed 16-bit """
    if x > 0x7fff: # 0x7fff ==  2**15-1 == 32767
        x = x - 0x10000 # 0x100 == 2**16 == 65536
    return x


def word2bytes(value):
    """
    >>> word2bytes(0xff09)
    (255, 9)

    >>> [hex(i) for i in word2bytes(0xffab)]
    ['0xff', '0xab']

    >>> word2bytes(0xffff +1)
    Traceback (most recent call last):
    ...
    AssertionError
    """
    assert 0 <= value <= 0xffff
    return (value >> 8, value & 0xff)


def bytes2word(byte_list):
    """
    >>> bytes2word([0xff,0xab])
    65451

    >>> hex(bytes2word([0xff,0xab]))
    '0xffab'
    """
    assert len(byte_list) == 2
    return (byte_list[0] << 8) + byte_list[1]


def bin2hexline(data, add_addr=True, width=16):
    """
    Format binary data to a Hex-Editor like format...

    >>> data = bytearray([i for i in range(256)])
    >>> print('\\n'.join(bin2hexline(data, width=16)))
    0000 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d 0e 0f ................
    0016 10 11 12 13 14 15 16 17 18 19 1a 1b 1c 1d 1e 1f ................
    0032 20 21 22 23 24 25 26 27 28 29 2a 2b 2c 2d 2e 2f  !"#$%&'()*+,-./
    0048 30 31 32 33 34 35 36 37 38 39 3a 3b 3c 3d 3e 3f 0123456789:;<=>?
    0064 40 41 42 43 44 45 46 47 48 49 4a 4b 4c 4d 4e 4f @ABCDEFGHIJKLMNO
    0080 50 51 52 53 54 55 56 57 58 59 5a 5b 5c 5d 5e 5f PQRSTUVWXYZ[\]^_
    0096 60 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f `abcdefghijklmno
    0112 70 71 72 73 74 75 76 77 78 79 7a 7b 7c 7d 7e 7f pqrstuvwxyz{|}~.
    0128 80 81 82 83 84 85 86 87 88 89 8a 8b 8c 8d 8e 8f ................
    0144 90 91 92 93 94 95 96 97 98 99 9a 9b 9c 9d 9e 9f ................
    0160 a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 aa ab ac ad ae af ................
    0176 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 ba bb bc bd be bf ................
    0192 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 ca cb cc cd ce cf ................
    0208 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 da db dc dd de df ................
    0224 e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 ea eb ec ed ee ef ................
    0240 f0 f1 f2 f3 f4 f5 f6 f7 f8 f9 fa fb fc fd fe ff ................


    with open("C:\Python27\python.exe", "rb") as f:
        data = f.read(150)

    print("\n".join(bin2hexline(data, width=16)))

    0000 4d 5a 90 00 03 00 00 00 04 00 00 00 ff ff 00 00 MZ..............
    0016 b8 00 00 00 00 00 00 00 40 00 00 00 00 00 00 00 ........@.......
    0032 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................
    0048 00 00 00 00 00 00 00 00 00 00 00 00 e8 00 00 00 ................
    0064 0e 1f ba 0e 00 b4 09 cd 21 b8 01 4c cd 21 54 68 ........!..L.!Th
    0080 69 73 20 70 72 6f 67 72 61 6d 20 63 61 6e 6e 6f is.program.canno
    0096 74 20 62 65 20 72 75 6e 20 69 6e 20 44 4f 53 20 t.be.run.in.DOS.
    0112 6d 6f 64 65 2e 0d 0d 0a 24 00 00 00 00 00 00 00 mode....$.......
    0128 9d 68 ba 89 d9 09 d4 da d9 09 d4 da d9 09 d4 da .h..............
    0144 d0 71 41 da d8 09                               .qA...
    """
    data = bytearray(data)

    # same as string.printable but without \t\n\r\v\f ;)
    printable = string.digits + string.ascii_letters + string.punctuation + " "

    addr = 0
    lines = []
    run = True
    line_width = 4 + (width * 3) + 1
    while run:
        if add_addr:
            line = ["%04i" % addr]
        else:
            line = []

        ascii_block = ""
        for i in range(width):
            b = data[addr]

            if chr(b) in printable:
                ascii_block += chr(b)
            else:
                ascii_block += "."

            line.append("%02x" % b)

            addr += 1
            if addr >= len(data):
                run = False
                break

        line = " ".join(line)
        line = line.ljust(line_width)
        line += ascii_block
        lines.append(line)
    return lines


def _bin2hexline_example():
    import sys

    with open(sys.executable, "rb") as f:
        data = f.read(500)

    print("\n".join(bin2hexline(data, width=16)))


if __name__ == "__main__":
    import doctest

    print(doctest.testmod(verbose=0))

    # _bin2hexline_example()
