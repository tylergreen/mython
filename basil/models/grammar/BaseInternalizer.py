#! /usr/bin/env python
# ______________________________________________________________________
"""Module basil.models.grammar.BaseInternalizer

Defines the abstract base class for translator classes that create
grammar models.

$Id: BaseInternalizer.py 0 2004-01-15 01:25:51Z jriehl $
"""
# ______________________________________________________________________
# Module imports

from basil.models.grammar import BasilGrammarModel

# ______________________________________________________________________

class BaseInternalizer (object):
    """Class BaseInternalizer
    Abstract base class for callable objects that will translate from a grammar
    file parse to the Basil grammar model.
    """
    # ____________________________________________________________
    def __init__ (self, factory = None):
        """PgenInternalizer.__init__
        """
        self.factory = factory
        if None == factory:
            factoryClass = BasilGrammarModel.getModelFactory()
            self.factory = factoryClass()
        self._initializeModel()

    # ____________________________________________________________
    def _initializeModel (self):
        """PgenInternalizer._initializeModel
        """
        self.crntMetadata = self.factory.buildElement('DataList')
        self.crntTerminals = self.factory.buildElement('Terminals')
        self.crntNonterminals = self.factory.buildElement('Nonterminals')
        self.crntProductions = self.factory.buildElement('Productions')
        self.crntGrammar = self.factory.buildElement('Grammar',
                                                     self.crntMetadata,
                                                     self.crntTerminals,
                                                     self.crntNonterminals,
                                                     self.crntProductions)
        self.nonterminalMap = {}
        self.terminalMap = {}

    # ____________________________________________________________
    def _getSymbol (self, sName):
        """PgenInternalizer._getSymbol
        """
        if self.nonterminalMap.has_key(sName):
            retVal = self.nonterminalMap[sName]
            if None == retVal:
                retVal = self.factory.buildElement('Nonterminal',
                                                   name = sName)
                self.nonterminalMap[sName] = retVal
                self.crntNonterminals.append(retVal)
        else:
            if self.terminalMap.has_key(sName):
                retVal = self.terminalMap[sName]
            else:
                retVal = self.factory.buildElement('Terminal',
                                                   name = sName)
                self.terminalMap[sName] = retVal
                self.crntTerminals.append(retVal)
        return retVal

    # ____________________________________________________________
    def __call__ (self, ast):
        """BaseInternalizer.__call__
        """
        raise self, "Override me!"

# ______________________________________________________________________
# End of BaseInternalizer.py
