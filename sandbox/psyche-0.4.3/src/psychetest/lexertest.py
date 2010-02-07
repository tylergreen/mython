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
Tests the psyche lexer module
"""

from StringIO import StringIO
import unittest

from psyche import lexer
from psyche.lexer import Token, LexerException

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.7 $"[11:-2]

class LexerTest(unittest.TestCase):
    """Tests the lexer"""

    def setUp(self):
        """Sets up the fixture"""
        pass


    def testSimple(self):
        """Tests lexing a simple expression"""

        expr = "(+ (* 3 (hello x)) 2)"

        tokens = lexer.tokenize(expr)

        expected = [ Token(Token.START, '('),
                     Token(Token.VARIABLE, '+'),
                     Token(Token.START, '('),
                     Token(Token.VARIABLE, '*'),
                     Token(Token.NUM, 3),
                     Token(Token.START, '('),
                     Token(Token.VARIABLE, 'hello'),
                     Token(Token.VARIABLE, 'x'),
                     Token(Token.STOP, ')'),
                     Token(Token.STOP, ')'),
                     Token(Token.NUM, 2),
                     Token(Token.STOP, ')')]

        self.assertEquals(expected,
                          tokens)

    def testWhitespace(self):
        """Lexical analysis of whitespace"""
        self.assertEquals([], lexer.tokenize(""))
        self.assertEquals([], lexer.tokenize("""

        """))
        self.assertEquals([], lexer.tokenize("\n\t\t\n"))

        self.assertEquals([], lexer.tokenize("; this is a comment\n"))
        

    def testComplex(self):
        """Tests lexing a more complex expression"""

        expr = """
        (define (square-list items)
          (define (iter things answer)
            (if (null? things)
                answer
                (iter (cdr things)
                      (cons answer
                            (square (car things))))))
          (iter items nil))
        """

        tokens = []
        for token in lexer.tokenize(expr):
            tokens.append(token)


        def tokenCount(tokenList, type):
            return len([t for t in tokenList if t.type() == type])

        # 12 opening brackets
        self.assertEquals(12, tokenCount(tokens, Token.START))

        # 12 closing brackets
        self.assertEquals(12, tokenCount(tokens, Token.STOP))

        # no numbers
        self.assertEquals(0, tokenCount(tokens, Token.NUM))

        # 19 variables
        self.assertEquals(19, tokenCount(tokens, Token.VARIABLE))

        # 3 syntactic keywords
        self.assertEquals(3, tokenCount(tokens, Token.SYNTACTIC))

    def testStrings(self):
        """Test lexing of an s-expression with strings"""
        expr = '(string<? "BBB" "AAA")'

        expected = [ Token(Token.START, '('),
                     Token(Token.VARIABLE, 'string<?'),
                     Token(Token.STRING, '"BBB"'),
                     Token(Token.STRING, '"AAA"'),
                     Token(Token.STOP, ')') ]

        tokens = lexer.tokenize(expr)
        self.assertEquals(tokens, expected)

    def testIllegalString(self):
        """Test that we cannot parse illegal strings"""
        expr = r'"hello\tworld\n"'

        try:
            lexer.tokenize(expr)
            self.fail("Could parse \\t and \\n")
        except LexerException:
            pass

    def testLexEscaped(self):
        """Test that we can parse escaped strings"""
        expr = '("\\\\" "\\"")'

        expected = [ Token(Token.START, '('),
                     Token(Token.STRING, r'"\\"'),
                     Token(Token.STRING, r'"\""'),
                     Token(Token.STOP, ')') ]

        tokens = lexer.tokenize(expr)
        self.assertEquals(tokens, expected)
                              

    def testLexSymbol(self):
        """Test that we can parse symbols"""
        expr = "'a"
        expected = [ Token(Token.PUNCT, "'"),
                     Token(Token.VARIABLE, "a") ]
        tokens = lexer.tokenize(expr)

        self.assertEquals(tokens, expected)

    def testLexList(self):
        """Tests that we can parse lists"""
        expr = "'(a b . c)"
        expected = [ Token(Token.PUNCT, "'"),
                     Token(Token.START, "("),
                     Token(Token.VARIABLE, "a"),
                     Token(Token.VARIABLE, "b"),
                     Token(Token.PUNCT, "."),
                     Token(Token.VARIABLE, "c"),
                     Token(Token.STOP, ")") ]
        tokens = lexer.tokenize(expr)
        self.assertEquals(tokens, expected)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(LexerTest, "test"))

    return suite
