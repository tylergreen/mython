#! /usr/bin/env python
# ______________________________________________________________________
"""Module ctreeutils.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.lang.c._cparser import *

# ______________________________________________________________________
# Function definitions

def verbosify_tree (pt):
    """verbosify_tree()
    """
    pt_payload, children = pt
    if type(pt_payload) == int:
        pt_payload = cNonterminals[pt_payload]
    else:
        pt_payload = (cTokens[pt_payload[0]],
                      pt_payload[1],
                      pt_payload[2],
                      pt_payload[3])
    return (pt_payload, [verbosify_tree(child) for child in children])

# ______________________________________________________________________
# Main routine (self-test)

def main ():
    from pprint import pprint
    pt1 = parseString("typedef struct foo { int a; } foo_t;\n")
    pprint(pt1)
    print
    pt2 = verbosify_tree(pt1)
    pprint(pt2)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of ctreeutils.py
