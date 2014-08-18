#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import re

from dragonlib.utils.logging_utils import log, log_program_dump
from dragonpy.utils.byte_word_values import word2bytes


class BasicTokenUtil(object):
    def __init__(self, basic_token_dict):
        self.basic_token_dict = basic_token_dict
        self.ascii2token_dict = dict([
            (code, token)
            for token, code in basic_token_dict.items()
        ])

        regex = "(%s)" % "|".join([
            re.escape(statement)
            for statement in self.basic_token_dict.values()
        ])
        self.regex = re.compile(regex)

    def token2ascii(self, value):
        try:
            result = self.basic_token_dict[value]
        except KeyError:
            if value > 0xff:
                log.critical("ERROR: Token $%04x is not in BASIC_TOKENS!", value)
                return ""
            result = chr(value)
        return result

    def ascii2token(self, ascii_code, debug=False):
        """
        TODO: replace no tokens in comments and strings
        """
        log.critical(repr(ascii_code))
        parts = self.regex.split(ascii_code)
        log.critical(repr(parts))
        tokens = []
        for part in parts:
            if not part:
                continue

            if part in self.ascii2token_dict:
                new_token = self.ascii2token_dict[part]
                log.critical("\t%r -> %x", part, new_token)
                if new_token > 0xff:
                    tokens.append(new_token >> 8)
                    tokens.append(new_token & 0xff)
                else:
                    tokens.append(new_token)
            else:
                new_tokens = [ord(char) for char in part]
                tokens += new_tokens
        return tokens

    def format_tokens(self, tokens):
        result = []
        token_value = None
        for token in tokens:
            if token == 0xff:
                token_value = token
                continue
            if token_value is not None:
                token_value = (token_value << 8) + token
            else:
                token_value = token

            char = self.token2ascii(token_value)
            if token_value > 0xff:
                result.append("\t$%04x -> %s" % (token_value, repr(char)))
            else:
                result.append("\t  $%02x -> %s" % (token_value, repr(char)))
            token_value = None

        return result

class BasicLine(object):
    def __init__(self, token_util):
        self.token_util = token_util
        self.line_number = None
        self.line_code = None

    def token_load(self, line_number, tokens):
        self.line_number = line_number
        assert tokens[-1] == 0x00, "line code %s doesn't ends with \\x00: %s" % (
            repr(tokens), repr(tokens[-1])
        )
        self.line_code = tokens[:-1] # rstrip \x00

    def ascii_load(self, line_ascii):
        try:
            line_number, ascii_code = line_ascii.split(" ", 1)
        except ValueError as err:
            msg = "Error split line number and code in line: %r (Origin error: %s)" % (
                line_ascii, err
            )
            raise ValueError(msg)
        self.line_number = int(line_number)
        self.line_code = self.token_util.ascii2token(ascii_code)

    def get_tokens(self):
        return [self.line_number] + self.line_code

    def get_content(self, code=None):
        if code is None: # start
            code = self.line_code

        line = "%i " % self.line_number
        old_value = None
        for value in code:
            if value == 0xff:
                old_value = value
                continue
            if old_value is not None:
                value = (old_value << 8) + value
                old_value = None
            code = self.token_util.token2ascii(value)
            line += code
        return line

    def log_line(self):
        log.critical("%r:\n\t%s",
            self.get_content(),
            "\n\t".join(self.token_util.format_tokens(self.line_code))
        )


class BasicListing(object):
    def __init__(self, basic_token_dict):
        self.token_util = BasicTokenUtil(basic_token_dict)

    def dump2basic_lines(self, dump, program_start, basic_lines=None):
        if basic_lines is None:
            basic_lines = []

        log.critical("progam start $%04x", program_start)
        next_address = (dump[0] << 8) + dump[1]
        log.critical("next_address: $%04x", next_address)
        if next_address == 0x0000:
            # program end
            log.critical("return: %s", repr(basic_lines))
            return basic_lines
        line_number = (dump[2] << 8) + dump[3]
        log.critical("line_number: %i", line_number)
        length = next_address - program_start
        log.critical("length: %i", length)
        tokens = dump[4:length]
        log.critical("tokens:\n\t%s", "\n\t".join(self.token_util.format_tokens(tokens)))

        basic_line = BasicLine(self.token_util)
        basic_line.token_load(line_number, tokens)
        basic_lines.append(basic_line)

        return self.dump2basic_lines(dump[length:], next_address, basic_lines)

    def basic_lines2program_dump(self, basic_lines, program_start):
        program_dump = []
        current_address = program_start
        count = len(basic_lines)
        for no, line in enumerate(basic_lines, 1):
            line.log_line()
            line_tokens = [0x00] + line.get_tokens() + [0x00]

            current_address += len(line_tokens) + 2
            program_dump += word2bytes(current_address)
            if no == count: # It's the last line
                line_tokens += [0x00, 0x00]
            program_dump += line_tokens

        return program_dump

    def ascii_listing2basic_lines(self, txt):
        basic_lines = []
        for line in txt.splitlines():
            line = line.strip()
            if line:
                basic_line = BasicLine(self.token_util)
                basic_line.ascii_load(line)
                basic_lines.append(basic_line)
        return basic_lines

    def debug_listing(self, basic_lines):
        for line in basic_lines:
            line.log_line()

    def log_ram_content(self, program_start, level=99):
        ram_content = self.basic_lines2program_dump(program_start)
        log_program_dump(ram_content, level)

    def ascii_listing2program_dump(self, basic_program_ascii, program_start):
        basic_lines = self.ascii_listing2basic_lines(basic_program_ascii)
        self.debug_listing(basic_lines)
        return self.basic_lines2program_dump(basic_lines, program_start)

    def program_dump2ascii_lines(self, dump, program_start):
        basic_lines = self.dump2basic_lines(dump, program_start)
        log.critical("basic_lines: %s", repr(basic_lines))
        ascii_lines = []
        for line in basic_lines:
            ascii_lines.append(line.get_content())
        return ascii_lines


class RenumTool(object):
    """
    Renumber a BASIC program
    """
    def __init__(self, renum_regex):
        self.line_no_regex = re.compile("(?P<no>\d+)(?P<code>.+)")
        self.renum_regex = re.compile(renum_regex, re.VERBOSE)

    def renum(self, ascii_listing):
        self.renum_dict = self.create_renum_dict(ascii_listing)
        log.info("renum: %s",
            ", ".join([
                "%s->%s" % (o, n)
                for o, n in sorted(self.renum_dict.items())
            ])
        )
        new_listing = []
        lines = ascii_listing.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        for new_number, line in enumerate(lines, 1):
            new_number *= 10
            line = self.line_no_regex.sub("%s\g<code>" % new_number, line)
            new_line = self.renum_regex.sub(self.renum_inline, line)
            new_listing.append(new_line)
        return "\n".join(new_listing)

    def _get_new_line_number(self, line, old_number):
        try:
            new_number = "%s" % self.renum_dict[old_number]
        except KeyError:
            log.error(
                "Error in line '%s': line no. '%s' doesn't exist.",
                line, old_number
            )
            new_number = old_number
        return new_number

    def _replace_statement(self, matchobj):
        old_number = matchobj.group("no")
        new_number = self._get_new_line_number(matchobj.group(0), old_number)
        return "".join([
            matchobj.group("statement"),
            matchobj.group("space"),
            new_number
        ])

    def _replace_on_goto(self, matchobj):
        old_numbers = matchobj.group("on_goto_no")
        if old_numbers[-1] == " ":
            # e.g.: space before comment: ON X GOTO 1,2 ' Comment
            space_after = " "
        else:
            space_after = ""
        old_numbers = [n.strip() for n in old_numbers.split(",")]
        new_numbers = [
            self._get_new_line_number(matchobj.group(0), old_number)
            for old_number in old_numbers
        ]
        return "".join([
            matchobj.group("on_goto_statement"),
            matchobj.group("on_goto_space"),
            ",".join(new_numbers), space_after
        ])

    def renum_inline(self, matchobj):
#         log.critical(matchobj.groups())
        if matchobj.group("on_goto_statement"):
            return self._replace_on_goto(matchobj)
        else:
            return self._replace_statement(matchobj)

    def create_renum_dict(self, ascii_listing):
        old_numbers = [match[0] for match in self.line_no_regex.findall(ascii_listing)]
        renum_dict = {}
        for new_number, old_number in enumerate(old_numbers, 1):
            new_number *= 10
            renum_dict[old_number] = new_number
        return renum_dict


if __name__ == "__main__":
    from dragonlib.api import Dragon32API

    api = Dragon32API()
    listing = """\
1 PRINT "ONE"
2 ON X GOSUB 1,12 , 14 , 15,455 ' foo
11 GOTO 12
12 PRINT "FOO":GOSUB 15
14 IF A=1 THEN 20 ELSE 1
15 PRINT "BAR"
16 RESUME
20 PRINT "END?"
30 GOTO 123 ' didn't exist
"""
    print listing
    print "-"*79
    print api.renum_ascii_listing(listing)
