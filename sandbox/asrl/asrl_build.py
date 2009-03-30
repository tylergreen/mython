#! /usr/bin/env python
# ______________________________________________________________________
"""Module asrl_build.py

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

from asrlir import ASRL
from asrl_utils import ASRLBuildFailure
from asrl_match import has_dots

# ______________________________________________________________________
# Function definition(s)

def build (asrl_ast, env = None):
    assert isinstance(asrl_ast, ASRL.rwexp), "Expecting an ASRL expression."
    if env is None:
        env = {}
    # ____________________________________________________________
    def __build (crnt_ast):
        ret_val = None
        if isinstance(crnt_ast, ASRL.Constructor):
            raise NotImplementedError("Implement me!")
        elif isinstance(crnt_ast, ASRL.List):
            if not has_dots(crnt_ast):
                ret_val = [__build(child) for child in crnt_ast.elems]
            else:
                raise NotImplementedError("Implement me!")
        elif isinstance(crnt_ast, ASRL.Tuple):
            if not has_dots(crnt_ast):
                ret_val = tuple((__build(child) for child in crnt_ast.elems))
            else:
                raise NotImplementedError("Implement me!")
        elif isinstance(crnt_ast, ASRL.Dots):
            raise ASRLBuildFailure("More naked dots!")
        elif isinstance(crnt_ast, ASRL.Var):
            var_id = crnt_ast.vid
            if var_id in env:
                ret_val = env[var_id]
            else:
                raise ASRLBuildFailure("Variable '%s' not bound in "
                                       "environment." % var_id)
        else:
            assert isinstance(crnt_ast, ASRL.Const)
            ret_val = crnt_ast.val
        return ret_val
    # ____________________________________________________________
    return __build(asrl_ast)

# ______________________________________________________________________
# Main (self-test) routine.

def main (*args):
    import sys
    from parse_rws import ASRLParser
    test_triples = (('"buildme"', "buildme", {}),
                    )
    if args:
        print "Ignoring arguments!"
    for rwexpstr, target_obj, build_env in test_triples:
        asrl_cst = ASRLParser.parse_string(rwexpstr, 'rwexp')
        asrl_ast = ASRLParser.cst_to_ast(asrl_cst)
        built_obj = build(asrl_ast, build_env)
        print repr(built_obj)
        assert built_obj == target_obj

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asrl_build.py
