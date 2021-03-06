#! /usr/bin/env python
# ______________________________________________________________________
"""test_regex.py

Unit tests for the basil.lang.regex module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import dis
import unittest
from basil.lang.mython.MyFrontUtils import toplevel_compile
from basil.lang.mython import myimport
myimport.install_import_hook()

# ______________________________________________________________________
# Test case definitions

class TestMythonRegex (unittest.TestCase):
    def _getmyre0 (self):
        mython_module_path = os.path.join(os.path.split(__file__)[0],
                                          "test_regex01.my")
        
        module_co, _ = toplevel_compile(mython_module_path)
        if __debug__:
            dis.dis(module_co)
        exec module_co
        return myre0

    def testmatch (self):
        myre0 = self._getmyre0()
        test_str = "you only need two \\ to match one backslash"
        match_obj = myre0.match(test_str)
        self.failUnless(match_obj)
        self.assertEquals(match_obj.group(), test_str)

    def testmatchfail (self):
        myre0 = self._getmyre0()
        test_str = "you only need two \\\\ to match one backslash"
        match_obj = myre0.match(test_str)
        self.assertEquals(match_obj, None)

    def testmatch02 (self):
        import test_regex02
        self.assertEquals(test_regex02.ex1.match('works').string, "works" )
        self.assertEquals(test_regex02.ex2.match('CraZyneSs').string, 'CraZyneSs')

    def testmatchfail02 (self):
        import test_regex02
        self.assertEquals(test_regex02.ex1.match('Works'), None)
        self.assertEquals(test_regex02.ex2.match('123'), None)

# ______________________________________________________________________

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_regex.py
