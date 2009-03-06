#! /usr/bin/env python
# ______________________________________________________________________
"""Module myasdl.py

Mython front-ends for the Basil ASDL support package.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import asdl_py
import EscASDLHandler
from basil.lang.mython import myfront_ast as ast

# ______________________________________________________________________
# Function definitions

def asdl_front (name, text, env):
    "Quotation function for ASDL."
    pt = asdl_py.parse_string(text)
    esc_handler = EscASDLHandler.EscASDLHandler()
    obj_to_esc = esc_handler.handle(pt)
    stmt_lst = [ast.Assign([ast.Name(name, ast.Store())],
                           env["myescape"](obj_to_esc))]
    return stmt_lst, env

# ______________________________________________________________________
# End of myasdl.py
