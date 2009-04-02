#! /usr/bin/env
# ______________________________________________________________________
"""Module MyFrontExceptions

Defines exceptions used by the MyFront compiler.

Jonathan Riehl"""
# ______________________________________________________________________
# Exception definition(s)

class MyFrontException (Exception):
    "Base class for all MyFront exceptions."

# ______________________________________________________________________

class MyFrontSyntaxError (MyFrontException):
    "Wrapper for syntax errors."

# ______________________________________________________________________

class MyFrontQuoteExprError (MyFrontException):
    "Wrapper for errors in a quotation expression."

# ______________________________________________________________________

class MyFrontCompileTimeError (MyFrontException):
    "Wrapper for errors raised inside of a quotation function."

# ______________________________________________________________________
# End of MyFrontExceptions.py
