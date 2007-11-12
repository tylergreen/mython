#! /usr/bin/env python
# ______________________________________________________________________
"""Module BisonLexor.py

Jonathan Riehl
1999.12.22

Lexor for Bison (and hopefully YACC) grammar files.  Based upon lex.c in
the Bison distribution.
"""
# ______________________________________________________________________
import sys
import string
import BisonSymbols
from BisonTokens import *

# ______________________________________________________________________
__DEBUG__ = 1

# ______________________________________________________________________
class StringLexor:
    """Class StringLexor
    """
    # ____________________________________________________________
    def __init__ (self, dataStr = None):
	self.setDataString(dataStr)

    # ____________________________________________________________
    def setDataString (self, dataStr = None):
	self.dataStr = dataStr
	self.position = 0
	self.lineno = 1
	self.symval = None
	self.strval = ""
	self.unlexed_symval = None
	self.unlexed = None

    # ____________________________________________________________
    def getc (self):
	if self.position > len(self.dataStr):
	    return None
	c = self.dataStr[self.position]
	self.position = self.position + 1
	return c

    # ____________________________________________________________
    def ungetc (self):
	self.position = self.position - 1
	if self.position < 0:
	    raise StringLexor, "Backed up past buffer origin."

    # ____________________________________________________________
    def warn (self, str):
	sys.stderr.write("Warning(%d): %s\n" % (self.lineno, str))
	#if __DEBUG__:
	#    raise StringLexor, "debug"

    # ____________________________________________________________
    def fatal (self, str):
	raise StringLexor, str

# ______________________________________________________________________
class BisonLexor (StringLexor):
    """Class BisonLexor
    """
    # ____________________________________________________________
    def __init__ (self, dataStr = None):
	StringLexor.__init__(self, dataStr)
	self.symval = None
	BisonSymbols.initialize()

    # ____________________________________________________________
    def unlex (self, tok):
	"""BisonLexor.unlex()
	"""
	self.unlexed = tok
	self.unlexed_symval = self.symval

    # ____________________________________________________________
    def skipWhiteSpace (self):
	c = self.getc()
	while (1):
	    cplus_comment = 0
	    if c == "/":
		c = self.getc()
		if c not in "*/":
		    self.warn("unexpected '/' found and ignored")
		    break
		cplus_comment = (c == "/")
		c = self.getc()
		inside = 1
		while (inside):
		    if not cplus_comment and c == "*":
			while c == "*":
			    c = self.getc()
			if c == "/":
			    inside = 0
			    c = self.getc()
		    elif c == "\n":
			self.lineno = self.lineno + 1
			if cplus_comment:
			    inside = 0
			c = self.getc()
		    elif c == None:
			self.fatal("unterminated comment")
		    else:
			c = self.getc()
	    elif c in string.whitespace:
		if c == "\n":
		    self.lineno = self.lineno + 1
		c = self.getc()
	    else:
		return c

    # ____________________________________________________________
    def literalChar (self, term):
	wasquote = 0
	c = self.getc()
	if c == "\n":
	    self.warn("unescaped newline in constant")
	    self.ungetc()
	    code = "?"
	    wasquote = 1
	elif c != "\\":
	    code = c
	    if c == term:
		wasquote = 1
	else:
	    c = self.getc()
	    if (c == 't'):
		code = '\t';
	    elif (c == 'n'):
		code = '\n';
	    elif (c == 'a'):
		code = '\007';
	    elif (c == 'r'):
		code = '\r';
	    elif (c == 'f'):
		code = '\f';
	    elif (c == 'b'):
		code = '\b';
	    elif (c == 'v'):
		code = '\013';
	    elif (c == '\\'):
		code = '\\';
	    elif (c == '\''):
		code = '\'';
	    elif (c == '\"'):
		code = '\"';
	    elif (c <= '7' and c >= '0'):
		code = 0
		while c <= '7' and c >= '0':
		    code = code * 8 + (ord(c) - ord('0'))
		    if code >= 256 or code < 0:
			self.warn("octal value outside range 0..255")
			code = 255
			break
		    c = self.getc()
		code = chr(code)
		self.ungetc()
	    elif c == 'x':
		c = self.getc()
		code = 0
		while 1:
		    if c >= '0' and c <= '9':
			code = code * 16 + (ord(c) - ord('0'))
		    elif c >= 'a' and c <= 'f':
			code = code * 16 + (ord(c) - ord('a') + 10)
		    elif c >= 'A' and c <= 'F':
			code = code * 16 + (ord(c) - ord('A') + 10)
		    else:
			break
		    if code >= 256 or code < 0:
			self.warn("hex value above 255")
			code = 255
			break
		    c = self.getc()
		code = chr(code)
		self.ungetc()
	    else:
		self.warn("unknown escape sequence")
		code = "?"
	if code == term and wasquote:
	    tokenStr = code
	elif code == '\\':
	    tokenStr = '\\\\'
	elif code == '\'':
	    tokenStr = '\\\''
	elif code == '\"':
	    tokenStr = '\\"'
	elif ord(code) >= 040 and ord(code) <= 0177:
	    tokenStr = code
	elif code == '\t':
	    tokenStr = '\\t'
	elif code == '\n':
	    tokenStr = '\\n'
	elif code == '/r':
	    tokenStr = '\\r'
	elif code == '\v':
	    tokenStr = '\\v'
	elif code == '\b':
	    tokenStr = '\\b'
	elif code == '\f':
	    tokenStr = '\\f'
	else:
	    tokenStr = ('\\' + (chr(ord(code) / 0100 + ord('0'))) +
			(chr(((ord(code) / 010) & 07) + ord('0'))) +
			(chr((ord(code) & 07) + ord('0'))))
	return tokenStr, code, wasquote
    
    # ____________________________________________________________
    def lex (self):
	if self.unlexed_symval != None:
	    self.symval = self.unlexed_symval
	    self.unlexed_symval = None
	    return self.unlexed
	idSpace = string.letters + "_" + "."
	c = self.skipWhiteSpace()
	if c == None:
	    self.strval = "EOF"
	    return ENDFILE
	elif c in idSpace:
	    idSpace = idSpace + string.digits
	    tokenBuf = ""
	    while c in idSpace:
		tokenBuf = tokenBuf + c
		c = self.getc()
	    self.ungetc()
	    self.strval = tokenBuf
	    self.symval = BisonSymbols.getSymbol(tokenBuf)
	    return IDENTIFIER
	elif c in string.digits:
	    numval = 0
	    tokenBuf = ""
	    while c in string.digits:
		tokenBuf = tokenBuf + c
		numval = (numval * 10) + (ord(c) - ord('0'))
		c = self.getc()
	    self.strval = tokenBuf
	    return NUMBER
	elif c == "'":
	    translations = -1
	    tokenBuf, code, dummy = self.literalChar("'")
	    c = self.getc()
	    if c != "'":
		self.warn('use "..." for multi-character literal tokens')
		while 1:
		    dummy, dummy1, wasquote = self.literalChar("'")
		    if wasquote == 1:
			break
	    self.strval = "'" + tokenBuf + "'"
	    self.symval = BisonSymbols.getSymbol(self.strval)
	    self.symval.klass = BisonSymbols.STOKEN
	    if self.symval.userTokenNumber == None:
		self.symval.userTokenNumber = ord(code)
	    return IDENTIFIER
	elif c == '"':
	    translations = -1
	    tokenBuf = c
	    while 1:
		next, code, wasquote = self.literalChar('"')
		tokenBuf = tokenBuf + next
		if wasquote:
		    break
	    self.strval = tokenBuf
	    self.symval = BisonSymbols.getSymbol(tokenBuf)
	    self.symval.klass = BisonSymbols.STOKEN
	    return IDENTIFIER
	elif c == ',':
	    return COMMA
	elif c == ':':
	    return COLON
	elif c == ';':
	    return SEMICOLON
	elif c == '|':
	    return BAR
	elif c == '{':
	    return LEFT_CURLY
	elif c == '=':
	    c = self.getc()
	    while c in string.whitespace:
		if c == '\n':
		    self.lineno = self.lineno + 1
		c = self.getc()
	    if c == '{':
		self.strval = "={"
		return LEFT_CURLY
	    else:
		self.ungetc()
		return ILLEGAL
	elif c == '<':
	    c = self.getc()
	    tokenBuf = ""
	    while c != '>':
		if c == None:
		    self.fatal("unterminated type name at end of file")
		if c == '\n':
		    self.warn("unterminated type name.")
		    self.ungetc()
		    break
		tokenBuf = tokenBuf + c
		c = self.getc()
	    self.strval = tokenBuf
	    return TYPENAME
	elif c == '%':
	    return self.parsePercentToken()
	else:
	    return ILLEGAL
    
    # ____________________________________________________________
    def parsePercentToken (self):
	percentTable = {
	    'token' : TOKEN,
	    'term' : TOKEN,
	    'nterm' : NTERM,
	    'type' : TYPE,
	    'guard' : GUARD,
	    'union' : UNION,
	    'expect' : EXPECT,
	    'thong' : THONG,
	    'start' : START,
	    'left' : LEFT,
	    'right' : RIGHT,
	    'nonassoc' : NONASSOC,
	    'binary' : NONASSOC,
	    'semantic_parser' : SEMANTIC_PARSER,
	    'pure_parser' : PURE_PARSER,
	    'prec' : PREC,
	    'no_lines' : NOOP,
	    'raw' : NOOP,
	    'token_table' : NOOP
	}
	c = self.getc()
	self.strval = "%%%s" % c
	if c == '%':
	    return TWO_PERCENTS
	elif c == '{':
	    return PERCENT_LEFT_CURLY
	elif c == '<':
	    return LEFT
	elif c == '>':
	    return RIGHT
	elif c == '2':
	    return NONASSOC
	elif c == '0':
	    return TOKEN
	elif c == '=':
	    return PREC
	if c not in string.letters:
	    return ILLEGAL
	tokenBuf = ""
	idStr = string.letters + "_-"
	while c in idStr:
	    tokenBuf = tokenBuf + c
	    c = self.getc()
	self.ungetc()
	self.strval = "%" + tokenBuf
	if percentTable.has_key(tokenBuf):
	    return percentTable[tokenBuf]
	return ILLEGAL

# ______________________________________________________________________
def main ():
    if len(sys.argv) == 2:
	text = open(sys.argv[1]).read()
	lexor = BisonLexor(text)
	while lexor.lex() != ENDFILE:
	    pass
	print "Done."

# ______________________________________________________________________
if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of BisonLexor.py
