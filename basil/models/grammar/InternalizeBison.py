#! /usr/bin/env python
# ______________________________________________________________________
"""Module InternalizeBison

This module provides the BisonInernalizer class.

$Id: InternalizeBison.py 3228 2004-03-12 03:14:44Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import sys
from basil.parsing import BisonParser
from basil.models.grammar import BaseInternalizer, BasilGrammarModel

# ______________________________________________________________________
# Class definition

class BisonInternalizer (BaseInternalizer.BaseInternalizer):
    """Class BisonInternalizer
    """
    # ____________________________________________________________
    def __call__ (self, grammarData):
        """BisonInternalizer.__call__()
        """
        self._initializeModel()
        start, prodList = grammarData
        self.preprocessProductions(prodList)
        self.processProductions(prodList)
        if start != None:
            startMd = self.factory.createDataItem(None,
                                                  self._getSymbol(start.tag),
                                                  tag = "start")
            self.crntMetadata.append(startMd)
        return self.crntGrammar

    # ____________________________________________________________
    def preprocessProductions (self, prodList):
        """BisonInternalizer.preprocessProductions()
        """
        for (lhs, rhs) in prodList:
            if not self.nonterminalMap.has_key(lhs.tag):
                self.nonterminalMap[lhs.tag] = None

    # ____________________________________________________________
    def processProductions (self, prodList):
        """BisonInternalizer.processProductions()
        """
        for (lhs, rhs) in prodList:
            lhsSymElem = self._getSymbol(lhs.tag)
            lhsElem = self.factory.createProductionLHS(None, lhsSymElem)
            rhsListElem = self.factory.createTokenList()
            rhsList = map(lambda bisonSym : self._getSymbol(bisonSym.tag), rhs)
            rhsListElem.extend(rhsList)
            rhsElem = self.factory.createProductionRHS(None, rhsListElem)
            prodElem = self.factory.createProduction(None, lhsElem, rhsElem)
            self.crntProductions.append(prodElem)

# ______________________________________________________________________

def main (fileName = None):
    """main()
    """
    text = None
    if None == fileName:
        text = sys.stdin.read()
    else:
        inFile = open(fileName)
        text = inFile.read()
        inFile.close()
    parser = BisonParser.BisonParser(text)
    parser.parse()
    grammarFactoryClass = BasilGrammarModel.getModelFactory()
    grammarFactory = grammarFactoryClass()
    internalizer = BisonInternalizer(grammarFactory)
    prodList = map(lambda prodData : (prodData[1], prodData[2]),
                   parser.productions)
    model = internalizer((parser.startVal, prodList))
    print grammarFactory.externalizeXML(model)

# ______________________________________________________________________

if __name__ == "__main__":
    fileName = None
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    main(fileName)

# ______________________________________________________________________
# End of InternalizeBison.py
