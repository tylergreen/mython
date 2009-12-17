#! /usr/bin/env python
# ______________________________________________________________________
"""test_trampoline.py

Tests the Basil 'trampoline' parser by comparing it to a
recursive-descent parser for the following little language:

start: arith_expr* ENDMARKER
arith_expr: term (('+'|'-') term)*
term: atom (('//'|'*'|'/'|'%') atom)*
atom: '(' arith_expr ')'
    | NUMBER
    | NAME

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import tokenize

from basil.parsing import trampoline

# ______________________________________________________________________
# Compatibility layer

if not hasattr(tokenize, 'ENCODING'):
    tokenize.ENCODING = 57

try:
    from StringIO import StringIO
    mktokenizer = tokenize.generate_tokens
except ImportError:
    import io
    def StringIO (in_str):
        return io.BytesIO(in_str.encode('utf-8'))
    mktokenizer = tokenize.tokenize

# ______________________________________________________________________

class WhitespaceInsensitiveTokenStream (trampoline.ExclusiveTokenStream):
    def __init__ (self, tokenizer):
        exclusion_set = set([getattr(tokenize, token_name)
                             for token_name in ('NEWLINE', 'DEDENT', 'INDENT',
                                                'NL', 'COMMENT', 'ENCODING')])
        trampoline.ExclusiveTokenStream.__init__(self, tokenizer,
                                                 exclusion_set)

# ______________________________________________________________________
# Generic top-level parsing class.

class Parser (object):
    def parse_string (self, in_str):
        return self.parse_fileobj(StringIO(in_str))

    def parse_file (self, file_name):
        return self.parse_fileobj(open(file_name))

    def parse_fileobj (self, file_obj):
        tokenizer = mktokenizer(file_obj.readline)
        outtree = trampoline.TreeBuilder()
        return self.parse_start(WhitespaceInsensitiveTokenStream(tokenizer),
                                outtree)

# ______________________________________________________________________
# Recursive-descent parsing class.

class CalcParser (Parser):
    def parse_start (self, instream, outtree):
        while not instream.test_lookahead(tokenize.ENDMARKER):
            self.parse_arith_expr(instream, outtree)
        outtree.pushpop(instream.expect(tokenize.ENDMARKER))
        return outtree

    def parse_arith_expr (self, instream, outtree):
        outtree.push('arith_expr')
        self.parse_term(instream, outtree)
        while instream.test_lookahead('-', '+'):
            if instream.test_lookahead('+'):
                outtree.pushpop(instream.expect('+'))
            else:
                outtree.pushpop(instream.expect('-'))
            self.parse_term(instream, outtree)
        outtree.pop()
        return outtree

    def parse_term (self, instream, outtree):
        outtree.push('term')
        self.parse_atom(instream, outtree)
        while instream.test_lookahead('//', '*', '/', '%'):
            if instream.test_lookahead('*'):
                outtree.pushpop(instream.expect('*'))
            elif instream.test_lookahead('/'):
                outtree.pushpop(instream.expect('/'))
            elif instream.test_lookahead('%'):
                outtree.pushpop(instream.expect('%'))
            else:
                outtree.pushpop(instream.expect('//'))
            self.parse_atom(instream, outtree)
        outtree.pop()
        return outtree

    def parse_atom (self, instream, outtree):
        outtree.push('atom')
        if instream.test_lookahead('('):
            outtree.pushpop(instream.expect('('))
            self.parse_arith_expr(instream, outtree)
            outtree.pushpop(instream.expect(')'))
        elif instream.test_lookahead(tokenize.NUMBER):
            outtree.pushpop(instream.expect(tokenize.NUMBER))
        else:
            outtree.pushpop(instream.expect(tokenize.NAME))
        outtree.pop()
        return outtree

# ______________________________________________________________________
# Trampoline parsing functions

class TrampolineParser (Parser):
    def __init__ (self, handlers):
        Parser.__init__(self)
        self.handlers = handlers

    def parse_start (self, instream, outtree):
        return trampoline.trampoline_parse(self.handlers, instream, outtree)


class TrampolineCalcParser (TrampolineParser):
    def __init__ (self):
        TrampolineParser.__init__(self, 
                                  {'start' : self.parse_start_gen,
                                   'arith_expr' : self.parse_arith_expr_gen,
                                   'term' : self.parse_term_gen,
                                   'atom' : self.parse_atom_gen})

    def parse_start_gen (self, instream, outtree):
        while not instream.test_lookahead(tokenize.ENDMARKER):
            yield 'arith_expr'
        outtree.pushpop(instream.expect(tokenize.ENDMARKER))
        return

    def parse_arith_expr_gen (self, instream, outtree):
        outtree.push('arith_expr')
        yield 'term'
        while instream.test_lookahead('-', '+'):
            if instream.test_lookahead('+'):
                outtree.pushpop(instream.expect('+'))
            else:
                outtree.pushpop(instream.expect('-'))
            yield 'term'
        outtree.pop()
        return

    def parse_term_gen (self, instream, outtree):
        outtree.push('term')
        yield 'atom'
        while instream.test_lookahead('//', '*', '/', '%'):
            if instream.test_lookahead('*'):
                outtree.pushpop(instream.expect('*'))
            elif instream.test_lookahead('/'):
                outtree.pushpop(instream.expect('/'))
            elif instream.test_lookahead('%'):
                outtree.pushpop(instream.expect('%'))
            else:
                outtree.pushpop(instream.expect('//'))
            yield 'atom'
        outtree.pop()
        return

    def parse_atom_gen (self, instream, outtree):
        outtree.push('atom')
        if instream.test_lookahead('('):
            outtree.pushpop(instream.expect('('))
            yield 'arith_expr'
            outtree.pushpop(instream.expect(')'))
        elif instream.test_lookahead(tokenize.NUMBER):
            outtree.pushpop(instream.expect(tokenize.NUMBER))
        else:
            outtree.pushpop(instream.expect(tokenize.NAME))
        outtree.pop()
        return

# ______________________________________________________________________
# Main routine

def main (*args):
    import pprint
    parser1 = CalcParser()
    parser2 = TrampolineCalcParser()
    if len(args) > 1:
        for arg in args:
            tree1 = parser1.parse_file(arg).tree
            tree2 = parser2.parse_file(arg).tree
            assert tree1 == tree2
    else:
        test_str = "x * 7 // 3 + (y - 42) % 5\n\n"
        tree1 = parser1.parse_string(test_str).tree
        tree2 = parser2.parse_string(test_str).tree
        assert tree1 == tree2

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*(sys.argv[1:]))

# ______________________________________________________________________
# End of test_trampoline.py
