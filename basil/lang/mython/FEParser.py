#! /usr/bin/env python
from tokenize import *
from LL1Parser import LL1Parser, parser_main

class FEParser (LL1Parser):
    def parse_arith_expr (self):
        self.push('arith_expr')
        self.parse_term()
        while self.test_lookahead('-', '+'):
            if self.test_lookahead('+'):
                self.expect('+')
            else:
                self.expect('-')
            self.parse_term()
        return self.pop()

    def parse_atom (self):
        self.push('atom')
        if self.test_lookahead('('):
            self.expect('(')
            self.parse_expr()
            self.expect(')')
            if self.test_lookahead('|'):
                self.expect('|')
                self.parse_bounds()
        elif self.test_lookahead('<'):
            self.expect('<')
            self.parse_expr()
            self.expect(',')
            self.parse_expr()
            self.expect('>')
            if self.test_lookahead('_'):
                self.parse_bounds()
        elif self.test_lookahead(NAME):
            self.expect(NAME)
        else:
            self.expect(NUMBER)
        return self.pop()

    def parse_bounds (self):
        self.push('bounds')
        self.expect('_')
        self.expect(NAME)
        return self.pop()

    def parse_constraint (self):
        self.push('constraint')
        self.parse_expr()
        while self.test_lookahead('='):
            self.expect('=')
            self.parse_expr()
        return self.pop()

    def parse_decl (self):
        self.push('decl')
        if self.test_lookahead('TestFunction'):
            self.expect('TestFunction')
            self.parse_id_list()
        elif self.test_lookahead('UnknownField'):
            self.expect('UnknownField')
            self.parse_id_list()
        elif self.test_lookahead('CoordinateFunction'):
            self.expect('CoordinateFunction')
            self.parse_id_list()
        else:
            self.expect('Field')
            self.parse_id_list()
        return self.pop()

    def parse_expr (self):
        self.push('expr')
        self.parse_arith_expr()
        while self.test_lookahead('dot', 'cross'):
            self.parse_vec_op()
            self.parse_arith_expr()
        return self.pop()

    def parse_factor (self):
        self.push('factor')
        if self.test_lookahead('grad', 'trans', 'div', '-', '+'):
            if self.test_lookahead('+'):
                self.expect('+')
            elif self.test_lookahead('-'):
                self.expect('-')
            elif self.test_lookahead('grad'):
                self.expect('grad')
            elif self.test_lookahead('div'):
                self.expect('div')
            else:
                self.expect('trans')
            self.parse_factor()
        else:
            self.parse_power()
        return self.pop()

    def parse_id_list (self):
        self.push('id_list')
        self.expect(NAME)
        while self.test_lookahead(','):
            self.expect(',')
            self.expect(NAME)
        return self.pop()

    def parse_line (self):
        self.push('line')
        if self.test_lookahead('TestFunction', 'CoordinateFunction', 'UnknownField', 'Field'):
            self.parse_decl()
        else:
            self.parse_constraint()
        self.expect(NEWLINE)
        return self.pop()

    def parse_power (self):
        self.push('power')
        self.parse_atom()
        if self.test_lookahead('^'):
            self.expect('^')
            self.parse_factor()
        return self.pop()

    def parse_start (self):
        self.push('start')
        while self.test_lookahead(NAME, 'grad', 'UnknownField', '-', NUMBER, 'TestFunction', 'trans', '(', 'Field', 'CoordinateFunction', 'div', '+', '<'):
            self.parse_line()
        self.expect(ENDMARKER)
        return self.pop()

    def parse_term (self):
        self.push('term')
        self.parse_factor()
        while self.test_lookahead('*', '/'):
            if self.test_lookahead('*'):
                self.expect('*')
            else:
                self.expect('/')
            self.parse_factor()
        return self.pop()

    def parse_vec_op (self):
        self.push('vec_op')
        if self.test_lookahead('cross'):
            self.expect('cross')
        else:
            self.expect('dot')
        return self.pop()

    def tokenize (self):
        ret_val = self.tokenizer.next()
        while ret_val[0] in (INDENT, DEDENT, COMMENT, NL):
            ret_val = self.tokenizer.next()
        return ret_val


if __name__ == '__main__':
    parser_main(FEParser)

