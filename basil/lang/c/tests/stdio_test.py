#! /usr/bin/env python
# ______________________________________________________________________
"""Script stdio_test.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import pprint
from basil.lang.c import cppString, parseString, getDeclMap, getTypedefMap

# ______________________________________________________________________
# Module data

CPP_FLAGS = [
    "-std=c99",
    "-D__extension__=",
    "-D__const=const",
    "-D__attribute__(x)=",
    "-D__restrict=",
    "-D__inline__=",
    ]

# ______________________________________________________________________
# Main routine

def main (*args):
    start_code = "#include <stdio.h>\n\n"
    # On Linux, this should get rid of GCC specific extensions.
    # XXX Should these be pushed into the grammar?  Cross reference
    # from current GCC syntax.
    preprocessed_code = cppString(start_code, *CPP_FLAGS)
    parse_tree = parseString(preprocessed_code)
    # Create a map from declarations to the declaration definition.
    decl_map = getDeclMap(parse_tree)
    typedef_map = getTypedefMap(parse_tree)
    tree_box = None
    if "-g" in args:
        from basil.visuals import TreeBox
        tree_box = TreeBox.showTree(parse_tree)
    elif "-nt" not in args:
        pprint.pprint(parse_tree)
    if "-ndm" not in args:
        pprint.pprint(decl_map)
    if "-ntm" not in args:
        pprint.pprint(typedef_map)
    if tree_box is not None:
        tree_box.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of stdio_test.py
