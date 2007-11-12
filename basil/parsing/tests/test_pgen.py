#! /usr/bin/env python
# ______________________________________________________________________
"""test_pgen - Run some quick tests on the pgen module.

$Id: test_pgen.py,v 1.3 2003/07/17 18:24:55 jriehl Exp $
"""
# ______________________________________________________________________

from basil.parsing import pgen
import sys, pprint

# ______________________________________________________________________

def main ():
    graphical = False
    tk = None
    if "-g" in sys.argv:
        from basil.visuals.TreeBox import showTree
        graphical = True
    # ____________________________________________________________
    # Check out the metagrammar.
    pprint.pprint(pgen.metaParser.stringToSymbolMap())
    pprint.pprint(pgen.metaParser.symbolToStringMap())
    # ____________________________________________________________
    # Parse the stock Python grammar.
    gAst = pgen.metaParser.parseFile("test.pgen")
    gAstTup = pgen.astToTuple(gAst)
    if graphical:
        tk = showTree(gAstTup)
    else:
        pprint.pprint(gAstTup)
    # ____________________________________________________________
    # Build a parser state machine.
    gParser = pgen.buildParser(gAst)
    print gParser
    # ____________________________________________________________
    # Test the state machine out.
    strToSymMap = gParser.stringToSymbolMap()
    pprint.pprint(strToSymMap)
    pprint.pprint(pgen.symbolToStringMap(gParser))
    # Use the default start symbol - the first symbol in the input grammar.
    testStr = open("test_pgen.py").read()
    fAst0 = gParser.parseString(testStr)
    fAst0Tup = fAst0.toTuple()
    if graphical:
        showTree(fAst0Tup, tk)
    else:
        pprint.pprint(fAst0Tup)
    # And now with a different start symbol.
    gParser.setStart(strToSymMap["file_input"])
    fAst1 = gParser.parseString(testStr)
    fAst1Tup = fAst1.toTuple()
    if graphical:
        showTree(fAst1Tup, tk)
    else:
        pprint.pprint(fAst1Tup)
    # Throw TK into its main loop.
    if graphical:
        tk.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of test_pgen.py
