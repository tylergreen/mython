#! /usr/bin/env python
# ______________________________________________________________________
"""Module cdeclutils.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.lang.c._cparser import *

from basil.utils import TreeUtils

# ______________________________________________________________________
# Function definitions

def isTypedef (pt):
    """isTypedef()
    Predicate function for determining if the current parse tree
    corresponds to a type definiton."""
    ret_val = False
    typedef_tok = cTokenMap["TYPEDEF"]
    for pt_payload in TreeUtils.prefix_tree_iter(pt):
        if type(pt_payload) == tuple and pt_payload[0] == typedef_tok:
            ret_val = True
            break
    return ret_val

# ______________________________________________________________________

def getTypedefMap (pt):
    """getTypeMap()
    Create a map from type names to type definitions based on an input
    C concrete parse tree."""
    decl_map = getDeclMap(pt)
    typedef_items = ((decl_key, decl_vals) for decl_key, decl_vals in
                     decl_map.iteritems()
                     if sum([isTypedef(decl_val) for decl_val in decl_vals]))
    ret_val = dict(typedef_items)
    return ret_val

# ______________________________________________________________________

def getFirstIdentifier (pt):
    """getFirstIdentifier()
    Get the first identifier token found in the given parse tree."""
    ret_val = None
    identifier_tok = cTokenMap["IDENTIFIER"]
    for pt_payload in TreeUtils.prefix_tree_iter(pt):
        if type(pt_payload) == tuple and pt_payload[0] == identifier_tok:
            ret_val = pt_payload
            break
    return ret_val

# ______________________________________________________________________

def getDeclMap (pt):
    """getDeclMap()
    Create a map from identifiers to type declarations based on a C
    concrete parse tree."""
    declaration = cNonterminalMap["DECLARATION"]
    function_definition = cNonterminalMap["FUNCTION_DEFINITION"]
    def recGetDeclMap (pt):
        ret_val = {}
        if type(pt[0]) == int:
            nt_number, children = pt
            if nt_number in (declaration, function_definition):
                _, identifier_key, _, _ = getFirstIdentifier(pt)
                if identifier_key not in ret_val:
                    if nt_number == function_definition:
                        val = pt[1][:-1]
                    else:
                        val = pt[1]
                    ret_val[identifier_key] = val
            else:
                for child_pt in children:
                    ret_val.update(recGetDeclMap(child_pt))
        return ret_val
    return recGetDeclMap(pt)

# ______________________________________________________________________
# Main routine

def main (*args):
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of cdeclutils.py
