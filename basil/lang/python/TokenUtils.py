#! /usr/bin/env python
# ______________________________________________________________________
"""Module TokenUtils

Implements utility data, functions and/or classes for use in developing
tokenizers for Python.

$Id: TokenUtils.py,v 1.1 2003/07/23 19:52:55 jriehl Exp $
"""
# ______________________________________________________________________

import string
import StringIO
import token

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
        '!=' : token.NOTEQUAL,
        '@' : token.AT
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
        global operatorMap
        self.tokenize = tokenize
        self.filename = filename
        self.fileObj = None
        self.operatorMap = operatorMap
        if None == linereader:
            self.tokenGenerator = None
        else:
            self.tokenGenerator = self.tokenize.generate_tokens(linereader)
    # ____________________________________________________________
    def getOperatorMap (self):
        """AbstractTokenizer.getOperatorMap
        """
        return self.operatorMap
    # ____________________________________________________________
    def tokenizeFile (self, filename):
        """StdTokenizer.tokenizeFile()
        """
        self.filename = filename
        self.fileObj = open(filename)
        rl = self.fileObj.readline
        self.tokenGenerator = self.tokenize.generate_tokens(rl)
    # ____________________________________________________________
    def tokenizeString (self, inString):
        """StdTokenizer.tokenizeString()
        """
        self.filename = "<string>"
        self.fileObj = None
        rl = StringIO.StringIO(inString).readline
        self.tokenGenerator = self.tokenize.generate_tokens(rl)
    # ____________________________________________________________
    def __call__ (self):
        """StdTokenizer.__call__()
        """
        while 1:
            if None != self.tokenGenerator:
                (type, name, (lineno, startCol), endPos,
                 crntLine) = self.tokenGenerator.next()
                # Drop tokens unique to tokenize
                if type in (self.tokenize.COMMENT, self.tokenize.NL):
                    continue
                elif type == token.OP:
                    type = self.operatorMap[name]
                return (type, name, lineno)
            else:
                # XXX - What kind of error should be raised?
                raise ValueError, "Uninitialized tokenizer object."

# ______________________________________________________________________

class TokenizerFactory:
    # ____________________________________________________________
    def __init__ (self, tokenizerClass, opMap = None):
        if None == opMap:
            global operatorMap
            opMap = operatorMap
        self.tokenizerClass = tokenizerClass
        self.operatorMap = opMap

    # ____________________________________________________________
    def getTokenizer (self):
        return self.tokenizerClass()

    # ____________________________________________________________
    def getTokenizerClass (self):
        return self.tokenizerClass

    # ____________________________________________________________
    def getOperatorMap (self):
        return self.operatorMap

# ______________________________________________________________________
# End of TokenUtils.py
