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
Contains the AST (Abstract Syntax Tree) nodes instantiated by the
Parser.

"""

import operator
import types

from schemefct import trueExpr
from types import TRUE, FALSE
from function import Function, Trampoline

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.17 $"[11:-2]


class _AST(object):
    """Abstract definition of ASTs"""

    inTailContext = 0
    """If this property is set to true, the object is in a tail
    context"""

    def __init__(self):
        """Intializes the AST

        args - the names of the variables used for comparison and
        representations.
        """
        self.type = self.__class__.__name__ # used by analyzers

    def __eq__(self, other):
        """Returns true if the other object has the same class, the
        same variables and the same values for those variables.
        """
        
        try:
             if self.__class__ != other.__class__:
                 return 0

             for s in self.__slots__:
                 if getattr(self, s) != getattr(other, s):
                     return 0
             return 1
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        return not (self == other)

    def __repr__(self):
        """Returns a constructor with the named arguments"""
        name = self.__class__.__name__
        argreprs = [repr(getattr(self, v)) for v in self.__slots__]
        
        return "psyche.ast.%s(%s)" % (name, ", ".join(argreprs))

    def __getitem__(self, i):
        """Returns the ith child object, using the arguments passed in
        the constructor.

        If one of the children is a sequence, __getitem__ recurses.
        """
        return self.__flattened()[i]

    def __flattened(self):
        """Returns a flattened list of all the arguments passed in the
        constructor.
        """
        result = []
        for v in self.__slots__:
            var = getattr(self, v)
            if type(var) is list or type(var) is tuple:
                result += var
            else:
                result.append(var)
        return result

    def evalSeq(self, sequence, environment):
        """Evaluates a sequence of ASTs"""
        for expr in sequence[:-1]:
            expr.eval(environment)
        return sequence[-1].eval(environment)

    def eval(self, environment):
        raise NotImplementedError(self.__class__.__name__)


class Number(_AST):
    """Represents a single number in any radix"""

    __slots__ = ["_val"]

    def __init__(self, stringValue):
        """Intializes the number

        value - the string representation of the number
        """
        assert type(stringValue) == type("")
        _AST.__init__(self)

        self._val = stringValue


    def eval(self, environment = None):
        """Returns the Python representation of the number

        environment - only here for API purposes, unused for
        evaluating numbers.
        """

        # Real?
        if "." in self._val:
            return float(self._val)

        # Integer!

        # It is assumed small numbers will occur more often than long
        # numbers, so using exceptions is acceptable.
        try:
            return int(self._val)
        except ValueError:
            return long(self._val)


class Boolean(_AST):
    """Represents a boolean.

    Note: the AST Boolean should not be confused with the scheme type
    Boolean. XXX: Naming???
    """

    __slots__ = ["_val"]

    def __init__(self, value):
        _AST.__init__(self)
        self._val = value

    def eval(self, environment = None):
        """Returns the scheme type Boolean representing the AST"""
        return types.Boolean(self._val)


class String(_AST):
    """Represents a string"""

    __slots__ = ["_val"]

    def __init__(self, value):
        _AST.__init__(self)
        self._val = value

    def eval(self, environment = None):
        """Returns the string representing the AST"""
        return (self._val[1:-1]
                .replace('\\"', '"')
                .replace("\\\\", "\\"))


class Character(_AST):
    """Represents a character"""

    __slots__ = ["_val"]

    def __init__(self, value):
        _AST.__init__(self)
        self._val = value

    def eval(self, environment = None):
        """Returns the character representing the AST"""
        return types.Character(self._val)


class Variable(_AST):
    """Represents a variable"""

    __slots__ = ["_name"]

    def __init__(self, name):
        """Initializes the variable"""
        _AST.__init__(self)
        self._name = name

    def eval(self, environment):
        """Evaluates the variable within the environment"""
        return environment[self._name]

    def name(self):
        """Returns the name of this variable"""
        return self._name

    def __str__(self):
        return self._name


class Symbol(_AST):
    """Represents a constant symbol"""

    __slots__ = ["_name"]

    def __init__(self, name):
        """Intializes the constant symbol"""
        _AST.__init__(self)
        self._name = name

    def eval(self, environment):
        """Evaluates the symbol"""
        return types.Symbol(self._name)

    def name(self):
        """Returns the name of the symbol"""
        return self._name


class List(_AST):
    """Represents a list datum"""

    __slots__ = ["_elements", "_end"]

    def __init__(self, elements = None, end = None):
        _AST.__init__(self)
        self._elements = elements
        self._end = end

    def eval(self, environment):
        # empty
        if not self._elements:
            return types.EMPTY_LIST

        elements = [e.eval(environment) for e in self._elements]

        if self._end is None:
            end = types.EMPTY_LIST
        else:
            end = self._end.eval(environment)
        elements.append(end)
        
        return types.pairFromList(elements, destructive = 1)

class Vector(_AST):
    """Represents a Vector datum"""

    __slots__ = ["_elements"]

    def __init__(self, elements = []):
        _AST.__init__(self)
        self._elements = elements

    def eval(self, environment):
        elements = [e.eval(environment) for e in self._elements]
        return types.Vector(elements, mutable=0)

class Program(_AST):
    """Represents a program"""

    __slots__ = ["_commands"]

    def __init__(self, commands):
        _AST.__init__(self)
        self._commands = commands

    def eval(self, environment):
        result = None
        
        for cmd in self._commands:
            result = cmd.eval(environment)

        return result

class Application(_AST):
    """Represents an application"""

    __slots__ = ["_op", "_args"]

    def __init__(self, operand, argumentList):
        _AST.__init__(self)
        self._op = operand
        self._args = argumentList


    def eval(self, environment):
        """Evaluates the expression within the specified
        environment"""
        args = [a.eval(environment) for a in self._args]
        operand = self._op.eval(environment)

        return self.__apply(operand, args)


    def __apply(self, operand, args):
        """Applies the specified function to the specified
        arguments.

        Non-primitive functions in tail context return a trampoline. 
        """

        if (self.__isPrimitive(operand)):
            return apply(operand, args)

        if self.inTailContext:
            return Trampoline(operand, args)

        result = operand.eval(args)
        if isinstance(result, Trampoline):
            result = result.eval()
        return result


    def __isPrimitive(self, operand):
        """Returns true if the specified operand is a primitive python
        callable.
        """
        return callable(operand)
        
    def __str__(self):
        return "(%s %s)" % (self._op,
                            " ".join([str(x) for x in self._args]))


class Definition(_AST):
    """Represents a name definition"""

    __slots__ = ["_var", "_expr"]

    def __init__(self, variable, expression):
        _AST.__init__(self)
        self._var = variable
        self._expr = expression


    def eval(self, environment):
        name = self._var.name()
        value = self._expr.eval(environment)

        environment[name] = value
        
class ProcDefinition(_AST):
    """Represents a procedure definition"""

    __slots__ = ["_var", "_formals", "_body"]

    def __init__(self, variable, formals, body):
        _AST.__init__(self)
        self._var = variable
        self._formals = formals
        self._body = body

    def eval(self, environment):
        name = self._var.name()
        fct = Function(name, self._formals, self._body, environment)

        environment[name] = fct

    def body(self):
        """Returns the AST that forms the body"""
        return self._body

    def formals(self):
        """Returns a list of formal variables"""
        return self._formals


class Lambda(_AST):
    """Represents a lambda expression"""

    __slots__ = ["_formals", "_body"]

    def __init__(self, formals, body):
        _AST.__init__(self)
        self._formals = formals
        self._body = body

    def eval(self, environment):
        return Function("lambda expression", self._formals,
                        self._body, environment) 

    def body(self):
        return self._body

    def formals(self):
        return self._formals


class CondClause(_AST):
    """Represents a non-else clause in a (cond) expression"""

    __slots__ = ["_test", "_sequence"]

    def __init__(self, test, sequence):
        """Initializes the clause

        test - the test expression
        sequence - the sequence following the clause (list of
        expressions)
        """
        _AST.__init__(self)
        self._test = test
        self._sequence = sequence

    def test(self):
        return self._test

    def sequence(self):
        return self._sequence

    def evalTest(self, environment):
        """Evaluates the test and returns true if the test evaluates
        to true.
        """
        return trueExpr(self._test.eval(environment))

    def eval(self, environment):
        """Evaluates the sequence; should only be called if evalTest
        returns true.
        """
        return self.evalSeq(self._sequence, environment)


class Cond(_AST):
    """Represents a (cond) expression"""

    __slots__ = ["_clauses", "_else"]

    def __init__(self, clauses, elseSeq):
        """Initializes the cond expression

        clauses - a list of flattened test, sequence pairs
        elseSeq - the else sequence
        """
        _AST.__init__(self)
        self._clauses = clauses
        self._else = elseSeq

    def eval(self, environment):
        for clause in self._clauses:
            if (clause.evalTest(environment)):
                return clause.eval(environment)
            
        if self._else:
            return self.evalSeq(self._else, environment)

        return None

    def clauses(self):
        """Returns a list of all clauses.

        Returns the empty list if there are no clauses
        """

        return self._clauses


    def elseSequence(self):
        """Returns the else sequence, or the empty list"""
        return self._else
        
        
        

class If(_AST):
    """Represents a conditional"""

    __slots__ = ["_test", "_cons", "_alt"]

    def __init__(self, test, consequent, alternate):
        _AST.__init__(self)
        self._test = test
        self._cons = consequent
        self._alt = alternate

    def eval(self, environment):
        if trueExpr(self._test.eval(environment)):
            return self._cons.eval(environment)
        else:
            if self._alt:
                return self._alt.eval(environment)
            else:
                return None

    def test(self):
        """Returns the test expression"""
        return self._test

    def consequent(self):
        """Returns the consequent"""
        return self._cons

    def alternate(self):
        """Returns the alternate"""
        return self._alt

class And(_AST):
    """Represents (and...)"""

    __slots__ = ["_tests"]

    def __init__(self, tests):
        _AST.__init__(self)
        self._tests = tests

    def eval(self, environment):
        if not self._tests:
            return TRUE
        
        for test in self._tests[:-1]:
            value = test.eval(environment)
            if not trueExpr(value):
                return value
        return self._tests[-1].eval(environment)

    def tests(self):
        """Return a list of expressions"""
        return self._tests
        

class Or(_AST):
    """Represents (or...)"""

    __slots__ = ["_tests"]
    
    def __init__(self, tests):
        _AST.__init__(self)
        self._tests = tests

    def eval(self, environment):
        if not self._tests:
            return FALSE
        
        for test in self._tests[:-1]:
            value = test.eval(environment)
            if trueExpr(value):
                return value
        return self._tests[-1].eval(environment)

    def tests(self):
        """Returns the list of expressions"""
        return self._tests

