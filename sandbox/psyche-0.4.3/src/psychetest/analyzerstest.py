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
Tests the different analyzers

"""

import unittest
from psyche import parser, lexer, analyzers

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.4 $"[11:-2]


class TailContextMarkerTest(unittest.TestCase):


    def mark(self, expr):
        """Returns a marked AST for the specified expression"""
        ast = parser.parse(lexer.tokenize(expr))
        analyzers.markTailContexts(ast)
        return ast[0]

    def testFunction(self):
        """Marks a function definition and checks the tail
        contexts. """ 
        ast = self.mark("(define (f x) y)")
        self.failIf(ast.inTailContext,
                    "Proc def in tail context")
        
        for formal in ast.formals():
            self.failIf(formal.inTailContext,
                        "Formal in tail context")

        for expr in ast.body()[:-1]:
            self.failIf(expr.inTailContext,
                        "Non-last statement in tail context")

        self.assert_(ast.body()[-1].inTailContext)

    def testLambda(self):
        """Marks a lambda expression and checks the tail contexts. """
        ast = self.mark("(lambda (x) (define plus +) (plus x 4))")

        self.failIf(ast.inTailContext,
                    "Lambda in tail context")

        for formal in ast.formals():
            self.failIf(formal.inTailContext,
                        "Formal in tail context")

        for expr in ast.body()[:-1]:
            self.failIf(expr.inTailContext,
                        "Non-last statement in tail context")

        self.assert_(ast.body()[-1].inTailContext)

    def testRecursion(self):
        """Uses the function from interpretertest.test1_2_1 and checks
        the markings.
        """
        ast = self.mark("""(define (plus x y)
                              (if (= x 0)
                                  y
                                  (plus (- x 1) (+ y 1))))""")
        self.failIf(ast.inTailContext,
                    "Proc def in tail context")

        for formal in ast.formals():
            self.failIf(formal.inTailContext,
                        "Formal in tail context")

        ifStmt = ast.body()[0]
        self.assert_(ifStmt.inTailContext,
                     "Last statement not in tail context")

        self.failIf(ifStmt.test().inTailContext,
                    "Test in tail context")
        self.assert_(ifStmt.consequent().inTailContext,
                     "Consequent not in tail context")
        self.assert_(ifStmt.alternate().inTailContext,
                     "Alternate not in tail context")
        
            

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TailContextMarkerTest, "test"))
    
    return suite
