#! /usr/bin/env python
# ______________________________________________________________________
"""test_basil.py

Unit testing script for the Basil framework.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import unittest

from basil.parsing.tests.test_trampoline \
     import TestTrampolineParser, TestPgenToHandler
from basil.parsing.tests.test_nfa import TestNFA
from basil.lang.mython.tests.test_mylexer import TestMythonScanner
from basil.lang.mython.tests.test_myparser import TestMyComposedParser
from basil.lang.mython.tests.test_mybuiltins import TestMyBuiltins
from basil.lang.mython.tests.test_myimport import TestMyImport
from basil.lang.tests.test_regex import TestMythonRegex
from basil.lang.tests.test_cheetah import TestMythonCheetah

# ______________________________________________________________________

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_basil.py
