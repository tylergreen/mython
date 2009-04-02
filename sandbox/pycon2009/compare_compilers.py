#! /usr/bin/env python

import dis

from basil.lang.mython import mybuiltins

def main (*args):
    for arg in args:
        print "_" * 70
        source = open(arg).read()
        ast, env0 = mybuiltins.myfrontend(source, mybuiltins.initial_environment())
        co0, env1 = mybuiltins.mybackend(ast, env0)
        dis.dis(co0)
        print "_" * 60
        co1 = compile(source, arg, "exec")
        dis.dis(co1)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of compare_compilers.py
