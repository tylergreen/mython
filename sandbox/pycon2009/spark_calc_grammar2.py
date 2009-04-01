#!/usr/bin/env python

from SPARK import *

class Token:
    # spark seems to dispatch in the parser based on a token's
    # type attribute
    def __init__(self, type, attr=None):
        self.type = type
        self.attr = attr

    def __str__(self):
        return self.type

    def __repr__(self):
        return str(self)

class SimpleScanner(GenericScanner):
    def __init__(self):
        GenericScanner.__init__(self)
    
    def tokenize(self, input):
        self.rv = []
        GenericScanner.tokenize(self, input)
        return self.rv
    
    def t_whitespace(self, s):
        r' \s+ '
        pass
        
    def t_op(self, s):
        r' \+ | \* '
        self.rv.append(Token(type=s))
        
    def t_number(self, s):
        r' \d+ '
        t = Token(type='number', attr=s)
        self.rv.append(t)

    def t_string(self,s):
        r'"\w*"'
        t = Token(type='string', attr=s)
        self.rv.append(t)


class ExprParser(GenericParser):
    def __init__(self, start='expr'):
        GenericParser.__init__(self, start)
                
    def p_expr_1(self, args):
        'expr ::= expr + term'
        return (args[1], [args[0],args[2]])

    def p_expr_2(self, args):
        'expr ::= term'
        return args[0]

    def p_term_1(self, args):
        'term ::= term * factor' 
        return (args[1], [args[0], args[2]])
        
    def p_term_2(self, args):
        'term ::= factor'
        return args[0]
        
    def p_factor_1(self, args):
        'factor ::= number'
        return (args[0],[])

scanner = SimpleScanner()
parser = ExprParser()

if __name__ == '__main__':
    while True:
       try:
           s = raw_input('calc > ')
       except EOFError:
           break
       if not s: continue
       toks = scanner.tokenize(s)
       print toks
       result = parser.parse(toks)
       print result
            
