#! /usr/bin/env python
# ______________________________________________________________________

from basil.lang.mython import mybuiltins

def nonquote_myboth (src, env = None):
    if env is None:
        env = mybuiltins.initial_environment()
    ast, env = env["myfrontend"](src, env)
    env = env.copy()
    _, env = env["myeval"](ast, env)
    return ast.body, env

def myboth (name, src, env):
    ast_list, env = nonquote_myboth(src, env)
    if name is not None:
        env[name] = ast_list
    return ast_list, env

mystring = mybuiltins.makequote(str)

# ______________________________________________________________________
# End of myutils.py
