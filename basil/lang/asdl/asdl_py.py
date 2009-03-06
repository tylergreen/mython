#! /usr/bin/env python
# ______________________________________________________________________
"""Script asdl_py.py

Translate an ASDL module into a set of Python classes.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import getopt
import sys

from basil.thirdparty import asdl

# XXX This is only being used for a code generation utility function.
# Move that function elsewhere.
from basil.lang.mython import pgen2LL1

import PyASDLHandler

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________

def parse_string (text):
    """parse_string()
    Hack of the parse() function in asdl, made to handle a string
    input."""
    ret_val = None
    scanner = asdl.ASDLScanner()
    parser = asdl.ASDLParser()
    tokens = scanner.tokenize(text)
    try:
        ret_val = parser.parse(tokens)
    except asdl.ASDLSyntaxError, err:
        print err
        lines = text.split("\n")
        print lines[err.lineno - 1]
    return ret_val

# ______________________________________________________________________
# Main routine

def main (*args):
    infilename = "<stdin>"
    infile = sys.stdin
    outfilename = "<stdout>"
    outfile = sys.stdout
    global __DEBUG__
    # ____________________________________________________________
    opts, args = getopt.getopt(args, "di:o:")
    for opt_key, opt_val in opts:
        if opt_key == "-i":
            infilename = opt_val
            infile = open(infilename)
        elif opt_key == "-o":
            outfilename = opt_val
            outfile = open(outfilename, "w")
        elif opt_key == "-d":
            __DEBUG__ = True
    # ____________________________________________________________
    text = infile.read()
    infile.close()
    asdl_pt = parse_string(text)
    if __DEBUG__:
        import pprint
        pprint.pprint(asdl_pt.types)
        print
    handler = PyASDLHandler.PyASDLHandler()
    handler.handle(asdl_pt)
    if __DEBUG__:
        pprint.pprint(handler.classes)
    code_text = handler.emit_classes()
    outfile.write(code_text)
    outfile.close()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asdl_py.py
