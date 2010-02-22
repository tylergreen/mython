#! /usr/bin/env python
# ______________________________________________________________________
"""Module test_mybuiltins

Unit tests for the basil.lang.mython.mybuiltins module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import unittest

from basil.lang.mython import mybuiltins

# ______________________________________________________________________
# Class (test case) definitions

class TestMyBuiltins (unittest.TestCase):
    def test_makequote (self):
        DUMMY_VALUE = 99
        def myprocessor (source):
            return DUMMY_VALUE
        env = mybuiltins.initial_environment()
        env["myquote"] = env["makequote"](myprocessor)
        _, env = env["myfront"](None, "quote [myquote] myval: anything\n\n",
                                env)
        self.assertEquals(env["myval"], DUMMY_VALUE)
        del env["myval"]
        _, env = env["myfront"](None, "quote [myquote]:\n\tno, really, "
                                "anything.\n\n", env)
        self.failUnlessRaises(KeyError, env.__getitem__, "myval")

    def test_makequote_with_mutation (self):
        DUMMY_VALUE = "kookamungous"
        def myotherprocessor (source, env):
            if "sideeffectuals" in env:
                env["sideeffectuals"]["otherval"] = DUMMY_VALUE
            return DUMMY_VALUE, env
        env = mybuiltins.initial_environment()
        env["sideeffectuals"] = {}
        env["myquote2"] = mybuiltins.makequote(myotherprocessor, True)
        _, env = env["myfront"](None, "quote [myquote2] myval2: anything2\n\n",
                                env)
        self.assertEquals(env["myval2"], env["sideeffectuals"]["otherval"])
        self.assertEquals(env["myval2"], DUMMY_VALUE)
        del env["myval2"]
        env["sideeffectuals"] = {}
        _, env = env["myfront"](None, "quote [myquote2]:\n\tI'm serious,\n\t"
                                "anything.\n\n", env)
        self.assertEquals(env["sideeffectuals"]["otherval"], DUMMY_VALUE)
        self.failUnlessRaises(KeyError, env.__getitem__, "myval2")

    def test_makedesugar (self):
        raise NotImplementedError()

# ______________________________________________________________________
# Main (test) routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_mybuiltins.py
