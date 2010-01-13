#! /usr/bin/env python
# ______________________________________________________________________
"""test_cheetah.py

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import new
import dis
import sys
import unittest

try:
    import Cheetah
except ImportError:
    Cheetah = None

from basil.lang.mython.MyFrontUtils import toplevel_compile

# ______________________________________________________________________
# Test case definitions

class TestMythonCheetah (unittest.TestCase):
    def _get_module (self):
        mython_module_path = os.path.join(os.path.split(__file__)[0],
                                          "test_cheetah01.my")
        module_co, _ = toplevel_compile(mython_module_path)
        if __debug__:
            dis.dis(module_co)
        module = new.module("test_cheetah01")
        eval(module_co, module.__dict__)
        return module

    def testProofOfConcept (self):
        if Cheetah is None:
            if __debug__:
                print("Optional Cheetah library not installed; skipping "
                      "tests...")
        else:
            module = self._get_module()
            self.failUnless(module.template)
            self.failUnlessEqual(str(module.template([module.__dict__])),
                                 str(module.etemplate))

# ______________________________________________________________________


if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_cheetah.py
