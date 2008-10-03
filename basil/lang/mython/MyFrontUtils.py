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

import mybuiltins

# ______________________________________________________________________
# Main routine

def main (*args):
    """main()
    Main routine for the MyFront compiler."""
    env = mybuiltins.initial_environment()
    for arg in args:
        env = mybuiltins._mycompile_file_to_pyc(arg, env)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MyFrontUtils.py
