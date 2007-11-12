#! /usr/bin/env python
# ______________________________________________________________________
"""Module BisonTokens

Jonathan Riehl
1999.12.23

Define a set of numerical values for tokens used in the Bison parser.
Copied from lex.h in the Bison distribution.

$Id: BisonTokens.py,v 1.1.1.1 2000/07/03 20:59:37 jriehl Exp $
"""
# ______________________________________________________________________

ENDFILE = 0
IDENTIFIER = 1
COMMA = 2
COLON = 3
SEMICOLON = 4
BAR = 5
LEFT_CURLY = 6
TWO_PERCENTS = 7
PERCENT_LEFT_CURLY = 8
TOKEN = 9
NTERM = 10
GUARD = 11
TYPE = 12
UNION = 13
START = 14
LEFT = 15
RIGHT = 16
NONASSOC = 17
PREC = 18
SEMANTIC_PARSER = 19
PURE_PARSER = 20
TYPENAME = 21
NUMBER = 22
EXPECT = 23
THONG = 24
NOOP = 25
SETOPT = 26
ILLEGAL = 27
MAXTOKEN = 1024

# ______________________________________________________________________
# End of BisonTokens.py
