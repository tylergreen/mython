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

FORMAT_MAP = {
    'pgen' : 'PGEN',
    'bison' : 'Y',
    'bnf' : 'BNF',
    'tree' : 'Tree',
    'xml' : 'XML',
    'mlyacc' : 'GRM',
    }

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

class ModelInternalizationError (Exception):
    """Class ModelInternalizationError
    Exception class thrown by getModel() if it has a problem.
    """

# ______________________________________________________________________

def getModel (inFile, inFormat = None, modelFactory = None):
    """getModel()
    Simply a hook for model internalization to a BasilGrammarModel instance.
    See the Basil Grammar Model and its internalize() method, most likely
    inherrited from BaseModelFactory."""
    retVal = None
    if inFormat == None:
        if inFile == None:
            raise ModelInternalizationError("Can not guess stdin format if "
                                            "none is specified.")
        else:
            import os.path
            _, ext = os.path.splitext(inFile)
            format = ext[1:].upper()
    elif FORMAT_MAP.has_key(inFormat):
        format = FORMAT_MAP[inFormat]
    else:
        raise ModelInternalizationError("Invalid model format: %s" % inFormat)
    if modelFactory is None:
        modelFactory = BasilGrammarModel.getModelFactory()()
    if inFile == None:
        targetFile = sys.stdin
    else:
        targetFile = open(inFile, "r")
    try:
        retVal = modelFactory.internalize(format, targetFile)
    finally:
        if inFile != None:
            targetFile.close()
    return retVal

# ______________________________________________________________________

def main ():
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of GrammarUtils.py
