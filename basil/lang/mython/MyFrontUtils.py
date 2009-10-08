#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyFrontUtils.py

XXX Not much of a module left.  Original idea was too keep mybuiltins
from being overburdened, but now supporting compile-time imports is
sucking it all back over.  TODO?

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import os
import sys
import traceback
import mybuiltins
from basil.lang.mython.MyFrontExceptions import (
    MyFrontException, MyFrontSyntaxError, MyFrontQuoteExprError,
    MyFrontCompileTimeError)

# ______________________________________________________________________
# Function definition(s)

def format_myfront_exc (exc):
    exc_strings = { MyFrontQuoteExprError :
                    "Error in quotation argument, line %d:",
                    MyFrontCompileTimeError :
                    "Error in quote-generated code, from block starting at "\
                    "line %d:" }
    if type(exc) in exc_strings:
        ret_val = exc_strings[type(exc)] % exc.args[1]
    else:
        ret_val = "MyFront error, near line %d:" % exc.args[1]
    return ret_val

# ______________________________________________________________________

def rewrite_traceback (tb):
    # XXX In order to really get at the heart of issue 3, one will
    # need to implement this function s.t. it removes all initial
    # frames up to the point where user code starts.  After that the
    # translator needs to be updated to offset line numbers and column
    # numbers while constructing AST nodes.
    return tb

# ______________________________________________________________________

def handle_toplevel_error (exc):
    def _handle_nested_error (exc, level = 0, filename = None, lineno = None):
        indent_str = "  " * level
        if isinstance(exc, MyFrontException) and len(exc.args) > 1:
            if isinstance(exc, MyFrontSyntaxError):
                # Can't figure out if the syntax error wrapper buys us
                # anything.  Ignoring for now.
                _handle_nested_error(exc.args[0], level)
            else:
                print >>sys.stderr, (indent_str + format_myfront_exc(exc))
                _handle_nested_error(exc.args[0], level + 1, lineno =
                                     exc.args[1])
        elif isinstance(exc, tuple) and len(exc) == 3:
            exc_ty, exc_val, tb = exc
            tb = rewrite_traceback(tb)
            tb_lns = traceback.format_exception(exc_ty, exc_val, tb)
            sys.stderr.writelines((indent_str + tb_ln for tb_ln in tb_lns))
        else:
            exc_ty_str = type(exc).__name__
            exc_str = str(exc)
            if len(exc_str) > 0:
                print >>sys.stderr, "%s%s:%s" % (indent_str, exc_ty_str,
                                                 exc_str)
            else:
                print >>sys.stderr, indent_str + exc_ty_str
    _handle_nested_error(exc)
    raise SystemExit()

# ______________________________________________________________________

def wrap_pass (compiler_pass):
    def _wrapped_pass (arg, env = None):
        if env is None:
            env = mybuiltins.initial_environment()
        try:
            compiler_pass_fn = compiler_pass
            if isinstance(compiler_pass_fn, str):
                if compiler_pass_fn in env:
                    compiler_pass_fn = env[compiler_pass_fn]
                else:
                    raise KeyError("%r not in compile-time environment"
                                   % (compiler_pass_fn,))
            ret_val = compiler_pass_fn(arg, env)
        except MyFrontException, myfront_exc:
            handle_toplevel_error(myfront_exc)
        return ret_val
    return _wrapped_pass

# ______________________________________________________________________

toplevel_compile = wrap_pass("mycompile_file")

toplevel_compile_to_file = wrap_pass("mycompile_file_to_pyc")

# ______________________________________________________________________
# Main routine

def main (*args):
    """main()
    Main routine for the MyFront compiler."""
    env = mybuiltins.initial_environment()
    for arg in args:
        arg_path = os.path.abspath(os.path.split(arg)[0])
        sys.path.append(arg_path)
        env = toplevel_compile_to_file(arg, env)
        sys.path.remove(arg_path)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MyFrontUtils.py
