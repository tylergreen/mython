#!/usr/bin/env python2.2

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

# Test suite for psyche


import unittest

from psychetest import lexertest, parsertest, interpretertest, asttest
from psychetest import analyzerstest
from psychetest import booleantest, fractiontest                    
     

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.1 $"[11:-2]


if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(booleantest.suite())
    suite.addTest(fractiontest.suite())
    suite.addTest(lexertest.suite())
    suite.addTest(parsertest.suite())
    suite.addTest(asttest.suite())
    suite.addTest(analyzerstest.suite())
    suite.addTest(interpretertest.suite())

    runner = unittest.TextTestRunner(verbosity = 2)
    runner.run(suite)
    

#
# $Log: test.py,v $
# Revision 1.1  2002/08/04 10:23:45  yigal
# Renamed scripts (and broke build)
#
# Revision 1.4  2002/07/19 22:22:53  yigal
# Added support for more types:
# * characters
# * strings
# * symbols
#
# Refactored all type objects to the types module.
# Refactored all scheme functions back to schemefct
#
# Fixed some oversights in string lexing
#
# Revision 1.3  2002/07/07 13:49:26  yigal
# Added true tail-recursion
# * new test in interpretertest.py
# * tree analyzer for marking expressions in tail context
# * call to analyzer in interpreter
# * tailcontext flag in AST
# * trampoline call for tail calls
#
# Made shell more usable
# Added CondClause for new parser
#
# Revision 1.2  2002/07/04 18:44:26  yigal
# Added tests for fraction and boolean
#
# Revision 1.1.1.1  2002/07/03 18:46:34  yigal
# First check-in of Psyche. In its current state, it is able to parse
# all examples described in the first two sections of SICP.
#
#
