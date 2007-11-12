#! /usr/bin/env python
# ______________________________________________________________________
"""Module GrammarUtils
Defines some basic utility functions for grammar models.

$Id: GrammarUtils.py 10042 2005-03-21 23:32:41Z jriehl $
"""
# ______________________________________________________________________
# Module imports

from basil.models.grammar import BasilGrammarModel

# ______________________________________________________________________
# Module data

__DEBUG__ = False

if __DEBUG__:
    import sys

# ______________________________________________________________________

def checkType (modelElement, ElementClass):
    """checkType
    XXX - Move me to a ModelUtils module in the modeling package?
    And/or fix Basil so type(modelElement) == ElementClass works...
    """
    return modelElement.__class__.__name__ == ElementClass.__name__

# ______________________________________________________________________

def findStartSymbol (model):
    """findStartSymbol
    Return the start symbol.
    """
    if __DEBUG__:
        print >> sys.stderr, "findStartSymbol()"
    retVal = None
    foundStart = False
    assert checkType(model, BasilGrammarModel.Grammar)
    # First check to see if there is a data item associated with the
    # grammar that denotes the start symbol.
    if (checkType(model[0], BasilGrammarModel.DataList) and
        (len(model[0]) > 0)):
        for dataItem in model[0]:
            assert checkType(dataItem, BasilGrammarModel.DataItem)
            if dataItem.tag == "start":
                if __DEBUG__:
                    print >> sys.stderr, ("findStartSymbol(): Found start "
                                          "metadata item.")
                assert len(dataItem) > 0
                assert checkType(dataItem[0], BasilGrammarModel.Nonterminal)
                retVal = dataItem[0].name
                foundStart = True
                break
    if foundStart == False:
        # Otherwise return the first symbol we see in a LHS
        assert checkType(model[-1], BasilGrammarModel.Productions)
        assert len(model[-1]) > 0
        assert checkType(model[-1][0], BasilGrammarModel.Production)
        assert checkType(model[-1][0][-2], BasilGrammarModel.ProductionLHS)
        assert len(model[-1][0][-2]) > 0
        assert checkType(model[-1][0][-2][0], BasilGrammarModel.Nonterminal)
        retVal = model[-1][0][-2][0].name
    return retVal

# ______________________________________________________________________

def main ():
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of GrammarUtils.py
