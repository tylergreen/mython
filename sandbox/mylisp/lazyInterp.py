import lisp_parser
from lisp_syntax import *

def interp(exp,env):
    '''
    exp is a python list (parsed from parser)
    env is a list of dicts { string : value }
    '''
    if self_eval(exp):
        return exp
    if variable(exp):
        return lookup(var_name(exp), env)
    if quoted(exp):
        return quotation_text(exp)
    if assignment(exp):
        return eval_assignment(exp,env) 
    if definition(exp):
        return eval_definition(exp,env) 
    if if_stmt(exp):
        return eval_if(exp,env)
    if lambda_exp(exp):
        return Procedure(exp,env)
    if begin(exp):
        return eval_sequence(exp[1:],env)
    # cond
    if application(exp):  # todo
        return lazy_apply(actual_value(operator(exp),env), 
                          args(exp),
                          env)
    else:
        raise Exception('unknown expression: ' + str(sexp))

#***************
# Thunk Section ( currently non-memoized )

class Thunk():
    def __init__(self,exp, env):
        self.exp = exp
        self.env = env

def thunk(obj):
    print  "thunk about it " , obj
    return type(obj) == tuple and obj[0] == 'thunk'

def delay_it(exp, env):
    return ('thunk', exp, env)

def force_it(obj):
    if thunk(obj):
        return actual_value(obj[1], obj[2])
    else:
        return obj

def actual_value(exp, env):
    print "actually...", exp
    return force_it(interp(exp, env))

#********

def lookup(var, env):
    for frame in env:
        if var in frame:
            return frame[var]
    raise Exception('unbound variable: ' + var)

class Procedure():
    def __init__(self,exp,env):
        self.params = lambda_params(exp)
        self.body = lambda_body(exp)
        self.env = env

def eval_definition(exp, env):
    v = definition_var(exp)
    env[0][v] = interp(var_value(exp), env)
    return v

# this version will only modify an existing variable
def eval_assignment(exp,env):
    v = assignment_var(exp)
    for f in env:
        if v in f:
            f[v] = interp(var_value(exp),env)
            return v
    raise Exception('undefined variable ' + v)

# modified for laziness
def eval_if(exp,env):
    if lisp_true(actual_value(if_pred(exp),env)):
        return interp(if_conseq(exp),env)
    else:
        return interp(if_alt(exp), env)

# truth as defined by our implementation
def lisp_true(exp):
    return not (exp == ('symbol', 'nil') or 
                exp == [])

def eval_sequence(exp, env):
    for e in exp:
        result = interp(e,env)
    return result  # just return the last result

def lazy_apply(proc, args, env):
    if primitive(proc):
        return proc(*[actual_value(a,env) for a in args])
    else:
        return eval_sequence(proc.body,
                             extend_env(proc.params,
                                        [delay_it(a,env) for a in args],
                                        proc.env))

def extend_env(vars, vals, base_env):
    return [dict(zip(vars,vals))] + base_env

#*****************
# primitives

def primitive(op):
    return op in prims.values()

# need to make these more efficient eventually
def car(lst):
    return lst[0]

def cdr(lst):
    return lst[1:]

def cons(x, y):
    return (x,y)

def l_list(*args):
    return reduce(cons, [], args)

# can we use decorators here or factor this in some other way
def plus(*args):
    return reduce(lambda x,y: x + y, args)

def minus(*args):
    return reduce(lambda x,y: x - y, args)

def mult(*args):
    return reduce(lambda x,y: x * y, args)

def divide(*args):
    return reduce(lambda x,y: x / y, args)

prims = { 'car' : car,
          'cdr' : cdr,
          'cons': cons,
          'list': l_list,
          '+' : plus,
          '-' : minus,
          '*' : mult,
          '/' : divide,
          } 

# how can I put definitions written in lisp in this file using mython?

init_env = [ prims ]

# ******************
# Running and crap

def parse(string):
    return lisp_parser.parser.parse(string)

def i(string):
    return interp(parse(string),init_env)
def lisp_interpreter(string):
    return interp(parse(string),init_env)
