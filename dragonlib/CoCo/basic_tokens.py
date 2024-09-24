"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    information from:

    * Color BASIC 1.3:
    http://sourceforge.net/p/toolshed/code/ci/default/tree/cocoroms/bas.asm

    * Extended Color BASIC 1.1:
    http://sourceforge.net/p/toolshed/code/ci/default/tree/cocoroms/extbas.asm

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

# Revesed word tokens from Color BASIC 1.3:
COCO_COLOR_BASIC_TOKENS = {
    0x80: "FOR",
    0x81: "GO",
    0x82: "REM",
    0x83: "'",
    0x84: "ELSE",
    0x85: "IF",
    0x86: "DATA",
    0x87: "PRINT",
    0x88: "ON",
    0x89: "INPUT",
    0x8A: "END",
    0x8B: "NEXT",
    0x8C: "DIM",
    0x8D: "READ",
    0x8E: "RUN",
    0x8F: "RESTORE",
    0x90: "RETURN",
    0x91: "STOP",
    0x92: "POKE",
    0x93: "CONT",
    0x94: "LIST",
    0x95: "CLEAR",
    0x96: "NEW",
    0x97: "CLOAD",
    0x98: "CSAVE",
    0x99: "OPEN",
    0x9A: "CLOSE",
    0x9B: "LLIST",
    0x9C: "SET",
    0x9D: "RESET",
    0x9E: "CLS",
    0x9F: "MOTOR",
    0xA0: "SOUND",
    0xA1: "AUDIO",
    0xA2: "EXEC",
    0xA3: "SKIPF",
    0xA4: "TAB(",
    0xA5: "TO",
    0xA6: "SUB",
    0xA7: "THEN",
    0xA8: "NOT",
    0xA9: "STEP",
    0xAA: "OFF",
    0xAB: "+",
    0xAC: "-",
    0xAD: "*",
    0xAE: "/",
    0xAF: "^",
    0xB0: "AND",
    0xB1: "OR",
    0xB2: ">",
    0xB3: "=",
    0xB4: "<",
    #
    # Function tokens - all proceeded by 0xff to differentiate from operators
    #
    0xFF80: "SGN",
    0xFF81: "INT",
    0xFF82: "ABS",
    0xFF83: "USR",
    0xFF84: "RND",
    0xFF85: "SIN",
    0xFF86: "PEEK",
    0xFF87: "LEN",
    0xFF88: "STR$",
    0xFF89: "VAL",
    0xFF8A: "ASC",
    0xFF8B: "CHR$",
    0xFF8C: "EOF",
    0xFF8D: "JOYSTK",
    0xFF8E: "LEFT$",
    0xFF8F: "RIGHT$",
    0xFF90: "MID$",
    0xFF91: "POINT",
    0xFF92: "INKEY$",
    0xFF93: "MEM",
}

# Revesed word tokens from Extended Color BASIC 1.1:
COCO_EXTENDED_COLOR_BASIC_TOKENS = {
    0xB5: "DEL",
    0xB6: "EDIT",
    0xB7: "TRON",
    0xB8: "TROFF",
    0xB9: "DEF",
    0xBA: "LET",
    0xBB: "LINE",
    0xBC: "PCLS",
    0xBD: "PSET",
    0xBE: "PRESET",
    0xBF: "SCREEN",
    0xC0: "PCLEAR",
    0xC1: "COLOR",
    0xC2: "CIRCLE",
    0xC3: "PAINT",
    0xC4: "GET",
    0xC5: "PUT",
    0xC6: "DRAW",
    0xC7: "PCOPY",
    0xC8: "PMODE",
    0xC9: "PLAY",
    0xCA: "DLOAD",
    0xCB: "RENUM",
    0xCC: "FN",
    0xCD: "USING",
    #
    # Function tokens - all proceeded by 0xff to differentiate from operators
    #
    0xFF94: "ATN",
    0xFF95: "COS",
    0xFF96: "TAN",
    0xFF97: "EXP",
    0xFF98: "FIX",
    0xFF99: "LOG",
    0xFF9A: "POS",
    0xFF9B: "SQR",
    0xFF9C: "HEX$",
    0xFF9D: "VARPTR",
    0xFF9E: "INSTR",
    0xFF9F: "TIMER",
    0xFFA0: "PPOINT",
    0xFFA1: "STRING$",
}

# Merged tokens:
COCO_BASIC_TOKENS = COCO_COLOR_BASIC_TOKENS.copy()
COCO_BASIC_TOKENS.update(COCO_EXTENDED_COLOR_BASIC_TOKENS)


if __name__ == '__main__':
    from dragonlib.dragon32.basic_tokens import DRAGON32_BASIC_TOKENS

    values = list(range(0x80, 0x100)) + list(range(0x8000, 0x10000))

    # Generate Wiki Table for:
    # http://archive.worldofdragon.org/index.php?title=Tokens

    print(
        """
* "CoCo A": - Tokens from Color BASIC 1.3
* "CoCo B": - Additional tokens from Extended Color BASIC 1.1 only
{| class="wikitable" style="font-family: monospace; background-color:#ffffcc;" cellpadding="10"
|-
! value
! Dragon
token
! CoCo A
token
! CoCo B
token
"""
    )
    for value in values:
        coco_basic_statement = COCO_COLOR_BASIC_TOKENS.get(value, "")
        coco_extended_basic_statement = COCO_EXTENDED_COLOR_BASIC_TOKENS.get(value, "")
        dragon_statement = DRAGON32_BASIC_TOKENS.get(value, "")

        if coco_basic_statement == coco_extended_basic_statement == dragon_statement == "":
            continue

        if value > 0xFF:
            value = "$%04x" % value
        else:
            value = "$%02x" % value

        print("|-")
        print("| %s" % value)
        print("| %s" % dragon_statement)
        print("| %s" % coco_basic_statement)
        print("| %s" % coco_extended_basic_statement)

    print("|-")
    print("|}")
