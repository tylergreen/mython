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
import StringIO

from basil.lang.mython import mylexer

# ______________________________________________________________________
# Module data

QUOTED_TEST_STR = """quote [dummystuff[1:4]]:
    testing
    some
    stuff

def and_then_something_else (*args, **kws):
    return 99.3
"""

BAD_QUOTE_INDENT_STR = """def eggs (*args, **kws):
    quote rv:
  this_is_a_bad_quote_block()
  this_is_a_very_bad_quote_block()
    return rv
"""

MULTILINE_QUOTE_ARG_STR = """quote [
this_is_legal_but_not_pretty()
                         ]:
    sure_enough;
"""

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

    def _testscanpyfile (self, filename):
        filepath = os.path.join(*(self.path, filename))
        file_obj = open(filepath)
        toklist1 = mylexer.scan_python_file(file_obj.next)
        file_obj.seek(0)
        toklist2 = mylexer.scan_python_file(file_obj.next,
                                            mylexer.tokenize.generate_tokens)
        file_obj.close()
        self.assertEquals(len(toklist1), len(toklist2))
        for tok1, tok2 in zip(toklist1, toklist2):
            self.assertEquals(tok1, tok2)

    def testmython01 (self):
        self._testscanfile('test01.my')

    def testmython02 (self):
        self._testscanfile('test02.my')

    def testmython03 (self):
        self._testscanfile('test03.my')

    def testmython04 (self):
        self._testscanfile('test04.my')

    def testmython05 (self):
        self._testscanfile('test05.my')

    def testmython06 (self):
        self._testscanfile('test06.my')

    def testmython12 (self):
        self._testscanfile('test12.my')

    def testmython13 (self):
        self._testscanfile('test13.my')

    def testmylexer (self):
        self._testscanpyfile(os.path.join('..', 'mylexer.py'))

    def testself (self):
        self._testscanpyfile('test_mylexer.py')

    def testquotation (self):
        sio_obj = StringIO.StringIO(QUOTED_TEST_STR)
        toks = mylexer.scan_mython_file(sio_obj)
        sio_obj.close()
        quoted_toks = [tok for tok in toks if tok[0] == mylexer.QUOTED]
        self.failUnless(len(quoted_toks) == 1)
        quoted_tok = quoted_toks[0]
        if __debug__:
            print "testquotation(): quoted_tok ="
            pprint.pprint(quoted_tok)
            print
        pos_line_count = quoted_tok[3][0] - quoted_tok[2][0]
        self.failUnless(pos_line_count > 0)
        str_line_count = quoted_tok[1].count("\n")
        self.assertEquals(pos_line_count, str_line_count)

    def test_bad_indent (self):
        sio_obj = StringIO.StringIO(BAD_QUOTE_INDENT_STR)
        self.failUnlessRaises(mylexer.MyFrontSyntaxError,
                              mylexer.scan_mython_file, sio_obj)
        sio_obj.close()

    def test_multiline_quote_arg (self):
        sio_obj = StringIO.StringIO(MULTILINE_QUOTE_ARG_STR)
        self.failUnless(mylexer.scan_mython_file(sio_obj))
        sio_obj.close()

# ______________________________________________________________________
# Main routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_mylexer.py
