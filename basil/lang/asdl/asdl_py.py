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

import PyASDLHandler
import MetaAST

# ______________________________________________________________________
# Module data

__DEBUG__ = False

__USAGE__ = """asdl_py.py

Usage:
    $ <asdl_py> [<opts>] [-i <infile>] [-o <outfile>]

Where <asdl_py> is 'asdl_py' or similar.

Options:
    -n          Generate newer style, meta-data based classes.  Default is to
                use an older format where constructors are type-specific.
    -h          Help!
    -i <file>   Use the given file name as the input ASDL specification.
                Default is to use stdin.
    -o <file>   Use the given file name as the output Python module.  Default
                is to use stdout.
"""

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
    handler_class = PyASDLHandler.PyASDLHandler
    infilename = "<stdin>"
    infile = sys.stdin
    outfilename = "<stdout>"
    outfile = sys.stdout
    emit_keys = {"self_contained" : True}
    global __DEBUG__
    # ____________________________________________________________
    opts, args = getopt.getopt(args, "dhni:o:")
    for opt_key, opt_val in opts:
        if opt_key == "-i":
            infilename = opt_val
            infile = open(infilename)
        elif opt_key == "-o":
            outfilename = opt_val
            outfile = open(outfilename, "w")
        elif opt_key == "-d":
            __DEBUG__ = True
        elif opt_key == "-n":
            handler_class = MetaAST.MetaASDLHandler
            emit_keys = {}
        elif opt_key == "-h":
            print __USAGE__
    # ____________________________________________________________
    text = infile.read()
    infile.close()
    asdl_pt = parse_string(text)
    if __DEBUG__:
        import pprint
        pprint.pprint(asdl_pt.types)
        print
    handler = handler_class()
    handler.handle(asdl_pt)
    if __DEBUG__ and hasattr(handler, "classes"):
        pprint.pprint(handler.classes)
    code_text = handler.emit_code(**emit_keys)
    outfile.write(code_text)
    outfile.close()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asdl_py.py
