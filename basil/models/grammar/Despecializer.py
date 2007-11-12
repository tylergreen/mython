#! /usr/bin/env python
# ______________________________________________________________________
"""Module Despecializer
Defines the Despecializer class, which is a BasilGrammarModel handler class.
Outputs a new BasilGrammarModel instance that does not contain any Special
elements.

Note that the stub for this handler was generated using (something similar
to):
 % DTD2PyHandler.py -c Despecializer BasilGrammar.dtd > Despecializer.py

Developer notes:
______________________________________________________________________
01.14.2004

Dumb despecializer: new production for each special grouping.

Test idead:
 % modeling/handle.py models/grammar/BasilGrammarModel models/grammar/Despecializer parsing/tests/test.bnf -printxml > t0
 % models/grammar/InternalizeBNF.py parsing/tests/test.bnf > t1
 % diff -c t0 t1
 No differences encountered
______________________________________________________________________

$Id: Despecializer.py 2871 2004-01-21 01:19:53Z jriehl $
"""
# ______________________________________________________________________
# Module imports

from basil.modeling.BaseModelHandler import BaseModelHandler
from basil.models.grammar import BasilGrammarModel

# ______________________________________________________________________
def simpleSymbolGen ():
    count = 0
    while 1:
        yield "symbol%d" % (count,)
        count = count + 1

# ______________________________________________________________________
class Despecializer (BaseModelHandler):
    # ____________________________________________________________
    def __init__ (self, factory = None, symbolGenerator = None):
        """Despecializer.__init__
        Associates a BasilGrammarModel factory with the handler.  If none
        is given, a new factory is instantiated from the default
        BasilGrammarModel module.
        """
        if None == factory:
            factoryClass = BasilGrammarModel.getModelFactory()
            factory = factoryClass()
        if None == symbolGenerator:
            symbolGenerator = simpleSymbolGen()
        self.factory = factory
        self.symbolGenerator = symbolGenerator
        self._pendingProductions = []
        self._leftRecursive = False
        self._crntLHS = None

    # ____________________________________________________________
    def _getNonterminal (self, symName):
        if not self.nonterminalMap.has_key(symName):
            retVal = self.factory.createNonterminal(None, name = symName)
            self.nonterminalMap[symName] = retVal
        else:
            retVal = self.nonterminalMap[symName]
        return retVal

    # ____________________________________________________________
    def _handlePendingProductions (self):
        """Despecializer._handlePendingProductions
        """
        result = []
        while self._pendingProductions:
            nontermElem, rhs, procRHS = self._pendingProductions[0]
            del self._pendingProductions[0]
            prodElem = self._buildProduction(nontermElem, rhs,
                                             processRHS = procRHS)
            result.append(prodElem)
        self._crntLHS = None
        return result

    # ____________________________________________________________
    def _buildProduction (self, nontermElem, rhsElems, metadata = None,
                          processRHS = True):
        """
        nontermElem - This should be a single Nonterminal instance.
        rhsElems - This must be a TokenList or a Special instance.
        metadata - Metadata to be associated with the production generated
        processRHS - Flag that will cause the rhsElems to be run through the
                     handler if set.  Set by default.
        """
        assert self.checkType(nontermElem, BasilGrammarModel.Nonterminal)
        assert ((None == metadata) or
                self.checkType(metadata, BasilGrammarModel.DataList))
        self._crntLHS = nontermElem
        lhsElem = self.factory.createProductionLHS(None, nontermElem)
        if processRHS:
            rhsListElem = self.handleModelElement(rhsElems)
        else:
            assert self.checkType(rhsElems, BasilGrammarModel.TokenList)
            rhsListElem = rhsElems
        rhsElem = self.factory.createProductionRHS(None, rhsListElem)
        if None == metadata:
            result = self.factory.createProduction(None, lhsElem, rhsElem)
        else:
            metadataElem = self.handleModelElement(metadata)
            result = self.factory.createProduction(None, metadataElem, lhsElem,
                                                   rhsElem)
        return result

    # ____________________________________________________________
    def _buildRecursiveList (self, lhsSymbol, other):
        recProdList = self.factory.createTokenList()
        if self._leftRecursive:
            recProdList.append(lhsSymbol)
            recProdList.append(other)
        else:
            recProdList.append(other)
            recProdList.append(lhsSymbol)
        return recProdList

    # ____________________________________________________________
    def _appendProduction (self, ntElem, rhsElem, procRHS = True):
        self._pendingProductions.append((ntElem, rhsElem, procRHS))

    # ____________________________________________________________
    def _insertProduction (self, ntElem, rhsElem, procRHS = True, index = 0):
        self._pendingProductions.insert(index, (ntElem, rhsElem, procRHS))

    # ____________________________________________________________
    def _insertProductions (self, ntElem, rhss, procRHS = True):
        self._pendingProductions = (map(lambda x: (ntElem, x, procRHS),
                                        rhss) + self._pendingProductions)

    # ____________________________________________________________
    def checkType (self, elem, elemType):
        """Despecializer.checkType
        Ensure the element object is of the same element type as the type
        passed.

        XXX - This is currently a hack and therefore quite brittle.
        Ideally, UserList should be derived from object, and this
        method is simply equivalent to
           type(elem) == elemType
        """
        return elem.__class__.__name__ == elemType.__name__

    # ____________________________________________________________
    def duplicate (self, modelElement, args = None):
        """Despecializer.duplicate
        Duplicates the model element, extends it with the handler results
        for its children, and returns the copy.
        """
        retVal = self.factory.duplicateElement(modelElement)
        childResults = self._handleChildren(modelElement, args)
        retVal.extend(childResults)
        return retVal

    # ____________________________________________________________
    def handleModel (self, rootModelElement, args = None):
        printprods = False
        printxml = False
        if None != args:
            if "-printxml" in args:
                printxml = True
            if "-printprods" in args:
                printprods = True
            if "-leftrec" in args:
                self._leftRecursive = True
        resultingModel = self.handleModelElement(rootModelElement)
        if printxml:
            print self.factory.externalizeXML(resultingModel)
        if printprods:
            print self.factory.externalizeProds(resultingModel)
        if self._leftRecursive:
            self._leftRecursive = False
        return resultingModel

    # ____________________________________________________________
    def handleNonterminals (self, modelElement, args = None):
        retVal = self.duplicate(modelElement)
        self.nonterminals = retVal
        return retVal

    # ____________________________________________________________
    def handleOneOf (self, modelElement, args = None):
        """Despecializer.handleOneOf
        OneOf will contain a list of TokenLists.  Return a new TokenList
        containing
        the first element in the child list, and queue the rest of the child
        list elements as new productions.
        """
        crntLHS = self._crntLHS
        firstList = modelElement[0]
        # XXX There appears to be a bug in UserList - the following is a
        # workaround for
        # self._insertProductions(crntLHS, modelElement[1:])
        self._insertProductions(crntLHS, list(modelElement)[1:])
        return self.handleModelElement(firstList, args)

    # ____________________________________________________________
    def handleGrammar (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleDataItem (self, modelElement, args = None):
        return self.duplicate(modelElement, args)
        
    # ____________________________________________________________
    def handleDataList (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleProductionLHS (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleTokenList (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleOneOrMore (self, modelElement, args = None):
        """Despecializer.handleOneOrMore
        OneOrMore will contain a TokenList.  Need to create three productions:
        symbol0 := symbol1 symbol0
                 | symbol1
        symbol1 := <Processed child TokenList>
        """
        symbol0Elem = self._crntLHS
        assert len(modelElement) == 1
        if len(modelElement[0]) > 1:
            symbol1 = self.symbolGenerator.next()
            symbol1Elem = self.factory.createNonterminal(None, name = symbol1)
            self.nonterminals.append(symbol1Elem)
            recProdElems = self._buildRecursiveList(symbol0Elem, symbol1Elem)
            # Queue pending productions
            dummyTokenList = self.factory.createTokenList(None, symbol1Elem)
            self._insertProduction(symbol0Elem, dummyTokenList)
            self._appendProduction(symbol1Elem, modelElement[0])
        else:
            symbol1Alias = self.handleModelElement(modelElement[0][0], args)
            recProdElems = self._buildRecursiveList(symbol0Elem, symbol1Alias)
            tokList = self.factory.createTokenList(None, symbol1Alias)
            self._insertProduction(symbol0Elem, tokList, False)
        return recProdElems

    # ____________________________________________________________
    def handleTerminal (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleTerminals (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleProductions (self, modelElement, args = None):
        productionsElemObj = self.factory.duplicateElement(modelElement)
        childResults = self._handleChildren(modelElement, args)
        for childResult in childResults:
            productionsElemObj.extend(childResult)
        return productionsElemObj

    # ____________________________________________________________
    def handleSpecial (self, modelElement, args = None):
        """Despecializer.handleSpecial
        """
        symbol = self.symbolGenerator.next()
        nontermElem = self.factory.createNonterminal(None, name = symbol)
        self.nonterminals.append(nontermElem)
        assert len(modelElement) == 1
        self._appendProduction(nontermElem, modelElement[0])
        return nontermElem

    # ____________________________________________________________
    def handleZeroOrOne (self, modelElement, args = None):
        """
        ZeroOrOne will contain a TokenList.  Need to create two productions:
        symbol0 := /* Empty */
                 | <Processed child TokenList>
        """
        symbol0Elem = self._crntLHS
        assert len(modelElement) == 1
        self._insertProduction(symbol0Elem, modelElement[0])
        return self.factory.createTokenList()

    # ____________________________________________________________
    def handleProductionRHS (self, modelElement, args = None):
        return self.duplicate(modelElement, args)

    # ____________________________________________________________
    def handleZeroOrMore (self, modelElement, args = None):
        """
        ZeroOrMore will contain a TokenList.  Need to create three productions:
        symbol0 := /* Empty */
                 | symbol1 symbol0
        symbol1 := <Processed child TokenList>
        """
        symbol0Elem = self._crntLHS
        assert len(modelElement) == 1
        if len(modelElement[0]) > 1:
            symbol1 = self.symbolGenerator.next()
            symbol1Elem = self.factory.createNonterminal(None, name = symbol1)
            self.nonterminals.append(symbol1Elem)
            recProdElems = self._buildRecursiveList(symbol0Elem, symbol1Elem)
            self._appendProduction(symbol1Elem, modelElement[0])
        else:
            recProdElems = self._buildRecursiveList(symbol0Elem,
                                                    modelElement[0][0])
        self._insertProduction(symbol0Elem, recProdElems)
        return self.factory.createTokenList()

    # ____________________________________________________________
    def handleProduction (self, modelElement, args = None):
        """Despecializer.handleProduction
        Handles the special case to make the following transformation:
        [(Production, [DataList_OPT, ProductionLHS,
                       (ProductionRHS, [(Special, [(OneOf, [TokenList0,
                                                            TokenList1, ...])
                                                  ])])])]
        =>
        [(Production, [DataList_OPT, ProductionLHS,
                       (ProductionRHS, [TokenList0])]),
         (Production, [ProductionLHS, (ProductionRHS, [TokenList1])]),
         ...]
        """
        result = []
        # Special case checking...
        assert self.checkType(modelElement[-1],
                              BasilGrammarModel.ProductionRHS)
        assert self.checkType(modelElement[-1][-1],
                              BasilGrammarModel.TokenList)
        # Handle the case where the top level of a production is a single
        # OneOf construct.
        if ((1 == len(modelElement[-2])) and
            (1 == len(modelElement[-1][-1])) and
            self.checkType(modelElement[-1][-1][0], BasilGrammarModel.Special)
            and self.checkType(modelElement[-1][-1][0][-1],
                               BasilGrammarModel.OneOf)):
            # In this case we don't want to synthesize a new symbol, we just
            # want to break each subcase into a new production (basically
            # doing what handleOneOf does without using a new LHS symbol.)
            # XXX - Note this is going to something funky with any metadata
            lhsElemObj = self.duplicate(modelElement[-2][0])
            oneOfElem = modelElement[-1][-1][0][-1]
            if len(modelElement) == 3:
                metadata = modelElement[0]
            else:
                metadata = None
            productionElemObj = self._buildProduction(lhsElemObj, oneOfElem[0],
                                                      metadata)
            result.append(productionElemObj)
            self._insertProductions(lhsElemObj, list(oneOfElem)[1:])
        else:
            productionElemObj = self.duplicate(modelElement)
            result.append(productionElemObj)
        result.extend(self._handlePendingProductions())
        return result

    # ____________________________________________________________
    def handleNonterminal (self, modelElement, args = None):
        return self.duplicate(modelElement)

# ______________________________________________________________________
def getModelHandler ():
    return Despecializer

# ______________________________________________________________________
# End of Despecializer.py

