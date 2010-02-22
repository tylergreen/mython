#! /usr/bin/env python
# ______________________________________________________________________
# Module imports

import pprint

from basil.parsing import PgenParser, PyPgen
from basil.lang.python import DFAParser
from basil.lang.mython.mybuiltins import makequote

# ______________________________________________________________________
# Function definitions

def pgen_to_grammar_obj (source):
    pgen = PyPgen.PyPgen()
    nfa_grammar = pgen.handleStart(PgenParser.parseString(source))
    dfa_grammar = pgen.generateDfaGrammar(nfa_grammar)
    pgen.translateLabels(dfa_grammar)
    pgen.generateFirstSets(dfa_grammar)
    dfa_grammar = DFAParser.addAccelerators(dfa_grammar)
    return dfa_grammar

grammar_obj_to_python_src = pprint.pformat

def pgen_to_python (source):
    return grammar_obj_to_python_src(pgen_to_grammar_obj(source))

def ct_mypgen (name, src, env):
    assert name is not None
    grammar_obj = pgen_to_grammar_obj(src)
    env = env.copy()
    env["quote_%s" % name] = makequote(
        PyPgen.PyPgenParser(grammar_obj).parseString)
    print env
    ast, env = env["myfrontend"]("from basil.parsing.PyPgen import "
                                 "PyPgenParser\n%s_gobj = %s\n"
                                 "%s_parser = PyPgenParser(%s_gobj)\n" %
                                 (name, pprint.pformat(grammar_obj), name,
                                  name), env)
    return ast.body, env

mypgen = makequote(pgen_to_grammar_obj)

DEMO_GRAMMAR = """start: term ('+' term)*
term: atom ('*' atom)*
atom: NAME | NUMBER
"""

if __name__ == "__main__":
    print pgen_to_python(DEMO_GRAMMAR)

# ______________________________________________________________________
# End of mypgen.py
