#! /usr/bin/env python
# ______________________________________________________________________
"""Module Testerizer

$Id: Testerizer.py 10042 2005-03-21 23:32:41Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import string, exceptions, pprint

# XXX Would like to do something like:
# from basil.modeling import ModelTools

from basil.models.grammar import BasilGrammarModel
from basil.models.grammar import GrammarUtils
from basil.models.grammar import Despecializer

# ______________________________________________________________________
# Module variable definitions

__DEBUG__ = False
__VERBOSE__ = False

# ______________________________________________________________________
# Module function and class definitions

#______________________________________________________________________
class StopSearch (exceptions.Exception):
    # ____________________________________________________________
    def __init__ (self, result):
        self.result = result
        exceptions.Exception.__init__(self)

    # ____________________________________________________________
    def getResult (self):
        return self.result

# ______________________________________________________________________
class TesterizerGrammar (object):
    """Class TesterizerGrammar

    Member variables:
     * nonterminals - List of nonterminal symbols in the grammar.
     * terminals - List of terminal symbols in the grammar.
     * productionMap - Map from a nonterminal symbol to a list of list of
       symbols (each sub-list represents the RHS of a production of the given
       LHS index).
    """
    # ____________________________________________________________
    def __init__ (self, productionMap = None):
        """TesterizerGrammar.__init__
        """
        if None == productionMap:
            productionMap = {}
        self.nonterminals = productionMap.keys()[:]
        self.nonterminals.sort()
        self.terminals = []
        for productionRHSList in productionMap.values():
            for productionRHS in productionRHSList:
                for symbol in productionRHS:
                    if not productionMap.has_key(symbol):
                        self.terminals.append(symbol)
        self.terminals.sort()
        self.productionMap = productionMap

    # ____________________________________________________________
    def __isAllTerminals (self, symbolList):
        """TesterizerGrammar.isAllTerminals
        Return True if all symbols in the passed list are terminal symbols.
        False if there is one or more nonterminal symbols in the list.
        """
        for symbol in symbolList:
            if self.productionMap.has_key(symbol):
                return False
        return True

    # ____________________________________________________________
    def __handleString (self, newString, costFn, oldStrs, newBranches):
        """TesterizerGrammar.__handleString
        """
        if self.__isAllTerminals(newString):
            raise StopSearch(newString)
        elif newString not in oldStrs:
            newCost = costFn(newString)
            newBranch = (newCost, newString)
            newBranches.append(newBranch)
            oldStrs.append(newString)

    # ____________________________________________________________
    def __handleNewSymList (self, newSymbolList, costFn, branches):
        if self.__isAllTerminals(newSymbolList):
            raise StopSearch(newSymbolList)
        else:
            newCost = costFn(newSymbolList)
            i = 0
            imax = len(branches)
            while i < imax and branches[i][0] < newCost:
                i += 1
            branches.insert(i, (newCost, newSymbolList))

    # ____________________________________________________________
    def __getApplicableProductions (self,
                                    symbolList,
                                    terminalSymbolListMap = None,
                                    symbolIndexMap = None):
        """TesterizerGrammar.__getApplicableProductions

        Returns a list of tuples of the form: (symbol, (symbol...))
        Each tuple represents a LHS/RHS pair of a grammar production or
        nonterminal symbol to terminal symbol list that could be applied to
        the symbol list input.
        """
        assert ((None == terminalSymbolListMap) or
                (type(terminalSymbolListMap == type({}))))
        result = []
        index = 0
        for symbol in symbolList:
            if self.productionMap.has_key(symbol):
                if ((terminalSymbolListMap != None) and
                    (terminalSymbolListMap[symbol] != None)):
                    productionTuple = (symbol,
                                       tuple(terminalSymbolListMap[symbol]))
                    if productionTuple not in result:
                        result.append(productionTuple)
                        if None != symbolIndexMap:
                            symbolIndexMap.append([index])
                    elif None != symbolIndexMap:
                        prodIndex = result.index(productionTuple)
                        symbolIndexMap[prodIndex].append(index)
                else:
                    for productionRHS in self.productionMap[symbol]:
                        productionTuple = (symbol, tuple(productionRHS))
                        if productionTuple not in result:
                            result.append(productionTuple)
                            if None != symbolIndexMap:
                                symbolIndexMap.append([index])
                        elif None != symbolIndexMap:
                            prodIndex = result.index(productionTuple)
                            symbolIndexMap[prodIndex].append(index)
            index += 1
        return result

    # ____________________________________________________________
    def __buildTerminalSymbolList (self,
                                   nonterminal,
                                   terminalSymbolListMap,
                                   costFunction):
        """TesterizerGrammar.__buildTerminalSymbolList
        """
        try:
            branches = [(10, [ nonterminal ])]
            stringList = { nonterminal : True }
            while len(branches) > 0:
                branchCost, branchSymbolList = branches[0]
                if __DEBUG__:
                    print ("   %s, branches %d, cost %d" %
                           (nonterminal, len(branches), branchCost))
                del branches[0]
                # XXX bc = (branchCost - costFunction(branchSymbolList)) + 5
                bc = 0
                astarCostFn = lambda x: costFunction(x) + bc
                indexMap = []
                productionList = self.__getApplicableProductions(
                    branchSymbolList, terminalSymbolListMap, indexMap)
                productionIndex = 0
                for (lhs, rhs) in productionList:
                    for symbolIndex in indexMap[productionIndex]:
                        newSymbolList = (branchSymbolList[:symbolIndex] +
                                         list(rhs) +
                                         branchSymbolList[symbolIndex + 1:])
                        newString = string.join(newSymbolList, " ")
                        if not stringList.has_key(newString):
                            self.__handleNewSymList(newSymbolList,
                                                    astarCostFn, branches)
                            stringList[newString] = True
                    productionIndex += 1
            assert False, ("Could not resolve string for %s!  This should "
                           "never happen." % nonterminal)
        except StopSearch, obj:
            terminalSymbolListMap[nonterminal] = obj.getResult()

    # ____________________________________________________________
    def buildTerminalMapping (self, costFunction = None):
        """TesterizerGrammar.buildTerminalMapping
        """
        terminalSymbolListMap = {}
        if None == costFunction:
            costFunction = len
        for nonterminal in self.nonterminals:
            terminalSymbolListMap[nonterminal] = None
        for nonterminal in self.nonterminals:
            self.__buildTerminalSymbolList(nonterminal,
                                           terminalSymbolListMap,
                                           costFunction)
        return terminalSymbolListMap

    # ____________________________________________________________
    def spanProductions (self,
                         startTok,
                         minApplications = 2,
                         productionUseMap = {},
                         productionAppMap = None):
        """TesterizerGrammar.spanProductions
        """
        result = []
        crntSymbolListList = [ ( [ startTok ], [] ) ]
        nextSymbolListList = []
        while len(crntSymbolListList) > 0:
            if __DEBUG__:
                print ("   Spanning;  Current ply size: %d, Results: %d" %
                       (len(crntSymbolListList), len(result)))
            for symbolList, prodAppList in crntSymbolListList:
                symbolIndexMap = []
                prods = self.__getApplicableProductions(
                    symbolList, symbolIndexMap = symbolIndexMap)
                prodIndex = 0
                for prodTup in prods:
                    if not productionUseMap.has_key(prodTup):
                        productionUseMap[prodTup] = 0
                    for symbolListIndex in symbolIndexMap[prodIndex]:
                        if productionUseMap[prodTup] >= minApplications:
                            symbolTuple = tuple(symbolList)
                            if symbolTuple not in result:
                                result.append(symbolTuple)
                                if None != productionAppMap:
                                    prodAppList.append((symbolListIndex,
                                                        prodTup))
                                    productionAppMap[symbolTuple] = prodAppList
                        else:
                            productionUseMap[prodTup] += 1
                            newSymbolList = (symbolList[:symbolListIndex] +
                                             list(prodTup[1]) +
                                             symbolList[symbolListIndex + 1:])
                            newProdAppList = prodAppList[:]
                            newProdAppList.append((symbolListIndex, prodTup))
                            nextSymbolListList.append((newSymbolList,
                                                       newProdAppList))
                    prodIndex += 1
            crntSymbolListList = nextSymbolListList
            nextSymbolListList = []
        return result

# ______________________________________________________________________

class Testerizer:
    """Class Testerizer
    This is basically a sham handler class for a grammar model that fronts for
    the test string generation code.
    """
    # ____________________________________________________________
    def handleModel (self, model, args = None):
        """Testerizer.handleModel
        """
        global __DEBUG__, __VERBOSE__
        if "-debug" in args:
            __DEBUG__ = True
        if "-verbose" in args:
            __VERBOSE__ = True
        despecializer = Despecializer.getModelHandler()()
        factory = despecializer.factory
        despecializedModel = despecializer.handleModel(model)
        productionMap = factory.externalizeProdMap(despecializedModel)
        if __DEBUG__:
            pprint.pprint(productionMap)
        startTok = GrammarUtils.findStartSymbol(model)
        print "Starting token:", startTok
        testerGrammarModel = TesterizerGrammar(productionMap)
        def myCostFunction (symbolList):
            cost = 0
            for symbol in symbolList:
                if productionMap.has_key(symbol):
                    cost += 11
                else:
                    cost += 10
            return cost
        nontermToTermsMap = testerGrammarModel.buildTerminalMapping(
            myCostFunction)
        if __DEBUG__ or __VERBOSE__:
            pprint.pprint(nontermToTermsMap)
        productionUseMap = {}
        productionAppMap = {}
        symbolTupleList = testerGrammarModel.spanProductions(
            startTok, productionUseMap = productionUseMap,
            productionAppMap = productionAppMap)
        index = 0
        if __DEBUG__ or __VERBOSE__:
            print "_" * 70
            for symbolTuple in symbolTupleList:
                print "%d. %s" % (index, symbolTuple)
                pprint.pprint(productionAppMap[symbolTuple])
                print "_" * 60
                index += 1
        if __DEBUG__:
            pprint.pprint(productionUseMap)
        if __VERBOSE__:
            print "_" * 70
        def nontermToTermMapFn (symbol):
            if nontermToTermsMap.has_key(symbol):
                return string.join(nontermToTermsMap[symbol])
            return symbol
        index = 0
        for symbolTuple in symbolTupleList:
            testString = ""
            testSymbolList = map(nontermToTermMapFn, symbolTuple)
            while (len(testSymbolList) > 0) and ('' == testSymbolList[0]):
                del testSymbolList[0]
            if len(testSymbolList) > 0:
                testString = "%s" % testSymbolList[0]
                for symbol in testSymbolList[1:]:
                    if len(symbol) > 0:
                        testString += " %s" % symbol
            if __VERBOSE__:
                print "%d." % (index,),
            print testString
            index += 1
        return None

# ______________________________________________________________________

def getModelHandler ():
    return Testerizer

# ______________________________________________________________________

def main ():
  pass

# ______________________________________________________________________

if __name__ == "__main__":
  main()

# ______________________________________________________________________
# End of Testerizer.py
