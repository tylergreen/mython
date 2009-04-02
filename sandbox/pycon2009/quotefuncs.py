#! /usr/bin/env python
# ______________________________________________________________________
"""Module quotefuncs

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

from basil.lang.mython.mython_ast import Assign, Expr, Name, Store

# ______________________________________________________________________
# Function definition(s)

def compose_passes (*passes, initial_env = None, debug_passes = None):
    def _composed_passes (data, env = None, **kws):
        if env is None:
            if initial_env is None:
                env = mybuiltins.initial_environment()
            else:
                env = initial_env
        for passobj in passes:
            if isinstance(passobj, str):
                passobj = env[passobj]
            data, env = passobj(data, env, **kws)
            if debug_passes is not None:
                debug_passes(data)
        return data, env
    return _composed_passes

# ______________________________________________________________________

def make_quote_function (translator):
    def _quote_function (name_opt, source, environment):
        ret_val = []
        runtime_expr, environment = translator(source, environment)
        if runtime_expr:
            if name_opt is None:
                runtime_stmt = Expr(runtime_expr)
            else:
                runtime_stmt = Assign([Name(name_opt, Store())], runtime_expr)
        return ret_val, environment
    return _quote_function

# ______________________________________________________________________
# End of quotefuncs.py
