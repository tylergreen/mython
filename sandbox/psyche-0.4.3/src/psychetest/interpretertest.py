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
Tests the interpreter module
"""

from psyche.interpreter import Interpreter, UndefinedException, \
                               SchemeException
from psyche.types import *
import unittest
import string

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.22 $"[11:-2]

class InterpreterTest(unittest.TestCase):
    """Tests the interpreter

    Other tests test are based on R5Rs, such as tail-recursion and
    static bindings.
    """

    def __init__(self, *args):
        unittest.TestCase.__init__(self, *args)
        self.interpreter = Interpreter()

    def eval(self, expression):
        return self.interpreter.eval(expression)

    def assertEval(self, expression, result):
        """Asserts that the specified expression evaluates to the
        specified result.
        """
        eval = self.interpreter.eval(expression)
        self.failIf(eval != result,
                    "%s => %s, expected %s"
                    % (expression, eval, result))

    def assertFEval(self, expression, floatResult, epsilon=0.0001):
        """Asserts that the specified expressions evaluates to a
        number that differs at most epsilon from floatResult.
        """
        eval = self.interpreter.eval(expression)

        self.failIf(abs(floatResult - eval) > epsilon,
                    "%s ==> %f, expected %f"
                    % (expression, eval, floatResult))

    def assertError(self, expression):
        """Asserts that the specified expression raises an error at
        evaluation.
        """
        try:
            self.interpreter.eval(expression)
        except Exception:
            return

        fail(expression + " did not raise an exception")

#
# SICP
#

class SICPTest(InterpreterTest):
    """
    Tests based on examples in SICP
    """
    
    def test1_1_1(self):
        """SICP 1.1.1 Expressions"""
        self.assertEval("486", 486)
        self.assertEval("(+ 137 349)", 486)
        self.assertEval("(- 1000 334)", 666)
        self.assertEval("(* 5 99)", 495)
        self.assertEval("(/ 10 5)", 2)
        self.assertEval("(+ 2.7 10)", (2.7 + 10) )
        self.assertEval("(+ 21 35 12 7)", 75)
        self.assertEval("(* 25 4 12)", 1200)
        self.assertEval("(+ (* 3 5) (- 10 6))", 19)
        self.assertEval("""(+ (* 3
                                 (+ (* 2 4)
                                    (+ 3 5)))
                              (+ (- 10 7)
                                 6))""", 57)
                                 

    def test1_1_2(self):
        """SICP 1.1.2 Naming and the Environment"""
        self.eval("(define size 2)")
        self.assertEval("size", 2)
        self.assertEval("(* 5 size)", 10)

        self.eval("(define pi 3.14159)")
        self.eval("(define radius 10)")
        self.assertEval("(* pi (* radius radius))", 100 * 3.14159)

        self.eval("(define circumference (* 2 pi radius))")
        self.assertEval("circumference", 20 * 3.14159)

    def test1_1_3(self):
        """SICP 1.1.3 Evaluating Combinations"""
        self.assertEval("""(* (+ 2 (* 4 6))
                              (+ 3 5 7))""", 390)
    def test1_1_4(self):
        """SICP 1.1.4 Compound Procedures"""
        self.eval("(define (square x) (* x x))")
        self.assertEval("(square 21)", 441)
        self.assertEval("(square (+ 2 5))", 49)
        self.assertEval("(square (square 3))", 81)

        self.eval("""(define (sum-of-squares x y)
                       (+ (square x) (square y)))""")
        self.assertEval("(sum-of-squares 3 4)", 25)

        self.eval("""(define (f a)
                       (sum-of-squares (+ a 1) (* a 2)))""")
        self.assertEval("(f 5)", 136)

    def test1_1_5(self):
        """SICP 1.1.5 The Substitution Model for Procedure Application"""
        pass

    def test1_1_6(self):
        """SICP 1.1.6 Conditional Expressions and Predicates"""
        def assertAbs():
            self.assertEval("(abs 10)", 10)
            self.assertEval("(abs 0)", 0)
            self.assertEval("(abs -10)", 10)

        # p.17
        self.eval("""(define (abs x)
                       (cond ((> x 0) x)
                             ((= x 0) 0)
                             ((< x 0) (- x))))""")
        assertAbs()

        # p.18
        self.eval("""(define (abs x)
                       (cond ((< x 0) (- x))
                             (else x)))""")
        assertAbs()

        self.eval("""(define (abs x)
                       (if (< x 0)
                           (- x)
                           x))""")
        assertAbs()

    def testEx1(self):
        """SICP Exercises 1"""
        self.assertEval("10", 10)
        self.assertEval("(+ 5 3 4)", 12)
        self.assertEval("(- 9 1)", 8)
        self.assertEval("(/ 6 2)", 3)
        self.assertEval("(+ (* 2 4) (- 4 6))", 6)
        self.eval("(define a 3)")
        self.eval("(define b (+ a 1))")
        self.assertEval("(+ a b (* a b))", 19)
        self.assertEval("(= a b)", FALSE)
        self.assertEval("""(if (and (> b a) (< b (* a b)))
                               b
                               a)""", 4)
        self.assertEval("""(cond ((= a 4) 6)
                                 ((= b 4) (+ 6 7 a))
                                 (else 25))""", 16)
        self.assertEval("(+ 2 (if (> b a) b a))", 6)
        self.assertEval("""(* (cond ((> a b) a)
                                    ((< a b) b)
                                    (else -1))
                              (+ a 1))""", 16)
        self.eval("""(define (a-plus-abs-b a b)
                        ((if (> b 0) + -) a b))""")
        self.assertEval("(a-plus-abs-b 10 10)", 20)
        self.assertEval("(a-plus-abs-b 10 -10)", 20)
        self.assertEval("(a-plus-abs-b -10 10)", 0)
        self.assertEval("(a-plus-abs-b -10 -10)", 0)
        
        self.eval("""(define (A x y)
                       (cond ((= y 0) 0)
                             ((= x 0) (* 2 y))
                             ((= y 1) 2)
                             (else (A (- x 1)
                                      (A x (- y 1))))))""")
        self.assertEval("(A 1 10)", 1024)
        self.assertEval("(A 2 4)", 65536)
        self.assertEval("(A 3 3)", 65536)

    def test1_1_7(self):
        """SICP 1.1.7 Example: Square Roots by Newton's Method"""
        self.eval("""(define (square x) (* x x))""")
        self.eval("""(define (sqrt-iter guess x)
                       (if (good-enough? guess x)
                           guess
                           (sqrt-iter (improve guess x)
                                      x)))""")
        self.eval("""(define (good-enough? guess x)
                        (< (abs (- (square guess) x)) 0.001))""")
        self.eval("""(define (average x y)
                        (/ (+ x y) 2))""")
        self.eval("""(define (improve guess x)
                        (average guess (/ x guess)))""")
        self.eval("""(define (sqrt x)
                        (sqrt-iter 1.0 x))""")

        self.assertFEval("(sqrt 9)", 3)
        self.assertFEval("(sqrt (+ 100 37))", 11.7046999)
        self.assertFEval("(sqrt (+ (sqrt 2) (sqrt 3)))", 1.773927)
        self.assertFEval("(square (sqrt 1000))", 1000.000, 0.001)

    def test1_1_8(self):
        """SICP 1.1.8 Procedures as Black-Box Abstractions"""
        self.eval("""(define (square x) (* x x))""")
        self.eval("""(define (average x y)
                        (/ (+ x y) 2))""")

        self.eval("""(define (sqrt x)
                        (define (good-enough? guess)
                          (< (abs (- (square guess) x)) 0.001))
                        (define (improve guess)
                          (average guess (/ x guess)))
                        (define (sqrt-iter guess)
                          (if (good-enough? guess)
                              guess
                              (sqrt-iter (improve guess))))
                        (sqrt-iter 1.0))""")

        self.assertFEval("(sqrt 9)", 3)
        self.assertFEval("(sqrt (+ 100 37))", 11.7046999)
        self.assertFEval("(sqrt (+ (sqrt 2) (sqrt 3)))", 1.773927)
        self.assertFEval("(square (sqrt 1000))", 1000.000, 0.001)

        try:
            self.eval("(improve 5 10)")
            self.fail("Function 'improve' is still in in scope")
        except UndefinedException:
            pass

    def test1_2_1(self):
        """SICP 1.2.1 Linear Recursion and Iteration"""
        self.eval("""(define (factorial n)
                        (fact-iter 1 1 n))""")
        self.eval("""(define (fact-iter product counter max-count)
                        (if (> counter max-count)
                            product
                            (fact-iter (* counter product)
                                       (+ counter 1)
                                       max-count)))""")

        self.assertEval("""(factorial 6)""", 720)

        # Added better recursion tester; factorial requires HUGE
        # numbers to reach the recursion limit
        # Example NOT taken from SICP, but the idea is that
        # AST evaluation uses recursion, therefore non-tail recursive
        # implementations quickly reach Python's recursion limit.
        self.eval("""(define (plus x y)
                        (if (= x 0)
                            y
                            (plus (- x 1) (+ y 1))))""")
        self.assertEval("(plus 4000 1)", 4001)

        # And another one to make sure that mutually recursive
        # procedures are tail-recursive as well
        # BTW, no idea what these functions do :-)
        self.eval("""(define (a x)
                        (if (<= x 1)
                            1
                            (b (- x 2))))""")
        self.eval("""(define (b x)
                        (if (<= x 1)
                            0
                            (a (+ x 1))))""")
        self.eval("(a 10000)") 

    def test1_2_2(self):
        """SICP 1.2.2 Tree Recursion"""
        self.eval("""(define (fib n)
                        (fib-iter 1 0 n))""")
        self.eval("""(define (fib-iter a b count)
                        (if (= count 0)
                            b
                            (fib-iter (+ a b) a (- count 1))))""")
        self.assertEval("(fib 25)", 75025)

        self.eval("""
        (define (count-change amount)
          (define (cc amount kinds-of-coins)
            (cond ((= amount 0) 1)
                  ((or (< amount 0) (= kinds-of-coins 0)) 0)
                  (else (+ (cc amount
                               (- kinds-of-coins 1))
                           (cc (- amount
                                  (first-denomination kinds-of-coins))
                               kinds-of-coins)))))
          (define (first-denomination kinds-of-coins)
            (cond ((= kinds-of-coins 1) 1)
                  ((= kinds-of-coins 2) 5)
                  ((= kinds-of-coins 3) 10)
                  ((= kinds-of-coins 4) 25)
                  ((= kinds-of-coins 5) 50)))
          (cc amount 5))""")
        self.assertEval("(count-change 100)", 292)

    def test1_2_6(self):
        """SICP 1.2.6 Example: Testing for Primality"""
        self.eval("""(define (smallest-divisor n)
                       (find-divisor n 2))""")
        self.eval("""
        (define (find-divisor n test-divisor)
           (cond ((> (square test-divisor) n) n)
                 ((divides?  test-divisor n) test-divisor)
                 (else (find-divisor n (+ test-divisor 1)))))""")
        self.eval("(define (divides? a b) (= (remainder b a) 0))")
        self.eval("(define (square x) (expt x 2))")
        self.eval("(define (prime? n) (= n (smallest-divisor n)))")

        self.assertEval("(prime? 3)", TRUE)
        self.assertEval("(prime? 4)", FALSE)
        self.assertEval("(prime? 100)", FALSE)
        self.assertEval("(prime? 113)", TRUE)

    def test1_3_1(self):
        """SICP 1.3.1 Procedures as Arguments"""
        # recursive definition breaks python recursion limit
        # replaced by iter-result of ex 1.30
        self.eval("""(define (sum term a next b)
                       (define (iter a result)
                         (if (> a b)
                             result
                             (iter (next a) (+ result (term a)))))
                       (iter a 0))""")
        self.eval("""(define (cube n) (expt n 3))""")
        self.eval("""(define (inc n) (+ n 1))""")

        self.eval("""(define (sum-cubes a b)
                       (sum cube a inc b))""")
        self.assertEval("(sum-cubes 1 10)", 3025)
        
        self.eval("""(define (identity x) x)""")
        self.eval("""(define (sum-integers a b)
                        (sum identity a inc b))""")
        self.assertEval("(sum-integers 1 10)", 55)

        self.eval("""(define (pi-sum a b)
                       (define (pi-term x)
                         (/ 1.0 (* x (+ x 2))))
                       (define (pi-next x)
                         (+ 4 x))
                       (sum pi-term a pi-next b))""")
        self.assertFEval("(* 8 (pi-sum 1 1000))", 3.139592)

        self.eval("""(define (integral f a b dx)
                       (define (add-dx x) (+ x dx))
                       (* (sum f (+ a (/ dx 2.0)) add-dx b)
                          dx))""")
        self.assertFEval("(integral cube 0 1 0.01)", 0.2499875)
        self.assertFEval("(integral cube 0 1 0.001)", 0.2499875)

    def test1_3_2(self):
        """SICP 1.3.2 Constructing Procedures using Lambda"""
        self.eval("(lambda (x) (+ x 4))")
        self.eval("""(define (sum term a next b)
                       (define (iter a result)
                         (if (> a b)
                             result
                             (iter (next a) (+ result (term a)))))
                       (iter a 0))""")
        self.eval("""(define (pi-sum a b)
                       (sum (lambda (x) (/ 1.0 (* x (+ x 2))))
                            a
                            (lambda (x) (+ x 4))
                            b))""")
        self.assertFEval("(* 8 (pi-sum 1 1000))", 3.139592)

        self.eval("""(define (integral f a b dx)
                       (* (sum f
                               (+ a (/ dx 2.0))
                               (lambda (x) (+ x dx))
                               b)
                           dx))""")
        self.eval("(define cube (lambda (x) (expt x 3)))")
        self.assertFEval("(integral cube 0 1 0.01)", 0.2499875)
        self.assertFEval("(integral cube 0 1 0.001)", 0.2499875)


        self.eval("""(define plus4 (lambda (x) (+ x 4)))""")
        self.assertEval("(plus4 100)", 104)

        self.eval("""(define square (lambda (x) (* x x)))""")
        self.assertEval("((lambda (x y z) (+ x y (square z))) 1 2 3)",
                        12)

        self.eval("(define x 5)")
        self.assertEval("""(+ (let ((x 3))
                                (+ x (* x 10)))
                              x)""", 38)

        self.eval("(define x 2)")
        self.assertEval("""(let ((x 3)
                                 (y (+ 2 x)))
                             (* x y))""", 12)

    def test1_3_3(self):
        """SICP 1.3.3 Procedures as General Methods"""
        self.eval("""
        (define (search f neg-point pos-point)
          (let ((midpoint (average neg-point pos-point)))
            (if (close-enough? neg-point pos-point)
                midpoint
                (let ((test-value (f midpoint)))
                  (cond ((positive? test-value)
                         (search f neg-point midpoint))
                        ((negative? test-value)
                         (search f midpoint pos-point))
                        (else midpoint))))))""")
        self.eval("""(define (close-enough? x y)
                       (< (abs (- x y)) 0.001))""")
        self.eval("""(define (average x y)
                       (/ (+ x y) 2))""")

        self.eval("""
        (define (half-interval-method f a b)
          (let ((a-value (f a))
                (b-value (f b)))
            (cond ((and (negative? a-value) (positive? b-value))
                   (search f a b))
                  ((and (negative? b-value) (positive? a-value))
                   (search f b a))
                  (else
                   (error "Values are not of opposite sign" a b)))))""")

        try:
            self.eval("(half-interval-method sin 4.0 4.0)")
            self.fail("Error did not work")
        except SchemeException:
            pass

        self.assertFEval("(half-interval-method sin 2.0 4.0)",
                         3.14111328)
        self.assertFEval("""
        (half-interval-method (lambda (x) (- (* x x x) (* 2 x) 3))
                              1.0
                              2.0)""",
                         1.89306640)

        self.eval("(define tolerance 0.00001)")
        self.eval("""
        (define (fixed-point f first-guess)
          (define (close-enough? v1 v2)
            (< (abs (- v1 v2)) tolerance))
          (define (try guess)
            (let ((next (f guess)))
              (if (close-enough? guess next)
                  next
                  (try next))))
          (try first-guess))""")
        self.assertFEval("(fixed-point cos 1.0)", 0.73908229852)
        self.assertFEval("""
        (fixed-point (lambda (y) (+ (sin y) (cos y)))
                     1.0)""", 1.258731596)

        self.eval("""(define (sqrt x)
                       (fixed-point (lambda (y) (average y (/ x y)))
                       1.0))""")
        self.assertFEval("(sqrt 4.0)", 2.0)

    def test1_3_4(self):
        """SICP 1.3.4 Procedures as Returned Values"""
        self.eval("""(define (average x y) 
                       (/ (+ x y) 2))""") 
        self.eval("""(define (average-damp f) 
                       (lambda (x) (average x (f x))))""") 
        self.eval("""(define (square x) (* x x))""")

        self.assertEval("((average-damp square) 10)", 55)

        self.eval("(define tolerance 0.00001)") 
        self.eval("""
        (define (fixed-point f first-guess)
          (define (close-enough? v1 v2)
            (< (abs (- v1 v2)) tolerance))
          (define (try guess)
            (let ((next (f guess)))
              (if (close-enough? guess next)
                  next
                  (try next))))
          (try first-guess))""")
        self.eval("""(define (sqrt x)
                       (fixed-point (average-damp (lambda (y) (/ x y)))
                                    1.0))""")
        self.assertFEval("(sqrt 4)", 2.0)

        self.eval("""(define (deriv g)
                       (lambda (x)
                         (/ (- (g (+ x dx)) (g x))
                            dx)))""")
        self.eval("(define dx 0.00001)")
        self.eval("(define (cube x) (* x x x))")
        self.assertFEval("((deriv cube) 5)", 75.0001499967)
        
        
#
#
# R5RS
#
#
        

# some useful constants
A = Symbol("a")
B = Symbol("b")
C = Symbol("c")
D = Symbol("d")
E = Symbol("e")
X = Symbol("x")
Y = Symbol("y")


class R5RSTest(InterpreterTest):
    """
    Sections from the Revised^5 Report on Scheme
    """

    def testMultipleCommands(self):
        """Interpreter can handle input containing multiple commands
        and expressions.
        """
        self.eval("""(define x 10) ; first def
                     (define y 20) ; second def
                     ; and now: the last def
                     (define z 30)""")
        self.assertEval("x", 10)
        self.assertEval("y", 20)
        self.assertEval("z", 30)

        self.assertEval("""(define a 1)
                           (define b 2)
                           (define c 3)
                           ; result of multiple commands is the
                           ; value of the last expression
                           (+ a b c)""", 6)

        self.assertEval("""(define n 1)
                           n
                           ; result is also last expression if
                           ; input ends with comments""", 1)

    
    def testLexicalScoping(self):
        """Scheme uses lexical scoping """

        # lexical scoping != dynamic scoping
        self.eval("""(define ten 10)""")
        self.eval("""(define (add10 x)
                       (+ ten x))""")
        self.eval("""(define (add20 x)
                       (define ten 20)
                       (add10 x))""")
        self.assertEval("(add20 7)", 17) # Dyn. scoping => 27
        self.assertEval("(add10 7)", 17)

        self.eval("""(define ten 100)""")
        self.assertEval("(add10 7)", 107) # Lex. scoping, Dyn. binding

        # but closer definitions take precedence
        self.eval("""(define plus +)""")
        self.eval("""(define (plus20 x) (plus 20 x))""")
        self.eval("""(define (times10 x)
                        (define plus *)
                        (plus 10 x))""")
        self.assertEval("(plus20 7)", 27)
        self.assertEval("(times10 7)", 70)


    def testFalse(self):
        """Some pathetic differences between Scheme and Python"""
        self.assertEval("(if 0 2 3)", 2)

    def test1_3_4(self):
        """R5RS 1.3.4 Evaluation examples"""
        self.assertEval("(* 5 8)", 40)

    def test2_1_1(self):
        """R5RS 2.1.1 Comments"""
        self.eval("""
        ;;; The FACT procedure computes the factorial
        ;;; of a non-negative integer
        (define fact
          (lambda (n)
            (if (= n 0)
            1               ; Base case, return 1
            (* n (fact (- n 1))))))
        """)
        self.assertEval("(fact 4)", 24)
        self.eval("; oops")
        self.assertEval('"hello; world"', "hello; world")

    def test4_1_1(self):
        """R5RS 4.1.1 Variable references"""
        self.eval("(define x 28)")
        self.assertEval("x", 28)

    def test4_1_2(self):
        """R5RS 4.1.2 Literal expressions"""
        self.assertEval("(quote a)", A)
        self.assertEval("(quote #(a b c))", Vector([A, B, C]))
        self.assertEval("(quote (+ 1 2))",
                        Pair(Symbol("+"),
                             Pair(1,
                                  Pair(2, EMPTY_LIST))))
        self.assertEval("'a", A)
        self.assertEval("'#(a b c)", Vector([A, B, C]))
        self.assertEval("'()", EMPTY_LIST)
        self.assertEval("'(+ 1 2)",
                        Pair(Symbol("+"),
                             Pair(1,
                                  Pair(2, EMPTY_LIST))))
        self.assertEval("'(quote a)",
                        Pair(Symbol("quote"),
                             Pair(A, EMPTY_LIST)))
        self.assertEval("''a",
                        Pair(Symbol("quote"),
                             Pair(A, EMPTY_LIST)))

        self.assertEval("'\"abc\"", "abc")
        self.assertEval("\"abc\"", "abc")
        self.assertEval("'145932", 145932)
        self.assertEval("145932", 145932)
        self.assertEval("'#t", TRUE)
        self.assertEval("#t", TRUE)

    def test4_1_3(self):
        """R5RS 4.1.3 Procedure calls"""
        self.assertEval("(+ 3 4)", 7)
        self.assertEval("((if #f + *) 3 4)", 12)

        # make sure only formals are used!
        self.eval("(define (square x) (* x x))")
        self.eval("(define x 5)")
        self.assertError("(square)")

    def test4_1_4(self):
        """R5RS 4.1.4 Procedures"""
        self.eval("(lambda (x) (+ x x))")
        self.assertEval("((lambda (x) (+ x x)) 4)", 8)
        self.eval("""(define reverse-substract
                        (lambda (x y) (- y x)))""")
        self.assertEval("(reverse-substract 7 10)", 3)
        self.eval("""(define add4
                        (let ((x 4))
                          (lambda (y) (+ x y))))""")
        self.assertEval("(add4 6)", 10)

##         self.assertEval("((lambda x x) 3 4 5 6)",
##                         Pair(3,
##                              Pair(4,
##                                   Pair(5,
##                                        Pair(6, [])))))
##         self.assertEval("((lambda (x y . z) z) 3 4 5 6)",
##                         Pair(5,
##                              Pair(6, [])))

    def test4_1_5(self):
        """R5RS 4.1.5 Conditionals"""
        self.assertEval("(if (> 3 2) 'yes 'no)", Symbol("yes"))
        self.assertEval("(if (> 2 3) 'yes 'no)", Symbol("no"))
        self.assertEval("""(if (> 3 2)
                               (- 3 2)
                               (+ 3 2))""", 1)

    def test4_1_6(self):
        """R5RS 4.1.6 Assignments"""
        self.eval("(define x 2)")
        self.assertEval("(+ x 1)", 3)
##         self.eval("(set! x 4)")
##         self.assertEval("(+ x 1)", 5)

    def test4_2_1(self):
        """R5RS 4.2.1 Conditionals"""
        self.assertEval("""(cond ((> 3 2) 'greater)
                                 ((< 3 2) 'less))""", Symbol("greater"))
        self.assertEval("""(cond ((> 3 3) 'greater)
                                 ((< 3 3) 'less)
                                 (else 'equal))""", Symbol("equal"))
##         self.assertEval("""(cond ((assv 'b
##                                         '((a 1) (b 2))) => cadr)
##                                  (else #f))""", 2)

##         self.assertEval("""(case (* 2 3)
##                               ((2 3 5 7) 'prime)
##                               ((1 4 6 8 9) 'composite))""",
##                         Symbol("composite"))
##         self.eval("""(case (car '(c d))
##                               ((a) 'a)
##                               ((b) 'b)""")
##         self.assertEval("""(case (car '(c d))
##                               ((a e o i u) 'vowel)
##                               ((w y) 'semivowel)
##                               (else 'consonant))""",
##                         Symbol("consonant"))
        
        self.assertEval("""(and (= 2 2) (> 2 1))""", TRUE)
        self.assertEval("""(and (= 2 2) (< 2 1))""", FALSE)
        self.assertEval("""(and 1 2 'c '(f g))""",
                        Pair(Symbol("f"),
                             Pair(Symbol("g"), EMPTY_LIST)))
        self.assertEval("""(and)""", TRUE)

        self.assertEval("""(or (= 2 2) (> 2 1))""", TRUE)
        self.assertEval("""(or (= 2 2) (< 2 1))""", TRUE)
        self.assertEval("""(or #f #f #f)""", FALSE)
        self.assertEval("""(or (memq 'b '(a b c))
                               (/ 3 0))""",
                        Pair(B,
                             Pair(C, EMPTY_LIST)))

    def test6_1(self):
        """R5RS 6.1   Equivalence predicates"""
        # unspecified results left out
        
        self.assertEval("(eqv? 'a 'a)", TRUE)
        self.assertEval("(eqv? 'a 'b)", FALSE)
        self.assertEval("(eqv? 2 2)", TRUE)
        self.assertEval("(eqv? '() '())", TRUE)
        self.assertEval("(eqv? 10000000 10000000)", TRUE)
        self.assertEval("(eqv? (cons 1 2) (cons 1 2))", FALSE)
        self.assertEval("(eqv? (lambda () 1) (lambda () 2))", FALSE)
        self.assertEval("(eqv? #f 'nil)", FALSE)
        self.assertEval("(let ((p (lambda (x) x))) (eqv? p p))", TRUE)

##         self.eval("""(define gen-counter
##                         (lambda ()
##                           (let ((n 0))
##                             (lambda () (set! n (+ n 1) n))))""")
##         self.assertEval("(let ((g (gen-counter))) (eqv? g g))", TRUE)
##         self.assertEval("(eqv? (gen-counter) (gen-counter))", FALSE)

        self.assertEval("(eq? 'a 'a)", TRUE)
        self.assertEval("(eq? (list 'a) (list 'a))", FALSE)
        self.assertEval("(eq? '() '())", TRUE)
        self.assertEval("(eq? car car)", TRUE)
        self.assertEval("(let ((x '(a))) (eq? x x))", TRUE)
        self.assertEval("(let ((x '#())) (eq? x x))", TRUE)
        self.assertEval("(let ((p (lambda (x) x))) (eq? p p))", TRUE)

        self.assertEval("(equal? 'a 'a)", TRUE)
        self.assertEval("(equal? '(a) '(a))", TRUE)
        self.assertEval("(equal? '(a (b) c) '(a (b) c))", TRUE)
        self.assertEval('(equal? "abc" "abc")', TRUE)
        self.assertEval("(equal? 2 2)", TRUE)
        self.assertEval("""(equal? (make-vector 5 'a)
                                   (make-vector 5 'a))""", TRUE)
        

    def test6_2_5(self):
        """R5RS 6.2.5 Numerical operations"""
        ### NOT FINISHED
        self.assertEval("(zero? 1)", FALSE)
        self.assertEval("(zero? 0)", TRUE)
        self.assertEval("(zero? -1)", FALSE)
        self.assertEval("(zero? 1.0)", FALSE)
        self.assertEval("(zero? 0.0)", TRUE)

        self.assertEval("(positive? 1)", TRUE)
        self.assertEval("(positive? 0)", FALSE)
        self.assertEval("(positive? -1)", FALSE)
        self.assertEval("(positive? 1.0)", TRUE)
        self.assertEval("(positive? 0.0)", FALSE)

        self.assertEval("(negative? 1)", FALSE)
        self.assertEval("(negative? 0)", FALSE)
        self.assertEval("(negative? -1)", TRUE)
        self.assertEval("(negative? 1.0)", FALSE)
        self.assertEval("(negative? 0.0)", FALSE)

        self.assertEval("(even? 1)", FALSE)       
        self.assertEval("(even? 2)", TRUE)       
        self.assertEval("(even? -1)", FALSE)       
        self.assertEval("(even? -2)", TRUE)       
        self.assertEval("(even? 1.0)", FALSE)       
        self.assertEval("(even? 2.0)", TRUE)       
        self.assertEval("(even? 0)", TRUE)       
        
        self.assertEval("(odd? 1)", TRUE)       
        self.assertEval("(odd? 2)", FALSE)       
        self.assertEval("(odd? -1)", TRUE)       
        self.assertEval("(odd? -2)", FALSE)       
        self.assertEval("(odd? 1.0)", TRUE)       
        self.assertEval("(odd? 2.0)", FALSE)       
        self.assertEval("(odd? 0)", FALSE)       
        
        self.assertEval("(+ 3 4)", 7)
        self.assertEval("(+ 3)", 3)
        self.assertEval("(+)", 0)
        self.assertEval("(* 4)", 4)
        self.assertEval("(*)", 1)

        self.assertEval("(- 3 4)", -1)
        self.assertEval("(- 3 4 5)", -6)
        self.assertEval("(- 3)", -3)
        self.assertEval("(/ 3 4 5)", frac(3, 20))
        self.assertEval("(/ 3)", frac(1, 3))

        self.assertEval("(abs -7)", 7)

        self.assertEval("(modulo 13 4)", 1)
        self.assertEval("(remainder 13 4)", 1)
        
        self.assertEval("(modulo -13 4)", 3)
        self.assertEval("(remainder -13 4)", -1)
        
        self.assertEval("(modulo 13 -4)", -3)
        self.assertEval("(remainder 13 -4)", 1)

        self.assertEval("(modulo -13 -4)", -1)
        self.assertEval("(remainder -13 -4)", -1)

        self.assertFEval("(remainder -13 -4.0)", -1.0)

        self.assertEval("(expt 2 8)", 256)
        self.assertFEval("(expt 2.5 2)", 6.25)
        self.assertEval("(expt 0 0)", 1)
        self.assertEval("(expt 0 2)", 0)
        self.assertEval("(expt 8 -1)", frac(1, 8))
        self.assertEval("(expt 4 -2)", frac(1, 16))
        self.assertFEval("(expt 4.1 -2)", 0.059488399762046409)
        

    def test6_3_1(self):
        """R5RS 6.3.1 Booleans"""
        self.assertEval("#t", TRUE)
        self.assertEval("#f", FALSE)
        self.assertEval("'#f", FALSE)

        self.assertEval("(not #t)", FALSE)
        self.assertEval("(not 3)", FALSE)
        self.assertEval("(not (list 3))", FALSE)
        self.assertEval("(not #f)", TRUE)
        self.assertEval("(not '())", FALSE)
        self.assertEval("(not (list))", FALSE)
        self.assertEval("(not 'nil)", FALSE)

        self.assertEval("(boolean? #f)", TRUE)
        self.assertEval("(boolean? 0)", FALSE)
        self.assertEval("(boolean? '())", FALSE)

    def test6_3_2(self):
        """R5RS 6.3.2 Pairs and Lists"""
        list1 = self.eval("'(a b c d e)")
        list2 = self.eval("'(a . (b . (c . (d . (e . ())))))")
        self.assertEquals(list1, list2)

        list1 = self.eval("'(a b c . d)")
        list2 = self.eval("'(a . (b . (c . d)))")
        self.assertEquals(list1, list2)

        self.assertEval("'(a)", Pair(A, EMPTY_LIST))

        self.eval("(define x (list 'a 'b 'c))")
        self.eval("(define y x)")
        self.assertEval("y", Pair(A,
                                  Pair(B,
                                       Pair(C, EMPTY_LIST))))
        
        self.assertEval("(list? y)", TRUE)
        self.eval("(set-cdr! x 4)")
        self.assertEval("x", Pair(A, 4))
        self.assertEval("(eqv? x y)", TRUE)
        self.assertEval("y", Pair(A, 4))
        self.assertEval("(list? y)", FALSE)
        self.eval("(set-cdr! x x)")
        self.assertEval("(list? x)", FALSE)

        self.assertEval("(pair? '(a . b))", TRUE)
        self.assertEval("(pair? '(a b c))", TRUE)
        self.assertEval("(pair? '())", FALSE)
        self.assertEval("(pair? '#(a b))", FALSE)

        self.assertEval("(cons 'a '())", Pair(A, EMPTY_LIST))
        self.assertEval("(cons '(a) '(b c d))",
                        Pair(Pair(A, EMPTY_LIST),
                             Pair(B,
                                  Pair(C,
                                       Pair(D, EMPTY_LIST)))))
        self.assertEval("(cons \"a\" '(b c))",
                        Pair("a",
                             Pair(B,
                                  Pair(C, EMPTY_LIST))))
        
        self.assertEval("(cons 'a 3)", Pair(A, 3))
        self.assertEval("(cons '(a b) 'c)",
                        Pair(Pair(A,
                                  Pair(B, EMPTY_LIST)),
                             C))
        self.assertEval("(car '(a b c))", A)
        self.assertEval("(car '((a) b c d))",
                        Pair(A, EMPTY_LIST))
        self.assertEval("(car '(1 . 2))", 1)
        
        self.assertEval("(cdr '((a) b c d))",
                        Pair(B,
                             Pair(C,
                                  Pair(D, EMPTY_LIST))))

        self.assertEval("(cdr '(1 . 2))", 2)

        self.eval("(define (f) (list 'not-a-constant-list))")
        self.eval("(define (g) '(constant-list))")
        self.eval("(set-car! (f) 3)")
        self.assertError("(set-car! (g) 3)")

        self.assertEval("(list? '(a b c))", TRUE)
        self.assertEval("(list? '())", TRUE)
        self.assertEval("(list? '(a . b))", FALSE)
        self.assertEval("""(let ((x (list 'a)))
                             (set-cdr! x x)
                             (list? x))""", FALSE)

        self.assertEval("(list 'a (+ 3 4) 'c)",
                        Pair(A,
                             Pair(7,
                                  Pair(C, EMPTY_LIST))))
        self.assertEval("(list)", EMPTY_LIST)

        self.assertEval("(length '(a b c))", 3)
        self.assertEval("(length '(a (b) (c d e)))", 3)
        self.assertEval("(length '())", 0)

        self.assertEval("(append '(x) '(y))",
                        Pair(X,
                             Pair(Y, EMPTY_LIST)))
        self.assertEval("(append '(a) '(b c d))",
                        Pair(A,
                             Pair(B,
                                  Pair(C,
                                       Pair(D, EMPTY_LIST)))))
        self.assertEval("(append '(a (b)) '((c)))",
                        Pair(A,
                             Pair(Pair(B, EMPTY_LIST),
                                  Pair(Pair(C, EMPTY_LIST),
                                       EMPTY_LIST))))
        
        self.assertEval("(append '(a b) '(c . d))",
                        Pair(A,
                             Pair(B,
                                  Pair(C, D))))

        self.assertEval("(append '() 'a)", A)
        self.assertEval("(append '(a) 'a)",
                        Pair(A, A))

        self.assertEval("(reverse '(a b c))",
                        Pair(C,
                             Pair(B, 
                                  Pair(A, EMPTY_LIST))))
        self.assertEval("(reverse '(1 (2 3) 4 (5 (6))))",
                        Pair(Pair(5,
                                  Pair(Pair(6, EMPTY_LIST), EMPTY_LIST)),
                             Pair(4,
                                  Pair((Pair(2,
                                             Pair(3, EMPTY_LIST))),
                                       Pair(1, EMPTY_LIST)))))
        
        self.assertEval("(reverse '())", EMPTY_LIST)
        self.assertEval("(reverse '(a))", Pair(A, EMPTY_LIST))
        
        self.assertEval("(list-tail '(0 1 2 3 4) 2)",
                        Pair(2,
                             Pair(3,
                                  Pair(4, EMPTY_LIST))))
        self.assertError("(list-tail '(0) 2)")

        self.assertEval("(list-ref '(a b c d) 2)", C)
##         self.assertEval("(list-ref '(a b c d)
##                                    (inexact->exact (round 1.8)))",
##                         C)
        self.assertError("(list-ref '(0) 2)")

        self.assertEval("(memq 'a '(a b c))",
                        Pair(A,
                             Pair(B,
                                  Pair(C, EMPTY_LIST))))
        self.assertEval("(memq 'b '(a b c))",
                        Pair(B, Pair(C, EMPTY_LIST)))
        self.assertEval("(memq 'a '(b c d))", FALSE)
        self.assertEval("(memq (list 'a) '(b (a) c))", FALSE)
        self.assertEval("(member (list 'a) '(b (a) c))",
                        Pair(Pair(A, EMPTY_LIST), Pair(C, EMPTY_LIST)))
        self.assertEval("(memv 101 '(100 101 102))",
                        Pair(101, Pair(102, EMPTY_LIST)))
        self.assertEval("(memq 'a '())", FALSE)

        self.eval("(define e '((a 1) (b 2) (c 3)))")
        self.assertEval("(assq 'a e)", Pair(A, Pair(1, EMPTY_LIST)))
        self.assertEval("(assq 'b e)", Pair(B, Pair(2, EMPTY_LIST)))
        self.assertEval("(assq 'd e)", FALSE)
        self.assertEval("(assq (list 'a) '(((a)) ((b)) ((c))))", FALSE)
        self.assertEval("(assoc (list 'a) '(((a)) ((b)) ((c))))",
                        Pair(Pair(A, EMPTY_LIST), EMPTY_LIST))
        self.assertEval("(assv 5 '((2 3) (5 7) (11 13)))",
                        Pair(5, Pair(7, EMPTY_LIST)))
        
                             
        
        
    def test6_3_3(self):
        """R5RS 6.3.3 Symbols"""
        self.assertEval("(symbol? 'a)", TRUE)
        self.assertEval("(symbol? (car '(a b)))", TRUE)
        self.assertEval('(symbol? "bar")', FALSE)
        self.assertEval("(symbol? 'nil)", TRUE)
        self.assertEval("(symbol? '())", FALSE)
        self.assertEval("(symbol? #f)", FALSE)

        self.assertEval("(symbol->string 'flying-fish)", "flying-fish")
        self.assertEval("(symbol->string 'Martin)", "martin")
        self.assertEval("""(symbol->string
                              (string->symbol "Malvina"))""", "Malvina")

        self.assertEval("(eq? 'mISSISSIppi 'mississippi)", TRUE)
        self.assertEval("""(string->symbol "mISSISSIppi")""",
                        Symbol("mISSISSIppi", fromString="mISSISSIppi"))
        self.assertEval("""(eq? 'bitBlt (string->symbol "bitBlt"))""",
                        FALSE)
        self.assertEval("""(eq? 'JollyWog
                                (string->symbol
                                  (symbol->string 'JollyWog)))""", TRUE)
        self.assertEval("""(string=? "K. Harper, M.D."
                                 (symbol->string
                                   (string->symbol "K. Harper, M.D.")))
                        """, TRUE)

    def test6_3_4(self):
        """R5RS 6.3.4 Characters"""
        self.assertEval(r"#\a", char("a"))
        self.assertEval(r"#\A", char("A"))
        self.assertEval(r"#\(", char("("))
        self.assertEval(r"#\ ", char(" "))
        self.assertEval(r"#\-", char("-"))

        self.assertEval(r"#\space", char(" "))
        self.assertEval(r"#\newline", char("\n"))

        self.assertEval(r"#\SPaCE", char(" "))
        self.assertEval(r"#\NEWLine", char("\n"))

        self.assertEval(r"(char? #\a)", TRUE)
        self.assertEval(r'(char? "a")', FALSE)

        self.assertEval(r"(char=? #\a #\a)", TRUE)
        self.assertEval(r"(char=? #\a #\a #\a)", TRUE)
        self.assertEval(r"(char=? #\a #\a #\A)", FALSE)

        self.assertEval(r"(char<? #\A #\B #\C)", TRUE)
        self.assertEval(r"(char>? #\c #\b #\a)", TRUE)
        self.assertEval(r"(char<=? #\1 #\2 #\3)", TRUE)
        self.assertEval(r"(char>=? #\2 #\1 #\3)", FALSE)

        self.assertEval(r"(char-ci=? #\A #\a #\a)", TRUE)

        self.assertEval(r"(char-alphabetic? #\a)", TRUE)
        self.assertEval(r"(char-alphabetic? #\A)", TRUE)
        self.assertEval(r"(char-alphabetic? #\0)", FALSE)
        self.assertEval(r"(char-alphabetic? #\space)", FALSE)
                        
        self.assertEval(r"(char-numeric? #\a)", FALSE)
        self.assertEval(r"(char-numeric? #\A)", FALSE)
        self.assertEval(r"(char-numeric? #\0)", TRUE)
        self.assertEval(r"(char-numeric? #\space)", FALSE)
                        
        self.assertEval(r"(char-whitespace? #\a)", FALSE)
        self.assertEval(r"(char-whitespace? #\A)", FALSE)
        self.assertEval(r"(char-whitespace? #\0)", FALSE)
        self.assertEval(r"(char-whitespace? #\space)", TRUE)
                        
        self.assertEval(r"(char-upper-case? #\a)", FALSE)
        self.assertEval(r"(char-upper-case? #\A)", TRUE)
        self.assertEval(r"(char-upper-case? #\0)", FALSE)
        self.assertEval(r"(char-upper-case? #\space)", FALSE)
                        
        self.assertEval(r"(char-lower-case? #\a)", TRUE)
        self.assertEval(r"(char-lower-case? #\A)", FALSE)
        self.assertEval(r"(char-lower-case? #\0)", FALSE)
        self.assertEval(r"(char-lower-case? #\space)", FALSE)

        prev = "a"
        for i in "bcdefghijklmnopqrstuvwxyz":
            self.assertEval(r"""(<= (char->integer #\%s)
                                  (char->integer #\%s))""" % (prev, i),
                            TRUE)
            prev = i

        for low, up in zip(string.ascii_lowercase, string.ascii_uppercase):
            self.assertEval(r"(char-upcase #\%s)" % (low), char(up))
            self.assertEval(r"(char-downcase #\%s)" % (up), char(low))
        

    def test6_3_5(self):
        """R5RS 6.3.5 Strings""" 
        self.assertEval(r'"The word \"recursion\" has many meanings"', 
                        'The word "recursion" has many meanings') 
        self.assertEval('(string? "hello world")', TRUE)
        self.assertEval("(string? 5)", FALSE)
        self.assertEval(r"(string? #\-)", FALSE)

        self.assertEval(r'(make-string 5 #\a)', "aaaaa")
        self.assertEval('(string? (make-string 100))', TRUE)

        self.assertEval(r'''(string #\H #\e #\l #\l #\o #\space
                                    #\W #\o #\r #\l #\d)''', "Hello World")

        self.assertEval('(string-length "hello world")', 11)
        self.assertEval('(string-length (make-string 43))', 43)

        self.assertEval('(string-ref "abc" 0)', char("a"))
        self.assertEval('(string-ref "abc" 2)', char("c"))
        self.assertError('(string-ref "abc", 3)')

        self.eval("(define (f) (make-string 3 #\*))")
        self.eval('(define (g) "***")')
        self.eval("(string-set! (f) 0 #\?)")
        self.assertError("(string-set! (g) 0 #\?")
        self.assertError("(string-set! (symbol->string 'immutable) 0 #\?)")

        self.assertEval(r"""(string=? (string #\H #\e #\l #\l #\o)
                                      "Hello")""", TRUE)
        self.assertEval(r"""(string-ci=? (make-string 5 #\q)
                                         "QqQqq")""", TRUE)

        self.assertEval(r'(string<? "aaa" "bbb")', TRUE)
        self.assertEval(r'(string<? "BBB" "AAA")', FALSE)

        self.assertEval(r'(string-ci<? "aaa" "BBB")', TRUE) 

        self.assertEval('(substring "hello world" 6 9)', "wor")
        self.assertError('(substring "hello world" 9 5)')
        self.assertError('(substring "hi" 0 3)')
        self.assertEval('(substring "hi" 0 0)', "")

        self.assertEval('(string-append "hello " "world")', "hello world")

        self.assertEval('(string->list "hi")',
                        Pair(Character("h"),
                             Pair(Character("i"), EMPTY_LIST)))
        self.assertEval(r"(list->string '(#\h #\e #\l #\l #\o))", "hello")
        self.assertEval('(string-copy "hello")', "hello")
        self.eval(r"(define x (string #\h #\i))")
        self.eval(r"(string-fill! x #\q)")
        self.assertEval("x", "qq")

    def test6_3_6(self):
        """R5RS 6.3.6 Vectors"""

        twos = pairFromList([2, 2, 2, 2, EMPTY_LIST])
        self.assertEval("'#(0 (2 2 2 2) \"Anna\")",
                        Vector([0, twos, "Anna"]))

        self.assertEval("(vector? '#(2 2))", TRUE)
        self.assertEval("(vector? '#())", TRUE)
        self.assertEval("(vector? '())", FALSE)
        self.assertEval("(vector? '(1 . 2))", FALSE)

        self.assertEval("(vector-length (make-vector 10))", 10)
        self.assertEval("(make-vector 10 2)",
                        Vector([2] * 10))
        self.assertEval("(vector 'a 'b 'c)",
                        Vector([A, B, C]))

        self.assertEval("(vector-length '#(a b c))", 3)
        self.assertEval("(vector-ref '#(a b c) 2)", C)

        self.assertEval("(vector-ref '#(1 1 2 3 5 8 13 21) 5)", 8)
##         self.assertEval("""(vector-ref '#(1 1 2 3 5 8 13 21)
##                                        (let ((i (round (* 2 (acos -1)))))
##                                          (if (inexact? i)
##                                              (inexact->exact i)
##                                              i)))""", 13)

        sue2 = pairFromList(["Sue", "Sue", EMPTY_LIST])
        self.assertEval("""(let ((vec (vector 0 '(2 2 2 2) "Anna")))
                              (vector-set! vec 1 '("Sue" "Sue"))
                              vec)""",
                        Vector([0, sue2, "Anna"]))

        self.assertError("(vector-set! '#(0 1 2) 1 \"doe\")")

        self.assertEval("(vector->list '#(dah dah didah))",
                        pairFromList([Symbol("dah"),
                                      Symbol("dah"),
                                      Symbol("didah")]))
        self.assertEval("(list->vector '(dididit dah))",
                        Vector([Symbol("dididit"), Symbol("dah")]))

        self.assertEval("""(define vec (make-vector 4))
                           (vector-fill vec 1)
                           vec""",
                        Vector([1, 1, 1, 1]))
                             
                        
        
        

def suite():
    """Returns the testsuite for this module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SICPTest, "test"))
    suite.addTest(unittest.makeSuite(R5RSTest, "test"))

    return suite
        


