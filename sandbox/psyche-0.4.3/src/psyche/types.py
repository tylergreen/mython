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
This file contains the Python equivalent of Scheme types that cannot
be converted to native Python types.

Boolean
Character
Fraction (fractional numbers)
MString (mutable strings)
Pair (pairs and lists)
Symbol
Vector 
"""

from __future__ import generators

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.9 $"[11:-2]

import string
from weakref import WeakValueDictionary
import UserString


def _gcd(a, b):
    """Returns the greatest common divisor of a and b"""
    while b != 0: a, b = b, a%b
    return a


class Fraction(object):
    """Represents a fraction as a number object in Python2.2"""

    def __init__(self, numerator, denominator):
        """Creates a new Fraction numerator/denominator

        numerator - an integral number
        denominator - an integral number
        """
        # check types and denominator
        numType = type(numerator)
        denType = type(denominator)
        if numType is not int and numType is not long:
            raise ValueError("Numerator must be int or long, not %s"
                             % (numType,))
        if denType is not int and denType is not long:
            raise ValueError("Denominator must be int or long, not %s"
                             % (denType,))

        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be 0")

        # normalize values
        gcd = _gcd(numerator, denominator)
        
        self.__num = numerator/gcd
        self.__den = denominator/gcd


    def __lt__(self, other):
        """a/b < c/d iff a*d < c*b"""
        self, other = coerce(self, other)
        
        if isinstance(other, Fraction):
            return ((self.__num * other.__den)
                    < (self.__den * other.__num))
        else:
            return type(other)(self) < other


    def __eq__(self, other):
        """Two fractions are equal if their normalized values are
        equal.
        """
        self, other = coerce(self, other)

        if isinstance(self, Fraction):
            return ((self.__num == other.__num)
                    and (self.__den == other.__den))
        else:
            return type(other)(self) == other

    def __ne__(self, other):
        return not (self == other)

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        return not(self < other) and not(self == other)

    def __ge__(self, other):
        return not(self < other)


    def __add__(self, other):
        self, other = coerce(self, other)

        if isinstance(other, Fraction):
            num = self.__num * other.__den + self.__den * other.__num
            den = self.__den * other.__den
            return frac(num, den)
        else:
            return self + other

    def __sub__(self, other):
        self, other = coerce(self, other)

        if isinstance(other, Fraction):
            num = self.__num * other.__den - self.__den * other.__num
            den = self.__den * other.__den
            return frac(num, den)
        else:
            return self - other

    def __mul__(self, other):
        self, other = coerce(self, other)

        if isinstance(other, Fraction):
            return frac(self.__num * other.__num,
                        self.__den * other.__den)
        else:
            return self * other

    def __div__(self, other):
        self, other = coerce(self, other)

        if isinstance(other, Fraction):
            return frac(self.__num * other.__den,
                        self.__den * other.__num)
        else:
            return self.__div__(other)

    def __pow__(self, other):
        if type(other) is not int:
            raise TypeError("Cannot raise to arbitrary power")
        
        num = self.__num ** other
        den = self.__den ** other
        return frac(num, den)

    def __rsub__(self, other):
        return -(self) + other

    def __rdiv__(self, other):
        return frac(self.__den, self.__num) * other
        
    __radd__ = __add__
    __rmul__ = __mul__
    __rtruediv__ = __rdiv__
    __rpow__ = __pow__
    __truediv__ = __div__


    def __neg__(self):
        return frac(-self.__num, self.__den)

    def __pos__(self):
        return frac(self.__num, self.__den)

    def __invert__(self):
        return frac(self.__den, self.__num)

    def __abs__(self):
        return frac(abs(self.__num), abs(self.__den))

    def __float__(self):
        return float(self.__num) / self.__den

    def __complex__(self):
        return complex(float(self))

    def __int__(self):
        return self.__num / self.__den

    def __long__(self):
        return self.__num / self.__den

    def __coerce__(self, other):
        if type(other) is int:
            return (self, frac(other, 1))

        if type(other) is long:
            return (self, frac(other, 1))

        if type(other) is type(self):
            return (self, other)

        return (type(other)(self), other)

    def __nonzero__(self):
        return self.__num

    def __hash__(self):
        return self.__num

    def __str__(self):
        if self.__den == 1:
            return str(self.__num)
        else:
            return "%d/%d" % (self.__num, self.__den)

    def __repr__(self):
        return "frac(%d,%d)" % (self.__num, self.__den)



def frac(*args):
    """Returns a new Fraction object

    frac(string) -> Fraction
    frac(int, int) -> Fraction
    """

    if len(args) == 1:
        raise NotImplementedError("String conversion not "
                                  "yet implemented")
    elif len(args) == 2:
        return Fraction(args[0], args[1])

    else:
        raise ValueError("Cannot convert %s to Fraction"
                         % (args,))



class Boolean(object):
    """Represents a Scheme boolean"""

    def __init__(self, value):
        """Creates a new Boolean object

        value - the boolean s-expression
        """
        if value == "#f":
            self.__val = 0
        else:
            self.__val = 1


    def __nonzero__(self):
        """Ensures that only #f is false in Python context """
        return self.__val


    def __eq__(self, other):
        return (self.__class__ == other.__class__
                and self.__val == other.__val)

    def __ne__(self, other):
        return not(self == other)


    def __str__(self):
        """Returns the s-expression"""
        if (self.__val):
            return "#t"
        else:
            return "#f"

    def __repr__(self):
        return "Boolean('%s')" % (str(self), )
    

TRUE = Boolean("#t")
"""Universal constant for #t"""

FALSE = Boolean("#f")
"""Universal constant for #f"""


class _Infinite(object):
    def __str__(self):
        return "..."

_INFINITE = _Infinite()


def pairFromList(seq, modifiable = 0, destructive = 0):
    """Creates a new pair from a list

    seq - the sequence to convert to nested pairs
    modifiable - if true, the resulting list will be modifiable
    destructive - if true, seq will not be copied but modified
    """
    if isinstance(seq, tuple):
        l = list(seq)
    elif destructive:
        l = seq[:]
    else:
        l = seq

    if len(seq) == 1:
        raise TypeError("Cannot create pair with one element")

    if len(seq) == 2:
        return Pair(seq[0], seq[1], modifiable)

    l.reverse()
    result = Pair(l[1], l[0], modifiable)
    for el in l[2:]:
        result = Pair(el, result, modifiable)
    return result
    

class Pair(object):
    """The Scheme pair type

    Non-modifiable pairs support car(), cdr() and __getitem__(); the
    latter functions as if the pairs were flattened.
    Modifiable pairs also support setCar() and setCdr().
    Pairs that are propert list dub as Python sequences.
    """

    __slots__ = ["_car", "_cdr", "_modifiable"]

    def __init__(self, car, cdr, modifiable = 0):
        """Creates a new pair

        car - the first element
        cdr - the second element
        constant - if true, this pair cannot be modified
        """
        self._modifiable = 1
        self.setCar(car)
        self.setCdr(cdr)
        self._modifiable = modifiable

    def setCar(self, car):
        self._checkModify()
        self._car = car

    def car(self):
        return self._car

    def setCdr(self, cdr):
        self._checkModify()
        
        if isinstance(cdr, Pair):
            self._cdr = cdr
        else:
            self._cdr = (cdr,)

    def cdr(self):
        if isinstance(self._cdr, tuple):
            return self._cdr[0]
        else:
            return self._cdr

    def _checkModify(self):
        """Raises a type error if this pair is not modifiable"""
        if not self._modifiable:
            raise TypeError("Pair not modifiable")

    def __normalizeIndex(self, i):
        if i < 0:
            return len(self) - abs(i)
        else:
            return i

    def __getitem__(self, i):
        """Returns the ith item or slice

        i - an integer or a slice
        returns the ith object if i is an integer, or a python *list*
        containing the elements of the slice
        """
        if type(i) is type(slice(1)):
            # get slice
            if i.start:
                start = self.__normalizeIndex(i.start)
            else:
                start = 0
            stop = self.__normalizeIndex(i.stop)
            if i.step:
                step = i.step
            else:
                step = 1

            result = []
            index = 0
            for el in self:
                if start <= index < stop:
                    result.append(el)
                index += step
            return result
        
        else:
            # get element
            i = self.__normalizeIndex(i)
        
            j = 0
            for el in self:
                if i == j:
                    return el
                j += 1
            raise IndexError("list index out of range: %s" % (i,))
            
    def __len__(self):
        len = 0
        for i in self:
            len += 1
        return len

    def __iter__(self):
        """Returns a generator that iterates over this pair, cdring
        down the list.

        The generator yields _INFINITE when it encounters a cycle
        """
        seen = [self]

        def haveSeen(pair):
            for i in seen:
                if i is pair:
                    return 1
            return 0
        
        cur = self
        cdr = cur.cdr()
        
        while isinstance(cdr, Pair):
            yield cur.car()
            cur = cdr
            cdr = cur.cdr()
            if haveSeen(cdr):
                yield _INFINITE
                return
            seen.append(cur)
        else:
            yield cur.car()
            
        yield cur.cdr()
        return

    def __eq__(self, other):
        while isinstance(self, Pair):
            if not isinstance(other, Pair):
                return 0

            if self.car() != other.car():
                return 0

            self, other = self.cdr(), other.cdr()

        return self == other

    def __ne__(self, other):
        return not (self == other)

    def isList(self):
        return self[-1] is EMPTY_LIST

    def __str__(self):
        strs = [str(e) for e in self]

        if self.isList():
            return "(%s)" % (" ".join(strs[:-1]),)
        else:
            return "(%s . %s)" % (" ".join(strs[:-1]), strs[-1])

    def __repr__(self):
        return "Pair(%s, %s)" % (`self.car()`, `self.cdr()`)
    

EMPTY_LIST = ()





class Symbol(object):
    """
    The Scheme symbol type

    There are two kinds of symbols: constant symbols and symbols
    obtained from string->symbol. The former use the flyweight
    pattern, assuring that equality can be done using 'is'. The latter
    are always constructed with an extra fromString field, indicating
    where they came from.

    The names of symbols are immediately lowercased
    """

    __symbols__ = WeakValueDictionary()

    def __new__(cls, name, fromString = None):
        name = name.lower()
        
        # only flyweight constants
        if fromString is not None:
            return object.__new__(cls)

        # check in pool
        sym = cls.__symbols__.get(name)
        if sym is not None:
            return sym

        # create new one
        sym = object.__new__(cls)
        cls.__symbols__[name] = sym
        return sym

    def __init__(self, name, fromString = None):
        self.name = name.lower()
        self.fromString = fromString

    def __str__(self):
        if self.fromString is not None:
            return "%s" % (self.fromString,)
        else:
            return "%s" % (self.name,)

    def __repr__(self):
        if self.fromString is not None:
            return "Symbol(%s, %s)" % (self.name, self.fromString)
        else:
            return "Symbol(%s)" % (self.name,)

    def __eq__(self, other):
        if self is other:
            return 1

        if isinstance(other, Symbol):
            return (self.name == other.name
                    and self.fromString == other.fromString)

        return NotImplemented

    def __ne__(self, other):
        return not(self == other)


class Character(object):
    """
    The Character type in Scheme.
    """
    
    __slots__ = ["_val"]

    def __init__(self, value):
        """Initializes the Character

        value - an s-expression or a python one-character string
        """
        if len(value) == 1:
            self._val = value
        elif len(value) == 3:
            self._val = value[-1]
        elif value.lower() == r"#\space":
            self._val = " "
        elif value.lower() == r"#\newline":
            self._val = "\n"
        else:
            raise TypeError("Not a legal character: %s" % (value,))

    def __str__(self):
        """Returns the s-expression represented by this object"""
        return r"#\%s" % (self._val,)

    def __repr__(self):
        return 'Character("%s")' % (self._val,)

    def __eq__(self, other):
        """Returns true if the other object is also a Character with
        the same value.
        """
        return (isinstance(other, Character)
                and self._val == other._val)

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        if isinstance(other, Character):
            return ord(self._val) < ord(other._val)
        else:
            return NotImplemented

    def __le__(self, other):
        return (self < other) or (self == other)

    def __ge__(self, other):
        return not (self < other)

    def __gt__(self, other):
        return not (self < other) or (self == other)

    def pval(self):
        """Returns the python equivalent of this class"""
        return self._val


def char(ch):
    return Character(ch)


class SymbolString(str):
    """String returned by the scheme function symbol->string

    """

    def __new__(cls, value, symbol):
        return str.__new__(cls, value)

    def __init__(self, value, symbol):
        """Initializes the string
     
        value - the string value
        symbol - the associated symbol
        """
        str.__init__(self, value)
        self._symbol = symbol

    def symbol(self):
        return self._symbol
        

class MString(UserString.MutableString):
    """Mutable string"""
    
    pass




class Vector(object):
    """A sequence object representing Vectors"""


    def __init__(self, elements, mutable = 1):
        """Creates a new vector

        elements - a list containing the initial elements of the vector
        mutable - if true, the vector can be modified
        """
        self.__elements = list(elements)
        self.__mutable = mutable

    def __getitem__(self, index):
        return self.__elements[index]

    def __setitem__(self, index, value):
        if self.__mutable:
            self.__elements[index] = value
        else:
            raise TypeError("Not a mutable vector")

    def __len__(self):
        return len(self.__elements)

    def __iter__(self):
        for el in self.__elements:
            yield el

    def pval(self):
        """Returns the Python equivalent of this class"""
        return self.__elements


    def __str__(self):
        """Returns the external representation of this class"""
        elements = [str(el) for el in self.__elements]
        return "#(%s)" % (" ".join(elements),)

    def __repr__(self):
        elements = [repr(el) for el in self.__elements]
        return "Vector([%s])" % (", ".join(elements),)


    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        return self.__elements == other.__elements

    def __ne__(self, other):
        return not (self == other)


