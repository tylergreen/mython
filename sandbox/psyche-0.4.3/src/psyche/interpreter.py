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
The scheme interpreter and shell.

The Shell is an interactive program for accessing the Interpreter.
The Interpreter combines tokenizing, parsing and evaluating into one
class.  

"""

try:
    import readline
except ImportError:
    # no readline support
    pass

import sys
import math
import operator

import lexer
import parser
import analyzers

import schemefct, types


__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.18 $"[11:-2]
RELEASE = "0.4.3"

class UndefinedException(Exception):
    """Raised when an undefined variable is looked up"""

    def __init__(self, name):
        Exception.__init__(self)
        self.__name = name

    def name(self):
        return self.__name

    def __str__(self):
        return "Variable '%s' is undefined" % (self.__name,)
        
class SchemeException(Exception):
    """Exception raised by the (error...) statement"""
    pass


class Environment:
    """The environment (Scheme combination of 'stack frames' and
    namespace)
    """

    def __init__(self, parent = None):
        self.__env = {}
        self.__parent = parent


    def __getitem__(self, index):
        """Returns bindings in the environment"""
        try:
            return self.__env[index]
        except KeyError, e:
            if self.__parent:
                return self.__parent[index]
            else:
                raise UndefinedException(e)


    def __setitem__(self, index, value):
        """Creates a binding in an environment"""
        self.__env[index] = value

    def extend(self):
        """Returns a new environment with this environment as its
        parent.
        """
        return Environment(self)

    def update(self, dictionary):
        """Updates the environment with the bindings in the specified
        dictionary.
        """
        self.__env.update(dictionary)

    def keys(self):
        """Returns the keys in this environment"""
        k = self.__env.keys()
        if self.__parent:
            k += self.__parent.keys()

        return k

    def __str__(self):
        return "%s, %s" % (self.__env, self.__parent)


class SchemeEnvironment5(Environment):
    """The environment as defined by R5RS"""

    def __init__(self):
        Environment.__init__(self)
        self.update(schemefct.procedures)

        
class Interpreter:
    """An interpreter for Scheme expressions.

    The result of an expression changing the environment remains legal
    until the next call to 'reset'. This makes it possible to eval() a
    script line by line.
    """

    USE_TAIL_RECURSION = 1
    """If set to true, the interpreter will use tail recursion"""

    def __init__(self, environment = None):
        """Intializes the interpreter

        environment - the initial environment
        """
        if environment is not None:
            self.__initial = environment
        else:
            self.__initial = SchemeEnvironment5()
        
        self.reset()


    def reset(self):
        """Resets the environment of this interpreter"""
        self.env = self.__initial.extend()


    def environment(self):
        """Returns the environment of the interpreter"""
        return self.env


    def eval(self, text):
        """Evaluates the specified text within this interpreter's
        environment.

        line - a string
        """
        tokens = lexer.tokenize(text)
        if not tokens:
            return None
        
        tree = parser.parse(tokens)

        if self.USE_TAIL_RECURSION:
            analyzers.markTailContexts(tree)

        return tree.eval(self.env)
        



class Shell:
    """An interactive interpreter for Scheme expressions."""

    KEYWORDS = ["quote", "lambda", "if", "set!", "begin", "cond",
                "and", "or", "case", "let", "let*", "letrec", "do",
                "delay", "quasi-quote", "else", "=>", "define", "unquote",
                "unquote-splicing"]

    def __init__(self):
        self.interpreter = Interpreter()

        try:
            readline.parse_and_bind("tab: complete")
            readline.set_completer(self.complete)
        except NameError:
            # no readline support
            pass

    def scheme_input(self):
        """Reads lines from stdin until a complete expression is read.
        """
        line = raw_input("\npsyche> ") + "\n"
        
        if not line:
            raise EOFError

        # repeat until closing brackets match
        while line.count("(") > line.count(")"):
            line2 = raw_input("......> ") + "\n"
            if not line2:
                raise EOFError
            line += line2

        return line

    def complete(self, text, state):
        """Completes the specified text"""
        possible = [k
                    for k in (self.interpreter.environment().keys() +
                              self.KEYWORDS) 
                    if k.startswith(text)]
        try:
            return possible[state]
        except IndexError:
            return None
        

    def printHeader(self):

        release = "$Name:  $"
        sys.stdout.write(

"""Psyche version %s, Copyright (C) 2002 Y. Duppen

Psyche comes with ABSOLUTELY NO WARRANTY.  This is free software, and
you are welcome to redistribute it under certain conditions; read the
attached COPYING for details.
""" % (RELEASE,))



    def run(self):
        """The read, eval, print loop
        """
        self.printHeader()
        
        while 1:
            try:
                line = self.scheme_input()
            except EOFError:
                sys.stdout.write('\n')
                break
            except KeyboardInterrupt:
                sys.stdout.write('\n^C\n')
                continue

            if not line:
                continue

            if line == "(quit)":
                break

            try:
                result = self.interpreter.eval(line)
            except KeyboardInterrupt:
                result = "^C"
            except Exception, e:
                result = self.getExceptionMessage(e)

            if result is not None:
                sys.stdout.write(str(result))
                sys.stdout.write('\n')


    def getExceptionMessage(self, exception):
        """Ensures that the error message is correct"""
        if isinstance(exception, ZeroDivisionError):
            return "Division by zero"

        return str(exception)


def run_shell():
    s = Shell()
    s.run()
