#! /usr/bin/env python
# ______________________________________________________________________
"""Module test_mybuiltins

Unit tests for the basil.lang.mython.mybuiltins module.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import unittest

from basil.lang.mython import mybuiltins
from basil.lang.mython import MyFrontExceptions

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________
# Class (test case) definitions

class TestMyBuiltins (unittest.TestCase):
    def setUp (self):
        self.path = os.path.split(__file__)[0]

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

    def _test_myfrontend_bad (self, filename):
        source = open(os.path.join(self.path, filename)).read()
        try:
            mybuiltins.myfrontend(source, mybuiltins.initial_environment())
            self.failUnless(False, "The previous line should have thrown an "
                            "exception.")
        except MyFrontExceptions.MyFrontCompileTimeError, ct_err:
            embedded_exception = ct_err.args[0][1]
            self.failUnless(type(embedded_exception) ==
                            MyFrontExceptions.MyFrontSyntaxError)
            # XXX I don't know how brittle this is if we ever change
            # the syntax error message:
            msg = embedded_exception.args[0].split()
            line_index = msg.index('line') + 1
            line_no = int(msg[line_index][:-1])
            column_index = msg.index('column') + 1
            column_no = int(msg[column_index][:-1])
            unexpected_index = msg.index('unexpected') + 1
            unexpected_str = eval(msg[unexpected_index][:-1])
            source_line = source.split("\n")[line_no - 1]
            source_str = source_line[column_no:column_no +
                                     len(unexpected_str)]
            if __DEBUG__:
                print line_no, column_no, `source_line`,
                print `source_line[column_no - 1:]`, `unexpected_str`
            self.failUnlessEqual(source_str, unexpected_str)

    def test_myfrontend_bad_01 (self):
        self._test_myfrontend_bad("bad01.my")

    def test_myfrontend_bad_02 (self):
        self._test_myfrontend_bad("bad02.my")

# ______________________________________________________________________
# Main (test) routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_mybuiltins.py
