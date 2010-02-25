"""This file contains the parser rules.

The function yacc.parse, which this function makes available, returns a parse 
tree.  The parse tree is a set of nested lists containing ints, floats, 
strings, Symbols, etc.
"""
import ply.yacc as yacc
import sys

from lisp_lexer import tokens
#from Symbol import Symbol

# add quotes, possibly read macros

def p_sexp(t):
    ''' sexp : atom
             | list
             | quoted
             | qquoted
             | unquoted
             | spliced
    '''
    t[0] = t[1]

def p_quoted(t):
    ''' quoted : QUOTE sexp '''
    t[0] = ('quote', t[2])

def p_qquoted(t):
    ''' qquoted : BACKQUOTE sexp '''
    t[0] = ('qquoted', t[2])

def p_unquoted(t):
    ''' unquoted : COMMA sexp '''
    t[0] = ('unquoted', t[2])

def p_spliced(t):
    ''' spliced : COMMA_AT list '''
    t[0] = ('spliced', t[2])

def p_list(t):
    'list : LPAREN sexps RPAREN'
    t[0] = t[2]

def p_sequence(t):
    'sexps : sexp sexps'
    t[0] = [t[1]] + t[2]

def p_atoms_empty(t):
    'sexps : empty'
    t[0] = []
def p_empty(t):
    'empty :'
    pass
def p_atom_int(t):
    'atom : INT'
    t[0] = t[1]
def p_atom_float(t):
    'atom : FLOAT'
    t[0] = t[1]
def p_atom_string(t):
    'atom : STRING'
    t[0] = t[1]
def p_atom_symbol(t):
    'atom : SYMBOL'
    t[0] = ('symbol',t[1])

# Error rule for syntax errors.
def p_error(t):
    raise SyntaxError("invalid syntax")
# Build the parser.
parser = yacc.yacc()

if __name__ == '__main__':
    while True:
       try:
           s = raw_input('sexp > ')
       except EOFError:
           break
       if not s: continue
       result = parser.parse(s)
       print result
