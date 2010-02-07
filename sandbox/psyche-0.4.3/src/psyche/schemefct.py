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
A huge set of standard scheme functions, implemented as python
functions.

Since Scheme identifiers can contain more characters than Python
identifiers, some of the Scheme functions had to be renamed. This was
done using the following translation (where X, Y are placeholders)

Scheme Identifier              Python Identifier
X?                             isX
X!                             X
<                              lt
>                              gt
=                              eq
<=                             le
>=                             ge
+                              add
*                              mul
-                              sub
/                              div
X->Y                           xToY

Furthermore, Scheme functions separate their words using '-'; in
Psyche this is done using camelCase; if the resulting python
identifier is reserved or well-known, it is appended with an
underscore.

This explains the following maps:
char-ci>?   --> isCharCiGt
not         --> not_
string-set! --> stringSet

"""

from __future__ import division

import operator
import math
import string

import interpreter
from psyche.types import *
from psyche.function import Function


__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.16 $"[11:-2]

#
# Helper methods
# Methods that make life much easier when implementing functions
#

def integral(x):
    """Returns true if the specified expression is an integer or long
    expression.
    """
    return type(x) is int or type(x) is long

def schemeBool(expr):
    """Returns the boolean value in Scheme associated with the
    specified boolean value in Python.

    For example, schemeBool(None) -> FALSE
    """
    if expr:
        return TRUE
    else:
        return FALSE


def trueExpr(expr):
    """Returns 1 if the specified expression is
    considered true in scheme, 0 otherwise
    """
    if isinstance(expr, Boolean):
        if expr:
            return 1
        else:
            return 0

    return 1


def compose(*args):
    """Returns a function that is the composition of the specified
    functions.
    """

    fcts = list(args)
    fcts.reverse()
    
    def composed(*args):
        result = fcts[0](*args)
        for f in fcts[1:]:
            result = f(result)
        return result

    return composed


#
# R5RS 3.2 Disjointness of Types
#
def __hasClass(o, cls):
    """Returns TRUE if o is an instance of the specified class"""
    return schemeBool(isinstance(o, cls))

def isBoolean(o):
    """(boolean? o)"""
    return __hasClass(o, Boolean)

def isSymbol(o):
    """(symbol? o)"""
    return __hasClass(o, Symbol)

def isChar(o):
    """(char? o)"""
    return __hasClass(o, Character)

def isPair(o):
    """(pair? o)"""
    return __hasClass(o, Pair)

def isNumber(o):
    """(number? o)"""
    return (__hasClass(o, int)
            or __hasClass(o, long)
            or __hasClass(o, Fraction)
            or __hasClass(o, float)
            or __hasClass(o, complex))

def isVector(o):
    """(vector? o)"""
    return __hasClass(o, Vector)

def isProcedure(o):
    """(procedure? o)"""
    return schemeBool(callable(o)) or __hasClass(o, Function)

def isString(o):
    """(string? o)"""
    return __hasClass(o, str) or __hasClass(o, MString)


#
# R5RS 6.1 Equivalence Procedures
#
def isEqv(a, b):
    """(eqv? a b)"""
    if a == TRUE:
        return schemeBool(b == TRUE)

    if a == FALSE:
        return schemeBool(b == FALSE)

    if isSymbol(a):
        return schemeBool(isSymbol(b)
                          and symbolToString(a) == symbolToString(b))

    if isNumber(a):
        return schemeBool(isNumber(b)
                          and a == b)
                # exactness!!!

    if isChar(a):
        return schemeBool(isCharacter(b)
                          and a == b)

    if a is EMPTY_LIST:
        return schemeBool(b is EMPTY_LIST)

    if isPair(a) or isString(a) or isVector(a):
        return schemeBool(a is b)

    if isProcedure(a):
        return schemeBool(a is b)

    
def isEq(a, b):
    """(eq? a b)"""
    return schemeBool(a is b)


def isEqual(a, b):
    """(equal? a b)"""
    return schemeBool(str(a) == str(b))


#
# R5RS 6.2.5 Numbers
#

def eq(*args):
    """(= x y z ...)"""
    return _cmp(operator.eq, args)


def lt(*args):
    """(< x y z ...)"""
    return _cmp(operator.lt, args)

def gt(*args):
    """(> x y z ...)"""
    return _cmp(operator.gt, args)

def le(*args):
    """(<= x y z ...)"""
    return _cmp(operator.le, args)

def ge(*args):
    """(>= x y z ...)"""
    return _cmp(operator.ge, args)


def _cmp(operator, args):
    """Comparison template (CMP x y z ...)"""
    if len(args) <= 1:
        return TRUE

    prev = args[0]
    for i in args[1:]:
        if not operator(prev, i):
            return FALSE
        prev = i
        
    return TRUE

def isZero(x):
    """(zero? x)"""
    return schemeBool(x == 0)

def isPositive(x):
    """(positive? x)"""
    return schemeBool(x > 0)

def isNegative(x):
    """(negative? x)"""
    return schemeBool(x < 0)

def isEven(x):
    """(even? x)"""
    return schemeBool(x % 2 == 0)

def isOdd(x):
    """(odd? x)"""
    return schemeBool(x % 2 != 0)


def add(*args):
    """(+ x y z ...)"""
    return reduce(operator.add, args, 0)


def mul(*args):
    """(* x y z ...)"""
    return reduce(operator.mul, args, 1)


def sub(*args):
    """(- x y z ...)"""
    if len(args) == 0:
        raise ValueError("- requires at least one argument")

    if len(args) == 1:
        return -(args[0])
    
    return reduce(operator.sub, args)


def div(*args):
    """(/ x y z ...)"""
    if len(args) == 0:
        raise ValueError("/ requires at least one argument")

    def div(x, y):
        if integral(x) and integral(y):
            return frac(x, y)
        else:
            return x / y

    if len(args) == 1:
        return div(1, args[0])

    return reduce(div, args)


def remainder(m, n):
    """Returns the remainder of m / n"""
    return m - (n * int(m/n))

def expt(x, y):
    """Exponentation"""
    if (y < 0):
        r = pow(x, abs(y))
        if integral(r):
            return frac(1, r)
        else:
            return 1/r
    else:
        return pow(x, y)

#
# R5RS 6.3.1 Booleans
#

def not_(value):
    """Returns TRUE if value is FALSE, FALSE otherwise"""
    if not trueExpr(value):
        return TRUE
    else:
        return FALSE

#
# R5RS 6.3.2 Pairs and Lists
#

def cons(a, b):
    """(cons a b)"""
    return Pair(a, b)

def car(pair):
    """(car pair)"""
    if isPair(pair):
        return pair.car()
    else:
        raise TypeError("Not a pair: " + pair)

def cdr(pair):
    """(cdr pair)"""
    if isPair(pair):
        return pair.cdr()
    else:
        raise TypeError("Not a pair: " + pair)

def setCar(pair, obj):
    """(set-car! pair obj)"""
    if isPair(pair):
        pair.setCar(obj)
    else:
        raise TypeError("Not a pair: " + pair)

def setCdr(pair, obj):
    """(set-cdr! pair obj)"""
    if isPair(pair):
        pair.setCdr(obj)
    else:
        raise TypeError("Not a pair: " + pair)

def isNull(o):
    """(null? o)"""
    return schemeBool(o is EMPTY_LIST)

def isList(o):
    """(list? l)"""
    if isPair(o):
        return schemeBool(o.isList())
    else:
        return isNull(o)

def list_(*args):
    """(list ...)"""
    if len(args) == 0:
        return EMPTY_LIST

    l = list(args)
    l.append(EMPTY_LIST)
    return pairFromList(l, modifiable = 1, destructive = 1)

def length(l):
    """(length list)"""
    if l is EMPTY_LIST:
        return 0
    
    if not isList(l):
        raise TypeError("Not a proper list")

    return len(l) - 1

def append(*args):
    """(append l1 ...)"""
    result = []

    # first elements should all be lists
    # append their contents
    for l in args[:-1]:     
        if not isList(l):
            raise TypeError("Not a proper list")
        for element in l[:-1]: # ignore empty list at end
            result.append(element)

    # if last element is a list, append that too
    if isList(args[-1]):
        for element in args[-1][:-1]:
            result.append(element)
        return list_(*result)
    # else set the cdr of the list to this object
    else:
        # in case of empty list, just return object
        if result == []:
            return args[-1]

        # otherwise, cdr it
        result = list_(*result)

        current = result
        while current.cdr() is not EMPTY_LIST:
            current = current.cdr()
        current.setCdr(args[-1])
        
        return result
        

def reverse(l):
    """(reverse list)"""
    if not isList(l):
        raise TypeError("Not a proper list")

    if l is EMPTY_LIST:
        return EMPTY_LIST

    result = Pair(l[0], EMPTY_LIST)
    for element in l[1:-1]:
        result = Pair(element, result)
        
    return result

def listTail(l, k):
    """(list-tail list k)"""
    if not isList(l):
        raise TypeError("Not a proper list")

    if k > length(l):
        raise IndexError("Index out of range")

    i = 0
    current = l
    while i < k:
        current = current.cdr()
        i += 1
    return current

def listRef(l, k):
    """(list-ref list k)"""
    if not isList(l):
        raise TypeError("Not a proper list")
    
    return l[k]

def _memX(obj, l, comp):
    """Implements the memq, memv, functions

    comp - the comparison function
    """
    if not isList(l):
        raise TypeError("Not a proper list")
    
    current = l
    while current is not EMPTY_LIST:
        if comp(current.car(), obj):
            return current
        current = current.cdr()
    return FALSE

def memq(obj, l):
    """(memq obj list)"""
    return _memX(obj, l, isEq)

def memv(obj, l):
    """(memv obj list)"""
    return _memX(obj, l, isEqv)

def member(obj, l):
    """(member obj list)"""
    return _memX(obj, l, isEqual)

def _assX(obj, l, comp):
    """Implements the assq, assv, assoc function

    comp - the comparison function
    """
    if not isList(l):
        raise TypeError("Not a proper list")

    current = l
    while current is not EMPTY_LIST:
        pair = current.car()
        if isPair(pair) and comp(pair.car(), obj):
            return pair
        current = current.cdr()
    return FALSE

def assq(obj, l):
    """(assq obj alist)"""
    return _assX(obj, l, isEq)

def assv(obj, l):
    """(assv obj alist)"""
    return _assX(obj, l, isEqv)

def assoc(obj, l):
    """(assoc obj alist)"""
    return _assX(obj, l, isEqual)

#
# R5RS 6.3.3 Symbols
#

def stringToSymbol(s):
    """Returns the Symbol derived from s"""
    if isinstance(s, SymbolString):
        return s.symbol()
    else:
        return Symbol(s, s)

def symbolToString(s):
    """Returns the string associated with s"""
    return SymbolString(str(s), s)

#
# R5RS 6.3.4 Characters
#

def asString(o):
    """Returns the python representation of the psyche character"""
    if not isChar(o):
        raise TypeError("Not a character")

    return o._val


def charToInteger(o):
    """Returns the ordinal of o"""
    return ord(o._val)


def integerToChar(n):
    """Returns the character associated with the specified integer"""
    return Character(chr(n))

def isCharEq(*args):
    return eq(*args)

def isCharLt(*args):
    return lt(*args)

def isCharGt(*args):
    return gt(*args)

def isCharLe(*args):
    return le(*args)

def isCharGe(*args):
    return ge(*args)

def isCharCiEq(*args):
    return eq(*[charDowncase(c) for c in args])

def isCharCiLt(*args):
    return lt(*[charDowncase(c) for c in args])

def isCharCiGt(*args):
    return gt(*[charDowncase(c) for c in args])

def isCharCiLe(*args):
    return le(*[charDowncase(c) for c in args])

def isCharCiGe(*args):
    return ge(*[charDowncase(c) for c in args])

def isCharAlphabetic(char):
    return schemeBool(asString(char) in string.ascii_letters)

def isCharNumeric(char):
    return schemeBool(asString(char) in string.digits)

def isCharWhitespace(char):
    return schemeBool(asString(char) in string.whitespace)

def isCharUpperCase(char):
    return schemeBool(asString(char) in string.ascii_uppercase)

def isCharLowerCase(char):
    return schemeBool(asString(char) in string.ascii_lowercase)

def charUpcase(char):
    return Character(char._val.upper())

def charDowncase(char):
    return Character(char._val.lower())


#
# R5RS 6.3.5 Strings
#

def makeString(k, char=None):
    """(make-string k [char])"""
    if not isinstance(k, int):
        raise TypeError("Not an integer")
    
    if char is None:
        return MString(k * " ")
    else:
        if not isinstance(char, Character):
            raise TypeError("Not a character")
        
        return MString(k * char.pval())

def string_(*args):
    """(string char ...)"""
    return MString("".join([asString(x) for x in args]))

def stringLength(s):
    """(string-length s)"""
    return len(s)

def stringRef(s, k):
    """(string-ref s k)"""
    return Character(s[k])

def stringSet(string, k, char):
    """(string-set! string k char)"""
    string[k] = asString(char)

def isStringEq(*args):
    """(string=? s r ...)"""
    return eq(*args)

def isStringLt(*args):
    """(string<? s r ...)"""
    return lt(*args)

def isStringLe(*args):
    """(string<=? s r ...)"""
    return le(*args)

def isStringGt(*args):
    """(string>? s r ...)"""
    return gt(*args)

def isStringGe(*args):
    """(string>=? s r ...)"""
    return ge(*args)

def isStringCiEq(*args):
    """(string-ci=? s r ...)"""
    return eq(*[s.lower() for s in args])

def isStringCiLt(*args):
    """(string-ci<? s r ...)"""
    return lt(*[s.lower() for s in args])

def isStringCiLe(*args):
    """(string-ci<=? s r ...)"""
    return le(*[s.lower() for s in args])

def isStringCiGt(*args):
    """(string-ci>? s r ...)"""
    return gt(*[s.lower() for s in args])

def isStringCiGe(*args):
    """(string-ci=>? s r ...)"""
    return ge(*[s.lower() for s in args])

def substring(s, start, end):
    """(substring s start end)"""
    if end < start:
        raise IndexError("Endpoint smaller than startpoint")

    if start < 0:
        raise IndexError("Negative startpoint")

    if end > len(s):
        raise IndexError("Endpoint too high")
    
    return MString(s[start:end])

def stringAppend(*strings):
    """(string-append string ...)"""
    return MString("".join(strings))

def stringToList(s):
    """(string->list s)"""
    return list_(*[Character(c) for c in s])

def listToString(l):
    """(list->string l)"""
    chars = [x.pval() for x in l[:-1]]
    return MString("".join(chars))

def stringCopy(s):
    """(string-copy s)"""
    return MString(s)

def stringFill(s, char):
    """(string-fill! s char)"""
    c = char.pval()
    
    for i in range(len(s)):
        s[i] = c


#
# R5RS 6.3.6 Vectors
#
def makeVector(length, fill = 0):
    """(make-vector k)
       (make-vector k fill)
    """
    if not isNumber(length):
        raise TypeError("make-vector expected number")
    
    l = [fill] * length
    return Vector(l, mutable = 1)

def vector(*args):
    """(vector obj ...)"""
    return Vector(args, mutable = 1)

def vectorLength(vector):
    """(vector-length vec)"""
    if not isVector(vector):
        raise TypeError("vector-length expected vector")
    
    return len(vector)

def vectorRef(vector, index):
    """(vector-ref vec k)"""
    if not isVector(vector):
        raise TypeError("vector-ref expected vector")
    
    return vector[index]

def vectorSet(vector, index, element):
    """(vector-set! vec k obj)"""
    if not isVector(vector):
        raise TypeError("vector-set! expected vector")
    
    vector[index] = element

def vectorToList(vector):
    """(vector->list vector)"""
    if not isVector(vector):
        raise TypeError("vector->list expected vector")
    
    return pairFromList(vector.pval())

def listToVector(l):
    """(list->vector list)"""
    if not isList(l):
        raise TypeError("list->vector expected list")
    return Vector(l[:-1])

def vectorFill(vector, fill):
    """(vector-fill vec fill)"""
    if not isVector(vector):
        raise TypeError("vector-fill expected vector")
    for i in range(len(vector)):
        vector[i] = fill

#
# SICP
#

def error(*args):
    """The SICP (error ...) procedure"""
    raise interpreter.SchemeException(" ".join([str(x) for x in args]))



        
# A dictionary containing schemename -> pythonfct bindings
procedures = {
    # 3.2
    'boolean?': isBoolean,
    'symbol?': isSymbol,
    'char?': isChar,
    'vector?': isVector,
    'procedure?': isProcedure,
    'pair?': isPair,
    'number?': isNumber,
    'string?': isString,
    #'port?': isPort,

    # 6.1
    'eqv?': isEqv,
    'eq?': isEq,
    'equal?': isEqual,
    
    # 6.2.5
    '=': eq,
    '>': gt,
    '<': lt,
    '>=': ge,
    '<=': le,
    'zero?': isZero,
    'positive?': isPositive,
    'negative?': isNegative,
    'even?': isEven,
    'odd?': isOdd,
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
    'abs': abs,
    'quotient': operator.floordiv,
    'remainder': remainder,
    'modulo': operator.mod,
    'exp': math.exp,
    'log': math.log,
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan,
    'asin': math.asin,
    'acos': math.acos,
    #'atan': 
    'expt': expt,
    
    # 6.3.1
    'not': not_,

    # 6.3.2
    'cons': cons,
    'car': car,
    'cdr': cdr,
    'set-car!': setCar,
    'set-cdr!': setCdr,
    #
    'null?': isNull,
    'list?': isList,
    'list': list_,
    'length': length,
    'append': append,
    'reverse': reverse,
    'list-tail': listTail,
    'list-ref': listRef,
    'memq': memq,
    'memv': memv,
    'member': member,
    'assq': assq,
    'assv': assv,
    'assoc': assoc,

    # 6.3.3
    'string->symbol': stringToSymbol,
    'symbol->string': symbolToString,
    
    # 6.3.4
    'char=?': isCharEq,
    'char<?': isCharLt,
    'char>?': isCharGt,
    'char<=?': isCharLe,
    'char>=?': isCharGe,
    
    'char-ci=?': isCharCiEq,
    'char-ci<?': isCharCiLt,
    'char-ci>?': isCharCiGt,
    'char-ci<=?': isCharCiLe,
    'char-ci>=?': isCharCiGe,
    
    'char-alphabetic?': isCharAlphabetic,
    'char-numeric?': isCharNumeric,
    'char-whitespace?': isCharWhitespace,
    'char-upper-case?': isCharUpperCase,
    'char-lower-case?': isCharLowerCase,
    
    'char->integer': charToInteger,
    'integer->char': integerToChar,
    
    'char-upcase': charUpcase,
    'char-downcase': charDowncase,
    
    # 6.3.5
    'make-string': makeString,
    'string': string_,
    'string-length': stringLength,
    'string-ref': stringRef,
    'string-set!': stringSet,
    'string=?': isStringEq,
    'string<?': isStringLt,
    'string<=?': isStringLe,
    'string>?': isStringGt,
    'string>=?': isStringGe,
    'string-ci=?': isStringCiEq,
    'string-ci<?': isStringCiLt,
    'string-ci<=?': isStringCiLe,
    'string-ci>?': isStringCiGt,
    'string-ci>=?': isStringCiGe,
    'substring': substring,
    'string-append': stringAppend,
    'string->list': stringToList,
    'list->string': listToString,
    'string-copy': stringCopy,
    'string-fill!': stringFill,

    # 6.3.5
    'make-vector': makeVector,
    'vector': vector,
    'vector-length': vectorLength,
    'vector-ref': vectorRef,
    'vector-set!': vectorSet,
    'vector->list': vectorToList,
    'list->vector': listToVector,
    'vector-fill': vectorFill,
    
    # SICP
    'error': error
    }

