#! /usr/bin/env python
# ______________________________________________________________________
"""Module TokenUtils

Implements utility data, functions and/or classes for use in developing
tokenizers for Python.

$Id: TokenUtils.py,v 1.2 2003/10/02 17:37:17 jriehl Exp $
"""
# ______________________________________________________________________

import StringIO
import string
import token

# ______________________________________________________________________

__DEBUG__ = True

# ______________________________________________________________________

operatorMap = {
        '(' : token.LPAR,
        ')' : token.RPAR,
        '[' : token.LSQB,
        ']' : token.RSQB,
        ':' : token.COLON,
        ',' : token.COMMA,
        ';' : token.SEMI,
        '+' : token.PLUS,
        '+=' : token.PLUSEQUAL,
        '-' : token.MINUS,
        '-=' : token.MINEQUAL,
        '*' : token.STAR,
        '**' : token.DOUBLESTAR,
        '**=' : token.DOUBLESTAREQUAL,
        '*=' : token.STAREQUAL,
        '/' : token.SLASH,
        '//' : token.DOUBLESLASH,
        '//=' : token.DOUBLESLASHEQUAL,
        '/=' : token.SLASHEQUAL,
        '|' : token.VBAR,
        '|=' : token.VBAREQUAL,
        '&' : token.AMPER,
        '&=' : token.AMPEREQUAL,
        '<' : token.LESS,
        '<>' : token.NOTEQUAL,
        '<=' : token.LESSEQUAL,
        '<<' : token.LEFTSHIFT,
        '<<=' : token.LEFTSHIFTEQUAL,
        '>' : token.GREATER,
        '>=' : token.GREATEREQUAL,
        '>>' : token.RIGHTSHIFT,
        '>>=' : token.RIGHTSHIFTEQUAL,
        '=' : token.EQUAL,
        '==' : token.EQEQUAL,
        '.' : token.DOT,
        '%' : token.PERCENT,
        '%=' : token.PERCENTEQUAL,
        '`' : token.BACKQUOTE,
        '{' : token.LBRACE,
        '}' : token.RBRACE,
        '^' : token.CIRCUMFLEX,
        '^=' : token.CIRCUMFLEXEQUAL,
        '~' : token.TILDE,
        '!=' : token.NOTEQUAL
    }

# ______________________________________________________________________

def testTokenizer (TokenizerClass):
    """testTokenizer()
    Run some silly little test on the tokenizer class argument.
    """
    import sys
    if len(sys.argv) == 1:
        tokenizer = TokenizerClass("<stdin>", sys.stdin.readline)
    else:
        tokenizer = TokenizerClass()
        tokenizer.tokenizeFile(sys.argv[1])
    tokenData = (token.NEWLINE, None, 0)
    while tokenData[0] not in (token.ENDMARKER, token.ERRORTOKEN):
        tokenData = tokenizer()
        print tokenData

# ______________________________________________________________________

class AbstractTokenizer:
    """Class AbstractTokenizer
    """
    # ____________________________________________________________
    def __init__ (self, tokenize, filename = None, linereader = None):
        """AbstractTokenizer.__init__()
        """
        self.tokenize = tokenize
        self.filename = filename
        self.fileObj = None
        if None == linereader:
            self.tokenGenerator = None
        else:
            self.tokenGenerator = self.tokenize.generate_tokens(linereader)
    # ____________________________________________________________
    def tokenizeFile (self, filename):
       """AbstractTokenizer.tokenizeFile()
       """
       self.filename = filename
       self.fileObj = open(filename)
       rl = self.fileObj.readline
       self.tokenGenerator = self.tokenize.generate_tokens(rl)
    # ____________________________________________________________
    def tokenizeString (self, inString):
        """AbstractTokenizer.tokenizeString()
        """
        self.filename = "<string>"
        self.fileObj = None
        rl = StringIO.StringIO(inString).readline
        self.tokenGenerator = self.tokenize.generate_tokens(rl)
    # ____________________________________________________________
    def __call__ (self):
        """AbstractTokenizer.__call__()
        """
        retVal = None
        while 1:
            if None != self.tokenGenerator:
                (type, name, (lineno, startCol), endPos,
                 crntLine) = self.tokenGenerator.next()
                # Drop tokens unique to tokenize
                if type in (self.tokenize.COMMENT, self.tokenize.NL):
                    continue
                elif type == token.OP:
                    type = operatorMap[name]
                retVal = (type, name, lineno)
                break
            else:
                # XXX - What kind of error should be raised?
                raise ValueError, "Uninitialized tokenizer object."
        if __DEBUG__:
            print "AbstractTokenizer.__call__():", retVal
        return retVal

# ______________________________________________________________________
# End of TokenUtils.py
