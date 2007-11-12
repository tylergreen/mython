#! /usr/bin/env python
# ______________________________________________________________________
"""Module BisonParser.py

Jonathan Riehl
1999.12.23

Parser for Bison grammar files.  Command line test usage:
	% BisonParser.py <file.y>

$Id: BisonParser.py,v 1.1.1.1 2000/07/03 20:59:37 jriehl Exp $
"""
# ______________________________________________________________________
from BisonTokens import *
import BisonLexor
import BisonSymbols

# ______________________________________________________________________
RIGHT_ASSOC = 1
LEFT_ASSOC = 2
NON_ASSOC = 3

# ______________________________________________________________________
class BisonParser:
    """Class BisonParser
    Class encapsulation of the reader.c module in the Bison source.
    """
    # ____________________________________________________________
    def __init__ (self, text = None):
	"""BisonParser.__init__()
	"""
	self.lexor = BisonLexor.BisonLexor(text)
	self.defn = ""
	self.valueComponentsUsed = 0
	self.nSyms = 1
	self.nVars = 0
	self.nRules = 0
	self.nItems = 0
	self.genSymCount = 0
	self.startVal = None
	self.productions = []

    # ____________________________________________________________
    def addDefn (self, str):
	"""BisonParser.addDefn()
	"""
	self.defn = "%s%s" % (self.defn, str)

    # ____________________________________________________________
    def skipToChar (self, target):
	"""BisonParser.skipToChar()
	"""
	if target == '\n':
	    self.lexor.warn("   skipping to next \\n")
	else:
	    self.lexor.warn("   skipping to next %s" % target)
	c = self.lexor.skipWhiteSpace()
	while c != target and c != None:
	    c = self.lexor.skipWhiteSpace()
	if c != None:
	    self.lexor.ungetc()

    # ____________________________________________________________
    def parse (self):
	"""BisonParser.parse()
	"""
	self.valueComponentsUsed = 0
	self.nSyms = 1
	self.nVars = 0
	self.nRules = 0
	self.nItems = 0
	self.genSymCount = 0
	self.startVal = None
	self.productions = []
	errtoken = BisonSymbols.getSymbol("error")
	errtoken.klass = BisonSymbols.STOKEN
	errtoken.userTokenNumber = 256
	undeftoken = BisonSymbols.getSymbol("$undefined")
	undeftoken.klass = BisonSymbols.STOKEN
	undeftoken.userTokenNumber = 2
	self.readDeclarations()
	self.readGrammar()

    # ____________________________________________________________
    def readDeclarations (self):
	"""BisonParser.readDeclarations()
	"""
	while 1:
	    c = self.lexor.skipWhiteSpace()
	    if c == '%':
		tok = self.lexor.parsePercentToken()
		if tok == TWO_PERCENTS:
		    return
		elif tok == PERCENT_LEFT_CURLY:
		    self.copyDefinition()
		elif tok == TOKEN:
		    self.parseTokenDecl(BisonSymbols.STOKEN,
					BisonSymbols.SNTERM)
		elif tok == NTERM:
		    self.parseTokenDecl(BisonSymbols.SNTERM,
					BisonSymbols.STOKEN)
		elif tok == TYPE:
		    self.parseTypeDecl()
		elif tok == START:
		    self.parseStartDecl()
		elif tok == UNION:
		    self.parseUnionDecl()
		elif tok == EXPECT:
		    self.parseExpectDecl()
		elif tok == THONG:
		    self.parseThongDecl()
		elif tok == LEFT:
		    self.parseAssocDecl(LEFT_ASSOC)
		elif tok == RIGHT:
		    self.parseAssocDecl(RIGHT_ASSOC)
		elif tok == NONASSOC:
		    self.parseAssocDecl(NON_ASSOC)
		elif tok == SEMANTIC_PARSER:
		    pass
		elif tok == PURE_PARSER:
		    pass
		elif tok == NOOP:
		    pass
		else:
		    self.lexor.warn("unrecognized: %s" % self.lexor.strval)
		    self.skipToChar('%')
	    elif c == None:
		self.lexor.fatal("no input grammar")
	    else:
		self.lexor.warn('unknown character: %s' % c)
		self.skipToChar('%')

    # ____________________________________________________________
    def copyDefinition (self):
	"""BisonParser.copyDefinition()

	From copy_definition() in reader.c:
	Copies the contents of a %{ ... %} into the definitions string.
	The %{ has already been read.  Return after reading the %}.
	"""
	after_percent = 0
	c = self.lexor.getc()
	while 1:
	    if c == '\n':
		self.addDefn(c)
		self.lexor.lineno = self.lexor.lineno + 1
	    elif c == '%':
		after_percent = 1
	    elif c in "\"'":
		match = c
		self.addDefn(c)
		c = self.lexor.getc()
		while c != match:
		    if c == None:
			self.lexor.fatal("unterminated string at end of file")
		    elif c == '\n':
			self.lexor.warn("unterminated string at end of file")
			self.lexor.ungetc()
			c = match
			continue
		    self.addDefn(c)
		    if c == '\\':
			c = self.lexor.getc()
			if c == None:
			    self.lexor.fatal('unterminated string at end of '
					     'file')
			self.addDefn(c)
			if c == '\n':
			    self.lexor.lineno = self.lexor.lineno + 1
		    c = self.lexor.getc()
		self.addDefn(c)
	    elif c == '/':
		self.addDefn(c)
		c = self.lexor.getc()
		if c not in '*/':
		    continue
		cplus_comment = c == '/'
		self.addDefn(c)
		c = self.lexor.getc()
		ended = 0
		while not ended:
		    if (not cplus_comment and c == '*'):
			while c == '*':
			    self.addDefn(c)
			    c = self.lexor.getc()
			if c == '/':
			    self.addDefn(c)
			    ended = 1
		    elif c == '\n':
			self.lexor.lineno = self.lexor.lineno + 1
			self.addDefn(c)
			if cplus_comment:
			    ended = 1
			else:
			    c = self.lexor.getc()
		    elif c == None:
			self.lexor.fatal('unterminated comment in `%{\' '
					 'definition')
		    else:
			self.addDefn(c)
			c = self.lexor.getc()
	    elif c == None:
		self.lexor.fatal('unterminated `%{\' definition')
	    else:
		self.addDefn(c)
	    c = self.lexor.getc()
	    if after_percent:
		if c == '}':
		    return
		self.addDefn('%')
	    after_percent = 0

    # ____________________________________________________________
    def parseTokenDecl (self, whatIs, whatIsNot):
	"""BisonParser.parseTokenDecl()

	From parse_token_decl() in reader.c:
	Parse what comes after %token or %nterm.  For %token, whatIs is STOKEN,
	and whatIsNot is SNTERM.  For %nterm, the arguments are reversed.
	"""
	typename = None
	symbol = None
	while 1:
	    tmpCh = self.lexor.skipWhiteSpace()
	    self.lexor.ungetc()
	    if tmpCh == '%':
		return
	    elif tmpCh == None:
		self.lexor.fatal('premature EOF after %s' % self.strval)
	    token = self.lexor.lex()
	    if token == COMMA:
		symbol = None
		continue
	    elif token == TYPENAME:
		typename = self.lexor.strval
		self.valueComponentsUsed = 1
		symbol = None
	    elif (token == IDENTIFIER and
		  self.lexor.symval.tag == '"' and
		  symbol):
		self.lexor.symval.klass = BisonSymbols.STOKEN
		self.lexor.symval.typeName = typename
		self.lexor.symval.userTokenNumber = symbol.userTokenNumber
		symbol.userTokenNumber = BisonSymbols.SALIAS
		self.lexor.symval.alias = symbol
		symbol.alias = self.lexor.symval
		symbol = None
		self.nSyms = self.nSyms - 1
	    elif token == IDENTIFIER:
		oldClass = self.lexor.symval.klass
		symbol = self.lexor.symval
		if symbol.klass == whatIsNot:
		    self.lexor.warn('symbol %s redefined' % symbol.tag)
		symbol.klass = whatIs
		if ((whatIs == BisonSymbols.SNTERM) and
		    (oldClass != BisonSymbols.SNTERM)):
		    symbol.value = self.nvars
		    self.nvars = self.nvars + 1
		if typename:
		    if symbol.typeName == None:
			symbol.typeName = typename
		    elif symbol.typeName != typename:
			self.lexor.warn('type redeclaration for %s' %
					symbol.tag)
	    elif symbol and token == NUMBER:
		symbol.userTokenNumber = string.atoi(self.lexor.strval)
	    else:
		if whatIs == BisonSymbols.STOKEN:
		    tmpStr = "%token"
		else:
		    tmpStr = "%nterm"
		self.lexor.warn("`%s' is invalid in %s" %
				(self.lexor.strval, tmpStr))
		self.skipToChar('%')
    
    # ____________________________________________________________
    def parseThongDecl (self):
	"""BisonParser.parseThongDecl()
	"""
	symbol = None
	typename = None
	token = self.lexor.lex()
	if token == TYPENAME:
	    typename = self.lexor.strval
	    self.valueComponentsUsed = 1
	    token = self.lexor.lex()
	if token != IDENTIFIER:
	    self.lexor.warn('unrecognized item %s, expected an identifier' %
			    self.lexor.strval)
	    self.skipToChar('%')
	    return
	self.lexor.symval.klass = BisonSymbols.STOKEN
	self.lexor.symval.typeName = typename
	self.lexor.symval.userTokenNumber = BisonSymbols.SALIAS
	symbol = self.lexor.symval
	token = self.lexor.lex()
	if token == NUMBER:
	    usrtoknum = string.atoi(self.lexor.strval)
	    token = self.lexor.lex()
	else:
	    usrtoknum = 0
	if token != IDENTIFIER or self.lexor.symval.tag != '"':
	    self.lexor.warn('expected string constant instead of %s' %
			    self.lexor.strval)
	    self.skipToChar('%')
	    return
	self.lexor.symval.klass = BisonSymbols.STOKEN
	self.lexor.symval.typeName = typename
	self.lexor.symval.userTokenNumber = usrtoknum
	self.lexor.symval.alias = symbol
	symbol.alias = self.lexor.symval
	self.nSyms = self.nSyms - 1

    # ____________________________________________________________
    def parseStartDecl (self):
	"""BisonParser.parseStartDecl()
	"""
        if self.startVal != None:
	    self.lexor.warn("multiple %start declarations")
	elif self.lexor.lex() != IDENTIFIER:
	    self.lexor.warn("invalid %start declaration")
	else:
	    self.startVal = self.lexor.symval

    # ____________________________________________________________
    def parseTypeDecl (self):
	"""BisonParser.parseTypeDecl()
	"""
        if self.lexor.lex() != TYPENAME:
	    self.lexor.warn("%type declaration has no <typename>")
	    self.skipToChar('%')
	    return
	name = self.lexor.strval[:]
	while 1:
	    tmpCh = self.lexor.skipWhiteSpace()
	    self.lexor.ungetc()
	    if tmpCh == '%':
		return
	    if tmpCh == None:
		self.lexor.fatal("Premature EOF after %s" % self.lexor.strval)
	    token = self.lexor.lex()
	    if token in [COMMA, SEMICOLON]:
		pass
	    elif token == IDENTIFIER:
		if self.lexor.symval.typeName == None:
		    self.lexor.symval.typeName = name
		elif self.lexor.symval.typeName != name:
		    self.lexor.warn("type redeclaration for %s" %
				    self.lexor.symval.tag)
	    else:
		self.warn("invalid %%type declaration due to item `%s'" %
			  self.lexor.strval)
		self.skipToChar('%')

    # ____________________________________________________________
    def parseAssocDecl (self, assoc):
	"""BisonParser.parseAssocDecl()

	Ignore assoc for now. - JDR
	"""
	name = None
	prev = 0
	while 1:
	    tmpCh = self.lexor.skipWhiteSpace()
	    self.lexor.ungetc()
	    if tmpCh == '%':
		return
	    elif tmpCh == None:
		self.fatal('premature EOF after %s' % self.lexor.strval)
	    token = self.lexor.lex()
	    if token == TYPENAME:
		name = self.lexor.strval
	    elif token == COMMA:
		pass
	    elif token == IDENTIFIER:
		# XXX - There was stuff here.
		pass
	    elif token == NUMBER:
		if prev == IDENTIFIER:
		    nrStr = self.lexor.strval
		    self.lexor.symval.userTokenNumber = string.atoi(nrStr)
		else:
		    self.lexor.warn("invalid text (%s) - number should be "
				    "after identifier" % self.lexor.strval)
		    self.skipToChar('%')
	    elif token == SEMICOLON:
		return
	    else:
		self.lexor.warn("unexpected item: %s" % self.lexor.strval)
		self.skipToChar('%')
	    prev = token
	    
    # ____________________________________________________________
    def parseUnionDecl (self):
	"""BisonParser.parseUnionDecl()
	"""
	self.addDefn("typedef union")
	count = 0
	inComment = 0
	c = self.lexor.getc()
	while c != None:
	    self.addDefn(c)
	    if c == '\n':
		self.lexor.lineno = self.lexor.lineno + 1
	    elif c == '/':
		c = self.lexor.getc()
		if c not in "/*":
		    self.lexor.ungetc()
		else:
		    self.addDefn(c)
		    cplusComment = c == '/'
		    inComment = 1
		    c = self.lexor.getc()
		    while inComment:
			self.addDefn(c)
			if c == '\n':
			    self.lexor.lineno = self.lexor.lineno + 1
			    if cplusComment:
				inComment = 0
				break
			if c == None:
			    self.lexor.fatal("unterminated comment at end of "
					     "file")
			if not cplusComment and c == '*':
			    c = self.lexor.getc()
			    if c == '/':
				self.addDefn(c)
				inComment = 0
			else:
			    c = self.lexor.getc()
	    elif c == '{':
		count = count + 1
	    elif c == '}':
		if count == 0:
		    self.lexor.warn("unmatched close brace (})")
		count = count - 1
		if count <= 0:
		    self.addDefn(" YYSTYPE;\n")
		    c = self.lexor.skipWhiteSpace()
		    if c != ';':
			self.lexor.ungetc()
		    return
	    c = self.lexor.getc()

    # ____________________________________________________________
    def parseExpectDecl (self):
	"""BisonParser.parseExpectDecl()

	Value is currently thrown away. -JDR
	"""
	c = self.lexor.getc()
	while c in ' \t':
	    c = self.lexor.getc()
	while c >= '0' and c <= '9':
	    c = self.lexor.getc()
	self.lexor.ungetc()
	
    # ____________________________________________________________
    def readGrammar (self):
	"""BisonParser.readGrammar()
	"""
	lhs = None
	t = self.lexor.lex()
	while t not in (TWO_PERCENTS, ENDFILE):
	    if t in (IDENTIFIER, BAR):
		actionFlag = 0
		ruleLength = 0
		if t == IDENTIFIER:
		    lhs = self.lexor.symval
		    if self.startVal == None:
			self.startVal = lhs
		    t = self.lexor.lex()
		    if t != COLON:
			self.lexor.warn("ill-formed rule: initial symbol not "
					"followed by colon")
			self.lexor.unlex(t)
		if self.nRules == 0 and t == BAR:
		    self.lexor.warn("grammar starts with vertical bar")
		    lhs = self.lexor.symval
		self.nRules = self.nRules + 1
		self.nItems = self.nItems + 1
		# Production format will be: [lineno, lhs, [rhs0, ...]]
		production = [self.lexor.lineno, lhs]
		self.productions.append(production)
		if lhs.klass == BisonSymbols.SUNKNOWN:
		    lhs.klass = BisonSymbols.SNTERM
		    lhs.value = self.nVars
		    self.nVars = self.nVars + 1
		elif lhs.klass == BisonSymbols.STOKEN:
		    self.lexor.warn("rule given for %s, which is a token" %
				    lhs.tag)
		# Read the right hand side of the rule.
		rhs = []
		production.append(rhs)
		while 1:
		    t = self.lexor.lex()
		    if (t == PREC):
			self.lexor.lex()
			# XXX Currently throw out any PREC's
			t = self.lexor.lex()
		    if t not in (IDENTIFIER, LEFT_CURLY):
			break
		    if t == IDENTIFIER:
			ssave = self.lexor.symval
			t1 = self.lexor.lex()
			self.lexor.unlex(t1)
			self.lexor.symval = ssave
			if t1 == COLON:
			    break
		    if actionFlag:
			sdummy = self.genSym()
			self.nRules = self.nRules + 1
			self.nItems = self.nItems + 1
			subordinateProd = [self.lexor.lineno, sdummy, []]
			self.productions.append(subordinateProd)
			self.nItems = self.nItems + 1
			rhs.append(sdummy)
			actionFlag = 0
		    if t == IDENTIFIER:
			self.nItems = self.nItems + 1
			rhs.append(self.lexor.symval)
		    else:
			# XXX Throw out any action as well...
			self.copyAction()
			actionFlag = 1
		production.append(rhs)
		if t == PREC:
		    self.lexor.warn("two @prec's in a row")
		    self.lexor.lex()
		    t = self.lexor.lex()
		if t == GUARD:
		    self.copyGuard()
		    t = self.lexor.lex()
		elif t == LEFT_CURLY:
		    if actionFlag:
			self.lexor.warn("two actions at end of one rule")
		    self.copyAction()
		    actionFlag = 1
		    t = self.lexor.lex()
		# Watch out...there are warnings in the real version that
		# are not implemented here.
		if t == SEMICOLON:
		    t = self.lexor.lex()
	    else:
		self.lexor.warn("invalid input: %s" % self.lexor.strval)
		t = self.lexor.lex()
	return self.productions
		
    # ____________________________________________________________
    def copyAction (self):
	"""BisonParser.copyAction()
	"""
	count = 1
	match = None
	c = self.lexor.getc()
	while count > 0:
	    # Kinda punted on this one...just throw out actions for now.
	    if c == '\n':
		self.lexor.lineno = self.lexor.lineno + 1
	    elif c == '{':
		count = count + 1
	    elif c == '}':
		count = count - 1
	    elif c == None:
		self.lexor.fatal("unterminated action at end of file")
	    elif c in ('"', "'"):
		match = c
		c = self.lexor.getc()
		while c != match:
		    if c == '\n':
			self.lexor.warn("unterminated string")
			break
		    elif c == None:
			self.lexor.fatal("unterminated string at end of file")
		    if c == '\\':
			c = self.lexor.getc()
			if c == None:
			    self.lexor.fatal("unterminated string at end of "
					     "file")
			elif c == '\n':
			    self.lexor.lineno = self.lexor.lineno + 1
		    c = self.lexor.getc()
	    elif c == '/':
		c = self.lexor.getc()
		if c not in "*/":
		    continue
		cplus_comment = (c == "/")
		c = self.lexor.getc()
		inside = 1
		while (inside):
		    if not cplus_comment and c == "*":
			while c == "*":
			    c = self.lexor.getc()
			if c == "/":
			    inside = 0
			    c = self.lexor.getc()
		    elif c == "\n":
			self.lexor.lineno = self.lexor.lineno + 1
			if cplus_comment:
			    inside = 0
			c = self.lexor.getc()
		    elif c == None:
			self.fatal("unterminated comment")
		    else:
			c = self.lexor.getc()
	    if count > 0:
		c = self.lexor.getc()
	# End of BisonParser.copyAction

    # ____________________________________________________________
    def copyGuard (self):
	"""BisonParser.copyGuard()
	"""
	self.lexor.fatal("guard not currently handled")

    # ____________________________________________________________
    def genSym (self):
	"""BisonParser.genSym()
	"""
	self.genSymCount = self.genSymCount + 1
	tokenName = '@%d' % self.genSymCount
	sym = BisonSymbols.getSymbol(tokenName)
	sym.klass = BisonSymbols.SNTERM
	sym.value = self.nVars
	self.nVars = self.nVars + 1
	return sym

# ______________________________________________________________________

def main ():
    import sys
    if len(sys.argv) == 2:
	text = open(sys.argv[1]).read()
	parser = BisonParser(text)
	parser.parse()
	print "Done."
	prods = parser.productions
	for prod in prods:
	    print prod[1].tag, "->",
	    for sym in prod[2]:
		print sym.tag,
	    print
    else:
	print __doc__

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of BisonParser.py
