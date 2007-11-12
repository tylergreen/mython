#! /usr/bin/env python
# ______________________________________________________________________

import types
import string
from UserList import UserList
from basil.modeling.BaseModelFactory import BaseModelFactory

# ______________________________________________________________________
class Nonterminals (UserList):
    elementName = "Nonterminals"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class OneOf (UserList):
    elementName = "OneOf"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Grammar (UserList):
    elementName = "Grammar"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class DataItem (UserList):
    elementName = "DataItem"
    def __init__ (self):
        UserList.__init__(self)
        self.tag = None

# ______________________________________________________________________
class DataList (UserList):
    elementName = "DataList"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class ProductionLHS (UserList):
    elementName = "ProductionLHS"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class TokenList (UserList):
    elementName = "TokenList"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class OneOrMore (UserList):
    elementName = "OneOrMore"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Terminal (UserList):
    elementName = "Terminal"
    def __init__ (self):
        UserList.__init__(self)
        self.name = None

# ______________________________________________________________________
class Terminals (UserList):
    elementName = "Terminals"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Productions (UserList):
    elementName = "Productions"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Special (UserList):
    elementName = "Special"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class ZeroOrOne (UserList):
    elementName = "ZeroOrOne"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class ProductionRHS (UserList):
    elementName = "ProductionRHS"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class ZeroOrMore (UserList):
    elementName = "ZeroOrMore"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Production (UserList):
    elementName = "Production"
    def __init__ (self):
        UserList.__init__(self)

# ______________________________________________________________________
class Nonterminal (UserList):
    elementName = "Nonterminal"
    def __init__ (self):
        UserList.__init__(self)
        self.name = None

# ______________________________________________________________________
class BasilGrammarModelFactory (BaseModelFactory):
    # ____________________________________________________________
    def __init__ (self):
        self.elements = {'Nonterminals': {}, 'OneOf': {}, 'Grammar': {}, 'DataItem': {'tag': 'tag'}, 'Terminals': {}, 'DataList': {}, 'ProductionLHS': {}, 'OneOrMore': {}, 'Terminal': {'name': 'name'}, 'TokenList': {}, 'Productions': {}, 'Nonterminal': {'name': 'name'}, 'ZeroOrOne': {}, 'ProductionRHS': {}, 'ZeroOrMore': {}, 'Production': {}, 'Special': {}}

    # ____________________________________________________________
    def createNonterminals (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Nonterminals, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createOneOf (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(OneOf, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createGrammar (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Grammar, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createDataItem (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(DataItem, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createDataList (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(DataList, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createProductionLHS (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(ProductionLHS, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createTokenList (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(TokenList, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createOneOrMore (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(OneOrMore, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createTerminal (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Terminal, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createTerminals (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Terminals, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createProductions (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Productions, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createSpecial (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Special, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createZeroOrOne (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(ZeroOrOne, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createProductionRHS (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(ProductionRHS, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createZeroOrMore (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(ZeroOrMore, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createProduction (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Production, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def createNonterminal (self, elementData = None, *elementChildren, **extraAttrs):
        return self._processElement(Nonterminal, elementData, elementChildren, extraAttrs)

    # ____________________________________________________________
    def internalizeBNF (self, stream):
        """BasilGrammarModelFactory.internalizeBnf
        """
        from basil.parsing import bnf
        from basil.models.grammar.InternalizeBNF import BNFInternalizer
        if type(stream) == types.StringType:
            text = stream
        else:
            text = stream.read()
        grammarMap = bnf.get_prods(text)
        internalizer = BNFInternalizer(self)
        return internalizer(grammarMap)

    # ____________________________________________________________
    def internalizePGEN (self, stream):
        """BasilGrammarModelFactory.internalizePgen
        """
        from basil.parsing import PgenParser
        from basil.models.grammar.InternalizePgen import PgenInternalizer
        if type(stream) == types.StringType:
            text = stream
        else:
            text = stream.read()
        parse = PgenParser.parseString(text)
        internalizer = PgenInternalizer(self)
        return internalizer(parse)

    # ____________________________________________________________
    def internalizeY (self, stream):
        """BasilGrammarModelFactory.internalizeY
        Internalize a Bison grammar specification.
        XXX The BisonParser needs some serious modifications, and this will
        have to change to suit that refactoring.
        """
        from basil.parsing import BisonParser
        from basil.models.grammar.InternalizeBison import BisonInternalizer
        if type(stream) == types.StringType:
            text = stream
        else:
            text = stream.read()
        parser = BisonParser.BisonParser(text)
        parser.parse()
        internalizer = BisonInternalizer(self)
        prodList = map(lambda prodData : (prodData[1], prodData[2]),
                       parser.productions)
        return internalizer((parser.startVal, prodList))

    # ____________________________________________________________
    def externalizeProds (self, model):
        """BasilGrammarModelFactory.externalizeProds
        XXX - I am not sure this belongs here; I am using this as a simple
        utility to evaluate performance of the Despecializer processor.
        """
        self._text = ""
        assert model.__class__ == Grammar
        for prod in model[-1]:
            # XXX - UserList workaround
            prod = list(prod)
            lhs, rhs = prod[-2:]
            lhs = string.join(map(lambda x: x.name, lhs), " ")
            rhs = string.join(map(lambda x: x.name, rhs[0]), " ")
            self._text += "%s -> %s\n" % (lhs, rhs)
        text = self._text
        del self._text
        return text

    # ____________________________________________________________
    def externalizeProdMap (self, model):
        """BasilGrammarModelFactory.externalizeProdMap
        XXX - This is another iffy method for utility grammar representations
        with the exception that this is used for the Testerizer, a far cooler
        handler than the Despecializer!
        """
        productionMap = {}
        assert model.__class__ == Grammar
        for prod in model[-1]:
            prod = list(prod)
            lhs, rhs = prod[-2:]
            assert len(lhs) == 1
            lhsSymbol = lhs[0]
            if not productionMap.has_key(lhsSymbol.name):
                productionMap[lhsSymbol.name] = []
            productionMap[lhsSymbol.name].append(map(lambda x: x.name, rhs[0]))
        return productionMap

# ______________________________________________________________________
def getModelFactory ():
    return BasilGrammarModelFactory

# ______________________________________________________________________
# End of BasilGrammarModel.py

