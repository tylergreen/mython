import lisp_parser
from lisp_syntax import *
from itertools import chain

# todo 
# pretty printer
# stdprelude
# quasi quote
# tail recursion
# first class continuations

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
    if quasiquoted(exp):
        return interp(qq_expand(tag_data(exp)), env)
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
    # a macro is just a normal function with an annotation that says don't evaluate args -- but what about all the symbol tag crap?  I think that will be ok
    if mac_def(exp):
        macro_name = exp[1][1]
        macros.append(macro_name)
        m = Macro(exp,env)
        env[0][macro_name] = m
        return m
    if macro(exp):
        expander = lookup(mac_name(exp), env)
        return interp(lisp_apply(expander, args(exp)), env) # need to extend env
    if application(exp):  # todo
        op = interp(operator(exp),env)
        vals = [interp(arg,env) for arg in args(exp)]
        return lisp_apply(op, vals)
    else:
        raise Exception('unknown expression: ' + str(exp))

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

class Macro(Procedure):
    def __init__(self, exp, env):
        self.params = mac_params(exp)
        self.body = mac_body(exp)
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

def eval_if(exp,env):
    if lisp_true(interp(if_pred(exp), env)):
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

def lisp_apply(proc, args):
    if primitive(proc):
        return proc(*args)
    else:
        return eval_sequence(proc.body,
                             extend_env(proc.params,
                                        args,
                                        proc.env))

def extend_env(vars, vals, base_env):
    return [dict(zip(vars,vals))] + base_env

#*****************
# primitives

def primitive(op):
    return op in prims

# need to make these more efficient eventually
def car(lst):
    return lst[0]

def cdr(lst):
    return lst[1:]

# very important to rectify the discrepcy between 
# lisp and python lists -- especially for quasi quote
def cons(x, y):
    return (x,y)

#def l_list(*args):
#    return reduce(cons, [], args)

def l_list(*args):
    return list(args)

def append(*args):
    return reduce(lambda x,y: x + y, args)

# can we use decorators here or factor this in some other way
def plus(*args):
    return reduce(lambda x,y: x + y, args)

def minus(*args):
    return reduce(lambda x,y: x - y, args)

def mult(*args):
    return reduce(lambda x,y: x * y, args)

def divide(*args):
    return reduce(lambda x,y: x / y, args)

# need to change these -- don't like
def greater_than(a,b):
    if a > b:
        return 1
    else: return []

def less_than(a,b):
    if a > b:
        return 1
    else: return []
    
def equal(a,b):
    if a == b:
        return 1
    else: return []

prim_dict =  { 'car' : car,
               'cdr' : cdr,
               'cons': cons,
               'list': l_list,
               'append' : append,
               '+' : plus,
               '-' : minus,
               '*' : mult,
               '/' : divide,
               '>' : greater_than,
               '<' : less_than,
               '=' : equal,
               } 

prims = prim_dict.values()

# careful, python is super not Functional.  prim_dict gets modified when 
# messing with init_env[0] 
init_env = [ prim_dict ]

# how can I put definitions written in lisp in this file using mython?

# need to add &body args 
def macro(exp):
    return type(exp) == list and len(exp) == 4 and (operator(exp)[1] in macros)


#*******************
# Quasi Quote

def tag(string, x):
    return type(x) == tuple and x[0] == string

def tag_data(x):
    return x[1]

def qq_expand(x):
    if tag('unquote',x):
        return tag_data(x)
    if tag('spliced',x):
        raise Exception('Illegal ,@')
    if tag('qquote', x):
        return qq_expand(qq_expand(tag_data(x)))
    if type(x) == list and x != [] :
        return [('symbol', 'append'),
                qq_expand_list(x[0]), 
                qq_expand(x[1:])] 
    else:
        return ('quote', x)

def qq_expand_list(x):
    if tag('unquote',x):
        return [('symbol', 'list'), tag_data(x) ]
    if tag('spliced', x):
        return tag_data(x)
    if tag('qquote', x):
        return qq_expand_list(qq_expand(tag_data(x)))
    if type(x) == list and x != []:
        return [('symbol', 'list'),
                [('symbol', 'append'),
                 qq_expand_list(x[0]),
                 qq_expand(x[1:]) ] ]
    else:
        return ('quote', [ x ])

# ******************
# Running and crap

def parse(string):
    return lisp_parser.parser.parse(string)

def i(string):
    return interp(parse(string),init_env)
def lisp_interpreter(string):
    return interp(parse(string),init_env)

macros = [ ]  # list of registered macros

# want to put defs in separate file
defs = ["(mac defn (name args body) `(def ,name (fn ,args ,body)))"]

def stdprelude():
    for d in defs:
        i(d)

stdprelude()


