#! /usr/bin/env python
# ______________________________________________________________________
"""Module asrl_rewrite.py

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

from asrlir import ASRL
import asrl_utils
from asrl_match import match
from asrl_build import build

# ______________________________________________________________________
# Module data

__DEBUG__ = True

# ______________________________________________________________________
# Function definition(s)

def rewrite (asrl_ast, obj, env = None):
    assert isinstance(asrl_ast, ASRL.Rewrite)
    env = match(asrl_ast.match, obj, env)
    if asrl_ast.where_clause is not None:
        exec asrl_ast.where_clause in globals(), env
    return build(asrl_ast.build, env), env

# ______________________________________________________________________

def id_combinator (obj, env = None):
    return obj, env

# ______________________________________________________________________

def fail_combinator (obj, env = None):
    raise ASRLMatchFailure()

# ______________________________________________________________________

def mk_rewrite_combinator (asrl_ast):
    def _wrapped_rewrite (obj, env = None):
        return rewrite(asrl_ast, obj, env)
    return _wrapped_rewrite

# ______________________________________________________________________

def compose_combinators (rw1, rw2):
    def _composed_rw (obj, env = None):
        try:
            ret_val = rw1(obj, env.copy())
        except asrl_utils.ASRLMatchFailure:
            ret_val = rw2(obj, env)
        return ret_val
    return _composed_rw

# ______________________________________________________________________

def fixpt_combinator (rwcomb):
    def _fixpt (obj, env = None):
        ret_val = None
        while True:
            nextobj, env = rwcomb(obj, env)
            # XXX This can get awfully expensive to compute, right?
            if nextobj == obj:
                ret_val = nextobj, env
                break
            else:
                obj = nextobj
        return ret_val
    return _fixpt

# ______________________________________________________________________
# Main (self-test) routine.

test_base_env = {
    "id" : ASRL.Builtin("id_combinator"),
    "fail" : ASRL.Builtin("fail_combinator")
    }

# ______________________________________________________________________

def test_asrl_unit (unit):
    asdl_file_name = unit.asdl_file
    asts_for_combination = []
    asts_for_tests = []
    for rwast in unit.rws:
        if rwast.label.startswith("test"):
            asts_for_tests.append(rwast)
        else:
            asts_for_combination.insert(0, rwast)
    rwcomb = id_combinator
    for rwast in asts_for_combination:
        rwcomb = compose_combinators(mk_rewrite_combinator(rwast),
                                     rwcomb)
    rwcomb = fixpt_combinator(rwcomb)
    # Build the base environment.
    base_env = {}
    base_env["asrlassert"] = asrl_utils.asrlassert
    # XXX
    for rwast in asts_for_tests:
        startobj = build(rwast.match, base_env)
        expectedobj = build(rwast.build, base_env)
        endobj, endenv = rwcomb(startobj, base_env)
        if __DEBUG__:
            print ("%s: %r => %r (expected %r)" %
                   ("PASS" if endobj == expectedobj else "FAIL",
                    startobj, endobj, expectedobj))

# ______________________________________________________________________

def test_asrl_string (asrl_string):
    from parse_rws import ASRLParser
    for unit in ASRLParser.parse_string(asrl_string,
                                        environment = test_base_env):
        test_asrl_unit(unit)

# ______________________________________________________________________

def test_asrl_file (asrl_filename):
    from parse_rws import ASRLParser
    for unit in ASRLParser.parse_file(asrl_filename,
                                      environment = test_base_env):
        test_asrl_unit(unit)

# ______________________________________________________________________

def main (*args):
    import sys
    if len(args) == 0:
        test_asrl_string(sys.stdin.read())
    for arg in args:
        test_asrl_file(arg)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asrl_rewrite.py
