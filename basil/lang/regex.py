#! /usr/bin/env python
import re
import pickle

def requote(name, src, env):
    reobj = re.compile(src.strip())
    recode = pickle.dumps(reobj)
    recode1 = "import pickle\n" + "%s = pickle.loads(%r)\n" % (name, recode)
    ast, env = env["myfrontend"](recode1, env)
    return ast.body, env

