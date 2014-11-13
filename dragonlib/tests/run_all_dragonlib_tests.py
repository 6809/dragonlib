#!/usr/bin/env python

"""
    DragonLib
    =========

    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

import unittest

from dragonlib.utils.unittest_utils import TextTestRunner2


if __name__ == "__main__":
    loader = unittest.TestLoader()
    tests = loader.discover('dragonlib')

    test_runner = TextTestRunner2(verbosity=2,
#         failfast=True,
    )

    test_runner.run(tests)
    print(" --- END --- ")