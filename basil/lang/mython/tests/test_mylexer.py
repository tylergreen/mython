#! /usr/bin/env python
# ______________________________________________________________________
"""Script test_mylexer.py

Unit tests for the basil.lang.mython.mylexer module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os.path
import unittest
import pprint

from basil.lang.mython import mylexer

# ______________________________________________________________________
# Test case definitions

class TestMythonScanner (unittest.TestCase):
    def setUp (self):
        self.path = os.path.split(__file__)[0]

    def _testscanfile (self, filename):
        file_obj = open(os.path.join(*(self.path, filename)))
        toklist = mylexer.scan_mython_file(file_obj)
        file_obj.close()
        if __debug__:
            pprint.pprint(toklist)
        self.assert_(toklist)

    def testmython04 (self):
        self._testscanfile('test04.my')

    def testmython05 (self):
        self._testscanfile('test05.my')

    def testmython06 (self):
        self._testscanfile('test06.my')

# ______________________________________________________________________
# Main routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_mylexer.py
