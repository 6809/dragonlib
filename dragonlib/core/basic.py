#!/usr/bin/env python
# encoding:utf8

"""
    DragonPy - Dragon 32 emulator in Python
    =======================================

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import logging
import re

from dragonlib.core import basic_parser
from dragonlib.utils import six
from dragonlib.utils.iter_utils import list_replace
from dragonlib.utils.logging_utils import pformat_byte_hex_list, \
    log_program_dump
from dragonlib.utils.byte_word_values import word2bytes


log = logging.getLogger(__name__)


class BasicTokenUtil(object):
    def __init__(self, basic_token_dict):
        self.basic_token_dict = basic_token_dict
        self.ascii2token_dict = dict([
            (code, token)
            for token, code in list(basic_token_dict.items())
        ])

        regex = r"(%s)" % "|".join([
            re.escape(statement)
            for statement in sorted(list(self.basic_token_dict.values()), key=len, reverse=True)
        ])
        self.regex = re.compile(regex)

    def token2ascii(self, value):
        try:
            result = self.basic_token_dict[value]
        except KeyError:
            if value > 0xff:
                log.info("ERROR: Token $%04x is not in BASIC_TOKENS!", value)
                return ""
            result = chr(value)
        if six.PY2:
            # Only for unittest, to avoid token representation as u"..."
            # There is only ASCII characters possible
            return str(result)
        else:
            return result

    def tokens2ascii(self, values):
        line=""
        old_value = None
        for value in values:
            if value == 0xff:
                old_value = value
                continue
            if old_value is not None:
                value = (old_value << 8) + value
                old_value = None
            code = self.token2ascii(value)
            line += code
        return line

    def chars2tokens(self, chars):
        return [ord(char) for char in chars]

    def ascii2token(self, ascii_code, debug=False):
        """
        TODO: replace no tokens in comments and strings
        """
        log.info(repr(ascii_code))
        parts = self.regex.split(ascii_code)
        log.info(repr(parts))
        tokens = []
        for part in parts:
            if not part:
                continue

            if part in self.ascii2token_dict:
                new_token = self.ascii2token_dict[part]
                log.info("\t%r -> %x", part, new_token)
                if new_token > 0xff:
                    tokens.append(new_token >> 8)
                    tokens.append(new_token & 0xff)
                else:
                    tokens.append(new_token)
            else:
                tokens += self.chars2tokens(part)
        return tokens

    def code_objects2token(self, code_objects):
        tokens = []
        for code_object in code_objects:
            if code_object.PART_TYPE == basic_parser.CODE_TYPE_CODE:
                # Code part
                content = code_object.content
                """
                NOTE: The BASIC interpreter changed REM shortcut and ELSE
                internaly:
                   "'" <-> ":'"
                "ELSE" <-> ":ELSE"

                See also:
                http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4310&p=11632#p11630
                """
                log.info("replace ' and ELSE with :' and :ELSE")
                content = content.replace("'", ":'")
                content = content.replace("ELSE", ":ELSE")
                tokens += self.ascii2token(content)
            else:
                # Strings, Comments or DATA
                tokens += self.chars2tokens(code_object.content)
        return tokens

    def iter_token_values(self, tokens):
        token_value = None
        for token in tokens:
            if token == 0xff:
                token_value = token
                continue

            if token_value is not None:
                yield (token_value << 8) + token
                token_value = None
            else:
                yield token

    def pformat_tokens(self, tokens):
        """
        format a tokenized BASIC program line. Useful for debugging.
        returns a list of formated string lines.
        """
        result = []
        for token_value in self.iter_token_values(tokens):
            char = self.token2ascii(token_value)
            if token_value > 0xff:
                result.append("\t$%04x -> %s" % (token_value, repr(char)))
            else:
                result.append("\t  $%02x -> %s" % (token_value, repr(char)))

        return result


class BasicLine(object):
    def __init__(self, token_util):
        self.token_util = token_util
        self.line_number = None
        self.line_code = None

        try:
            colon_token = self.token_util.ascii2token_dict[":"]
        except KeyError: # XXX: Always not defined as token?
            colon_token = ord(":")
        rem_token = self.token_util.ascii2token_dict["'"]
        else_token = self.token_util.ascii2token_dict["ELSE"]
        self.tokens_replace_rules = (
            ((colon_token, rem_token), rem_token),
            ((colon_token, else_token), else_token),
        )

    def token_load(self, line_number, tokens):
        self.line_number = line_number
        assert tokens[-1] == 0x00, "line code %s doesn't ends with \\x00: %s" % (
            repr(tokens), repr(tokens[-1])
        )

        """
        NOTE: The BASIC interpreter changed REM shortcut and ELSE
        internaly:
           "'" <-> ":'"
        "ELSE" <-> ":ELSE"

        See also:
        http://archive.worldofdragon.org/phpBB3/viewtopic.php?f=8&t=4310&p=11632#p11630
        """
        for src, dst in self.tokens_replace_rules:
            log.info("Relace tokens %s with $%02x",
                pformat_byte_hex_list(src), dst
            )
            log.debug("Before..: %s", pformat_byte_hex_list(tokens))
            tokens = list_replace(tokens, src, dst)
            log.debug("After...: %s", pformat_byte_hex_list(tokens))

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

    def code_objects_load(self, line_number, code_objects):
        self.line_number = line_number
        self.line_code = self.token_util.code_objects2token(code_objects)

    def get_tokens(self):
        """
        return two bytes line number + the code
        """
        return list(word2bytes(self.line_number)) + self.line_code

    def reformat(self):
        # TODO: Use BASICParser to exclude string/comments etc.
        space = self.token_util.ascii2token(" ")[0]

        to_split=self.token_util.basic_token_dict.copy()
        dont_split_tokens=self.token_util.ascii2token(":()+-*/^<=>")

        for token_value in dont_split_tokens:
            try:
                del(to_split[token_value])
            except KeyError: # e.g.: () are not tokens
                pass

        tokens=tuple(self.token_util.iter_token_values(self.line_code))

        temp = []
        was_token=False
        for no, token in enumerate(tokens):
            try:
                next_token=tokens[no+1]
            except IndexError:
                next_token=None

            if token in to_split:
                log.debug("X%sX" % to_split[token])

                try:
                    if temp[-1]!=space:
                        temp.append(space)
                except IndexError:
                    pass
                temp.append(token)

                if not (next_token and next_token in dont_split_tokens):
                    temp.append(space)
                was_token=True
            else:
                if was_token and token==space:
                    was_token=False
                    continue
                log.debug("Y%rY" % self.token_util.tokens2ascii([token]))
                temp.append(token)

        temp = list_replace(temp, self.token_util.ascii2token("GO TO"), self.token_util.ascii2token("GOTO"))
        temp = list_replace(temp, self.token_util.ascii2token("GO SUB"), self.token_util.ascii2token("GOSUB"))
        temp = list_replace(temp, self.token_util.ascii2token(": "), self.token_util.ascii2token(":"))
        temp = list_replace(temp, self.token_util.ascii2token("( "), self.token_util.ascii2token("("))
        temp = list_replace(temp, self.token_util.ascii2token(", "), self.token_util.ascii2token(","))

        self.line_code = temp


    def get_content(self, code=None):
        if code is None: # start
            code = self.line_code

        line = "%i " % self.line_number
        line += self.token_util.tokens2ascii(code)

        return line

    def __repr__(self):
        return "%r: %s" % (self.get_content(), " ".join(["$%02x" % t for t in self.line_code]))

    def log_line(self):
        log.critical("%r:\n\t%s",
            self.get_content(),
            "\n\t".join(self.token_util.pformat_tokens(self.line_code))
        )


class BasicListing(object):
    def __init__(self, basic_token_dict):
        self.token_util = BasicTokenUtil(basic_token_dict)

    def dump2basic_lines(self, dump, program_start, basic_lines=None):
        if basic_lines is None:
            basic_lines = []

        log.debug("progam start $%04x", program_start)
        try:
            next_address = (dump[0] << 8) + dump[1]
        except IndexError as err:
            log.debug("Can't get address: %s", err)
            return basic_lines

        log.debug("next_address: $%04x", next_address)
        if next_address == 0x0000:
            # program end
            log.debug("return: %s", repr(basic_lines))
            return basic_lines

        assert next_address > program_start, "Next address $%04x not bigger than program start $%04x ?!?" % (
            next_address, program_start
        )

        line_number = (dump[2] << 8) + dump[3]
        log.debug("line_number: %i", line_number)
        length = next_address - program_start
        log.debug("length: %i", length)
        tokens = dump[4:length]
        log.debug("tokens:\n\t%s", "\n\t".join(self.token_util.pformat_tokens(tokens)))

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
            line_tokens = line.get_tokens() + [0x00]

            current_address += len(line_tokens) + 2
            program_dump += word2bytes(current_address)
            if no == count: # It's the last line
                line_tokens += [0x00, 0x00]
            program_dump += line_tokens

        if six.PY3:
            return bytes(program_dump)
        else:
            return "".join(program_dump)

    def ascii_listing2basic_lines(self, txt):
        basic_lines = []
        for line in txt.splitlines():
            line = line.strip()
            if line:
                basic_line = BasicLine(self.token_util)
                basic_line.ascii_load(line)
                basic_lines.append(basic_line)
        return basic_lines

    def pformat_program_dump(self, program_dump, program_start, formated_dump=None):
        """
        format a BASIC program dump. Useful for debugging.
        returns a list of formated string lines.
        """
        if formated_dump is None:
            formated_dump = []
            formated_dump.append(
                "program start address: $%04x" % program_start
            )

        assert isinstance(program_dump, six.binary_type)

        try:
            next_address = (program_dump[0] << 8) + program_dump[1]
        except IndexError as err:
            raise IndexError(
                "Can't get next address from: %s program start: $%04x (Origin error: %s)" % (
                    repr(program_dump), program_start, err
            ))

        if next_address == 0x0000:
            formated_dump.append("$%04x -> end address" % next_address)
            return formated_dump

        assert next_address > program_start, "Next address $%04x not bigger than program start $%04x ?!?" % (
            next_address, program_start
        )

        length = next_address - program_start
        formated_dump.append(
            "$%04x -> next address (length: %i)" % (next_address, length)
        )
        line_number = (program_dump[2] << 8) + program_dump[3]
        formated_dump.append("$%04x -> %i (line number)" % (line_number, line_number))

        tokens = program_dump[4:length]
        formated_dump.append("tokens:")
        formated_dump += self.token_util.pformat_tokens(tokens)

        return self.pformat_program_dump(program_dump[length:], next_address, formated_dump)

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


#     def parsed_lines2program_dump(self, parsed_lines, program_start):
#         for line_no, code_objects in sorted(parsed_lines.items()):
#             for code_object in code_objects:


    def program_dump2ascii_lines(self, dump, program_start):
        basic_lines = self.dump2basic_lines(dump, program_start)
        log.info("basic_lines: %s", repr(basic_lines))
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
        for new_number, line in enumerate(self._iter_lines(ascii_listing), 1):
            new_number *= 10
            line = self.line_no_regex.sub("%s\g<code>" % new_number, line)
            new_line = self.renum_regex.sub(self.renum_inline, line)
            log.debug("%r -> %r", line, new_line)
            new_listing.append(new_line)
        return "\n".join(new_listing)

    def get_destinations(self, ascii_listing):
        """
        returns all line numbers that are used in a jump.
        """
        self.destinations = set()
        def collect_destinations(matchobj):
            numbers = matchobj.group("no")
            if numbers:
                self.destinations.update(set(
                    [n.strip() for n in numbers.split(",")]
                ))

        for line in self._iter_lines(ascii_listing):
            self.renum_regex.sub(collect_destinations, line)

        return sorted([int(no) for no in self.destinations if no])

    def _iter_lines(self, ascii_listing):
        lines = ascii_listing.splitlines()
        lines = [line.strip() for line in lines if line.strip()]
        for line in lines:
            yield line

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

    def renum_inline(self, matchobj):
#         log.critical(matchobj.groups())
        old_numbers = matchobj.group("no")
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
            matchobj.group("statement"),
            matchobj.group("space"),
            ",".join(new_numbers), space_after
        ])

    def create_renum_dict(self, ascii_listing):
        old_numbers = [match[0] for match in self.line_no_regex.findall(ascii_listing)]
        renum_dict = {}
        for new_number, old_number in enumerate(old_numbers, 1):
            new_number *= 10
            renum_dict[old_number] = new_number
        return renum_dict


def _test_renum():
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
    print(listing)
    print("-" * 79)
    print(api.renum_ascii_listing(listing))
    print("-" * 79)
    print(api.renum_tool.get_destinations(listing))
    print("-" * 79)


def _test_reformat():
    from dragonlib.utils.logging_utils import setup_logging

    setup_logging(
#        level=1 # hardcore debug ;)
#         level=10  # DEBUG
#         level=20  # INFO
#         level=30  # WARNING
#         level=40 # ERROR
#         level=50 # CRITICAL/FATAL
        level=99
    )

    from dragonlib.api import Dragon32API
    api = Dragon32API()

    # filepath = os.path.join(os.path.abspath(os.path.dirname(__file__)),
    #     # "..", "BASIC examples", "hex_view01.bas"
    #     "..", "..", "BASIC games", "INVADER.bas"
    # )
    #
    # with open(filepath, "r") as f:
    #     listing_ascii = f.read()

    listing_ascii="""\
10 ONPOINT(Y,K)GOTO250,250'ONPOINT(Y,K)GOTO250,250
20 FORT=479TO 542:T(T)=0:Y(T)=28:NEXT
30 I=I+1:PRINT"FORX=1TO 2:Y(Y)=0:NEXT"
730 CLS:PRINT"FIXME: PLEASE WAIT [           ]";
"""

    print(
        api.reformat_ascii_listing(listing_ascii)
    )

if __name__ == "__main__":
    # _test_renum()
    _test_reformat()
