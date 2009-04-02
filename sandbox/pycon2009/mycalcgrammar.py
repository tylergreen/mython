import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from calclex import tokens

__DEBUG__ = False

def p_start_assign(p):
    ' start : ID ASSIGN expression '
    p[0] = ('<-', [(p[1],[]),p[3]])

def p_start(p):
    ' start : expression '
    p[0] = p[1]

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = ('+', [ p[1],p[3]])

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = ('-', [ p[1],p[3]])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', [ p[1],p[3]])

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('/', [ p[1],p[3]])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = (p[1],[])

def p_factor_num(p):
    'factor : NUMBER'
    if __DEBUG__:
        print type(p[1]), p[1]
    p[0] = (p[1],[])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input!"

# Build the parser
parser = yacc.yacc()

if __name__ == '__main__':
    while True:
       try:
           s = raw_input('calc-parse> ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print result
    
