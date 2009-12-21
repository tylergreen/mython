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
import unittest

import basil.lang.python
from basil.parsing import trampoline, PgenParser, PyPgen

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

class PythonicTokenStream (trampoline.TokenStream):
    """Special token stream that ignores COMMENT and NL tokens, while
    properly converting OP tokens."""

    def tokenize (self):
        ret_val = next(self.tokenizer)
        while ret_val[0] in (tokenize.NL, tokenize.COMMENT):
            ret_val = next(self.tokenizer)
        if ((ret_val[0] == tokenize.OP) and
            (ret_val[1] in basil.lang.python.TokenUtils.operatorMap)):
            # This is a workaround for using the Python tokenize module.
            _, tok_str, tok_start, tok_end, tok_ln = ret_val
            tok_type = basil.lang.python.TokenUtils.operatorMap[tok_str]
            ret_val = (tok_type, tok_str, tok_start, tok_end, tok_ln)
        return ret_val

# ______________________________________________________________________
# Generic top-level parsing class.

class Parser (object):
    def parse_string (self, in_str):
        return self.parse_fileobj(StringIO(in_str))

    def parse_file (self, file_name):
        return self.parse_fileobj(open(file_name))

    def parse_fileobj (self, file_obj):
        tokenizer = mktokenizer(file_obj.readline)
        return self.parse_start(WhitespaceInsensitiveTokenStream(tokenizer))

    def parse_start (self, instream, outtree=None):
        raise NotImplementedError("parse_start() must be overridden")

# ______________________________________________________________________
# Recursive-descent parsing class.

class CalcParser (Parser):
    def parse_start (self, instream, outtree=None):
        if outtree is None:
            outtree = trampoline.TreeBuilder()
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
# Trampoline parsing classes

class TrampolineParser (Parser):
    def __init__ (self, handlers):
        Parser.__init__(self)
        self.handlers = handlers

    def parse_start (self, instream, outtree=None):
        return trampoline.trampoline_parse(self.handlers, instream, outtree)

# ______________________________________________________________________

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
# Unit test classes.

class TestTrampolineParser (unittest.TestCase):
    def setUp (self):
        self.parser1 = CalcParser()
        self.parser2 = TrampolineCalcParser()

    def _testparse (self, in_str):
        tree1 = self.parser1.parse_string(in_str).tree
        tree2 = self.parser2.parse_string(in_str).tree
        self.assertEqual(tree1, tree2)

    def testatoms (self):
        self._testparse("x")
        self._testparse("192838")
        self._testparse("(y)")

    def testterms (self):
        self._testparse("8 // 2")
        self._testparse("93 * x")
        self._testparse("y / z")
        self._testparse("84839 % m")

    def testariths (self):
        self._testparse("a + b + c")
        self._testparse("b - 8983")

    def testfullexpr (self):
        self._testparse("x * 7 // 3 + (y - 42) % 5\n\n")

# ______________________________________________________________________

def convert_pypgen_tree (grammar_obj, in_tree):
    symbol_to_string_map = grammar_obj.symbolToStringMap()
    def _convert_nt (nt_tup):
        symbol_index, _, _ = nt_tup
        if symbol_index in symbol_to_string_map:
            return symbol_to_string_map[symbol_index]
        return nt_tup
    def _convert_pypgen_tree (in_tree):
        return (_convert_nt(in_tree[0]),
                [_convert_pypgen_tree(child) for child in in_tree[1]])
    return _convert_pypgen_tree(in_tree)

# ______________________________________________________________________

def convert_trampoline_tree (in_tree):
    payload, children0 = in_tree
    children1 = [convert_trampoline_tree(child) for child in children0]
    if isinstance(payload, tuple):
        payload = (payload[0], payload[1], payload[2][0])
    return (payload, children1)

# ______________________________________________________________________

class TestPgenToHandler (unittest.TestCase):
    def setUp (self):
        # Parse the MyFront grammar, create a set of automata for it (like
        # pgen does), and then convert the automata to generators for the
        # treepoline.
        grammar_st = PgenParser.parseFile(basil.lang.python.__path__[0] +
                                          "/python26/Grammar")
        grammar_obj = PyPgen.buildParser(grammar_st)
        grammar_obj.setStart(grammar_obj.stringToSymbolMap()['file_input'])
        self.parser1 = grammar_obj
        gram_tup0 = grammar_obj.toTuple()
        gram_tup1 = basil.lang.python.DFAParser.addAccelerators(gram_tup0)
        handlers = trampoline.pgen_grammar_to_handlers(gram_tup1, {})
        # Override the start special nonterminal to just do what it is
        # supposed to:
        def parse_start (instream, outtree):
            yield 'file_input'
        handlers['start'] = parse_start
        self.handlers = handlers

    def _parsefile (self, filename):
        if filename[-2:] != "py":
            filename = filename[:-1]
        tree1 = convert_pypgen_tree(self.parser1,
                                    self.parser1.parseFile(filename))
        token_stream = PythonicTokenStream(
            mktokenizer(open(filename).readline))
        tree2 = convert_trampoline_tree(trampoline.trampoline_parse(
            self.handlers, token_stream).tree[1][0])
        if __debug__:
            print(" ".join((str(elem) for elem in [tree1[0], tree2[0]])))
        self.assertEquals(tree1, tree2)

    def testparsingme (self):
        self._parsefile(__file__)

    def testparsingtrampoline (self):
        trampoline_filename = trampoline.__file__
        self._parsefile(trampoline_filename)

# ______________________________________________________________________
# Main routine

if __name__ == "__main__":
    unittest.main()

# ______________________________________________________________________
# End of test_trampoline.py
