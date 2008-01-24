#! /usr/bin/env python
# ______________________________________________________________________
"""Module IRToCplusHandler

Defines a visitor class that walks a boundary-value problem
intermediate representation (BVP IR) instance, generating C++ code.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import bvpir

# FIXME: Get ASTUtils out of the Mython language package.
from ..mython import ASTUtils

# ______________________________________________________________________
# Module functions

ir_get_children = ASTUtils.mk_ast_get_children(bvpir)

# ______________________________________________________________________
# Class definitions

class IRToCplusHandler (ASTUtils.GenericASTHandler):

    def __init__ (self):
        self.cplus_code = []
        self.indent_level = 0

    def get_children (self, node):
        global ir_get_children
        return ir_get_children(node)

    def _handle_Assign (self, node):
        pass

    def _handle_BVPClosure (self, node):
        pass

    def _handle_Const (self, node):
        pass

    def _handle_Index (self, node):
        pass

    def _handle_LIndex (self, node):
        pass

    def _handle_LVar (self, node):
        pass

    def _handle_Loop (self, node):
        pass

    def _handle_Mult (self, node):
        pass

    def _handle_Special (self, node):
        pass

    def _handle_Sum (self, node):
        pass

    def _handle_SumAssign (self, node):
        pass

    def _handle_Var (self, node):
        pass

# ______________________________________________________________________
# Main routine

def main (*args):
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of IRToCplusHandler.py
