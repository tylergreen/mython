#! /usr/bin/env python
"""Module myopts.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

# XXX

# ______________________________________________________________________
# Function definitions

def dummy_opt (tree, env):
    print tree
    return tree, env

# ______________________________________________________________________

def compose_passes (pass_1, pass_2):
    return lambda tree, env : pass_2(*pass_1(tree, env))

# ______________________________________________________________________

def compose_rewrites (*rws):
    def _composed_rewrites (tree, env):
        ret_val = (None, env)
        for rw in rws:
            rw_result = rw(tree, env)
            if rw_result[0] is not None:
                return rw_result
        return ret_val
    return _composed_rewrites

# ______________________________________________________________________

def simple_rw_opt (tree, env):
    rw_result = None
    rw_fn = env.get("rw_%s" % type(tree).__name__, None)
    if rw_fn is not None:
        rw_result, env = rw_fn(tree, env)
    if rw_result is None:
        ctor, kids = explode(tree)
        opt_kids = []
        for kid in kids:
            opt_kid, env = simple_rw_opt(kid, env)
            opt_kids.append(opt_kid)
        rw_result = ctor(opt_kids)
    return rw_result, env

# Using this, how would we do constant folding?
class XXX:
    def fold_binary_op (tree):
        if ((type(tree) == BinOp) and
            (type(tree.left) == Num) and
            (type(tree.right) == Num)):
            op_fn = get_op(tree.op)
            return Num(op_fn(tree.left.n,
                             tree.right.n))
        return None
    def rw_BinOp (tree, env):
        return fold_binary_op(tree), env

# ______________________________________________________________________

def extend_rws (node_type_name, rw, env):
    env_out = env.copy()
    rw_name = "rw_%s" % node_type_name
    if rw_name in env:
        env_out[rw_name] = compose_rewrites(*[rw, env[rw_name]])
    else:
        env_out[rw_name] = rw
    return env_out

# ______________________________________________________________________

def deforestation_test ():
    quote [myfront]:
        my_mvs = ('x', 'y', 'z', 'i0', 'i1')
    quote [mypattern(*my_mvs)] p0:
        [x(i0) for i0 in [y(i1) for i1 in z]]
    quote [mypattern(*my_mvs)] p1:
        [x(y(i1)) for i1 in z]
    quote [myrewrite]: p0 => p1

def mypattern (*mvs):
    def _quoter (name, code, env0):
        env1 = env0.copy()
        expr_ast = myparse_expr(code, env1)
        val = (mvs, expr_ast)
        if name is not None:
            env1[name] = val
        return [], env1
    return _quoter

def myrewrite (name, code, env0):
    lhs_name, rhs_name = code.split("=>")
    lhspat = env0[lhs_name]
    rhspat = env0[rhs_name]
    def _rewriter (expr, rwenv):
        match_env = mymatch(lhspat, expr)
        if match_env is not None:
            return myctor(rhspat, match_env), rwenv
        return None, rwenv
    match_node_type_name, _, _ = explode(lhs)
    env1 = extend_rws(match_node_type_name, _rewriter, env0)
    if name is not None:
        env1[name] = val
    return [], env1

def pattern2lambda (pattern):
    mvs, expr = pattern
    return _ast.Lambda(([_ast.Name(n, _ast.Load()) for n in mvs],
                        None, None, []),
                       expr)

def add_hlop (name, pattern, env0):
    if 'hlops' in env0:
        hlops = env0['hlops'].copy()
    else:
        hlops = {}
    hlops[name] = pattern
    env1 = env0.copy()
    env1['hlops'] = hlops
    return env1

def hlop (*params):
    def _quoter (name, code, env0):
        lineno = env0.get('lineno', -1)
        assert name is not None, ("Quotation error, line %d: quotation form "
                                  "must be named." % lineno)
        assert name not in env0.get('hlops', {}), ("Quotation error, line %d: "
                                                   "'%s' already defined in "
                                                   "HLOPs." % (lineno, name))
        expr_ast = myparse_expr(code, env0)
        pat = (params, expr_ast)
        env1 = add_hlop(name, pat, env0)
        lam_expr = pattern2lambda(pat)
        stmt_list = [_ast.Assign([_ast.Name(name, _ast.Store())], lam_expr)]
        env1[name] = lam_expr
        return stmt_list, env1
    return _quoter

def hlop_rw (expr, env0):
    if type(expr.func) == _ast.Name:
        fnname = expr.func.id
        hlops = env0.get('hlops', {})
        if fnname in hlops:
            return myinliner(pat, expr, env0), env0
    return None, env0

def myinliner (pat, expr, env0):
    # XXX Implement me!
    return None

"""
mymatchexpr (mvs, Name(id, ctx), e1) = if id in mvs then Some({id : e1})
                                       else case e1 of
                                              Name(id, ctx) => Some({})
                                              _ => None
                                            end
mymatchexpr (mvs, e0, e1) =
  if asttypeeq(e0, e1) then
    unify_envs([mymatchexpr(k1, k2) for k1, k2 in zip(kids(e0), kids(e1))])
  else None
"""

def mymatchexpr (mvs, tree0, tree1):
    node_type_name0, ctor0, kids0 = explode(tree0)
    node_type_name1, ctor1, kids1 = explode(tree1)
    if (node_type_name0 == "Name") and (tree0.id in mvs):
        return {tree0.id : tree1}
    elif (node_type_name0 == node_type_name1) and (len(kids0) == len(kids1)):
        return unify_env(*[mymatchexpr(mvs, kid0, kid1, env)
                           for kid0, kid1 in zip(kids0, kids1)])
    return None

mkmatch = lambda mvs, expr0 : (lambda expr1 : mymatchexpr(mvs, expr0, expr1))

def unify_env (*envs):
    if len(envs) == 0:
        return None
    unified_env = {}
    for env in envs:
        if env is None:
            return None
        for key, val in env.items():
            if key in unified_env:
                # XXX Requires special equality test for AST nodes...
                if unified_env[key] != val:
                    return None
            else:
                unified_env[key] = val
    return unified_env

def mkctor

# ______________________________________________________________________

def copyast (tree, mvmap):
    node_type_name, ctor, kids = explode(tree)
    if node_type_name == "Name" and tree.id in mvmap:
        return copyast(mvmap[tree.id], {})
    return ctor([copyast(kid, mvmap) for kid in kids])

# ______________________________________________________________________

def compose_pass_list (*passes):
    def _composed_passes (tree, env):
        ret_val = (tree, env)
        for pass in passes:
            ret_val = pass(*ret_val)
        return ret_val
    return _composed_passes

# ______________________________________________________________________

def rw_default (tree, env):
    return None, env

# ______________________________________________________________________

def mk_simple_rw_opt (prefix):
    def _simple_rw_opt (tree, env):
        rw_name = prefix + type(tree).__name__
        if rw_name in env:
            rw_fn = env[rw_name]
        else:
            rw_fn = env['rw_default']
        rw_result, env = rw_fn(tree, env)
        if rw_result is None:
            did_rw = False
            ctor, kids = explode(tree)
            opt_kids = []
            for kid in kids:
                opt_kid, env = _simple_rw_opt(kid, env)
                if opt_kid is not None:
                    did_rw = True
                    opt_kids.append(opt_kid)
                else:
                    opt_kids.append(kid)
            rw_result = ctor(opt_kids)
        return rw_result, env
    _simple_rw_opt.__name__ = "%s_simple_rw_opt" % prefix
    _simple_rw_opt.__doc__ = ("Rewrite optimization pass for rewrite "
                              "functions using the '%s' prefix." % prefix)
    return _simple_rw_opt

# ______________________________________________________________________

def qtest ():
    def mybackend (tree, env):
        print "mybackend", tree, env
        return (None, env)

    def myopt (tree, env):
        print "myopt", tree, env
        return (tree, env)

    def compose_pass(f1, f2):
        return lambda tree, env : f1(*f2(tree, env))

    mybackend('xxx', {})
    myopt('xxx', {})
    mybackend = compose_pass(mybackend, myopt)
    mybackend('xxx', {})


# ______________________________________________________________________
# End of myopts.py
