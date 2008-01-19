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
from . import FEParser
from ..mython import LL1ParserUtil
from ..mython import myfront_ast as ast

# ______________________________________________________________________
# Function definitions

bvpParser = LL1ParserUtil.mkMyParser(FEParser.FEParser)

# ______________________________________________________________________

def bvpFrontEnd (name, text, env):
    global bvpParser, bvpToIR
    cst, env_1 = bvpParser(text, env)
    ir = bvpCSTToIR(cst)
    esc_ir = env_1['myescape'](ir)
    stmt_lst = [ast.Assign([ast.Name(name, ast.Store())], esc_ir)]
    return stmt_lst, env_1

# ______________________________________________________________________

def bvpCSTToIR (cst):
    return cst

# ______________________________________________________________________

def bvpIRToCplus (ir):
    return ir

# ______________________________________________________________________
# End of FEniCS.py
