#! /usr/bin/env python
# ______________________________________________________________________
"""Module DTD2PyHandler.py

Usage:
        % DTD2PyHandler.py [-h] [-b modelBaseName] <model.dtd>

Flags and arguments:
        -h Display the documentation for this module.
        -b <modelBaseName>  Set the base name (model prefix) for the model
            handler (default is the input DTD file root name.)
        -c <handlerClassName>  Set the handler class name, overriding the
            default handler classname (<modelBaseName>ModelHandler).  This
            also overrides the -b option.
        <model.dtd> The XML document type definition (DTD) used to define the
            model.

$Id: DTD2PyHandler.py 12206 2005-05-11 23:25:13Z jriehl $
"""
# ______________________________________________________________________
# Module imports.

import sys
import string
import getopt
import os.path
from basil.utils import TreeUtils
from basil.xml import DTDParser
from basil.modeling.PyHandlerStrings import defaultCodeStrings

# ______________________________________________________________________
# Global data

SCRIPT_NAME = "basil/modeling/DTD2PyHandler.py"

# ______________________________________________________________________
# Function definitions

def noContent (treeNode):
    contentNode = TreeUtils.bredthSearch(treeNode,
                                         lambda x: x[0][0] == "ContentSpec")
    if contentNode:
        emptyNode = TreeUtils.depthSearch(contentNode,
                                          lambda x: x[0][0] == "EMPTY")
        if emptyNode:
            return 1
        return 0
    return 1

# ______________________________________________________________________

def main (strMap = None):
    # ____________________________________________________________
    # Process the script arguments.
    options, args = getopt.getopt(sys.argv[1:], "hb:c:")
    if ("-h" in options) or (len(args) != 1):
        print __doc__
        sys.exit(0)
    handlerClassName = None
    moduleBaseName = os.path.splitext(os.path.basename(args[0]))[0]
    for option in options:
        flag, arg = option
        if flag == "-b":
            moduleBaseName = arg
        elif flag == "-c":
            handlerClassName = arg
    if None == handlerClassName:
        handlerClassName = "%sModelHandler" % (moduleBaseName,)
    if None == strMap:
        global defaultCodeStrings
        strMap = defaultCodeStrings
    # ____________________________________________________________
    # Read the DTD file.
    text = open(args[0]).read()
    parser = DTDParser.DTDParser()
    parser.feed(text)
    parser.close()
    print strMap["header"] % SCRIPT_NAME
    # ____________________________________________________________
    # Generate handler class.
    print strMap["classFront"] % (handlerClassName,)
    elementNames = parser.elements.keys()
    elementNames.sort()
    for elementName in elementNames:
        print strMap["methodFront"] % (string.upper(elementName[0]),
                                       elementName[1:])
        if noContent((elementName, parser.elements[elementName])):
            print strMap["childlessMethodBody"]
        else:
            print strMap["methodBody"]
    print strMap["footer"] % (handlerClassName, handlerClassName)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of DTD2PyHandler.py
