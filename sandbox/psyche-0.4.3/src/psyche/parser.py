#
# This file is part of Psyche, the Python Scheme Interpreter
#
# Copyright (c) 2002
#       Yigal Duppen
#
# Psyche is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Psyche is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Psyche; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

"""
Contains the Parser definitions for scheme expressions and
programs.
"""

from spark import GenericParser
import ast
import operator

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.15 $"[11:-2]


class _Parser(GenericParser):
    """The parser for scheme expressions.

    Note: the parser is private; this makes it possible to change
    the API completely.

    Note: those rules starting with an _ are rules not present in the
    R5RS; however, the R5RS is written in EBNF, something spark does
    not fully support.
    """
 
    def __init__(self, start="program"):
        """Creates a new parser

        start - the start symbol; interesting values are 'datum',
        'expression' and 'program'
        """
        GenericParser.__init__(self, start)

    #
    # Error reporting
    #

    def _getTokensOnSameLine(self, tokens, index):
        """Returns all tokens on the same line as
        tokens[index]

        tokens - a sequence of tokens
        index - the index of the offending token
        """
        tok = tokens[index]
        if not tok:
            raise ValueError("Syntax error - missing token")

        return [t for t in tokens if tok.same_line(t)]
    
    def error(self, tokens, index):
        # t - current token
        # col - column of current token
        # error - list of error strings, to be joined with spaces, in
        #         emacs-error format
        # prefix-len - length of prefix of ^ (indicating offending token)
        t = tokens[index]
        col = t.col_no()
        error = ["%s:%d:%d:%d:%d:" % (t.input_name(),
                                     t.line_no(), t.col_no(),
                                     t.line_no(), t.col_no()),
                 "\nSyntax error:"]
        prefix_len = len("\nSyntax error:")
        
        # 1. Get entire offending line
        same_line = self._getTokensOnSameLine(tokens, index)
        error += [t.value() for t in same_line]
        error += "\n"

        # 2. obtain length of tokens before 
        same_line_before = [t for t in same_line if t.col_no() < col]
        prefix_len += reduce(operator.add,
                             [len(t) for t in same_line_before],
                             0)
        
        prefix_len += len(same_line_before)

        # 3. Construct error string
        error_string = (" ".join(error)
                        + " " * prefix_len
                        + "^")

        raise ValueError(error_string)

        
        
    #
    # External representations
    #
 
    def p_datum(self, args): 
        """
        datum ::= simple_datum
        datum ::= compound_datum
        """
        return args[0]

    def p_simple_datum(self, args):
        """
        simple_datum ::= _boolean
        simple_datum ::= _number
        simple_datum ::= _character
        simple_datum ::= _string
        simple_datum ::= symbol
        """
        return args[0]

    def p_symbol(self, args):
        """
        symbol ::= variable
        symbol ::= syntactic_keyword
        """
        return ast.Symbol(args[0].value())


    def p_compound_datum(self, args):
        """
        compound_datum ::= list
        compound_datum ::= vector
        """
        return args[0]


    def p_list(self, args):
        """
        list ::= ( )
        list ::= ( _datum_list )
        list ::= ( _datum_list __.__ datum )
        list ::= abbreviation
        """
        if len(args) == 2:
            return ast.List()
        elif len(args) == 3:
            return ast.List(args[1])
        elif len(args) == 5:
            return ast.List(args[1], args[3])
        elif len(args) == 1:
            return args[0]

    def p_abbreviation(self, args):
        """
        abbreviation ::= abbrev_prefix datum
        """
        return ast.List([args[0], args[1]])

    def p_abbrev_prefix(self, args):
        """
        abbrev_prefix ::= __'__
        abbrev_prefix ::= __`__
        abbrev_prefix ::= __,@__
        abbrev_prefix ::= __,__
        """
        if args[0].value() == "'":
            return ast.Symbol("quote")
        
        raise NotImplementedError()

    def p_vector(self, args):
        """
        vector ::= __#(__ )
        vector ::= __#(__ _datum_list )
        """
        if len(args) == 2:
            return ast.Vector([])
        else:
            assert len(args) == 3
            return ast.Vector(args[1])

    #
    # Expressions
    #

    def p_expression(self, args):
        """
        expression ::= _variable
        expression ::= literal
        expression ::= procedure_call
        expression ::= lambda_expression
        expression ::= conditional
        expression ::= assignment
        expression ::= derived_expression
        expression ::= macro_use
        expression ::= macro_block
        """
        return args[0]

    def p_literal(self, args):
        """
        literal ::= quotation
        literal ::= self_evaluating
        """
        return args[0]

    def p_self_evaluating(self, args):
        """
        self_evaluating ::= _boolean
        self_evaluating ::= _number
        self_evaluating ::= _character
        self_evaluating ::= _string
        """
        return args[0]


    def p_quotation(self, args):
        """
        quotation ::= __'__ datum
        quotation ::= ( __quote__ datum )
        
        """
        if len(args) == 2:
            return args[1]
        else:
            return args[2]

 
    def p_procedure_call(self, args):
        """
        procedure_call ::= ( operator )
        procedure_call ::= ( operator _operand_list )
        """
        if (len(args) == 3):
            return ast.Application(args[1], [])
        else:
            return ast.Application(args[1], args[2])


    def p_operator(self, args):
        """
        operator ::= expression
        """
        return args[0]

    def p_operand(self, args):
        """
        operand ::= expression
        """
        return args[0]


    def p_lambda_expression(self, args):
        """
        lambda_expression ::= ( __lambda__ formals body ) 
        """
        return ast.Lambda(args[2], args[3])

    def p_formals(self, args):
        """
        formals ::= _variable
        formals ::= ( )
        formals ::= ( _variable_list )
        formals ::= ( _variable_list . _variable ) 
        """
        if len(args) == 1:
            raise NotImplementedError("lambda var (body)")
        elif len(args) == 2:
            return []
        elif len(args) == 3:
            return args[1]
        elif len(args) == 5:
            raise NotImplementedError("( var+ . var )")


    def p_body(self, args):
        """
        body ::= sequence
        body ::= _definition_list sequence
        """
        if len(args) == 1:
            return args[0]
        else:
            return args[0] + args[1]

    def p_sequence(self, args):
        """
        sequence ::= expression
        sequence ::= _command_list expression
        """
        if len(args) == 1:
            return [args[0]]
        else:
            args[0].append(args[1])
            return args[0]


    def p_command(self, args):
        """
        command ::= expression
        """
        return args[0]


    def p_conditional(self, args):
        """
        conditional ::= ( __if__ test consequent )
        conditional ::= ( __if__ test consequent alternate )
        """
        if len(args) == 5:
            return ast.If(args[2], args[3])
        elif len(args) == 6:
            return ast.If(args[2], args[3], args[4])
    

    def p_test(self, args):
        """
        test ::= expression
        """
        return args[0]

    def p_consequent(self, args):
        """
        consequent ::= expression
        """
        return args[0]

    def p_alternate(self, args):
        """
        alternate ::= expression
        """
        return args[0]


    def p_derived_expression(self, args):
        """
        derived_expression ::= _cond
        derived_expression ::= _case
        derived_expression ::= _and
        derived_expression ::= _or
        derived_expression ::= _let
        derived_expression ::= _letrec
        derived_expression ::= _begin
        derived_expression ::= _do
        derived_expression ::= _delay
        derived_expression ::= quasiquotation
        """
        return args[0]

    def p__cond(self, args):
        """
        _cond ::= ( __cond__ _clause_list )
        _cond ::= ( __cond__ ( __else__ sequence ) )
        _cond ::= ( __cond__ _clause_list ( __else__ sequence ) )
        """
        if len(args) == 4:
            return ast.Cond(args[2], [])
        elif len(args) == 7:
            return ast.Cond([], args[4])
        elif len(args) == 8:
            return ast.Cond(args[2], args[5])

    def p__and(self, args):
        """
        _and ::= ( __and__ )
        _and ::= ( __and__ _test_list )
        """
        if len(args) == 3:
            return ast.And([])
        else:
            return ast.And(args[2])

    def p__or(self, args):
        """
        _or ::= ( __or__ )
        _or ::= ( __or__ _test_list )
        """
        if len(args) == 3:
            return ast.Or([])
        else:
            return ast.Or(args[2])

    def p__let(self, args):
        """
        _let ::= ( __let__ ( ) body )
        _let ::= ( __let__ ( _binding_spec_list ) body )
        """
        if len(args) == 6:
            bindings = []
        else:
            bindings = args[3]

        return ast.Application(
            ast.Lambda([var for (var,expr) in bindings],
                       args[-2]),
            [expr for (var, expr) in bindings])

    def p_cond_clause(self, args):
        """
        cond_clause ::= ( test )
        cond_clause ::= ( test sequence )
        cond_clause ::= ( test __=>__ recipient )
        """
        if len(args) == 3:
            return ast.CondClause(args[1], [])
        elif len(args) == 4:
            return ast.CondClause(args[1], args[2])
        elif len(args) == 5:
            return ast.CondClause(args[1], [args[3]])

    def p_recipient(self, args):
        """
        recipient ::= expression
        """
        return args[0]

    def p_binding_spec(self, args):
        """
        binding_spec ::= ( _variable expression )
        """
        return [ args[1], args[2] ]


    def p_program(self, args):
        """
        program ::= _command_def_list
        """
        return ast.Program(args[0])

    def p__command_def_list(self, args):
        """
        _command_def_list ::=
        _command_def_list ::= _command_def_list command_or_definition
        """
        if len(args) == 0:
            return []
        else:
            return args[0] + [args[1]]


    def p_command_or_definition(self, args):
        """
        command_or_definition ::= command
        command_or_definition ::= definition
        command_or_definition ::= syntax_definition
        command_or_definition ::= ( __begin__ _c_or_d_list __)
        """
        if len(args) == 1:
            return args[0]
        else:
            raise NotImplementedError("(begin...)")

    def p_definition(self, args):
        """
        definition ::= ( __define__ _variable expression )
        definition ::= ( __define__ ( _variable def_formals ) body )
        definition ::= ( __begin__ )
        definition ::= ( __begin__ _definition_list)
        """
        if len(args) == 5:
            # (define x y)
            return ast.Definition(args[2], args[3])
        
        if len(args) == 8:
            # (define (f x) expr)
            return ast.ProcDefinition(args[3], args[4], args[6])

        raise NotImplementedError("(begin...)")

    def p_def_formals(self, args):
        """
        def_formals ::= 
        def_formals ::= _variable_list
        def_formals ::= __.__ _variable
        def_formals ::=_variable_list __.__ _variable
        """
        if len(args) == 0:
            return []
        elif len(args) == 1:
            return args[0]
        else:
            raise NotImplementedError("(x . y)")

    def p_syntax_definition(self, args):
        """
        syntax_definition ::= ( __define-syntax__ keyword transformer_spec )
        """
        raise NotImplementedError()


    # Helper methods for different kinds of lists
    def p__datum_list(self, args):
        """
        _datum_list ::= _datum_list datum
        _datum_list ::= datum
        """
        return self.__prefix_list(args)

    def p__operand_list(self, args):
        """
        _operand_list ::= _operand_list operand
        _operand_list ::= operand
        """
        return self.__prefix_list(args)

    def p__c_or_d_list(self, args):
        """
        _c_or_d_list ::= command_or_definition
        _c_or_d_list ::= _c_or_d_list_ command_or_definition
        """
        return self.__prefix_list(args)

    def p__definition_list(self, args):
        """
        _definition_list ::= definition
        _definition_list ::= _definition_list definition
        """
        return self.__prefix_list(args)

    def p__command_list(self, args):
        """
        _command_list ::= command
        _command_list ::= _command_list command
        """
        return self.__prefix_list(args)
        

    def p__variable_list(self, args):
        """
        _variable_list ::= _variable
        _variable_list ::= _variable_list _variable
        """
        return self.__prefix_list(args)

    def p__clause_list(self, args):
        """
        _clause_list ::= cond_clause
        _clause_list ::= _clause_list cond_clause
        """
        return self.__prefix_list(args)

    def p__binding_spec_list(self, args):
        """
        _binding_spec_list ::= binding_spec
        _binding_spec_list ::= _binding_spec_list binding_spec
        """
        return self.__prefix_list(args)

    def p__test_list(self, args):
        """
        _test_list ::= test
        _test_list ::= _test_list test
        """
        return self.__prefix_list(args)
        

    def __prefix_list(self, args):
        """Returns a list object for a grammar defined as
           X_LIST ::= X | X_LIST X
        """
        if len(args) == 1:
            return [args[0]]
        else:
            args[0].append(args[1])
            return args[0]

    # Helper elements to easy creation of correct AST node
    def p__character(self, args):
        """
        _character ::= character
        """
        return char.char(args[0].value())
    
    def p__boolean(self, args):
        """
        _boolean ::= boolean
        """
        return ast.Boolean(args[0].value())

    def p__number(self, args):
        """
        _number ::= number
        """
        return ast.Number(args[0].value())

    def p__character(self, args):
        """
        _character ::= character
        """
        return ast.Character(args[0].value())

    def p__string(self, args):
        """
        _string ::= string
        """
        return ast.String(args[0].value())

    def p__variable(self, args):
        """
        _variable ::= variable
        """
        return ast.Variable(args[0].value())



__parser = _Parser()

def parse(tokens):
    """Parses a list of tokens."""
    return __parser.parse(tokens)


