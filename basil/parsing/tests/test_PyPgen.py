#! /usr/bin/env python
# ______________________________________________________________________
"""test_PyPgen

Unit test for PyPgen module.

$Id$
"""
# ______________________________________________________________________

from basil.lang.python import DFAParser, StdTokenizer
from basil.parsing import pgen

import sys

sys.path.append("..")

import PyPgen, PgenParser

# ______________________________________________________________________

def main ():
    graphical = False
    if "-g" in sys.argv:
        from basil.visuals.TreeBox import showTree
        graphical = True
    # ____________________________________________________________
    grammarST0 = PgenParser.parseFile("test.pgen")
    grammarST1Obj = pgen.metaParser.parseFile("test.pgen")
    grammarST1 = grammarST1Obj.toTuple()
    print "Preliminaries:", grammarST0 == grammarST1
    if graphical:
        tk = showTree(grammarST0)
        showTree(grammarST1, tk)
    pgenObj = PyPgen.PyPgen()
    parser0 = pgenObj(grammarST0)
    parser1 = pgenObj(grammarST1)
    parser2Obj = pgen.buildParser(grammarST1Obj)
    parser2 = parser2Obj.toTuple()
    print "Test 1:", parser0 == parser1
    print "Test 2:", parser0 == parser2
    # __________________________________________________
    # The funny part of this sequence is: if the previous tests worked, isn't
    # it reasonable to assume the next test is given?  (i.e. the inputs are
    # structurally identical!)
    testPythonFile = "../PyPgen.py"
    fileObj = open(testPythonFile)
    tokenizer0 = StdTokenizer.StdTokenizer(testPythonFile, fileObj.readline)
    parse0 = DFAParser.parsetok(tokenizer0, parser0, 257)
    # __________________________________________________
    fileObj.seek(0)
    tokenizer1 = StdTokenizer.StdTokenizer(testPythonFile, fileObj.readline)
    parse1 = DFAParser.parsetok(tokenizer1, parser1, 257)
    # __________________________________________________
    fileObj.seek(0)
    tokenizer2 = StdTokenizer.StdTokenizer(testPythonFile, fileObj.readline)
    parse2 = DFAParser.parsetok(tokenizer2, parser2, 257)
    # __________________________________________________
    print "Test 3:", parse0 == parse1
    print "Test 4:", parse0 == parse2
    if graphical:
        showTree(parse0, tk)
        showTree(parse1, tk)
        showTree(parse2, tk)
        tk.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of test_PyPgen.py
