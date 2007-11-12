#! /usr/bin/env python
# ______________________________________________________________________
"""Script MyFront.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import os
import mybuiltins

# ______________________________________________________________________
# Function definitions

def load_file (filename, env):
    """load_file()
    Given a file name, and an environment, load the file, and
    extend/modify the environment with information about the current
    file to be processed."""
    text = open(filename).read()
    env["filename"] = filename
    env["output_file"] = "%s.pyc" % (os.path.splitext(filename)[0])
    return text, env

# ______________________________________________________________________

def mycompile_file (filename, env = None):
    """mycompile_file()
    """
    if env is None:
        env = mybuiltins.initial_environment()
    text, env = load_file(filename, env)
    ast, env = env["myfrontend"](text, env)
    return env["mybackend"](ast, env)

# ______________________________________________________________________
# Main routine

def main (*args):
    """main()
    Main routine for the MyFront compiler."""
    env = mybuiltins.initial_environment()
    for arg in args:
        co, env = mycompile_file(arg, env)
        env = env["output_module_co"](env.get("output_file"), co, env)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MyFront.py
