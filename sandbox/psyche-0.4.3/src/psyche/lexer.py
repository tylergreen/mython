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
Contains a lexer and Token definitions for scheme expressions and
programs. 
"""

import string
from StringIO import StringIO
from Plex import *

__author__ = "yduppen@xs4all.nl"
__version__ = "$Revision: 1.9 $"[11:-2]

class LexerException(Exception):
    """Raised when the lexer encounters an error"""
    pass


class Token:
    """A token"""

    START = "("
    """The start delimiters and  '(' '#(' """

    STOP = ")"
    """The stop delimiter ')'"""

    NUM = "number"
    """The numeral type"""

    BOOLEAN = "boolean"
    """The boolean type"""

    CHAR = "character"
    """The character type"""

    STRING = "string"
    """The string type"""

    COMMENT = "comment"
    """The comment type"""

    VARIABLE = "variable"
    """The variable type"""

    SYNTACTIC = "syntactic_keyword"
    """The syntactic keyword type"""

    PUNCT = "punctuation"
    """Punctuation such as quote and unquote"""


    def __init__(self, type, value=None, name=None, line=0, col=0):
        """Creates a new Token

        type - one of the Token types
        value - the value of the token; optional
        name - the name of the original input
        line - this token's line number in the input
        col - the column of this token's starting point in the input
        """
        assert type, "No type given"
        assert value, "No value given"
        
        self.__type = type

        if value is None:
            self.__value = None
        else:
            self.__value = str(value)

        self.__input = name
        self.__line = line
        self.__col = col

    def value(self):
        """Returns the value of this token or None if there is no
        value associated
        """
        return self.__value

    def type(self):
        """Returns the type of this token"""
        return self.__type

    def input_name(self):
        """Returns the name of the input"""
        return self.__input

    def line_no(self):
        """Returns the line number of this token in the input"""
        return self.__line

    def col_no(self):
        """Returns the column number of this token in the input"""
        return self.__col

    def same_line(self, token):
        """Returns true if both tokens are on the same line"""
        return self.__line == token.__line

    def __len__(self):
        """Returns the length of this token's value"""
        return len(self.__value)

    def __cmp__(self, other):
        """Orders the tokens, first by their type and then by their
        value.

        If other is a string, only the type is compared; if other is a
        string starting and ending with '__', the value is compared

        This weird __cmp__ function is used to cater for the
        peculiarities of the parser which
        a) compares its non-terminal strings against Tokens and
        b) does not support non-token terminals (hence the __ form)
        """

        # Token comparison
        if (isinstance(other, Token)):
            if (self.type() == other.type()):
                return cmp(self.value(), other.value())
            else:
                return cmp(self.type(), other.type())

        # String comparison
        elif type(other) is type(""):
            # Literals
            if other[:2] == "__" and other[-2:] == "__":
                return cmp(self.value(), other[2:-2])

            # Tokens
            return cmp(self.type(), other)

        else:
            return NotImplemented


    def __hash__(self):
        """Returns the hash of this token"""
        return hash(self.type()) ^ hash(self.value())

    def __repr__(self):
        return "Token(%s, %s)" % (self.type(), self.value())

    def __str__(self):
        return self.value()


whitespace = Any(string.whitespace)
comment = Str(";") + Rep(AnyChar) + Eol

boolean = Str("#t", "#f")

letter = Any(string.letters)
digit = Any(string.digits)
special_initial = Any("!$%&*/:<=>?^_~")
special_subsequent = Any("+-.@")
peculiar = Str("+", "-", "...")

initial = letter | special_initial
subsequent = initial | digit | special_subsequent

identifier = (initial + Rep(subsequent)) | peculiar

expression_keyword = Str("quote", "lambda", "if",
                         "set!", "begin", "cond", "and", "or",
                         "case", "let", "let*", "letrec", "do",
                         "delay", "quasiquote")
syntactic = expression_keyword | Str("else", "=>", "define",
                                     "unquote", "unquote-splicing")

character_name = NoCase(Str(r"#\space", r"#\newline"))
character = (Str("#\\") + Any(string.printable)) | character_name

escaped_quote = Str('\\"')
escaped_backslash = Str('\\\\')

string_element = AnyBut('"\\') | escaped_quote | escaped_backslash
a_string = Str('"') + Rep(string_element) + Str('"')


digit2 = Any("01")
digit8 = Any("01234567")
digit10 = Any(string.digits)
digit16 = Any(string.hexdigits)

radix2 = Str("#b")
radix8 = Str("#o")
radix10 = Empty | Str("#d")
radix16 = Str("#x")

exactness = Empty | Str("#i", "#e")
sign = Empty | Any("+-")
exponent_marker = Any("esfdl")
suffix = Empty | (exponent_marker + sign + Rep1(digit10))


prefix2 = (radix2 + exactness) | (exactness + radix2)
uinteger2 = Rep1(digit2) + Rep(Str("#"))
ureal2 = (uinteger2
          | (uinteger2 + Str("/") + uinteger2))
real2 = sign + ureal2
complex2 = (real2
            | (real2 + Str("@") + real2)
            | (real2 + Str("+") + ureal2 + Str("i"))
            | (real2 + Str("-") + ureal2 + Str("i"))
            | (real2 + Str("+") + Str("i"))
            | (real2 + Str("-") + Str("i"))
            | (Str("+") + ureal2 + Str("i"))
            | (Str("-") + ureal2 + Str("i"))
            | Str("+i")
            | Str("-i"))
num2 = prefix2 + complex2

prefix8 = (radix8 + exactness) | (exactness + radix8)
uinteger8 = Rep1(digit8) + Rep(Str("#"))
ureal8 = (uinteger8
          | (uinteger8 + Str("/") + uinteger8))
real8 = sign + ureal8
complex8 = (real8
            | (real8 + Str("@") + real8)
            | (real8 + Str("+") + ureal8 + Str("i"))
            | (real8 + Str("-") + ureal8 + Str("i"))
            | (real8 + Str("+") + Str("i"))
            | (real8 + Str("-") + Str("i"))
            | (Str("+") + ureal8 + Str("i"))
            | (Str("-") + ureal8 + Str("i"))
            | Str("+i")
            | Str("-i"))
num8 = prefix8 + complex8

prefix10 = (radix10 + exactness) | (exactness + radix10)
uinteger10 = Rep1(digit10) + Rep(Str("#"))
decimal10 = ((uinteger10 + suffix)
             | (Str(".") + Rep1(digit10) + Rep(Str("#")) + suffix)
             | (Rep1(digit10) + Str(".") + Rep(digit10) +
                Rep(Str("#")) + suffix)
             | (Rep1(digit10) + Rep1(Str("#")) + Str(".") + Rep(Str("#")) +
                suffix)) 
ureal10 = (uinteger10
          | (uinteger10 + Str("/") + uinteger10)
          | decimal10)
real10 = sign + ureal10
complex10 = (real10
            | (real10 + Str("@") + real10)
            | (real10 + Str("+") + ureal10 + Str("i"))
            | (real10 + Str("-") + ureal10 + Str("i"))
            | (real10 + Str("+") + Str("i"))
            | (real10 + Str("-") + Str("i"))
            | (Str("+") + ureal10 + Str("i"))
            | (Str("-") + ureal10 + Str("i"))
            | Str("+i")
            | Str("-i"))
num10 = prefix10 + complex10

prefix16 = (radix16 + exactness) | (exactness + radix16)
uinteger16 = Rep1(digit16) + Rep(Str("#"))
ureal16 = (uinteger16
          | (uinteger16 + Str("/") + uinteger16))
real16 = sign + ureal16
complex16 = (real16
            | (real16 + Str("@") + real16)
            | (real16 + Str("+") + ureal16 + Str("i"))
            | (real16 + Str("-") + ureal16 + Str("i"))
            | (real16 + Str("+") + Str("i"))
            | (real16 + Str("-") + Str("i"))
            | (Str("+") + ureal16 + Str("i"))
            | (Str("-") + ureal16 + Str("i"))
            | Str("+i")
            | Str("-i"))
num16 = prefix16 + complex16

number = num2 | num8 | num10 | num16

punct = Str("'", "`", ",", ",@", ".", "#(")



# The lexicon
lexicon = Lexicon([
    (whitespace,        IGNORE),
    (Str("(", "#("),    Token.START),
    (Str(")"),          Token.STOP),
    (comment,           IGNORE),
    (syntactic,         Token.SYNTACTIC),
    (identifier,        Token.VARIABLE),
    (number,            Token.NUM),
    (boolean,           Token.BOOLEAN),
    (character,         Token.CHAR),
    (a_string,          Token.STRING),
    (punct,             Token.PUNCT)
    ])


class _Lexer:
    """The Lexer lies on top of an input stream. Using the nextToken
    method or the xtokens() generator, Token objects can be obtained.

    The Lexer is private; this makes it possible to change the API
    completely.
    """

    def __init__(self, input):
        """Creates a new Lexer.

        input - a file-like object containing the input
        """
        if type(input) == type(""):
            self.__input = StringIO(input)
        else:
            self.__input = input

        try:
            name = input.name()
        except AttributeError:
            name = "<stdin>"
            
        self.__scanner = Scanner(lexicon, self.__input, name)


    def close(self):
        """Closes the lexer and the underlying input stream"""
        self.__input.close()


    def tokenize(self):
        """Returns a list of all the tokens"""
        result = []
        while 1:

            try:
                token = self.__scanner.read()
            except Errors.UnrecognizedInput, e:
                raise LexerException(str(e))
                
            if token[0] is None:
                return result

            (name, line, col) = self.__scanner.position()
            
            result.append(Token(token[0], token[1], name, line, col))


def tokenize(expr):
    """Returns a list of tokens obtained by lexing the specified
    expression.

    Raises a LexerException if the specified expression could not be
    tokenized.
    """
    lexer = _Lexer(expr)
    try:
        return lexer.tokenize()
    finally:
        lexer.close()


