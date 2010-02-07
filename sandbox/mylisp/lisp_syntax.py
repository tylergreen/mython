# **************
# Syntax Definitions

def self_eval(sexp):
    return (type(sexp) in [int, str]
            or sexp == ('symbol', 'nil')
            or sexp == ('symbol', 't'))

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

def lambda_exp(sexp):
    return sexp[0] == ('symbol', 'fn')

def begin(sexp):
    return sexp[0] == ('symbol', 'begin')

# def primitive(str):
#    return str in ['list', 'cons','car','cdr']

# **************
# Accessors


# ('symbol', 'name')
def var_name(symbol_obj):
    return symbol_obj[1]

def assignment_var(sexp):
    return var_name(sexp[1])

def definition_var(sexp):
    return var_name(sexp[1])

def var_value(sexp):
    return sexp[2]

def quotation_text(sexp):
    return sexp[1]

def lambda_params(sexp):
    return [ p[1] for p in sexp[1] ]

def lambda_body(sexp):
    return sexp[2:]

def operator(sexp):
    return sexp[0]

def args(sexp):
    return sexp[1:]

def if_pred(sexp):
    return sexp[1]

def if_conseq(sexp):
    return sexp[2]

def if_alt(sexp):
    return sexp[3]


    
