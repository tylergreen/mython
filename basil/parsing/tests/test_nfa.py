#! /usr/bin/env python
# ______________________________________________________________________
"""Script test_nfa.py

Unit tests for the basil.parsing.nfa module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import unittest

from basil.parsing import PgenParser, PyPgen, nfa

# ______________________________________________________________________
# Class definitions

class TestNFA (unittest.TestCase):
    def test_simple_compose (self):
        testpath = os.path.split(__file__)[0]
        gobj1 = PyPgen.PyPgen().handleStart(
            PgenParser.parseFile(os.path.join(testpath, 'test.pgen')))
        gobj2 = PyPgen.PyPgen().handleStart(
            PgenParser.parseFile(os.path.join(testpath, 'ext.pgen')))
        gobj3 = nfa.compose_nfas(gobj1, gobj2)
        self.assertTrue(gobj3)
        self.assertEqual(len(gobj3[0]), len(gobj1[0]))
        self.assertNotEqual(gobj3[0], gobj1[0])

# ______________________________________________________________________
# Main routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_nfa.py
