#!/usr/bin/env python

"""
    loggin utilities
    ~~~~~~~~~~~~~~~~

    :created: 2014 by Jens Diemer - www.jensdiemer.de
    :copyleft: 2014 by the DragonPy team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""


import logging
import sys

from dragonlib.utils.byte_word_values import bin2hexline


log = logging.getLogger(__name__)


# log.critical("Log handlers: %s", repr(log.handlers))
# if len(log.handlers) > 1:  # FIXME: tro avoid doublicated output
#     log.handlers = (log.handlers[0],)
#     log.critical("Fixed Log handlers: %s", repr(log.handlers))


def get_log_levels(additional_levels=None):
    if additional_levels is None:
        levels = [100, 99]
    else:
        levels = additional_levels.copy()
    levels += logging._nameToLevel.values()
    levels.sort()
    return levels


LOG_LEVELS = get_log_levels()


def set_handler(logger, handler):
    """
    Remove all existing log handler and set
    only the given handler.
    """
    logger.handlers = []
    logger.addHandler(handler)


def setup_logging(level, logger_name=None, handler=None, log_formatter=None):
    """
    levels:
         1 - hardcode DEBUG ;)
        10 - DEBUG
        20 - INFO
        30 - WARNING
        40 - ERROR
        50 - CRITICAL/FATAL
        99 - nearly off
       100 - complete off
    """
    root_logger = logging.getLogger()

    if logger_name is None:
        logger = root_logger
        root_logger.info("Set %i level to root logger", level)
    else:
        logger = logging.getLogger(logger_name)
        root_logger.info("Set %i level to logger %r", level, logger_name)

    if level == 100:
        # Remove all existing handlers and set only NullHandler():
        set_handler(logger, logging.NullHandler())
        logger.disabled = True
        return

    logger.setLevel(level=level)

    if log_formatter is None:
        log_formatter = "%(relativeCreated)-5d %(levelname)8s %(module)13s %(lineno)d %(message)s"
    formatter = logging.Formatter(log_formatter)

    if handler is None:
        handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    if hasattr(handler, "baseFilename"):
        root_logger.debug("Log to file: %s (%s)", handler.baseFilename, repr(handler))
    else:
        root_logger.debug("Log to handler: %s", repr(handler))

    # Remove all existing handlers and set only the given handler:
    set_handler(logger, handler)

    log.log(level, "Set logging to level %i %s", level, logging.getLevelName(level))


def log_memory_dump(memory, start, end, mem_info, level=99):
    log.log(level, "Memory dump from $%04x to $%04x:", start, end)

    for addr in range(start, end + 1):
        value = memory[addr]
        if isinstance(value, int):
            msg = "$%04x: $%02x (dez: %i)" % (addr, value, value)
        else:
            msg = f"${addr:04x}: {repr(value)} (is type: {type(value)})"
        msg = "%-25s| %s" % (msg, mem_info.get_shortest(addr))
        log.log(level, "\t%s", msg)


def pformat_hex_list(hex_list):
    return " ".join(["$%x" % v for v in hex_list])


def pformat_byte_hex_list(hex_list):
    return " ".join(["$%02x" % v for v in hex_list])


def pformat_word_hex_list(hex_list):
    return " ".join(["$%02x" % v for v in hex_list])


def log_hexlist(byte_list, group=8, start=0x0000, level=99):
    def _log(level, addr, line):
        msg = pformat_byte_hex_list(line)
        msg = f"{addr:04x} - {msg}"
        log.log(level, msg)

    pos = 0
    addr = start
    line = []
    for value in byte_list:
        pos += 1
        line.append(value)
        if pos >= group:
            _log(level, addr, line)
            addr += pos
            pos = 0
            line = []
    _log(level, addr, line)


def pformat_program_dump(ram_content):
    msg = pformat_byte_hex_list(ram_content)
    msg = msg.replace("$00 ", "\n$00\n")
    return msg


def log_program_dump(ram_content, level=99):
    msg = "BASIC program dump:\n"
    msg += pformat_program_dump(ram_content)
    log.log(level, msg)


def log_bytes(data, msg="%s", level=logging.DEBUG):
    data = bytearray(data)
    data = " ".join(["%02X" % item for item in data])
    log.log(level, msg, data)


def log_hexlines(data, msg="Data:", level=logging.DEBUG, width=16):
    log.log(level, msg)
    for line in bin2hexline(data, width):
        log.log(level, line)


def test_run():
    import os
    import subprocess

    cmd_args = [
        sys.executable,
        os.path.join("..", "DragonPy_CLI.py"),
        #         "-h"
        #         "--log_list",
        "--verbosity",
        "50",
        "--log",
        "DragonPy.cpu6809,50;dragonpy.Dragon32.MC6821_PIA,40",
        #         "--verbosity", " 1", # hardcode DEBUG ;)
        #         "--verbosity", "10", # DEBUG
        #         "--verbosity", "20", # INFO
        #         "--verbosity", "30", # WARNING
        #         "--verbosity", "40", # ERROR
        #         "--verbosity", "50", # CRITICAL/FATAL
        #         "--verbosity", "99", # nearly all off
        "--machine",
        "Dragon32",
        "run",
        #        "--machine", "Vectrex", "run",
        #        "--max_ops", "1",
        #        "--trace",
    ]
    print("Startup CLI with: %s" % " ".join(cmd_args[1:]))
    subprocess.Popen(cmd_args, cwd="..").wait()


if __name__ == "__main__":
    dump = (
        0x1E,
        0x07,
        0x00,
        0x0A,
        0xA0,
        0x00,
        0x1E,
        0x1A,
        0x00,
        0x14,
        0x80,
        0x20,
        0x49,
        0x20,
        0xCB,
        0x20,
        0x30,
        0x20,
        0xBC,
        0x20,
        0x32,
        0x35,
        0x35,
        0x3A,
        0x00,
        0x1E,
        0x2D,
        0x00,
        0x1E,
        0x93,
        0x20,
        0x31,
        0x30,
        0x32,
        0x34,
        0xC3,
        0x28,
        0x49,
        0xC5,
        0x32,
        0x29,
        0x2C,
        0x49,
        0x00,
        0x1E,
        0x35,
        0x00,
        0x28,
        0x8B,
        0x20,
        0x49,
        0x00,
        0x1E,
        0x4E,
        0x00,
        0x32,
        0x49,
        0x24,
        0x20,
        0xCB,
        0x20,
        0xFF,
        0x9A,
        0x3A,
        0x85,
        0x20,
        0x49,
        0x24,
        0xCB,
        0x22,
        0x22,
        0x20,
        0xBF,
        0x20,
        0x35,
        0x30,
        0x00,
        0x00,
        0x00,
    )
    log_hexlist(dump)
    #    log_hexlist(dump, group=4)
    #    log_hexlist(dump, group=5)

    test_run()
