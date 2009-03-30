#! /usr/bin/env python
# ______________________________________________________________________
"""Module asrl_match.py

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

from basil.lang.asdl.AST import map_fields
from asrlir import ASRL
import asrl_utils

# ______________________________________________________________________
# Function definitions

def build_rwenv_from_module_class (module_class):
    ret_val = {}
    ty_md = {}
    ret_val["$ASDL"] = ty_md
    for name, obj in module_class.__dict__.items():
        if hasattr(obj, "__asdl_meta__"):
            ty_md[name] = obj
    return ret_val
            
# ______________________________________________________________________

def has_dots (seq):
    ret_val = False
    for element in seq.elems:
        if isinstance(element, ASRL.Dots):
            ret_val = True
            break
    return ret_val

# ______________________________________________________________________

def match (asrl_ast, obj, env = None):
    assert isinstance(asrl_ast, ASRL.rwexp), "Expecting an ASRL expression."
    if env is None:
        env = {}
    # ____________________________________________________________
    def __match (crnt_ast, obj, env):
        ret_val = env
        obj_type = type(obj)
        if isinstance(crnt_ast, ASRL.Constructor):
            ret_val = __match_constructor(crnt_ast.label, crnt_ast.args,
                                          obj, ret_val)
        elif isinstance(crnt_ast, ASRL.List):
            if not issubclass(obj_type, list):
                raise asrl_utils.ASRLMatchFailure()
            elif not has_dots(crnt_ast):
                ret_val = __match_seq(crnt_ast, obj, ret_val)
            else:
                raise NotImplementedError("Implement me!")
        elif isinstance(crnt_ast, ASRL.Tuple):
            if type(obj) != tuple:
                raise asrl_utils.ASRLMatchFailure()
            elif not has_dots(crnt_ast):
                ret_val = __match_seq(crnt_ast, obj, ret_val)
            else:
                raise NotImplementedError("Implement me!")
        elif isinstance(crnt_ast, ASRL.Dots):
            raise asrl_utils.ASRLMatchFailure("Naked dots!")
        elif isinstance(crnt_ast, ASRL.Var):
            var_id = crnt_ast.vid
            if var_id in env:
                # XXX Does this test get more interesting if I add
                # aliases?  Going to say no.  An alias binds after the
                # subexpression matches, and binds to the matching
                # object.
                if obj != env[var_id]:
                    raise asrl_utils.ASRLMatchFailure((env[var_id], obj))
            else:
                # Vacuuously match an unbound variable.
                ret_val = ret_val.copy()
                ret_val[var_id] = obj
        else:
            assert isinstance(crnt_ast, ASRL.Const)
            if crnt_ast.val != obj:
                raise asrl_utils.ASRLMatchFailure((crnt_ast, obj))
        return ret_val
    # ____________________________________________________________
    def __match_seq (seq_ast, obj, env):
        ret_val = env
        if len(seq_ast.elems) != len(obj):
            raise asrl_utils.ASRLMatchFailure()
        else:
            for sub_ast, sub_obj in zip(seq_ast.elems, obj):
                ret_val = __match(sub_ast, sub_obj, ret_val)
        return ret_val
    # ____________________________________________________________
    def __match_constructor (constructor_name, constructor_args, obj, env):
        ret_val = env
        obj_type = type(obj)
        if ((not hasattr(obj_type, "__name__")) or
            (obj_type.__name__ != constructor_name)):
            raise asrl_utils.ASRLMatchFailure()
        else:
            # XXX Attributes are not currently handled.  Would like to
            # add keyword style syntax (xxx = yyy) for noting that a
            # constuctor argument is an attribute and not a field.
            # ??? How to make this compatible with syntax for binding? 
            # ???  Is there precident for establishing this?
            # ________________________________________
            # Look up field and attribute data for the given label.
            field_list = env['$ASDL'][constructor_name].__asdl_meta__['fields']
            # Map AST arguments to fields and attributes.
            field_map = map_fields(field_list, constructor_args)
            # Match fields against the current object; must match all
            # fields.
            for field_name, _, _, _ in field_list:
                match_val = field_map[field_name]
                obj_attr = getattr(obj, field_name)
                if match_val is None:
                    if obj_attr is not None:
                        raise asrl_utils.ASRLMatchFailure()
                else:
                    ret_val = __match(match_val, obj_attr, ret_val)
        return ret_val
    # ____________________________________________________________
    return __match(asrl_ast, obj, env)

# ______________________________________________________________________
# Main (self-test) routine.

def main (*args):
    import sys
    from parse_rws import ASRLParser
    base_env = build_rwenv_from_module_class(ASRL)
    test_pairs = (('"matchme"', "matchme", {}),
                  ('[1,2,3]', [1,2,3], {}),
                  ('(1.,2.,3.)', (1.,2.,3.), {}),
                  ('(a,a,b)', ("fred", "fred", "barney"), {"b":"barney"}),
                  ('Constructor("Constructor", args)',
                   ASRL.Constructor("Constructor", []), base_env),
                  )
    if args:
        print >>sys.stderr, "Ignoring arguments..."
    for rwexpstr, testobj, base_env in test_pairs:
        asrl_cst = ASRLParser.parse_string(rwexpstr, 'rwexp')
        asrl_ast = ASRLParser.cst_to_ast(asrl_cst)
        print match(asrl_ast, testobj, base_env)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asrl_match.py
