#! /usr/bin/env python
# ______________________________________________________________________
"""Scropt test_myparser

Unit tests for the basil.lang.mython.myparser module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import unittest

from basil.lang.mython import myparser
from basil.lang.mython.tests import test_mylexer

# ______________________________________________________________________
# Class definition

class TestMyComposedParser (unittest.TestCase):
    def setUp (self):
        self.path = os.path.split(__file__)[0]

    def _test_parse_file (self, filename):
        filepath = os.path.join(self.path, filename)
        self.assert_(myparser.MyComposedParser().parse_file(filepath))

    def test_mython_01 (self):
        self._test_parse_file('test01.my')

    def test_mython_02 (self):
        self._test_parse_file('test02.my')

    def test_mython_03 (self):
        self._test_parse_file('test03.my')

    def test_mython_04 (self):
        self._test_parse_file('test04.my')

    def test_mython_12 (self):
        self._test_parse_file('test12.my')

    def test_mython_13 (self):
        self._test_parse_file('test13.my')

    def test_parse_string (self):
        self.assert_(myparser.MyComposedParser().parse_string(
            test_mylexer.QUOTED_TEST_STR))

# ______________________________________________________________________
# Main routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_myparser.py
