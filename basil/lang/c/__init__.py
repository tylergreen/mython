#! /usr/bin/env python
# ______________________________________________________________________
"""basil/lang/c/__init__.py

This is the C language parser integration.

$Id: __init__.py,v 1.1 2003/07/10 22:08:16 jriehl Exp $
"""
# ______________________________________________________________________

from basil.lang.c._cparser import *
from basil.lang.c.cdeclutils import *
from basil.lang.c.ctreeutils import *

# ______________________________________________________________________

class CPPError (Exception):
    pass

# ______________________________________________________________________

def cppString (in_string, *args):
    from subprocess import Popen, PIPE
    cmd = ["cpp"]
    if len(args) > 0:
        cmd = cmd + list(args)
    subproc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE,
                    close_fds = True)
    subproc.stdin.write(in_string)
    subproc.stdin.close()
    try:
        subproc.wait()
        if subproc.returncode == 0:
            ret_val = subproc.stdout.read()
        else:
            raise CPPError(subproc.stderr.read())
    finally:
        subproc.stdout.close()
        subproc.stderr.close()
    return ret_val

# ______________________________________________________________________

def myctypes (name, code, env):
    from basil.lang.c.MyCTypeFactory import MyCTypeFactory
    # Step 1: parse the code.
    pt = parseString(code)
    # Step 2: convert the code to C types.
    handler = CDeclHandler(MyCTypeFactory())
    ctypes_decls = handler.handle_node(pt)
    # Step 3: convert the C types to calls to the ctypes constructors.
    wrap_src = "\n".join(["import ctypes",
                          "try:",
                          "    %s = ctypes.CDLL('%s')" % (name, name),
                          "except OSError:",
                          "    %s = ctypes.CDLL('%s.so')" % (name, name)] +
                         [ctypes_decl.to_wrapper(name)
                          for ctypes_decl in ctypes_decls] + [""])
    wrap_ast, env = env["myfrontend"](wrap_src, env)
    return wrap_ast.body, env

# ______________________________________________________________________
# End of basil/lang/c/__init__.py
