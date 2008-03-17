#! /usr/bin/env python
# ______________________________________________________________________
"""Module CBaseHandler

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.lang.c._cparser import cNonterminals, cNonterminalMap, cTokens
from basil.utils.Handler import Handler

# ______________________________________________________________________
# Class definitions

class CBaseHandler (Handler):
    # ____________________________________________________________
    def get_nonterminal (self, node):
        ret_val = None
        if not self.is_token(node):
            ret_val = cNonterminals[node[0]]
        return ret_val

    # ____________________________________________________________
    def get_children (self, node):
        return node[1]

    # ____________________________________________________________
    def make_node (self, node_id, children):
        if type(node_id) == str:
            node_id = cNonterminalMap[node_id]
        return (node_id, children)

    # ____________________________________________________________
    def is_token (self, node):
        return ((type(node[0]) == tuple) and
                (len(node[0]) >= 2) and
                (type(node[0][0] == int)) and
                (node[0][0] < len(cTokens)) and
                (node[0][0] >= 0))

# ______________________________________________________________________
# Main (self-test) function definition

class CTestHandler (CBaseHandler):
    handle_default = CBaseHandler.handle_children

    def handle_file (self, filename):
        self.handle_str(open(filename).read())
    
    def handle_str (self, in_str):
        from pprint import pprint
        from basil.lang.c._cparser import parseString
        pt = parseString(in_str)
        pprint(pt)
        pprint(self.handle_node(pt))

# ______________________________________________________________________

def main (*args):
    handler = CTestHandler()
    if args:
        for arg in args:
            handler.handle_file(arg)
    else:
        handler.handle_str("void this_is_a_test (int testify){\n return;\n}\n")

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of CBaseHandler.py
