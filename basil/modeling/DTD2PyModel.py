#! /usr/bin/env python
# ______________________________________________________________________
"""Module DTD2PyModel.py

Usage:
        % DTD2PyModel.py [-h] [-b modelBaseName] [-c elementBaseClass] \
                         <model.dtd>
Flags and arguments:
        -h  Display the documentation for this module.
        -b [modelBaseName]  Set the base name for the model and model factory
            (Default is the input DTD file root name.)
        -c [elementBaseClass] Absolute Python path of the element base class.
            This includes the module name. (Default is UserList.UserList)
        <model.dtd>  The XML document type definition (DTD) used to define the
            model.

$Id: DTD2PyModel.py 2765 2004-01-15 01:25:51Z jriehl $
"""
# ______________________________________________________________________
# Module imports.

import sys
import string
import getopt
import os.path
from basil.utils import TreeUtils
from basil.xml import DTDParser

# ______________________________________________________________________

def getElementAttributes (parseNode):
    """getElementAttributes
    """
    attributeList = []
    attlistNode = TreeUtils.bredthSearch(parseNode,
                                         lambda x: x[0][0] == "AttlistDecl")
    if attlistNode:
        for attDef in attlistNode[1]:
            attNameNode = TreeUtils.depthSearch(attDef,
                                                lambda x: x[0][0] == "Name")
            attributeList.append(attNameNode[0][1])
    return attributeList

# ______________________________________________________________________

def main ():
    """main
    """
    # ____________________________________________________________
    # Process the script arguments.
    options, args = getopt.getopt(sys.argv[1:], "hb:c:")
    if ("-h" in options) or (len(args) != 1):
        print __doc__
        sys.exit(0)
    # Set defaults.
    elementBaseClass = "UserList"
    elementBaseModule = "UserList"
    moduleBaseName = os.path.splitext(os.path.basename(args[0]))[0]
    for option in options:
        flag, arg = option
        if flag == "-b":
            moduleBaseName = arg
        elif flag == "-c":
            baseClassInput = string.split(arg, ".")
            elementBaseClass = baseClassInput[-1]
            elementBaseModule = string.join(baseClassInput[:-1], ".")
    # ____________________________________________________________
    # Read the DTD file.
    text = open(args[0]).read()
    parser = DTDParser.DTDParser()
    parser.feed(text)
    parser.close()
    # ____________________________________________________________
    # Generate prolog.
    print "#! /usr/bin/env python"
    print "# %s" % ("_" * 70)
    print
    print "from %s import %s" % (elementBaseModule, elementBaseClass)
    print "from basil.modeling.BaseModelFactory import BaseModelFactory"
    print
    # ____________________________________________________________
    # Generate classes.
    modelElementList = []
    modelElementMap = {}
    for item in parser.elements.items():
        # XXX Note that XML elements may require the same kind of lexical
        # mapping that have just been added for attributes.  Also note that
        # the handler framework will not like any element named model or
        # modelElement (these should be mapped to something like model2 or
        # modelElement2.)
        modelElementName = item[0]
        modelElementAttrs = getElementAttributes(item)
        print "# %s" % ("_" * 70)
        print "class %s (%s):" % (modelElementName, elementBaseClass)
        print "    elementName = \"%s\"" % (modelElementName)
        print "    def __init__ (self):"
        print "        %s.__init__(self)" % (elementBaseClass)
        modelElementAttrMap = {}
        pyModelElementAttrs = []
        for attributeName in modelElementAttrs:
            pyAttributeName = attributeName
            for ch in ".-:":
                pyAttributeName = string.replace(pyAttributeName, ch, "_")
            print "        self.%s = None" % (pyAttributeName)
            # XXX This does not currently handle the possibility of an
            # attribute difference such as egg-spam vs. egg_spam, i.e. these
            # will create an ambiguous mapping.
            modelElementAttrMap[attributeName] = pyAttributeName
            pyModelElementAttrs.append(pyAttributeName)
        print
        modelElementList.append(modelElementName)
        modelElementMap[modelElementName] = modelElementAttrMap
    # ____________________________________________________________
    # Generate factory class.
    print "# %s" % ("_" * 70)
    print "class %sModelFactory (BaseModelFactory):" % moduleBaseName
    print "    # %s" % ("_" * 60)
    print "    def __init__ (self):"
    print "        self.elements = %s" % `modelElementMap`
    print
    for elementName in modelElementList:
        print "    # %s" % ("_" * 60)
        print ("    def create%s%s (self, elementData = None, "
               "*elementChildren, **extraAttrs):"
               % (string.upper(elementName[0]), elementName[1:]))
        print ("        return self._processElement(%s, elementData, "
               "elementChildren, extraAttrs)" % (elementName,))
        print
    print "# %s" % ("_" * 70)
    print "def getModelFactory ():"
    print "    return %sModelFactory" % moduleBaseName
    print
    print "# %s" % ("_" * 70)
    print "# End of %sModel.py" % moduleBaseName
    print
    
# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of DTD2PyModel.py
