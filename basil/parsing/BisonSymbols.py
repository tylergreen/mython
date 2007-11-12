#! /bin/usr/env python
# ______________________________________________________________________
"""Module BisonSymbols.py

Jonathan Riehl
1999.12.23

$Id: BisonSymbols.py,v 1.1.1.1 2000/07/03 20:59:37 jriehl Exp $
"""
# ______________________________________________________________________
bisonSymbols = {}

# ______________________________________________________________________
class SUNKNOWN:
    pass

class STOKEN:
    pass

class SNTERM:
    pass

class SALIAS:
    pass

# ______________________________________________________________________
def initialize ():
    global bisonSymbols
    bisonSymbols = {}

# ______________________________________________________________________
def getSymbol (key):
    """getSymbol()
    """
    if bisonSymbols.has_key(key):
	return bisonSymbols[key]
    newSymbol = BisonSymbols()
    newSymbol.tag = key[:]
    newSymbol.klass = SUNKNOWN
    bisonSymbols[key] = newSymbol
    return newSymbol

# ______________________________________________________________________
class BisonSymbols:
    """Class BisonSymbols:
    """
    # ____________________________________________________________
    def __init__ (self):
	self.tag = None
	self.typeName = None
	self.value = None
	self.userTokenNumber = None
	self.alias = None
	self.klass = SUNKNOWN

# ______________________________________________________________________
# End of BisonSymbols.py
