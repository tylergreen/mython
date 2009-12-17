"""
super tiny lisp to prolog compiler

supporting number, strings, if statements and some primitives

"""

from lisp_parser import parser

def rc(str):
    return compile_lisp(parser.parse(str))

# python_sexp -> string
def compile_lisp(sexp):
    if self_eval(sexp):
        return compile_self_eval(sexp)
    if quoted(sexp):
        return compile_quotation(sexp)
    if variable(sexp):
        return compile_variable(sexp)
    if if_stmt(sexp):
        return compile_if(sexp)
    if method_call(sexp):
        return compile_method_call(sexp)
    if application(sexp):
        return compile_application(sexp)
    if definition(sexp):
        return compile_def(sexp)
    else:
        e = 'unknown expression: ' + str(sexp)
        raise Exception(e)

# **************
# Syntax Definitions

def self_eval(sexp):
    return type(sexp) in [int, bool, str]

def quoted(sexp):
    return 'quote' == sexp[0]

def variable(sexp):
    return type(sexp) == tuple and sexp[0] == 'symbol'

def if_stmt(sexp):
    return ('symbol', 'if') == sexp[0] and len(sexp) == 4

def definition(sexp):
    return ('symbol', 'def') == sexp[0] 

def assignment(sexp):
    return ('symbol', 'set!') == sexp[0] and len(sexp) == 3

def method_call(sexp):
    return type(sexp) == list and sexp[0] == ('symbol','.')

def application(sexp):
    return type(sexp) == list

def binop(str):
    return str in ['+', '-','*', '/', '==']

def primitive(str):
    return str in ['list', 'cons','car','cdr']

# *******************
# Python Back End

def compile_self_eval(sexp):
    return repr(sexp)

def compile_quotation(sexp):
    _, text = sexp
    return text

def compile_variable(sexp):
    return sexp[1]

def compile_method_call(sexp):
    obj = sexp[2]
    _, method = sexp[1]
    args = ','.join( map(  compile_lisp, sexp[3:]))
    return "%r.%s(%s)" % (obj, method, args)

def compile_if(sexp):    
    cond = compile_lisp(sexp[1])
    conseq = compile_lisp(sexp[2])
    alt = compile_lisp(sexp[3])
    return "if %s: %s \n else: %s" % (cond, conseq, alt)

def compile_application(sexp):
    _, fn = sexp[0]
    args = sexp[1:]
    python_fn = lookup(fn)
    if binop(fn):
        return "reduce(lambda x,y: x %s y, [ %s ])" % (python_fn, ",".join(map(compile_lisp, args)))
    else:
        return "%s(%s)" % (python_fn, ",".join(map(compile_lisp, args)))
                           
def lookup(fn):
    return fn
