#! /usr/bin/env python
# ______________________________________________________________________
"""Module FEniCS.py

Mython API for using the FEniCS boundary value problem (BVP)
domain-specific language (DSL).

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import StringIO
import tokenize
from . import FEParser, BVPToIRHandler, bvpir, IRToCplusHandler
from ..mython import LL1ParserUtil
from ..mython import myfront_ast as ast
from ..mython import ASTUtils

# ______________________________________________________________________
# Function definitions

bvpParser = LL1ParserUtil.mkMyParser(FEParser.FEParser)

# TODO: Consider making this hook into myescape (maybe convert
# mk_escaper into something that reads a dispatch table in the
# environment?)
bvp_escaper = ASTUtils.mk_escaper(bvpir)

# ______________________________________________________________________

def bvpFrontEnd (name, text, env):
    global bvpParser, bvpToIR, bvp_escaper
    cst, env_1 = bvpParser(text, env)
    ir = bvpCSTToIR(cst)
    esc_ir = bvp_escaper(ir)
    stmt_lst = [ast.Assign([ast.Name(name, ast.Store())], esc_ir)]
    return stmt_lst, env_1

# ______________________________________________________________________

def bvpCSTToIR (cst):
    return BVPToIRHandler.BVPToIRHandler()(cst)

# ______________________________________________________________________

def bvpIRToCplus (ir):
    return IRToCplusHandler.IRToCplusHandler()(ir)

# ______________________________________________________________________
# End of FEniCS.py
