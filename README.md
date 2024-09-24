# Dragon/CoCO Python Library

[![tests](https://github.com/6809/dragonlib/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/6809/dragonlib/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/jedie/dragonlib/branch/main/graph/badge.svg)](https://app.codecov.io/github/jedie/dragonlib)
[![dragonlib @ PyPi](https://img.shields.io/pypi/v/dragonlib?label=dragonlib%20%40%20PyPi)](https://pypi.org/project/dragonlib/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dragonlib)](https://github.com/6809/dragonlib/blob/main/pyproject.toml)
[![License GPL-3.0-or-later](https://img.shields.io/pypi/l/dragonlib)](https://github.com/6809/dragonlib/blob/main/LICENSE)

Python Modules/Tools Open source (GPL v3 or later) for 6809 based homecomputer like:

* [Dragon 32](http://en.wikipedia.org/wiki/Dragon_32)
* [Tandy TRS-80 Color Computer](http://en.wikipedia.org/wiki/TRS-80_Color_Computer) (CoCo)

Used in:

* [DragonPy](https://github.com/jedie/DragonPy) - Emulator for 6809 CPU based system like Dragon 32 / CoCo written in Python:
* [DwLoadServer](https://github.com/DWLOAD/DwLoadServer) - DWLOAD server implemented in Python


## Start hacking

```shell
~$ git clone https://github.com/6809/dragonlib.git
~$ cd dragonlib
~/dragonlib$ ./cli.py --help
```
Looks like:
[comment]: <> (✂✂✂ auto generated main help start ✂✂✂)
```
Usage: ./cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ update-readme-history      Update project history base on git commits/tags in README.md          │
│ version                    Print version and exit                                                │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated main help end ✂✂✂)

TODO: Expand the CLI ;)


### Development CLI

Start the dev CLI, e.g.:
```shell
~/dragonlib$ ./dev-cli.py --help
```
Looks like:

[comment]: <> (✂✂✂ auto generated dev help start ✂✂✂)
```
Usage: ./dev-cli.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────╮
│ --help      Show this message and exit.                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────╮
│ check-code-style            Check code style by calling darker + flake8                          │
│ coverage                    Run tests and show coverage report.                                  │
│ fix-code-style              Fix code style of all cli_base source code files via darker          │
│ install                     Run pip-sync and install 'cli_base' via pip as editable.             │
│ mypy                        Run Mypy (configured in pyproject.toml)                              │
│ pip-audit                   Run pip-audit check against current requirements files               │
│ publish                     Build and upload this project to PyPi                                │
│ test                        Run unittests                                                        │
│ tox                         Run tox                                                              │
│ update                      Update "requirements*.txt" dependencies files                        │
│ update-test-snapshot-files  Update all test snapshot files (by remove and recreate all snapshot  │
│                             files)                                                               │
│ version                     Print version and exit                                               │
╰──────────────────────────────────────────────────────────────────────────────────────────────────╯
```
[comment]: <> (✂✂✂ auto generated dev help end ✂✂✂)



## History

[comment]: <> (✂✂✂ auto generated history start ✂✂✂)

* [v0.2.0](https://github.com/6809/dragonlib/compare/v0.1.7...v0.2.0)
  * 2024-09-24 - Setup README and tests for it
  * 2024-09-24 - Add github action
  * 2024-09-24 - Activate pre-commit hooks on install
  * 2024-09-24 - Reformat with black and fix old code parts
  * 2024-09-24 - Add .editorconfig
  * 2024-09-24 - Run pyupgrade
  * 2024-09-24 - Modernize Project Setup
* [v0.1.7](https://github.com/6809/dragonlib/compare/v0.1.6...v0.1.7)
  * 2015-08-21 - Bugfix logging, remove six and code cleanup
  * 2015-08-19 - remove obsolete code + run tests also with pypy3
* [v0.1.6](https://github.com/6809/dragonlib/compare/v0.1.5...v0.1.6)
  * 2015-08-19 - +AUTHORS
  * 2015-08-19 - add test for BasicLexer
  * 2015-08-19 - use nose to run unittests
  * 2015-08-19 - update travis config
  * 2015-08-19 - Bugfix disable logging:
* [v0.1.5](https://github.com/6809/dragonlib/compare/v0.1.4...v0.1.5)
  * 2015-05-26 - fixup! WIP: support PY2, too
  * 2015-05-26 - WIP: support PY2, too
  * 2015-05-26 - TODO: Add Support for Python 2 and PyPy
  * 2015-05-26 - disable pypy test :(

<details><summary>Expand older history entries ...</summary>

* [v0.1.4](https://github.com/6809/dragonlib/compare/v0.1.3...v0.1.4)
  * 2015-05-26 - bugfix for ReSt
  * 2015-05-26 - TODO python 2 support!
  * 2015-05-26 - add "publish" in setup.py
  * 2015-05-26 - add links to travis/coveralls
  * 2015-05-26 - add a AUTOLOAD.DWL for unittest
  * 2015-05-26 - Bugfix: don't print new lines etc.
  * 2015-05-26 - exclude undone test
  * 2015-05-26 - test_suite="dragonlib.tests.get_tests"
  * 2015-05-26 - update meta files
* [v0.1.3](https://github.com/6809/dragonlib/compare/v0.1.2...v0.1.3)
  * 2014-12-15 - add a pygments lexer
  * 2014-11-20 - better error message
  * 2014-11-20 - use string.printable
* [v0.1.2](https://github.com/6809/dragonlib/compare/v0.1.1...v0.1.2)
  * 2014-11-19 - Bugfix/enhanced the whole binary stuff and add more unittests
  * 2014-11-18 - WIP: add unittest for BinaryFile()
  * 2014-11-18 - bugfix in log_bytes()
  * 2014-11-18 - Bugfix parse binary files
  * 2014-11-17 - FIXME
  * 2014-11-17 - that's enough
  * 2014-11-17 - more robust
  * 2014-11-17 - less debug
  * 2014-11-17 - display log settings
* [v0.1.1](https://github.com/6809/dragonlib/compare/5030bac...v0.1.1)
  * 2014-11-15 - lower some log output
  * 2014-11-15 - add api.bas2bin() too
  * 2014-11-15 - Add for converting Dragon DOS Binary to ASCII listing
  * 2014-11-13 - create a package
  * 2014-11-13 - update README
  * 2014-11-13 - Initial commit
  * 2014-11-13 - move LOG_LEVELS
  * 2014-09-30 - WIP: BASIC editor: reformat code
  * 2014-09-30 - add more info
  * 2014-09-30 - Bugfix
  * 2014-09-30 - Bugfix renum tool + renum INVADER.bas
  * 2014-09-30 - Bugfix if line number > $ff
  * 2014-09-30 - Add a more informative "display tokens" window
  * 2014-09-22 - Don't raise error, if dump doesn't include address...
  * 2014-09-22 - Better default log formatter
  * 2014-09-18 - change logging setup
  * 2014-09-13 - Update unittests in dragonlib, too.
  * 2014-09-13 - bugfix six.moves.xrange
  * 2014-09-13 - use xrange from six.py
  * 2014-09-12 - replace own lib2and3 with six
  * 2014-09-12 - WIP: refactor logging usage
  * 2014-09-11 - better tracebacks by using reraise
  * 2014-09-04 - remove from __future__ import unicode_literals
  * 2014-09-04 - bugfix string.letters vs. string.ascii_letters
  * 2014-09-03 - chnages to support python 2 and 3 with the same code
  * 2014-09-03 - changes to run with python2 and __future__ imports
  * 2014-09-03 - just run 2to3 script
  * 2014-08-28 - Highlight line numbers and more the just one
  * 2014-08-28 - First, simple code highlighting
  * 2014-08-28 - Don't consume spaces between line number and code
  * 2014-08-27 - reimplement the CLI, today only for Dragon32/64 and CoCo
  * 2014-08-27 - Bugfix: CoCo used the same default start address
  * 2014-08-27 - update CoCo tokens with Extended Color BASIC 1.1
  * 2014-08-20 - CoCo used a other default program start address than dragon
  * 2014-08-20 - +    0xff80: "SGN"
  * 2014-08-20 - WIP: Support CoCo in editor
  * 2014-08-20 - do the ' <-> :' and ELSE <-> :ELSE replacement internaly
  * 2014-08-20 - Use the new BASIC parser - TODO: Code cleanup!
  * 2014-08-20 - convert line number to int
  * 2014-08-20 - rename format functions
  * 2014-08-20 - add a BASIC parser with unittests
  * 2014-08-20 - code formating
  * 2014-08-18 - Add TODO unittests
  * 2014-08-18 - Better debug output
  * 2014-08-18 - better log output while load/inject BASIC program
  * 2014-08-18 - Bugfix: support ON...GOTO and ON...GOSUB in renumbering
  * 2014-08-17 - add another renum unittest +code cleanup
  * 2014-08-17 - add "renumber listing" tool in editor
  * 2014-08-17 - TODO: Don't replace reversed words into tokens in comments and strings.
  * 2014-08-16 - Bugfix in inject BASIC program:
  * 2014-08-16 - WIP: move dump/load stuff into editor
  * 2014-08-15 - WIP: start splitting project: add "dragonlib"

</details>


[comment]: <> (✂✂✂ auto generated history end ✂✂✂)
