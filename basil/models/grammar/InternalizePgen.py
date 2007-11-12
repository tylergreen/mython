#! /usr/bin/env python
# ______________________________________________________________________
"""Module InternalizePgen

This moduel defines the PgenInternalizer class.  Instances of the
PgenInternalizer class are callable objects that translate a pgen AST into a
Basil grammar model.

When called from the command line, the module accepts an optional file name of
a pgen grammar file.  If no file name is given, a pgen input grammar will be
read from stdin.  The module will translate the pgen input to a Basil grammar
model, serialize the model in XML, and output the XML to stdout.

$Id: InternalizePgen.py 2765 2004-01-15 01:25:51Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import sys
import token
from basil.parsing import PgenParser
from basil.models.grammar import BaseInternalizer, BasilGrammarModel

# ______________________________________________________________________

class PgenInternalizer (BaseInternalizer.BaseInternalizer):
    """Class PgenInternalizer
    Instances of PgenInternalizer are callable objects that Create a Basil
    grammar model instance from an input pgen AST.
    """
    # ____________________________________________________________
    def __call__ (self, pgenAst):
        """PgenInternalizer.__call__
        """
        self._initializeModel()
        self.handleStart(pgenAst)
        return self.crntGrammar

    # ____________________________________________________________
    def handleStart (self, ast):
        """PgenInternalizer.handleStart
        Handle a start node in a Pgen parse tree.
        
        XXX Note that I am duplicating code from PyPgen, which is unhappy.
        I do face, however, a chicken and egg problem with building walkers to
        create walkers.
        """
        type, children = ast
        assert type == PgenParser.MSTART
        # Unfortunately, this requires two passes to infer terminals...
        for child in children:
            if child[0] == PgenParser.RULE:
                name, colon, rhs, newline = child[1]
                assert name[0][0] == token.NAME
                self.nonterminalMap[name[0][1]] = None
        # Now we can proceed since we know which symbols are terminal and
        # nonterminal.
        for child in children:
            if child[0] == PgenParser.RULE:
                self.crntProductions.append(self.handleRule(child))

    # ____________________________________________________________
    def handleRule (self, ast):
        """PgenInternalizer.handleRule
        """
        type, children = ast
        assert type == PgenParser.RULE
        name, colon, rhs, newline = children
        lhsElem = self.factory.createProductionLHS(None,
                                                   self._getSymbol(name[0][1]))
        rhsElem = self.factory.createProductionRHS(None,
                                                   self.handleRhs(rhs))
        return self.factory.createProduction(None, lhsElem, rhsElem)

    # ____________________________________________________________
    def handleRhs (self, ast):
        """PgenInternalizer.handleRhs

        This will supposedly always return a TokenList model element.
        """
        type, children = ast
        assert type == PgenParser.RHS
        retVal = self.handleAlt(children[0])
        if len(children) > 1:
            altElem = self.factory.createOneOf(None, retVal)
            for child in children[2:]:
                if child[0] == PgenParser.ALT:
                    altElem.append(self.handleAlt(child))
            specialElem = self.factory.createSpecial(None, altElem)
            retVal = self.factory.createTokenList(None, specialElem)
        return retVal

    # ____________________________________________________________
    def handleAlt (self, ast):
        """PgenInternalizer.handleAlt

        This will supposedly always return a TokenList model element.
        """
        type, children = ast
        assert type == PgenParser.ALT
        retVal = self.factory.createTokenList()
        for child in children:
            retVal.extend(self.handleItem(child))
        return retVal

    # ____________________________________________________________
    def handleItem (self, ast):
        """PgenInternalizer.handleItem

        This will supposedly always return a list of model element that can be
        contained by a TokenList element (currently: Nonterminal or Terminal
        or Special).
        """
        type, children = ast
        assert type == PgenParser.ITEM
        retVal = None
        if children[0][0] != PgenParser.ATOM:
            assert children[0][0][0] == token.LSQB
            rhsElem = self.handleRhs(children[1])
            optElem = self.factory.createZeroOrOne(None, rhsElem)
            specElem = self.factory.createSpecial(None, optElem)
            retVal = [specElem]
        else:
            atomElem = self.handleAtom(children[0])
            if len(children) == 1:
                retVal = atomElem
            else:
                assert len(children) == 2
                containerElem = self.factory.createTokenList()
                containerElem.extend(atomElem)
                if children[1][0][0] == token.STAR:
                    numElem = self.factory.createZeroOrMore(None,
                                                            containerElem)
                else:
                    assert children[1][0][0] == token.PLUS
                    numElem = self.factory.createOneOrMore(None,
                                                           containerElem)
                specElem = self.factory.createSpecial(None, numElem)
                retVal = [specElem]
        return retVal

    # ____________________________________________________________
    def handleAtom (self, ast):
        """PgenInternalizer.handleAtom
        """
        ntype, children = ast
        assert ntype == PgenParser.ATOM
        if children[0][0][0] == token.LPAR:
            assert len(children) == 3
            # By simply converting the TokenList element, returned by
            # handleRhs(), to a real list, we effectively flatten the nested
            # TokenList.
            retVal = list(self.handleRhs(children[1]))
        else:
            retVal = [self._getSymbol(children[0][0][1])]
        return retVal

# ______________________________________________________________________

def main (fileName = None):
    """main
    Read a pgen input grammar from the given file name.  If no file name is
    given, read the grammar from stdin.  Print a XML document for the
    resulting grammar model translation.
    """
    if None == fileName:
        parseTree = PgenParser.parseString(sys.stdin.read())
    else:
        parseTree = PgenParser.parseFile(fileName)
    grammarFactoryClass = BasilGrammarModel.getModelFactory()
    grammarFactory = grammarFactoryClass()
    internalizer = PgenInternalizer(grammarFactory)
    model = internalizer(parseTree)
    print grammarFactory.externalizeXML(model)

# ______________________________________________________________________

if __name__ == "__main__":
    fileName = None
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
    main(fileName)

# ______________________________________________________________________
# End of InternalizePgen.py
