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
Test Suite for the fraction type
"""

import unittest
from psyche.types import *

__author__ = "yduppen@xs4all.nl"
__revision__ = "$Revision: 1.2 $"[11:-2]

class FractionTest(unittest.TestCase):
    """Tests the fraction type"""


    def testRepresentation(self):
        """Do we use the correct string representation?"""
        self.assertEquals(str(frac(1, 2)), "1/2")
        self.assertEquals(str(frac(98, 99)), "98/99")
        self.assertEquals(str(frac(1L, 2L)), "1/2")
        self.assertEquals(str(frac(74839, 1)), "74839")

    def testNormalizing(self):
        """Are the string representations of
        fractions always normalized?
        """
        self.assertEquals(str(frac(2, 4)), "1/2")
        self.assertEquals(str(frac(1, 3)), "1/3")
        self.assertEquals(str(frac(2L, 4)), "1/2")
        self.assertEquals(str(frac(263019, 350692)), "3/4")

    def testNegative(self):
        """Is the negative sign always in front?"""
        self.assertEquals(str(frac(-1, 2)), "-1/2")
        self.assertEquals(str(frac(1, -2)), "-1/2")
        self.assertEquals(str(frac(-1, -2)), "1/2")


    def testEquality(self):
        """Tests the equality operator"""
        self.assert_(frac(1, 2) == frac(-1, -2))
        self.assert_(frac(1, 3) != frac(1, 2))
        self.assert_(frac(2L, 4) == frac(1, 2))


    def testComparison(self):
        """Compare different fractions"""
        self.assert_(frac(1,3) < frac(1,2))
        self.assert_(frac(1,4) <= frac(1,2))
        self.assert_(frac(1,4) > frac(1,8))
        self.assert_(frac(1,5) >= frac(1,90))


    def testArithmetic(self):
        """Tests basic arithmetic"""
        a = frac(1,4)
        b = frac(15,41)

        self.assertEquals(a + b, frac(101, 164))
        self.assertEquals(a - b, frac(-19, 164))
        self.assertEquals(a * b, frac(15, 164))
        self.assertEquals(a / b, frac(41, 60))

        self.assertEquals(a ** 2, frac(1, 16))
        self.assertEquals(frac(2,3) ** 3, frac(8, 27))

    def testUnary(self):
        """Do the unary thingies work?"""
        a = frac(2, 15)
        b = frac(-2, 3)
        
        self.assertEquals(-a, frac(-2, 15))
        self.assertEquals(-b, frac(2, 3))
        self.assertEquals(+a, frac(2, 15))
        self.assertEquals(+b, frac(-2, 3))
        self.assertEquals(abs(a), frac(2, 15))
        self.assertEquals(abs(b), frac(2, 3))
        self.assertEquals(abs(frac(-5, -6)), frac(5, 6))


    def testConversion(self):
        """Convert to other numeric types"""
        a = frac(-15, 40)
        af = -15.0/40
        
        b = frac(40, 15)
        bf = 40.0/15
        

        self.assertEquals(float(a), af)
        self.assertEquals(complex(a), complex(af))
        self.assertEquals(int(a), -1)
        self.assertEquals(long(a), -1L)

        self.assertEquals(float(b), bf)
        self.assertEquals(complex(b), complex(bf))
        self.assertEquals(int(b), 2)
        self.assertEquals(long(b), 2L)


    def testLCoercionInteger(self):
        """Test left arithmetic with integer types"""
        a = frac(2,3)
        b = frac(17,5)

        self.assertEquals(a + 1, frac(5, 3))
        self.assertEquals(b + 2, frac(27, 5))
        self.assertEquals(a - 1, frac(-1, 3))
        self.assertEquals(b - 2, frac(7, 5))
        self.assertEquals(a * 1, a)
        self.assertEquals(b * 2, frac(34, 5))
        self.assertEquals(a / 1, frac(2, 3))
        self.assertEquals(b / 2, frac(17, 10))
        self.assert_(a < 1)
        self.assert_(a > 0)
        self.assert_(b > 3)
        self.assert_(b < 4)
        
    def testLCoercionFloat(self):
        """Test left arithmetic with float types"""
        a = frac(2,3)
        af = 2.0/3
        b = frac(17,5)
        bf = 17.0/5

        self.assertEquals(a + 1.0, 1+af)
        self.assertEquals(b + 2.0, 2+bf)
        self.assertEquals(a - 1.0, af-1)
        self.assertEquals(b - 2.0, bf-2)
        self.assertEquals(a * 1.0, af)
        self.assertEquals(b * 2.0, 2*bf)
        self.assertEquals(a / 1.0, af)
        self.assertEquals(b / 2.0, bf/2)
        self.assert_(a < 1.0)
        self.assert_(a > 0.3)
        self.assert_(b > 3.0)
        self.assert_(b < 4.0)

    def testRCoercionInteger(self):
        """Test right arithmetic with integer types"""
        a = frac(2,3)
        b = frac(17,5)

        self.assertEquals(1 + a, frac(5, 3))
        self.assertEquals(2 + b, frac(27, 5))
        self.assertEquals(1 - a, frac(1, 3))
        self.assertEquals(2 - b, frac(-7, 5))
        self.assertEquals(1 * a, a)
        self.assertEquals(2 * b, frac(34, 5))
        self.assertEquals(1 / a, frac(3, 2))
        self.assertEquals(2 / b, frac(10, 17))
        self.assert_(1 > a)
        self.assert_(0 < a)
        self.assert_(3 < b)
        self.assert_(4 > b)
        
    def testRCoercionFloat(self):
        """Test right arithmetic with float types"""
        a = frac(2,3)
        af = 2.0/3
        b = frac(17,5)
        bf = 17.0/5

        self.assertEquals(1.0 + a, 1+af)
        self.assertEquals(2.0 + b, 2+bf)
        self.assertEquals(1.0 - a, 1-af)
        self.assertEquals(2.0 - b, 2-bf)
        self.assertEquals(1.0 * a, af)
        self.assertEquals(2.0 * b, 2*bf)
        self.assertEquals(1.0 / a, 1/af)
        self.assertEquals(2.0 / b, 2/bf)
        self.assert_(1.0 > a)
        self.assert_(0.0 < a)
        self.assert_(3.0 < b)
        self.assert_(4.0 > b)

    def testLen(self):
        """Tests that 0/x is false"""
        self.assert_(not frac(0,100))

    def testStoringInDictionaries(self):
        """Test use in dictionaries"""
        dict = {}

        # With different numerators
        for i in range(100):
            dict[frac(1, i+1)] = i

        for i in range(100):
            self.assertEquals(dict[frac(1, i+1)], i)

        # with different denominators
        for i in range(100):
            dict[frac(i+1, 1)] = i

        for i in range(100):
            self.assertEquals(dict[frac(i+1, 1)], i)


    def testReciprocal(self):
        """Test reciprocals"""
        self.assertEquals(~frac(1,10), 10)
        self.assertEquals(~frac(-4378, 432L), frac(-432L, 4378))
        

    def FAILtestFromString(self):
        """Convert strings to fractions"""
        self.assertEquals(frac("1/2"), frac(1, 2))
        self.assertEquals(frac("1/-2"), frac(-1, 2))


def suite():
    """Returns this test suite as a unittest.TestSuite object. """
    return unittest.makeSuite(FractionTest, "test")


