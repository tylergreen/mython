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
Tests the boolean module
"""

from psyche.types import *
import unittest

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.3 $"[11:-2]

class BooleanTest(unittest.TestCase):

    def testStringRepr(self):
        """String representation #t and #f"""
        self.assertEquals(str(TRUE), "#t")
        self.assertEquals(str(FALSE), "#f")


    def testFromExpression(self):
        """In Scheme, only #f is false"""
        self.assert_(not(Boolean("#f")))
        self.assert_(not(FALSE))

        self.assert_(Boolean(""))
        self.assert_(Boolean(None))
        self.assert_(Boolean(0))


def suite():
    """Returns the testsuite for this module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(BooleanTest, "test"))

    return suite
        
