#! /usr/bin/env python
# ______________________________________________________________________
"""Module myparser

The Mython parser.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import StringIO
from tokenize import *

from LL1Parser import LL1Parser, parser_main

from basil.parsing import PgenParser, PyPgen, nfa, trampoline
import basil.lang.python
from basil.lang.python import DFAParser
from basil.lang.mython import mylexer
from basil.lang.mython.MyFrontExceptions import MyFrontSyntaxError

# ______________________________________________________________________
# Module data

MY_GRAMMAR_EXT = """
compound_stmt: quotedef
quotedef: 'quote' ['[' expr ']'] [NAME] qsuite
qsuite: ':' (QUOTED NEWLINE | NEWLINE QUOTED)
"""

MY_START_SYMBOL = 'file_input'

pgen = PyPgen.PyPgen()
py_grammar_path = os.path.split(basil.lang.python.__file__)[0]
py_nfa_grammar = pgen.handleStart(PgenParser.parseFile(
    os.path.join(py_grammar_path, 'python26/Grammar')))
ext_nfa_grammar = pgen.handleStart(PgenParser.parseString(MY_GRAMMAR_EXT))
my_nfa_grammar = nfa.compose_nfas(py_nfa_grammar, ext_nfa_grammar)
my_grammar0 = pgen.generateDfaGrammar(my_nfa_grammar, MY_START_SYMBOL)
pgen.translateLabels(my_grammar0, {'QUOTED' : mylexer.QUOTED})
pgen.generateFirstSets(my_grammar0)
my_grammar0[0] = map(tuple, my_grammar0[0])
my_grammar0 = tuple(my_grammar0)
my_grammar = DFAParser.addAccelerators(my_grammar0)
del my_grammar0

__DEBUG__ = False

if __DEBUG__:
    import pprint

# ______________________________________________________________________
# Class and function definitions

class MyComposedParser (object):
    def __init__ (self):
        global my_grammar
        self.handlers = trampoline.pgen_grammar_to_handlers(my_grammar, {})
        self.handlers['start'] = self.parse_start
        self.handlers['qsuite'] = self.parse_qsuite
        qsuite_index = [dfa[0] for dfa in my_grammar[0]
                        if dfa[1] == 'qsuite'][0]
        self.handlers[qsuite_index] = self.parse_qsuite

    def parse_start (self, instream, outtree):
        global MY_START_SYMBOL
        yield MY_START_SYMBOL

    def parse_qsuite (self, instream, outtree):
        instream.start_quote()
        # NOTE: The extension grammar has a small hack so that the
        # lookahead for pushing a qsuite is a colon, not a QUOTED or
        # NEWLINE.
        outtree.pushpop(instream.expect(':'))
        outtree.push('qsuite')
        if instream.test_lookahead(NEWLINE):
            outtree.pushpop(instream.expect(NEWLINE))
            outtree.pushpop(instream.expect(mylexer.QUOTED))
        else:
            outtree.pushpop(instream.expect(mylexer.QUOTED))
            outtree.pushpop(instream.expect(NEWLINE))
        outtree.pop()
        if False:
            yield 'dummy'

    def parse_lineiter (self, lineiter, env = None):
        if env is None:
            env = {}
        line_offset = env.get("lineno", 1) - 1
        column_offset = env.get("column_offset", 0)
        filename = env.get("filename", "<string>")
        readliner = mylexer.MythonReadliner(lineiter)
        token_stream = mylexer.MythonTokenStream(readliner,
                                                 lnum = line_offset,
                                                 column_offset = column_offset)
        tree_builder = trampoline.TreeBuilder()
        try:
            tree_builder = trampoline.trampoline_parse(
                self.handlers, token_stream, tree_builder)
        except SyntaxError, syntax_err:
            if __DEBUG__:
                pprint.pprint(tree_builder.__dict__)
            if syntax_err.args[0].startswith("Line"):
                err_str = "File '%s', l%s" % (filename, syntax_err.args[0][1:])
            else:
                err_str = "File '%s', %s" % (filename, syntax_err.args[0])
            raise MyFrontSyntaxError(err_str)
        return tree_builder.tree

    def parse_file (self, filename, env = None):
        if env is not None:
            if "filename" not in env:
                env = env.copy()
                env["filename"] = filename
        return self.parse_lineiter(open(filename).next, env)

    def parse_string (self, src_str, env = None):
        if env is not None:
            if "filename" not in env:
                env = env.copy()
                env["filename"] = "<string>"
        return self.parse_lineiter(StringIO.StringIO(src_str).next, env)

# ______________________________________________________________________
# Older parser -- DEPRECATED

class MyParser (LL1Parser):
    """Class MyParser

    DEPRECATED.
    """
    def __init__ (self, *args, **kws):
        LL1Parser.__init__(self, *args, **kws)
        self.keywords = set(['and', 'elif', 'is', 'global', 'as', 'in', 'if', 'from', 'raise', 'for', 'except', 'finally', 'print', 'import', 'pass', 'return', 'exec', 'quote', 'else', 'assert', 'not', 'with', 'class', 'break', 'yield', 'try', 'while', 'continue', 'del', 'or', 'def', 'lambda'])

    def parse_and_expr (self):
        self.push('and_expr')
        self.parse_shift_expr()
        while self.test_lookahead('&'):
            self.expect('&')
            self.parse_shift_expr()
        return self.pop()

    def parse_and_test (self):
        self.push('and_test')
        self.parse_not_test()
        while self.test_lookahead('and'):
            self.expect('and')
            self.parse_not_test()
        return self.pop()

    def parse_arglist (self):
        self.push('arglist')
        while self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
            self.parse_argument()
            self.expect(',')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
            self.parse_argument()
            if self.test_lookahead(','):
                self.expect(',')
        elif self.test_lookahead('*'):
            self.expect('*')
            self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
                self.expect('**')
                self.parse_test()
        else:
            self.expect('**')
            self.parse_test()
        return self.pop()

    def parse_argument (self):
        self.push('argument')
        self.parse_test()
        if self.test_lookahead('='):
            self.expect('=')
            self.parse_test()
        else:
            if self.test_lookahead('for'):
                self.parse_gen_for()
        return self.pop()

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

    def parse_assert_stmt (self):
        self.push('assert_stmt')
        self.expect('assert')
        self.parse_test()
        if self.test_lookahead(','):
            self.expect(',')
            self.parse_test()
        return self.pop()

    def parse_atom (self):
        self.push('atom')
        if self.test_lookahead('('):
            self.expect('(')
            if self.test_lookahead('~', 'not', '-', NUMBER, 'yield', '(', '{', '[', STRING, 'lambda', '`', '+', NAME):
                if self.test_lookahead('yield'):
                    self.parse_yield_expr()
                else:
                    self.parse_testlist_gexp()
            self.expect(')')
        elif self.test_lookahead('['):
            self.expect('[')
            if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
                self.parse_listmaker()
            self.expect(']')
        elif self.test_lookahead('{'):
            self.expect('{')
            if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
                self.parse_dictmaker()
            self.expect('}')
        elif self.test_lookahead('`'):
            self.expect('`')
            self.parse_testlist1()
            self.expect('`')
        elif self.test_lookahead(NAME):
            self.expect(NAME)
        elif self.test_lookahead(NUMBER):
            self.expect(NUMBER)
        else:
            self.expect(STRING)
            while self.test_lookahead(STRING):
                self.expect(STRING)
        return self.pop()

    def parse_augassign (self):
        self.push('augassign')
        if self.test_lookahead('+='):
            self.expect('+=')
        elif self.test_lookahead('-='):
            self.expect('-=')
        elif self.test_lookahead('*='):
            self.expect('*=')
        elif self.test_lookahead('/='):
            self.expect('/=')
        elif self.test_lookahead('%='):
            self.expect('%=')
        elif self.test_lookahead('&='):
            self.expect('&=')
        elif self.test_lookahead('|='):
            self.expect('|=')
        elif self.test_lookahead('^='):
            self.expect('^=')
        elif self.test_lookahead('<<='):
            self.expect('<<=')
        elif self.test_lookahead('>>='):
            self.expect('>>=')
        elif self.test_lookahead('**='):
            self.expect('**=')
        else:
            self.expect('//=')
        return self.pop()

    def parse_break_stmt (self):
        self.push('break_stmt')
        self.expect('break')
        return self.pop()

    def parse_classdef (self):
        self.push('classdef')
        self.expect('class')
        self.expect(NAME)
        if self.test_lookahead('('):
            self.expect('(')
            if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
                self.parse_testlist()
            self.expect(')')
        self.expect(':')
        self.parse_suite()
        return self.pop()

    def parse_comp_op (self):
        self.push('comp_op')
        if self.test_lookahead('<'):
            self.expect('<')
        elif self.test_lookahead('>'):
            self.expect('>')
        elif self.test_lookahead('=='):
            self.expect('==')
        elif self.test_lookahead('>='):
            self.expect('>=')
        elif self.test_lookahead('<='):
            self.expect('<=')
        elif self.test_lookahead('<>'):
            self.expect('<>')
        elif self.test_lookahead('!='):
            self.expect('!=')
        elif self.test_lookahead('in'):
            self.expect('in')
        elif self.test_lookahead('not'):
            self.expect('not')
            self.expect('in')
        else:
            self.expect('is')
            if self.test_lookahead('not'):
                self.expect('not')
        return self.pop()

    def parse_comparison (self):
        self.push('comparison')
        self.parse_expr()
        while self.test_lookahead('!=', '>', 'not', '<>', '==', 'in', '<=', 'is', '>=', '<'):
            self.parse_comp_op()
            self.parse_expr()
        return self.pop()

    def parse_compound_stmt (self):
        self.push('compound_stmt')
        if self.test_lookahead('if'):
            self.parse_if_stmt()
        elif self.test_lookahead('while'):
            self.parse_while_stmt()
        elif self.test_lookahead('for'):
            self.parse_for_stmt()
        elif self.test_lookahead('try'):
            self.parse_try_stmt()
        elif self.test_lookahead('with'):
            self.parse_with_stmt()
        elif self.test_lookahead('@', 'def'):
            self.parse_funcdef()
        elif self.test_lookahead('class'):
            self.parse_classdef()
        else:
            self.parse_quotedef()
        return self.pop()

    def parse_continue_stmt (self):
        self.push('continue_stmt')
        self.expect('continue')
        return self.pop()

    def parse_decorator (self):
        self.push('decorator')
        self.expect('@')
        self.parse_dotted_name()
        if self.test_lookahead('('):
            self.expect('(')
            if self.test_lookahead('~', '**', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '*', '[', '`', '+', NAME):
                self.parse_arglist()
            self.expect(')')
        self.expect(NEWLINE)
        return self.pop()

    def parse_decorators (self):
        self.push('decorators')
        self.parse_decorator()
        while self.test_lookahead('@'):
            self.parse_decorator()
        return self.pop()

    def parse_del_stmt (self):
        self.push('del_stmt')
        self.expect('del')
        self.parse_exprlist()
        return self.pop()

    def parse_dictmaker (self):
        self.push('dictmaker')
        self.parse_test()
        self.expect(':')
        self.parse_test()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_test()
            self.expect(':')
            self.parse_test()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_dotted_as_name (self):
        self.push('dotted_as_name')
        self.parse_dotted_name()
        if self.test_lookahead(NAME, 'as'):
            if self.test_lookahead('as'):
                self.expect('as')
            else:
                self.expect(NAME)
            self.expect(NAME)
        return self.pop()

    def parse_dotted_as_names (self):
        self.push('dotted_as_names')
        self.parse_dotted_as_name()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_dotted_as_name()
        return self.pop()

    def parse_dotted_name (self):
        self.push('dotted_name')
        self.expect(NAME)
        while self.test_lookahead('.'):
            self.expect('.')
            self.expect(NAME)
        return self.pop()

    def parse_encoding_decl (self):
        self.push('encoding_decl')
        self.expect(NAME)
        return self.pop()

    def parse_eval_input (self):
        self.push('eval_input')
        self.parse_testlist()
        while self.test_lookahead(NEWLINE):
            self.expect(NEWLINE)
        self.expect(ENDMARKER)
        return self.pop()

    def parse_except_clause (self):
        self.push('except_clause')
        self.expect('except')
        if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
            self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
        return self.pop()

    def parse_exec_stmt (self):
        self.push('exec_stmt')
        self.expect('exec')
        self.parse_expr()
        if self.test_lookahead('in'):
            self.expect('in')
            self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
        return self.pop()

    def parse_expr (self):
        self.push('expr')
        self.parse_xor_expr()
        while self.test_lookahead('|'):
            self.expect('|')
            self.parse_xor_expr()
        return self.pop()

    def parse_expr_stmt (self):
        self.push('expr_stmt')
        self.parse_testlist()
        if self.test_lookahead('>>=', '*=', '%=', '**=', '&=', '|=', '+=', '^=', '//=', '/=', '-=', '<<='):
            self.parse_augassign()
            if self.test_lookahead('yield'):
                self.parse_yield_expr()
            else:
                self.parse_testlist()
        else:
            while self.test_lookahead('='):
                self.expect('=')
                if self.test_lookahead('yield'):
                    self.parse_yield_expr()
                else:
                    self.parse_testlist()
        return self.pop()

    def parse_exprlist (self):
        self.push('exprlist')
        self.parse_expr()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_expr()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_factor (self):
        self.push('factor')
        if self.test_lookahead('-', '~', '+'):
            if self.test_lookahead('+'):
                self.expect('+')
            elif self.test_lookahead('-'):
                self.expect('-')
            else:
                self.expect('~')
            self.parse_factor()
        else:
            self.parse_power()
        return self.pop()

    def parse_file_input (self):
        self.push('file_input')
        while self.test_lookahead('import', '~', NUMBER, 'def', '`', 'try', 'return', 'assert', NEWLINE, 'yield', '(', 'break', 'continue', '@', 'raise', STRING, 'quote', 'not', '{', 'class', 'lambda', 'print', 'exec', 'while', NAME, 'with', 'pass', '-', '[', 'global', 'for', 'from', 'if', 'del', '+'):
            if self.test_lookahead(NEWLINE):
                self.expect(NEWLINE)
            else:
                self.parse_stmt()
        self.expect(ENDMARKER)
        return self.pop()

    def parse_flow_stmt (self):
        self.push('flow_stmt')
        if self.test_lookahead('break'):
            self.parse_break_stmt()
        elif self.test_lookahead('continue'):
            self.parse_continue_stmt()
        elif self.test_lookahead('return'):
            self.parse_return_stmt()
        elif self.test_lookahead('raise'):
            self.parse_raise_stmt()
        else:
            self.parse_yield_stmt()
        return self.pop()

    def parse_for_stmt (self):
        self.push('for_stmt')
        self.expect('for')
        self.parse_exprlist()
        self.expect('in')
        self.parse_testlist()
        self.expect(':')
        self.parse_suite()
        if self.test_lookahead('else'):
            self.expect('else')
            self.expect(':')
            self.parse_suite()
        return self.pop()

    def parse_fpdef (self):
        self.push('fpdef')
        if self.test_lookahead(NAME):
            self.expect(NAME)
        else:
            self.expect('(')
            self.parse_fplist()
            self.expect(')')
        return self.pop()

    def parse_fplist (self):
        self.push('fplist')
        self.parse_fpdef()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_fpdef()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_funcdef (self):
        self.push('funcdef')
        if self.test_lookahead('@'):
            self.parse_decorators()
        self.expect('def')
        self.expect(NAME)
        self.parse_parameters()
        self.expect(':')
        self.parse_suite()
        return self.pop()

    def parse_gen_for (self):
        self.push('gen_for')
        self.expect('for')
        self.parse_exprlist()
        self.expect('in')
        self.parse_or_test()
        if self.test_lookahead('for', 'if'):
            self.parse_gen_iter()
        return self.pop()

    def parse_gen_if (self):
        self.push('gen_if')
        self.expect('if')
        self.parse_old_test()
        if self.test_lookahead('for', 'if'):
            self.parse_gen_iter()
        return self.pop()

    def parse_gen_iter (self):
        self.push('gen_iter')
        if self.test_lookahead('for'):
            self.parse_gen_for()
        else:
            self.parse_gen_if()
        return self.pop()

    def parse_global_stmt (self):
        self.push('global_stmt')
        self.expect('global')
        self.expect(NAME)
        while self.test_lookahead(','):
            self.expect(',')
            self.expect(NAME)
        return self.pop()

    def parse_if_stmt (self):
        self.push('if_stmt')
        self.expect('if')
        self.parse_test()
        self.expect(':')
        self.parse_suite()
        while self.test_lookahead('elif'):
            self.expect('elif')
            self.parse_test()
            self.expect(':')
            self.parse_suite()
        if self.test_lookahead('else'):
            self.expect('else')
            self.expect(':')
            self.parse_suite()
        return self.pop()

    def parse_import_as_name (self):
        self.push('import_as_name')
        self.expect(NAME)
        if self.test_lookahead(NAME, 'as'):
            if self.test_lookahead('as'):
                self.expect('as')
            else:
                self.expect(NAME)
            self.expect(NAME)
        return self.pop()

    def parse_import_as_names (self):
        self.push('import_as_names')
        self.parse_import_as_name()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_import_as_name()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_import_from (self):
        self.push('import_from')
        self.expect('from')
        if self.test_lookahead(NAME):
            self.parse_dotted_name()
        else:
            self.expect('.')
            while self.test_lookahead('.'):
                self.expect('.')
            if self.test_lookahead(NAME):
                self.parse_dotted_name()
        self.expect('import')
        if self.test_lookahead('*'):
            self.expect('*')
        elif self.test_lookahead('('):
            self.expect('(')
            self.parse_import_as_names()
            self.expect(')')
        else:
            self.parse_import_as_names()
        return self.pop()

    def parse_import_name (self):
        self.push('import_name')
        self.expect('import')
        self.parse_dotted_as_names()
        return self.pop()

    def parse_import_stmt (self):
        self.push('import_stmt')
        if self.test_lookahead('import'):
            self.parse_import_name()
        else:
            self.parse_import_from()
        return self.pop()

    def parse_lambdef (self):
        self.push('lambdef')
        self.expect('lambda')
        if self.test_lookahead('*', '(', NAME, '**'):
            self.parse_varargslist()
        self.expect(':')
        self.parse_test()
        return self.pop()

    def parse_list_and_or_kw_args (self):
        self.push('list_and_or_kw_args')
        if self.test_lookahead('*'):
            self.expect('*')
            self.expect(NAME)
            if self.test_lookahead(','):
                self.expect(',')
                self.expect('**')
                self.expect(NAME)
        else:
            self.expect('**')
            self.expect(NAME)
        return self.pop()

    def parse_list_for (self):
        self.push('list_for')
        self.expect('for')
        self.parse_exprlist()
        self.expect('in')
        self.parse_testlist_safe()
        if self.test_lookahead('for', 'if'):
            self.parse_list_iter()
        return self.pop()

    def parse_list_if (self):
        self.push('list_if')
        self.expect('if')
        self.parse_old_test()
        if self.test_lookahead('for', 'if'):
            self.parse_list_iter()
        return self.pop()

    def parse_list_iter (self):
        self.push('list_iter')
        if self.test_lookahead('for'):
            self.parse_list_for()
        else:
            self.parse_list_if()
        return self.pop()

    def parse_listmaker (self):
        self.push('listmaker')
        self.parse_test()
        if self.test_lookahead('for'):
            self.parse_list_for()
        else:
            while self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
        return self.pop()

    def parse_not_test (self):
        self.push('not_test')
        if self.test_lookahead('not'):
            self.expect('not')
            self.parse_not_test()
        else:
            self.parse_comparison()
        return self.pop()

    def parse_old_lambdef (self):
        self.push('old_lambdef')
        self.expect('lambda')
        if self.test_lookahead('*', '(', NAME, '**'):
            self.parse_varargslist()
        self.expect(':')
        self.parse_old_test()
        return self.pop()

    def parse_old_test (self):
        self.push('old_test')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', '[', '`', '+', STRING):
            self.parse_or_test()
        else:
            self.parse_old_lambdef()
        return self.pop()

    def parse_or_test (self):
        self.push('or_test')
        self.parse_and_test()
        while self.test_lookahead('or'):
            self.expect('or')
            self.parse_and_test()
        return self.pop()

    def parse_parameters (self):
        self.push('parameters')
        self.expect('(')
        if self.test_lookahead('*', '(', NAME, '**'):
            self.parse_varargslist()
        self.expect(')')
        return self.pop()

    def parse_pass_stmt (self):
        self.push('pass_stmt')
        self.expect('pass')
        return self.pop()

    def parse_power (self):
        self.push('power')
        self.parse_atom()
        while self.test_lookahead('(', '.', '['):
            self.parse_trailer()
        if self.test_lookahead('**'):
            self.expect('**')
            self.parse_factor()
        return self.pop()

    def parse_print_stmt (self):
        self.push('print_stmt')
        self.expect('print')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
            if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
                self.parse_test()
                while self.test_lookahead(','):
                    self.expect(',')
                    self.parse_test()
                if self.test_lookahead(','):
                    self.expect(',')
        else:
            self.expect('>>')
            self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
                while self.test_lookahead(','):
                    self.expect(',')
                    self.parse_test()
                if self.test_lookahead(','):
                    self.expect(',')
        return self.pop()

    def parse_qsuite (self):
        self.push('qsuite')
        if self.test_lookahead(QUOTED):
            self.expect(QUOTED)
        else:
            self.expect(NEWLINE)
            self.expect(INDENT)
            self.expect(QUOTED)
            self.expect(DEDENT)
        return self.pop()

    def parse_quotedef (self):
        self.push('quotedef')
        self.expect('quote')
        if self.test_lookahead('['):
            self.expect('[')
            self.parse_expr()
            self.expect(']')
        if self.test_lookahead(NAME):
            self.expect(NAME)
        self.expect(':')
        self.parse_qsuite()
        return self.pop()

    def parse_raise_stmt (self):
        self.push('raise_stmt')
        self.expect('raise')
        if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
            self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
                if self.test_lookahead(','):
                    self.expect(',')
                    self.parse_test()
        return self.pop()

    def parse_return_stmt (self):
        self.push('return_stmt')
        self.expect('return')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
            self.parse_testlist()
        return self.pop()

    def parse_shift_expr (self):
        self.push('shift_expr')
        self.parse_arith_expr()
        while self.test_lookahead('>>', '<<'):
            if self.test_lookahead('<<'):
                self.expect('<<')
            else:
                self.expect('>>')
            self.parse_arith_expr()
        return self.pop()

    def parse_simple_stmt (self):
        self.push('simple_stmt')
        self.parse_small_stmt()
        while self.test_lookahead(';'):
            self.expect(';')
            self.parse_small_stmt()
        if self.test_lookahead(';'):
            self.expect(';')
        self.expect(NEWLINE)
        return self.pop()

    def parse_single_input (self):
        self.push('single_input')
        if self.test_lookahead(NEWLINE):
            self.expect(NEWLINE)
        elif self.test_lookahead('raise', '~', 'yield', 'not', NUMBER, '{', 'lambda', 'print', '`', 'exec', STRING, 'return', 'assert', NAME, 'del', 'pass', 'import', '-', '[', 'global', '(', 'from', 'break', 'continue', '+'):
            self.parse_simple_stmt()
        else:
            self.parse_compound_stmt()
            self.expect(NEWLINE)
        return self.pop()

    def parse_sliceop (self):
        self.push('sliceop')
        self.expect(':')
        if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
            self.parse_test()
        return self.pop()

    def parse_small_stmt (self):
        self.push('small_stmt')
        if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
            self.parse_expr_stmt()
        elif self.test_lookahead('print'):
            self.parse_print_stmt()
        elif self.test_lookahead('del'):
            self.parse_del_stmt()
        elif self.test_lookahead('pass'):
            self.parse_pass_stmt()
        elif self.test_lookahead('break', 'continue', 'raise', 'yield', 'return'):
            self.parse_flow_stmt()
        elif self.test_lookahead('import', 'from'):
            self.parse_import_stmt()
        elif self.test_lookahead('global'):
            self.parse_global_stmt()
        elif self.test_lookahead('exec'):
            self.parse_exec_stmt()
        else:
            self.parse_assert_stmt()
        return self.pop()

    def parse_start (self):
        self.push('start')
        self.parse_file_input()
        return self.pop()

    def parse_stmt (self):
        self.push('stmt')
        if self.test_lookahead('raise', '~', 'yield', 'not', NUMBER, '{', 'lambda', 'print', '`', 'exec', STRING, 'return', 'assert', NAME, 'del', 'pass', 'import', '-', '[', 'global', '(', 'from', 'break', 'continue', '+'):
            self.parse_simple_stmt()
        else:
            self.parse_compound_stmt()
        return self.pop()

    def parse_subscript (self):
        self.push('subscript')
        if self.test_lookahead('.'):
            self.expect('.')
            self.expect('.')
            self.expect('.')
        elif self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
            self.parse_test()
            if self.test_lookahead(':'):
                self.expect(':')
                if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
                    self.parse_test()
                if self.test_lookahead(':'):
                    self.parse_sliceop()
        else:
            self.expect(':')
            if self.test_lookahead('~', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '[', '`', '+', NAME):
                self.parse_test()
            if self.test_lookahead(':'):
                self.parse_sliceop()
        return self.pop()

    def parse_subscriptlist (self):
        self.push('subscriptlist')
        self.parse_subscript()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_subscript()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_suite (self):
        self.push('suite')
        if self.test_lookahead('raise', '~', 'yield', 'not', NUMBER, '{', 'lambda', 'print', '`', 'exec', STRING, 'return', 'assert', NAME, 'del', 'pass', 'import', '-', '[', 'global', '(', 'from', 'break', 'continue', '+'):
            self.parse_simple_stmt()
        else:
            self.expect(NEWLINE)
            self.expect(INDENT)
            self.parse_stmt()
            while self.test_lookahead('~', NUMBER, 'def', '`', 'try', 'return', 'assert', 'global', 'import', 'yield', '(', 'break', 'continue', '@', 'raise', STRING, 'quote', 'not', '{', 'class', 'lambda', 'print', 'exec', 'while', NAME, 'with', 'pass', '-', '[', 'del', 'for', 'from', 'if', '+'):
                self.parse_stmt()
            self.expect(DEDENT)
        return self.pop()

    def parse_term (self):
        self.push('term')
        self.parse_factor()
        while self.test_lookahead('//', '*', '/', '%'):
            if self.test_lookahead('*'):
                self.expect('*')
            elif self.test_lookahead('/'):
                self.expect('/')
            elif self.test_lookahead('%'):
                self.expect('%')
            else:
                self.expect('//')
            self.parse_factor()
        return self.pop()

    def parse_test (self):
        self.push('test')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', '[', '`', '+', STRING):
            self.parse_or_test()
            if self.test_lookahead('if'):
                self.expect('if')
                self.parse_or_test()
                self.expect('else')
                self.parse_test()
        else:
            self.parse_lambdef()
        return self.pop()

    def parse_testlist (self):
        self.push('testlist')
        self.parse_test()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_test()
        if self.test_lookahead(','):
            self.expect(',')
        return self.pop()

    def parse_testlist1 (self):
        self.push('testlist1')
        self.parse_test()
        while self.test_lookahead(','):
            self.expect(',')
            self.parse_test()
        return self.pop()

    def parse_testlist_gexp (self):
        self.push('testlist_gexp')
        self.parse_test()
        if self.test_lookahead('for'):
            self.parse_gen_for()
        else:
            while self.test_lookahead(','):
                self.expect(',')
                self.parse_test()
            if self.test_lookahead(','):
                self.expect(',')
        return self.pop()

    def parse_testlist_safe (self):
        self.push('testlist_safe')
        self.parse_old_test()
        if self.test_lookahead(','):
            self.expect(',')
            self.parse_old_test()
            while self.test_lookahead(','):
                self.expect(',')
                self.parse_old_test()
            if self.test_lookahead(','):
                self.expect(',')
        return self.pop()

    def parse_trailer (self):
        self.push('trailer')
        if self.test_lookahead('('):
            self.expect('(')
            if self.test_lookahead('~', '**', 'not', '-', NUMBER, '{', '(', 'lambda', STRING, '*', '[', '`', '+', NAME):
                self.parse_arglist()
            self.expect(')')
        elif self.test_lookahead('['):
            self.expect('[')
            self.parse_subscriptlist()
            self.expect(']')
        else:
            self.expect('.')
            self.expect(NAME)
        return self.pop()

    def parse_try_stmt (self):
        self.push('try_stmt')
        self.expect('try')
        self.expect(':')
        self.parse_suite()
        if self.test_lookahead('except'):
            self.parse_except_clause()
            self.expect(':')
            self.parse_suite()
            while self.test_lookahead('except'):
                self.parse_except_clause()
                self.expect(':')
                self.parse_suite()
            if self.test_lookahead('else'):
                self.expect('else')
                self.expect(':')
                self.parse_suite()
            if self.test_lookahead('finally'):
                self.expect('finally')
                self.expect(':')
                self.parse_suite()
        else:
            self.expect('finally')
            self.expect(':')
            self.parse_suite()
        return self.pop()

    def parse_varargslist (self):
        self.push('varargslist')
        if self.test_lookahead('*', '**'):
            self.parse_list_and_or_kw_args()
        else:
            self.parse_fpdef()
            if self.test_lookahead('='):
                self.expect('=')
                self.parse_test()
            if self.test_lookahead(','):
                self.parse_varargslist_end()
        return self.pop()

    def parse_varargslist_end (self):
        self.push('varargslist_end')
        self.expect(',')
        if self.test_lookahead('*', '(', NAME, '**'):
            if self.test_lookahead('(', NAME):
                self.parse_fpdef()
                if self.test_lookahead('='):
                    self.expect('=')
                    self.parse_test()
                if self.test_lookahead(','):
                    self.parse_varargslist_end()
            else:
                self.parse_list_and_or_kw_args()
        return self.pop()

    def parse_while_stmt (self):
        self.push('while_stmt')
        self.expect('while')
        self.parse_test()
        self.expect(':')
        self.parse_suite()
        if self.test_lookahead('else'):
            self.expect('else')
            self.expect(':')
            self.parse_suite()
        return self.pop()

    def parse_with_stmt (self):
        self.push('with_stmt')
        self.expect('with')
        self.parse_test()
        if self.test_lookahead(NAME, 'as'):
            self.parse_with_var()
        self.expect(':')
        self.parse_suite()
        return self.pop()

    def parse_with_var (self):
        self.push('with_var')
        if self.test_lookahead('as'):
            self.expect('as')
        else:
            self.expect(NAME)
        self.parse_expr()
        return self.pop()

    def parse_xor_expr (self):
        self.push('xor_expr')
        self.parse_and_expr()
        while self.test_lookahead('^'):
            self.expect('^')
            self.parse_and_expr()
        return self.pop()

    def parse_yield_expr (self):
        self.push('yield_expr')
        self.expect('yield')
        if self.test_lookahead('~', NAME, 'not', '-', NUMBER, '{', '(', 'lambda', '[', '`', '+', STRING):
            self.parse_testlist()
        return self.pop()

    def parse_yield_stmt (self):
        self.push('yield_stmt')
        self.parse_yield_expr()
        return self.pop()

    def tokenize (self):
        ret_val = self.tokenizer.next()
        while ret_val[0] in (NL, COMMENT):
            ret_val = self.tokenizer.next()
        return ret_val


# ______________________________________________________________________
# Main routine

if __name__ == '__main__':
    parser_main(MyParser)

# ______________________________________________________________________
# End of myparser.py
