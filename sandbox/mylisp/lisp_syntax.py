# **************
# Syntax Definitions

def self_eval(exp):
    return (type(exp) in [int, str]
            or exp == ('symbol', 'nil')
            or exp == ('symbol', 't'))

def quoted(exp):
    return 'quote' == exp[0]

def quasiquoted(exp):
    return 'qquote' == exp[0]

def variable(exp):
    return type(exp) == tuple and exp[0] == 'symbol'

def if_stmt(exp):
    return ('symbol', 'if') == exp[0] and len(exp) == 4

def definition(exp):
    return ('symbol', 'def') == exp[0]

def assignment(exp):
    return ('symbol', 'set!') == exp[0] and len(exp) == 3

def method_call(exp):
    return type(exp) == list and exp[0] == ('symbol','.')

def application(exp):
    return type(exp) == list

def lambda_exp(exp):
    return exp[0] == ('symbol', 'fn')

def begin(exp):
    return exp[0] == ('symbol', 'begin')

# **************
# Accessors

# ('symbol', 'name')
def var_name(symbol_obj):
    return symbol_obj[1]

def assignment_var(exp):
    return var_name(exp[1])

def definition_var(exp):
    return var_name(exp[1])

def var_value(exp):
    return exp[2]

def quotation_text(exp):
    return exp[1]

# unwraps symbols tags
def lambda_params(exp):
    return [ p[1] for p in exp[1] ]

def lambda_body(exp):
    return exp[2:]

def mac_def(exp):
    return type(exp) == list and exp[0] == ('symbol','mac')

def mac_name(exp):
    return exp[0][1]

def mac_params(exp):
    return [ p[1] for p in exp[2] ]

def mac_body(exp):
    return exp[3:]

def operator(exp):
    return exp[0]

def args(exp):
    return exp[1:]

def if_pred(exp):
    return exp[1]

def if_conseq(exp):
    return exp[2]

def if_alt(exp):
    return exp[3]

       
