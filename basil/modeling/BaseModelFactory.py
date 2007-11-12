#! /usr/bin/env python
# ______________________________________________________________________
"""Module BaseModelFactory.py

Defines the base class for model factories.

$Id: BaseModelFactory.py 2765 2004-01-15 01:25:51Z jriehl $
"""
# ______________________________________________________________________
# Module imports.

import types
import string
import UserList
from basil.utils import TreeUtils
from basil.xml import XML2Tree

# ______________________________________________________________________

class BaseModelFactory (object):
    """Class BaseModelFactory
    """
    # ____________________________________________________________
    def __init__ (self):
        """BaseModelFactory.__init__
        """
        raise "Override Me!"

    # ____________________________________________________________
    def externalize (self, format, modelObject):
        """BaseModelFactory.externalize
        """
        handlerMethod = getattr(self, "externalize" + format)
        return handlerMethod(modelObject)

    # ____________________________________________________________
    def externalizeTree (self, modelObject):
        """BaseModelFactory.externalizeTree
        """
        childList = []
        for childObject in modelObject:
            childList.append(self.externalizeTree(childObject))
        elementName = modelObject.__class__.__name__
        elementAttrs = {}
        elementAttrMap = {}
        # XXX As noted in the factory generator (DTD2PyModel,) multiple
        # attributes may map to one Python attribute, and this mapping
        # inversion will only output the one such Python attribute to one of
        # its mappings.
        for item in self.elements[elementName].items():
            elementAttrMap[item[1]] = item[0]
        for attrItem in modelObject.__dict__.items():
            pyAttrName, pyValue = attrItem
            if elementAttrMap.has_key(pyAttrName):
                attrName = elementAttrMap[pyAttrName]
                # XXX Need some conversion routine, esp for things that should
                # be mapped to entities.
                elementAttrs[attrName] = pyValue
        return ((elementName, elementAttrs), childList)

    # ____________________________________________________________
    def externalizeXML (self, modelObject):
        """BaseModelFactory.externalizeXML
        """
        externalTree = self.externalizeTree(modelObject)
        self._text = ""
        TreeUtils.depthTraverse(externalTree, self._openTreeXMLTag,
                                self._closeTreeXMLTag)
        text = self._text
        del self._text
        return text
    
    # ____________________________________________________________
    def _openTreeXMLTag (self, treeNode, depth):
        """BaseModelFactory._externalizeTreeToXML
        """
        elementData = treeNode[0]
        attrText = ""
        for attrItem in elementData[1].items():
            attrText = attrText + (' %s="%s"' % (attrItem[0],
                                                 str(attrItem[1])))
        if len(treeNode[1]) > 0:
            endText = ""
        else:
            endText = "/"
        self._text = self._text + ("%s<%s%s%s>\n" %
                                   (" " * depth, elementData[0], attrText,
                                    endText))
    
    # ____________________________________________________________
    def _closeTreeXMLTag (self, treeNode, depth):
        """BaseModelFactory._closeTreeXMLTag
        Postfix tree visitation routine used to generate an XML closing
        tag for a model serialization.
        """
        elementName = treeNode[0][0]
        if len(treeNode[1]) > 0:
            self._text = self._text + ("%s</%s>\n" % (" " * depth,
                                                      elementName))
    
    # ____________________________________________________________
    def internalize (self, format, stream):
        """BaseModelFactory.internalize
        """
        handlerMethod = getattr(self, "internalize" + format)
        return handlerMethod(stream)

    # ____________________________________________________________
    def internalizeTree (self, tree):
        """BaseModelFactory.internalizeTree
        """
        modelNode = self.creationHandler(tree[0])
        if modelNode != None:
            for branch in tree[1]:
                childNode = self.internalizeTree(branch)
                if childNode != None:
                    modelNode.append(childNode)
        return modelNode

    # ____________________________________________________________
    def internalizeXML (self, stream):
        """BaseModelFactory.internalizeXML
        """
        if type(stream) == types.StringType:
            text = stream
        else:
            text = stream.read()
        parser = XML2Tree.XML2TreeParser()
        parser.parse(text)
        assert len(parser.treeRoot[1]) == 1
        return self.internalizeTree(parser.treeRoot[1][0])

    # ____________________________________________________________
    def creationHandler (self, elementData):
        """BaseModelFactory.creationHandler
        """
        elementName = elementData[0]
        if elementName != None:
            handlerName = "create%s%s" % (string.upper(elementName[0]),
                                          elementName[1:])
            if hasattr(self, handlerName):
                handlerMethod = getattr(self, handlerName)
                return handlerMethod(elementData)
        return self.createDefault(elementData)

    # ____________________________________________________________
    def createDefault (self, elementData):
        """BaseModelFactory.createDefault
        """
        return self._processElement(UserList.UserList, elementData)

    # ____________________________________________________________
    def buildElement (self, elementName, *children, **attrs):
        """BaseModelFactory.buildElement
        """
        elem = self.creationHandler((elementName, attrs))
        elem.extend(children)
        return elem

    # ____________________________________________________________
    def _processElement (self, baseClass, elementData, elementContent = None,
                         extraAttrs = None):
        """BaseModelFactory._processElement
        """
        elementObj = baseClass()
        if None == elementData:
            elementName = baseClass.__name__
            elementAttrs = {}
        else:
            elementName, elementAttrs = elementData
        if None != extraAttrs:
            elementAttrs.update(extraAttrs)
        elementAttrMap = self.elements[elementName]
        for item in elementAttrs.items():
            if elementAttrMap.has_key(item[0]):
                setattr(elementObj, elementAttrMap[item[0]], item[1])
        if None != elementContent:
            elementObj.extend(elementContent)
        return elementObj

    # ____________________________________________________________
    def duplicateElement (self, elementObj):
        """BaseModelFactory.duplicateElement
        Creates a duplicate element object using the standard object creation
        routines (i.e. there is a dispatch hit; this is not a simple call to
        copy()).  Note that any contained elements are NOT duplicated.
        """
        elementName = elementObj.__class__.__name__
        elementAttrs = elementObj.__dict__
        return self.creationHandler((elementName, elementAttrs))

# ______________________________________________________________________
#

def getModelFactory ():
    """getModelFactory
    """
    return BaseModelFactory

# ______________________________________________________________________
# End of BaseModelFactory.py
