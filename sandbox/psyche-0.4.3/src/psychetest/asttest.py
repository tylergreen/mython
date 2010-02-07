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
Tests the different AST nodes, especially their 'evaluation'
"""

from psyche.ast import *
import unittest

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.2 $"[11:-2]

class NumberTest(unittest.TestCase):

    def testInteger(self):
        """Tests evaluating an integer number"""
        self.assertEquals(Number("5").eval(),
                          5)
        self.assertEquals(Number("-17").eval(),
                          -17)
        self.assertEquals(Number("123456789987654321").eval(),
                                 123456789987654321)

    def testReal(self):
        """Tests evaluating a real number"""
        self.assertEquals(Number("5.75").eval(),
                          5.75)

        self.assertEquals(Number("-1238.4587").eval(),
                          -1238.4587)

        self.assertEquals(Number(".34").eval(),
                          0.34)


    def FAILtestComplex(self):
        """Tests evaluating a complex number"""
        self.assertEquals(Number("3+1i").eval(),
                          3+1j)
        
        self.assertEquals(Number("3-2i").eval(),
                          3-2j)


    # TODO
    # Different radices
    # Exponentation
    # More complex numbers



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(NumberTest, "test"))

    return suite

