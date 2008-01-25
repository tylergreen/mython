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
    """Class IRToCplusHandler

    BVP intermediate representation (IR) visitor class used to
    generate C++ from an IR instance."""
    # ____________________________________________________________
    def __call__ (self, node):
        self.init_cpp()
        self.handle(node)
        return "\n".join(self.cpp_lines)

    # ____________________________________________________________
    def init_cpp (self):
        self.cpp_lines = []
        self.indent_level = 0
        self.sum_count = 0
        
    # ____________________________________________________________
    def get_children (self, node):
        global ir_get_children
        return ir_get_children(node)

    # ____________________________________________________________
    def add_line (self, line_content):
        self.cpp_lines.append("%s%s" % ("  " * self.indent_level,
                                        line_content))

    # ____________________________________________________________
    def indent (self):
        self.indent_level += 1

    # ____________________________________________________________
    def dedent (self):
        assert self.indent_level > 0
        self.indent_level -= 1

    # ____________________________________________________________
    def get_summer (self):
        ret_val = "sum%d" % self.sum_count
        self.sum_count += 1
        return ret_val

    # ____________________________________________________________
    # Handler methods
    def handle_Assign (self, node):
        if isinstance(node.rhs, bvpir.Sum):
            self.handle_Sum(node.rhs, self.handle(node.lhs))
        else:
            self.add_line("%s = %s;" % (self.handle(node.lhs),
                                        self.handle(node.rhs)))

    def handle_BVPClosure (self, node):
        self.add_line("{")
        self.indent()
        for child in node.body:
            self.handle(child)
        self.dedent()
        self.add_line("}")

    def handle_Const (self, node):
        return str(node.val)

    def handle_Index (self, node):
        return "%s[%s]" % (self.handle(node.iexpr), self.handle(node.index))

    def handle_LIndex (self, node):
        return "%s[%s]" % (self.handle(node.expr), self.handle(node.index))

    def handle_LVar (self, node):
        return node.lvid

    def handle_Loop (self, node):
        if node.loop_var is None:
            assert node.loop_iter[-1] == "s"
            loop_var = node.loop_iter[:-1]
        else:
            loop_var = node.loop_var
        self.add_line("for (%s in %s) {" % (loop_var, node.loop_iter))
        self.indent()
        for child in node.body:
            self.handle(child)
        self.dedent()
        self.add_line("}")

    def handle_Mult (self, node):
        return " * ".join([self.handle(child) for child in node.exprs])

    def handle_Special (self, node):
        handler = getattr(self, node.sid, None)
        if handler is None:
            raise NotImplementedError("Can't handle special form '%s'." %
                                      node.sid)
        return handler()

    def handle_Sum (self, node, sum_var = None):
        if sum_var is None:
            sum_var = self.get_summer()
            self.add_line("double %s = 0.;" % sum_var)
        self.add_line("for (%s in %s) %s += %s;" %
                      (node.loop_var, node.loop_iter, sum_var,
                       self.handle(node.sexpr)))
        return sum_var

    def handle_SumAssign (self, node):
        self.add_line("%s += %s;" % (self.handle(node.lhs),
                                     self.handle(node.rhs)))

    def handle_Var (self, node):
        return node.vid

    def init (self):
        self.add_line("init();")

    def deinit (self):
        self.add_line("deinit();")

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
