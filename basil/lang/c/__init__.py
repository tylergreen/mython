#! /usr/bin/env python
# ______________________________________________________________________
"""basil/lang/c/__init__.py

This is the C language parser integration.

$Id: __init__.py,v 1.1 2003/07/10 22:08:16 jriehl Exp $
"""
# ______________________________________________________________________

from basil.lang.c._cparser import *

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
# End of basil/lang/c/__init__.py
