#!/usr/bin/env python
# coding: utf-8

"""
    distutils setup
    ~~~~~~~~~~~~~~~

    :copyleft: 2014 by the DragonLib team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, division, print_function

from setuptools import setup, find_packages
import os
import sys

import dragonlib

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))


if "publish" in sys.argv:
    import subprocess
    args = [sys.executable or "python", "setup.py", "sdist", "bdist_wheel", "upload"]
    print("\nCall: %r\n" %  " ".join(args))
    subprocess.call(args)

    print("\nDon't forget to tag this version, e.g.:")
    print("\tgit tag v%s" % dragonlib.__version__)
    print("\tgit push --tags")
    sys.exit()


# convert creole to ReSt on-the-fly, see also:
# https://code.google.com/p/python-creole/wiki/UseInSetup
try:
    from creole.setup_utils import get_long_description
except ImportError as err:
    if "check" in sys.argv or "register" in sys.argv or "sdist" in sys.argv or "--long-description" in sys.argv:
        raise ImportError("%s - Please install python-creole >= v0.8 -  e.g.: pip install python-creole" % err)
    long_description = None
else:
    long_description = get_long_description(PACKAGE_ROOT)


setup(
    name="dragonlib",
    version=dragonlib.__version__,
    py_modules=["dragonlib"],
    provides=["dragonlib"],
    author="Jens Diemer",
    author_email="dragonlib@jensdiemer.de",
    description="Library around 6809 computers like Dragon 32/64, CoCo...",
    keywords="6809 Dragon CoCo",
    long_description=long_description,
    url="https://github.com/6809/dragonlib",
    license="GPL v3+",
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: System :: Emulators",
        "Topic :: Software Development :: Assemblers",
        "Topic :: Software Development :: Testing",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite="dragonlib.tests.get_tests",
)
