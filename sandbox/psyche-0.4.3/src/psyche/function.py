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
Contains the internal representation of a Scheme function.

"""

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.7 $"[11:-2]

import operator

class Function(object):
    """Represents a function as it is stored in the environment"""

    def __init__(self, name, formals, body, environment):
        """Creates a new Function object

        formals - a list of Variable objects denoting the formal
        parameters.
        body - the AST of the body
        environment - the environment within which this function is
        defined.
        """
        self._name = name
        self._formals = [x.name() for x in formals]
        self._body = body
        self._env = environment

    def eval(self, arguments):
        """Evaluate the specified function with the specified
        arguments
        """
        if len(arguments) != len(self._formals):
            raise TypeError("%s takes exactly "
                            "%d arguments (%d given)"
                            % (self._name, len(self._formals),
                               len(arguments))) 
                            
        myEnv = self._env.extend()
        
        for (name, value) in zip(self._formals, arguments):
            myEnv[name] = value

        for cmd in self._body[:-1]:
            cmd.eval(myEnv)

        return self._body[-1].eval(myEnv)

    def __str__(self):
        return "<function '%s'>" % (self._name)

class Trampoline(object):
    """Trampolines are used for implementing tail-recursive calls.

    A tail-recursive call should return a Trampoline, causing Function
    to behave in a tail-recursive fashion.
    """

    def __init__(self, function, args):
        """Returns a trampoline with the specified function and
        arguments.
        """

        self.__function = function
        self.__args = args

    def eval(self):
        """Evaluates the trampoline until it returns a non-trampoline
        object.
        """
        result = self.__evalOne()
        while isinstance(result, Trampoline):
            result = result.__evalOne()

        return result

    def __evalOne(self):
        """Evaluates one step of the trampoline"""
        return self.__function.eval(self.__args)

