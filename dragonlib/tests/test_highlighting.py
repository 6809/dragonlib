#!/usr/bin/env python
# encoding:utf8

"""
    unittests
    =========

    :created: 2015 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2015 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import unittest
from pygments.token import Token

from dragonlib.dragon32.pygments_lexer import BasicLexer


class TestHighlighting(unittest.TestCase):
    def test(self):
        lexer = BasicLexer()
        listing='10 PRINT"FOO"'
        tokensource = lexer.get_tokens(listing)
        self.assertEqual(list(tokensource), [
            (Token.Name.Label, '10'),
            (Token.Text, ' '),
            (Token.Name.Builtin, 'PRINT'),
            (Token.Literal.String, '"FOO"'),
            (Token.Text, '\n')
        ])
