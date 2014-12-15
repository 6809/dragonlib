# encoding:utf8

"""
    DragonLib - needful python modules for Dragon/CoCo stuff
    ========================================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import re
from collections import namedtuple

from pygments.lexer import RegexLexer
from pygments.styles import get_style_by_name
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation



class BasicLexer(RegexLexer):
    """
    Pygments lexer for Dragon/CoCo BASIC
    """
    name = 'Dragon/CoCo BASIC'
    aliases = ['basic']
    filenames = ['*.bas']

    tokens = {
        'root': [
            (r"(REM|').*\n", Comment.Single),

            (r'\s+', Text),
            (r'^\d+', Name.Label),


            (
                r'RUN|RESTORE|STOP|RENUM|'
                r'GOTO|'
                r'OPEN|CLOSE|READ|CLOAD|CSAVE|DLOAD|LLIST|MOTOR|SKIPF|'
                r'LIST|CLEAR|NEW|EXEC|DEL|EDIT|TRON|TROFF',
                Keyword
            ),
            (
                r'SOUND|AUDIOLINE|PLAY|'
                r'PCLS|PSET|SCREEN|PCLEAR|COLOR|CIRCLE|PAINT|GET|PUT|DRAW|PCOPY|PMODE',
                Keyword.Reserved
            ),
            (r'DATA|DIM|LET|DEF', Keyword.Declaration),

            (
                r'PRINT|CLS|INPUT|INKEY$|'
                r'HEX$|LEFT$|RIGHT$|MID$|STRING$|STR$|CHR$|'
                r'SGN|INT|ABS|POS|RND|SQR|LOG|EXP|SIN|COS|TAN|ATN|LEN|VAL|ASC',
                Name.Builtin
            ),

            (
                r'FOR|TO|STEP|NEXT|IF|THEN|ELSE|RETURN|'
                r'GOSUB|'
                r'POKE|PEEK|'
                r'ON|END|CONT|SET|RESET|PRESET|TAB|SUB|FN|OFF|'
                r'USING|EOF|JOYSTK|FIX|POINT|MEM|VARPTR|INSTR|TIMER|PPOINT|USR',
                Name.Function
            ),

            (r'([+\-*/^>=<])', Operator),
            (r'AND|OR|NOT', Operator.Word),

            (r'"[^"\n]*.', String),
            (r'\d+|[-+]?\d*\.\d*(e[-+]?\d+)?', Number.Float),
            (r'[(),:]', Punctuation),
            (r'\w+[$%]?', Name),
        ]
    }

    def analyse_text(self, text):
        # if it starts with a line number, it shouldn't be a "modern" Basic
        # like VB.net
        if re.match(r'\d+', text):
            return 0.2


def list_styles(style_name):
    """
    Just list all different styles entries
    """
    style = get_style_by_name(style_name)

    keys = list(style)[0][1]
    Styles = namedtuple("Style", keys)

    existing_styles = {}

    for ttype, ndef in style:
        s = Styles(**ndef)
        if s in existing_styles:
            existing_styles[s].append(ttype)
        else:
            existing_styles[s] = [ttype]

    for ndef, ttypes in existing_styles.items():
        print(ndef)
        for ttype in sorted(ttypes):
            print("\t%s" % str(ttype).split("Token.",1)[1])


if __name__ == "__main__":
    list_styles("default")