#! /usr/bin/env python
# ______________________________________________________________________
"""Module PyPatActionizer

Defines a handler class that converts productions in a grammar model to PyPat
actions.

Note: Parts were automatically generated using basil/modeling/DTD2PyHandler.py

Jonathan Riehl

$Id: PyPatActionizer.py 12226 2005-05-13 00:03:19Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import string
from basil.modeling.BaseModelHandler import BaseModelHandler

# ______________________________________________________________________
# Module utility functions
# XXX - Consider moving these out of here; they don't belong here.

def getArg (args, argName):
    """getArg()
    Stupid utility function for getting arguments passed to a handler function.
    """
    retVal = None
    if (args != None) and (args.has_key(argName)):
        retVal = args[argName]
    return retVal

# ______________________________________________________________________

def setArg (args, key, value):
    """setArg()
    Stupid utility function for setting arguments within a handler function.
    """
    if args == None:
        args = {}
    else:
        args = args.copy()
    args[key] = value
    return args

# ______________________________________________________________________

def matchesTup (elem, tup):
    """matchesTup()
    XXX Perhaps a herald of the future?  A herald that should be moved?
    """
    retVal = True
    tName, tChildren = tup
    if elem.elementName != tName:
        retVal = False
    else:
        if tChildren != None:
            if len(tChildren) != len(elem):
                retVal = False
            else:
                i1 = iter(elem)
                i2 = iter(tChildren)
                try:
                    while retVal == True:
                        retVal = matchesTup(i1.next(), i2.next())
                except StopIteration:
                    pass
    return retVal

# ______________________________________________________________________
# Handler class definition

class PyPatActionizer (BaseModelHandler):
    # ____________________________________________________________
    def handleDataItem (self, modelElement, args = None):
        # Insert prefix actions here.
        childResults = self._handleChildren(modelElement, args)
        # Insert postfix actions here.
        return childResults

    # ____________________________________________________________
    def handleDataList (self, modelElement, args = None):
        return ""

    # ____________________________________________________________
    def handleGrammar (self, modelElement, args = None):
        # Insert prefix actions here.
        childResults = self._handleChildren(modelElement, args)
        # Insert postfix actions here.
        return string.join(childResults, "")

    # ____________________________________________________________
    def handleNonterminal (self, modelElement, args = None):
        """handleNonterminal()
        """
        retVal = None
        emit = not getArg(args, "extendedActions")
        if emit == True:
            retVal = "match %s:\n    pass\n\n" % modelElement.name
        else:
            retVal = modelElement.name
        return retVal

    # ____________________________________________________________
    def handleNonterminals (self, modelElement, args = None):
        retVal = ""
        emit = not getArg(args, "extendedActions")
        if emit == True:
            childResults = self._handleChildren(modelElement, args)
            retVal = string.join(childResults, "")
        return retVal

    # ____________________________________________________________
    def handleOneOf (self, modelElement, args = None):
        # Insert prefix actions here.
        childResults = self._handleChildren(modelElement, args)
        # Insert postfix actions here.
        return string.join(childResults, " | ")

    # ____________________________________________________________
    def handleOneOrMore (self, modelElement, args = None):
        assert len(modelElement) == 1
        retVal = "%s+" % self.handleModelElement(modelElement[0], args)
        return retVal

    # ____________________________________________________________
    def handleProduction (self, modelElement, args = None):
        """handleProduction()
        Note: This method already assumes that emission was cleared by the
        handleProductions() method, and does not check the arguments.
        """
        retVal = ""
        lhs, rhs = [child for child in modelElement
                    if child.elementName in ("ProductionLHS", "ProductionRHS")]
        # Ensure element contents are well ordered.
        assert lhs.elementName == "ProductionLHS"
        lhsName = self.handleModelElement(lhs, args)
        rhsArgs = setArg(args, "lhsName", lhsName)
        retVal = self.handleModelElement(rhs, rhsArgs)
        return retVal

    # ____________________________________________________________
    def handleProductionLHS (self, modelElement, args = None):
        if len(modelElement) != 1:
            raise PyPatActionizerError("The grammar is not a context free "
                                       "grammar!")
        else:
            retVal = self.handleModelElement(modelElement[0], args)
        return retVal

    # ____________________________________________________________
    def handleProductionRHS (self, modelElement, args = None):
        """handleProductionRHS()
        Note: This method already assumes that emission was cleared by the
        handleProductions() method, and does not check the arguments.
        """
        retVal = ""
        if matchesTup(modelElement, ("ProductionRHS",
                                     [("TokenList",
                                       [("Special", [("OneOf", None)])])])):
            # Split each element of the OneOf list into its own thing.
            oneOfElem = modelElement[0][0][0]
            childResults = []
            for child in oneOfElem:
                childResult = self.handleModelElement(child, args)
                if childResult[0] != "(":
                    childResult = "(%s)" % childResult
                childResults.append("match %s%s:\n    pass\n\n" %
                                    (args["lhsName"], childResult))
            retVal = string.join(childResults, "")
        else:
            childResult = string.join(self._handleChildren(modelElement, args),
                                      "")
            if childResult[0] != "(":
                childResult = "(%s)" % childResult
            retVal = "match %s%s:\n    pass\n\n" % (args["lhsName"],
                                                    childResult)
        return retVal

    # ____________________________________________________________
    def handleProductions (self, modelElement, args = None):
        """handleProductions()
        """
        retVal = ""
        emit = getArg(args, "extendedActions")
        if emit == True:
            childResults = self._handleChildren(modelElement, args)
            retVal = string.join(childResults, "")
        return retVal

    # ____________________________________________________________
    def handleSpecial (self, modelElement, args = None):
        """handleSpecial()
        Just return the result of handling the single contained child element.
        """
        assert len(modelElement) == 1
        return self.handleModelElement(modelElement[0], args)

    # ____________________________________________________________
    def handleTerminal (self, modelElement, args = None):
        return modelElement.name

    # ____________________________________________________________
    def handleTerminals (self, modelElement, args = None):
        return ""

    # ____________________________________________________________
    def handleTokenList (self, modelElement, args = None):
        retVal = ""
        myLen = len(modelElement)
        if myLen > 1:
            childResults = self._handleChildren(modelElement, args)
            retVal = "(%s)" % (string.join(childResults, ", "))
        elif myLen == 1:
            retVal = self.handleModelElement(modelElement[0], args)
        return retVal

    # ____________________________________________________________
    def handleZeroOrMore (self, modelElement, args = None):
        assert len(modelElement) == 1
        retVal = "%s*" % (self.handleModelElement(modelElement[0], args))
        return retVal

    # ____________________________________________________________
    def handleZeroOrOne (self, modelElement, args = None):
        assert len(modelElement) == 1
        childResult = self.handleModelElement(modelElement[0], args)
        if childResult[0] == "(" and childResult[-1] == ")":
            childResult = childResult[1:-1]
        retVal = "[%s]" % (childResult)
        return retVal

# ______________________________________________________________________

def getModelHandler ():
    return PyPatActionizer

# ______________________________________________________________________
# End of PyPatActionizer.py

