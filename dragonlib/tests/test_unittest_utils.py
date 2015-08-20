import unittest
import six
import sys
from dragonlib.tests.test_base import BaseTestCase
from dragonlib.utils.unittest_utils import StdoutStderrBuffer


class TestStdoutStderrBuffer(BaseTestCase):
    def test_text_type(self):
        with StdoutStderrBuffer() as buffer:
            print(six.text_type("print text_type"))
            sys.stdout.write(six.text_type("stdout.write text_type\n"))
            sys.stderr.write(six.text_type("stderr.write text_type"))
        self.assertEqual_dedent(buffer.get_output(), """
            print text_type
            stdout.write text_type
            stderr.write text_type
        """)

    def test_binary_type(self):
        if six.PY2:
            with StdoutStderrBuffer() as buffer:
                print("print str")
                sys.stdout.write("stdout.write str\n")
                sys.stderr.write("stderr.write str")
            self.assertEqual_dedent(buffer.get_output(), """
                print str
                stdout.write str
                stderr.write str
            """)
        elif six.PY3:
            # The print function will use repr
            with StdoutStderrBuffer() as buffer:
                print(b"print binary_type")
                sys.stdout.write(b"stdout.write binary_type\n")
                sys.stderr.write(b"stderr.write binary_type")
            self.assertEqual_dedent(buffer.get_output(), """
                b'print binary_type'
                stdout.write binary_type
                stderr.write binary_type
            """)
        else:
            self.fail()