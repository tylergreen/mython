#! /usr/bin/env python
# ______________________________________________________________________
"""Module BaseModelHandler.py

Defines the base class for model handlers.

$Id: BaseModelHandler.py 12206 2005-05-11 23:25:13Z jriehl $
"""
# ______________________________________________________________________
# Module imports.

import string

# ______________________________________________________________________

class BaseModelHandler (object):
    """Class BaseModelHandler
    """
    # ____________________________________________________________
    def handleModel (self, rootModelElement, args = None):
        """BaseModelHandler.handleModel
        The main handler routine for any BaseModelHandler derived class.
        Overload this to add preprocessing and postprocessing actions.
        """
        return self.handleModelElement(rootModelElement, args)

    # ____________________________________________________________
    def handleModelElement (self, modelElement, args = None):
        """BaseModelHandler.handleModelElement
        """
        elementName = modelElement.__class__.__name__
        methodPostfix = string.upper(elementName[0]) + elementName[1:]
        preHandlerName = "handle%s" % methodPostfix
        if hasattr(self, preHandlerName):
            handlerMethod = getattr(self, preHandlerName)
            return handlerMethod(modelElement, args)
        return None

    # ____________________________________________________________
    def _handleChildren (self, modelElement, args = None):
        """BaseModelHandler._handleChildren
        Dispatch the children of the current element to their respective
        handlers.
        """
        results = []
        for childElement in modelElement:
            childResult = self.handleModelElement(childElement, args)
            results.append(childResult)
        return results

# ______________________________________________________________________

def getModelHandler ():
    return BaseModelHandler

# ______________________________________________________________________
# End of BaseModelHandler.py
        
        
        
