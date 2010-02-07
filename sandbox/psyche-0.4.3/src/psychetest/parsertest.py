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
Tests the psyche parser module
"""

import unittest

from psyche import lexer, parser, ast
from psyche.ast import *

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.10 $"[11:-2]

class ParserTest(unittest.TestCase):
    """Tests the Parser class"""

    def setUp(self):
        """Sets up the fixture"""
        pass

    def parse(self, expr):
        """Uses the parser to convert a program to an AST

        Always ignores the top-level Program AST
        """
        tokens = lexer.tokenize(expr)
        return parser.parse(tokens)[0]


    def testNumber(self):
        """Test whether we can parse a number"""
        tree = self.parse("5")

        self.assertEquals(tree,
                          ast.Number("5"))

    def testExpression(self):
        """Tests whether we can parse (+ 1 2 3)"""
        tree = self.parse("(+ 1 2 3)")

        expected = ast.Application(
            ast.Variable("+"),
            [ ast.Number("1"), ast.Number("2"), ast.Number("3") ])

        
        self.assertEquals(expected, tree)

    def testOperatorExpression(self):
        """Expressions without operands are expressions too"""
        tree = self.parse("(*)")

        expected = ast.Application(
            ast.Variable("*"), [])

        self.assertEquals(expected, tree)

    def testDefine(self):
        """Definitions of names and of compound procedures"""

        tree = self.parse("(define x 5)")
        expected = ast.Definition(
            ast.Variable("x"),
            ast.Number("5"))
        self.assertEquals(expected, tree)
        
        tree = self.parse("(define (f x y) (g 20 y))")
        expected = ast.ProcDefinition(
            ast.Variable("f"),
            [ast.Variable("x"), ast.Variable("y")],
            [ast.Application(
                ast.Variable("g"), [ast.Number("20"), ast.Variable("y")])
            ])
        self.assertEquals(expected, tree)

    def testCond(self):
        """Cond and if statements"""
        tree = self.parse("""(cond ((< x 0) x)
                                   ((= x 0) => 7)
                                   (else 10))""")
        expected = Cond(
            [CondClause(
              Application(Variable("<"),
                          [Variable("x"), Number("0")]),
              [Variable("x")]),
             CondClause(
              Application(Variable("="),
                          [Variable("x"), Number("0")]),
               [Number("7")])],
            [Number("10")])
        self.assertEquals(expected, tree)

        tree = self.parse("""(if (< x 0) x y)""")
        expected = If(
            Application(Variable("<"),
                         [Variable("x"), Number("0")]),
            Variable("x"),
            Variable("y"))
        self.assertEquals(expected, tree)

    def testBool(self):
        """Tests the boolean statements (and...) and (or...)"""
        tree = self.parse("""(or (and #t #f) #f)""")
        expected = Or(
            [And([Boolean("#t"), Boolean("#f")]), Boolean("#f")])
        self.assertEquals(expected, tree)

    def testLambda(self):
        """Tests lambda statements"""
        tree = self.parse("""((lambda (x) (+ x 4)) 7)""")
        expected = Application(
            Lambda([Variable("x")],
                   [Application(Variable("+"),
                                [Variable("x"), Number("4")])]),
            [Number("7")])

        self.assertEquals(expected, tree)

    def testLet(self):
        """Tests let statements (which should be converted to
        applications"""
        tree = self.parse("""(let ((x 3)) (* x x))""")
        expected = Application(
            Lambda([Variable("x")],
                   [Application(Variable("*"),
                                [Variable("x"), Variable("x")])]),
            [Number("3")])

        self.assertEquals(expected, tree)

    def testString(self):
        """Tests a string statement"""
        tree = self.parse(r'(string<? "BBB" "AAA")')
        expected = Application(
            Variable("string<?"),
            [String('"BBB"'), String('"AAA"')])

        self.assertEquals(expected, tree)

    def testList(self):
        """Tests some list statements"""
        tree = self.parse("'()")
        expected = List(None, None)
        self.assertEquals(expected, tree)

        tree = self.parse("'(1 2)")
        expected = List([Number("1"), Number("2")])
        self.assertEquals(expected, tree)

        tree = self.parse("'(1 2 3)")
        expected = List([Number("1"), Number("2"), Number("3")], [])

        tree = self.parse("'(1 2 . 3)")
        expected = List([Number("1"), Number("2")], Number("3"))
        self.assertEquals(expected, tree)

        tree = self.parse("'(1 . (2 . 3))")
        expected = List([Number("1")], List([Number("2")], Number("3")))
        self.assertEquals(tree, expected)

        tree = self.parse("'(1 . (2 . ()))")
        expected = List([Number("1")], List([Number("2")], []))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParserTest, "test"))

    return suite

