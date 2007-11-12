#! /usr/bin/env python
# ______________________________________________________________________
"""Module InternalizeBNF

This module provides the BNFInternalizer class, which generates callable
instances for translation of a BasilBNF parse tree (actually a dict) into a
grammar model instance.

When called from the command line, the module accepts an optional file name of
a BNF input file.  If no file name is given, the BNF grammar will be read from
stdin.  The module will translate the BNF input to a Basil grammar model, then
serialize the model to XML, and output to stdout.

$Id: InternalizeBNF.py 0 2004-01-15 01:25:51Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import sys
from basil.parsing import bnf
from basil.models.grammar import BaseInternalizer, BasilGrammarModel

# ______________________________________________________________________

class BNFInternalizer (BaseInternalizer.BaseInternalizer):
    """Class BNFInternalizer
    """
    # ____________________________________________________________
    def __call__ (self, grammar):
        """BNFInternalizer.__call__
        """
        self._initializeModel()
        start, prodMap = grammar
        self.preprocessProductions(prodMap)
        self.processProductions(prodMap)
        startMd = self.factory.createDataItem(None, self._getSymbol(start),
                                              tag = "start")
        self.crntMetadata.append(startMd)
        return self.crntGrammar

    # ____________________________________________________________
    def preprocessProductions (self, prodMap):
        """BNFInternalzier.preprocessProductions
        Tease out terminal and nonterminal symbols.
        """
        for lhsSymbol in prodMap.keys():
            if not self.nonterminalMap.has_key(lhsSymbol):
                self.nonterminalMap[lhsSymbol] = None

    # ____________________________________________________________
    def processProductions (self, prodMap):
        """BNFInternalizer.processProductions
        """
        for lhsSymbol in prodMap.keys():
            prods = prodMap[lhsSymbol]
            for prod in prods:
                lhsSymElem = self._getSymbol(lhsSymbol)
                lhsElem = self.factory.createProductionLHS(None, lhsSymElem)
                rhsListElem = self.factory.createTokenList()
                rhsListElem.extend(map(self._getSymbol, prod))
                rhsElem = self.factory.createProductionRHS(None, rhsListElem)
                prodElem = self.factory.createProduction(None,
                                                         lhsElem, rhsElem)
                self.crntProductions.append(prodElem)

# ______________________________________________________________________

def main (fileName = None):
    """main()
    Read a BNF input grammar from the given file name and print the XML
    representation of the corresponding Basil grammar model.
    """
    text = None
    if None == fileName:
        text = sys.stdin.read()
    else:
        inFile = open(fileName)
        text = inFile.read()
        inFile.close()
    grammar = bnf.get_prods(text)
    grammarFactoryClass = BasilGrammarModel.getModelFactory()
    grammarFactory = grammarFactoryClass()
    internalizer = BNFInternalizer(grammarFactory)
    model = internalizer(grammar)
    print grammarFactory.externalizeXML(model)

# ______________________________________________________________________

if __name__ == "__main__":
    fileName = None
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    main(fileName)

# ______________________________________________________________________
# End of InternalizeBNF.py
