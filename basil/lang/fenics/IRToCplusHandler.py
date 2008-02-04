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
# Module data

VDec = bvpir.VDec

INIT_DECS_1 = [
    VDec("discs", "const Obj<std::set<std::string> >&", None,
         "m->getDiscretizations()"),
    VDec("coordinates", "const Obj<ALE::Mesh::real_section_type>&", None,
         'm->getRealSection("coordinates")'),
    VDec("cells", "const Obj<ALE::Mesh::label_sequence>&", None,
         "m->heightStratum(0)"),
    VDec("dim", "const int", None, "m->getDimension()"),
    VDec("detJ", "double", None, "0.0"),
    VDec("totBasisFuncs", "int", None, "0"),
    VDec("quad", "int", None, "0")
    ]

INIT_DECS_2 = [
    VDec("elemMat", "PetscScalar", "totBasisFuncs*totBasisFuncs"),
    VDec("v0", "double", "dim"),
    VDec("J", "double", "dim*dim"),
    VDec("invJ", "double", "dim*dim"),
    ]

DISC_DECLS = [
    VDec("disc", "const Obj<ALE::Discretization>&", None,
         "m->getDiscretization(*field)"),
    VDec("numQuadPoints", "const int", None, "disc->getQuadratureSize()"),
    VDec("quadWeights", "const double *", None,
         "disc->getQuadratureWeights()"),
    VDec("numBasisFuncs", "const int", None, "disc->getBasisSize()"),
    VDec("basis", "const double *", None, "disc->getBasis()"),
    # XXX: One 'optimization' to do here is to elminate unused
    # variables.  For example, basisDer is not used by the 'mass' test
    # case.
    VDec("basisDer", "const double *", None, "disc->getBasisDerivatives()"),
    VDec("indices", "const int *", None, "disc->getIndices()"),
    ]

def integer_bound (bound_name):
    return ("int %s = 0", "%%s < %s" % bound_name, "++%s")

LOOPS = {
    "cells" : ("ALE::Mesh::label_sequence::iterator %s = cells->begin()",
               "%s != cells->end()", "++%s"),
    "fields" : ("std::set<std::string>::const_iterator %s = discs->begin()",
                "%s != discs->end()", "++%s"),
    "quads" : integer_bound("numQuadPoints"),
    "numBasisFuncs" : integer_bound("numBasisFuncs"),
    "dim" : integer_bound("dim"),
    }

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
        self.heap_vars = {}
        self.intermediates = []

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
    def handle_Add (self, node):
        children = [self.handle(child) for child in node.exprs]
        if len(children) > 1:
            ret_val = "(%s)" % (" + ".join(children))
        else:
            ret_val = children[0]
        return ret_val

    def handle_Assign (self, node):
        if isinstance(node.rhs, bvpir.Sum):
            self.handle_Sum(node.rhs, self.handle(node.lhs))
        else:
            self.add_line("%s = %s;" % (self.handle(node.lhs),
                                        self.handle(node.rhs)))

    def handle_BVPClosure (self, node):
        self.add_line("{")
        self.indent()
        # FIXME: These sometimes depend on variables set up by the
        # initialization (init) code generator, and therefore are
        # declared by init().  Consider mixing declarations into the
        # statement IR, and just handling them as they come (this is
        # okay in C++, after all).
        self.intermediates = node.decs
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

    def _make_for (self, loop_var, loop_iter):
        if loop_iter in LOOPS:
            loop_init_fmt, loop_test_fmt, loop_iter_fmt = LOOPS[loop_iter]
            ret_val = ("for (%s; %s; %s)" %
                       (loop_init_fmt % loop_var,
                        loop_test_fmt % loop_var,
                        loop_iter_fmt % loop_var))
        else:
            ret_val = "for (%s in %s)" % (loop_var, node.loop_iter)
        return ret_val

    def handle_Loop (self, node):
        if node.loop_var is None:
            assert node.loop_iter[-1] == "s"
            loop_var = node.loop_iter[:-1]
        else:
            loop_var = node.loop_var
        self.add_line("%s {" % self._make_for(loop_var, node.loop_iter))
        self.indent()
        for child in node.body:
            self.handle(child)
        self.dedent()
        self.add_line("}")

    def handle_Mult (self, node):
        children = [self.handle(child) for child in node.exprs]
        if len(children) > 1:
            ret_val = "(%s)" % (" * " .join(children))
        else:
            ret_val = children[0]
        return ret_val

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
        self.add_line("%s %s += %s;" %
                      (self._make_for(node.loop_var, node.loop_iter), sum_var,
                       self.handle(node.sexpr)))
        return sum_var

    def handle_SumAssign (self, node):
        self.add_line("%s += %s;" % (self.handle(node.lhs),
                                     self.handle(node.rhs)))

    def handle_Var (self, node):
        return node.vid

    def handle_VDec (self, node):
        dec_ty = node.ty
        if node.dim is not None:
            dec_ty += " *"
        dec_rhs = node.id
        if node.init is not None:
            dec_rhs += " = %s" % node.init
        else:
            if node.dim is not None:
                dec_rhs += " = new %s[%s]" % (node.ty, node.dim)
                self.heap_vars[node.id] = node.dim
        self.add_line("%s %s;" % (dec_ty, dec_rhs))

    def init (self):
        for init_decl in INIT_DECS_1:
            self.handle(init_decl)
        self.add_line("MatZeroEntries(A);")
        self.handle(
            bvpir.Loop("f_iter", "fields", [
            bvpir.SumAssign(bvpir.LVar("totBasisFuncs"),
                            bvpir.Var("m->getDiscretization(*f_iter)->"
                                      "getBasisSize()"))]))
        for init_decl in INIT_DECS_2:
            self.handle(init_decl)
        for intermediate_decl in self.intermediates:
            self.handle(intermediate_decl)

    def deinit (self):
        for heap_var_name in self.heap_vars.keys():
            self.add_line("delete [] %s;" % heap_var_name)
        self.add_line("MatAssemblyBegin(A, MAT_FINAL_ASSEMBLY);")
        self.add_line("MatAssemblyEnd(A, MAT_FINAL_ASSEMBLY);")

    def compute_geometry (self):
        self.add_line("m->computeElementGeometry(coordinates, *cell, v0, J, "
                      "invJ, detJ);")

    def get_disc (self):
        for disc_decl in DISC_DECLS:
            self.handle(disc_decl)

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
