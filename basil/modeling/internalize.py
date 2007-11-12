#! /usr/bin/env python
# ______________________________________________________________________
"""Module internalize.py

Internalizes a model data file into inmemory instances of a given Python
object model.  Command line usage:
        % internalize.py [options] <model> <datafile>

<model> - Python model module name.  Should be specified as a file
          path to the model module without the .py at the end.
<datafile> - Data file to internalize.  Internalization routine
             determined by the data file extension and model library
             implementation.

Options:
-g - Attempt to run the graphical viewer on the resulting model.

$Id: internalize.py 10210 2005-04-01 01:57:02Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import imp
import sys
import string
import getopt
import os.path
import pprint

# ______________________________________________________________________
# Module definitions

__DEBUG__ = False

__topdoc__ = __doc__

# ______________________________________________________________________

def loadModule (moduleName):
    """loadModule()
    """
    modulePath, moduleName = os.path.split(moduleName)
    modulePath = sys.path[:] + [os.path.abspath(modulePath)]
    moduleFile, modulePath, moduleDesc = imp.find_module(moduleName,
                                                         modulePath)
    retModule = None
    try:
        retModule = imp.load_module(moduleName, moduleFile, modulePath,
                                    moduleDesc)
    finally:
        if moduleFile != None:
            moduleFile.close()
    return retModule

# ______________________________________________________________________

def internalize (module, targetName):
    """internalize()
    """
    modelFactory = module.getModelFactory()()
    targetFile = open(targetName)
    dummy, ext = os.path.splitext(targetName)
    retModel = None
    try:
        retModel = modelFactory.internalize(string.upper(ext[1:]), targetFile)
    finally:
        targetFile.close()
    return retModel

# ______________________________________________________________________

def main ():
    """main()
    Main routine for the internalize module.  Supposed to load a model based
    on the input file extension and the formats supported by the model
    factory.
    """
    global __DEBUG__
    # ____________________________________________________________
    graphical = False
    help = False
    retVal = 0
    opts, args = getopt.getopt(sys.argv[1:], "dhgv")
    for (opt_key, opt_arg) in opts:
        if opt_key in ("-g", "-v"):
            graphical = True
        elif opt_key == "-h":
            help = True
        elif opt_key == "-d":
            __DEBUG__ = True
    if (len(args) != 2) or (help == True):
        print __topdoc__
        if not help:
            retVal = -1
        sys.exit(retVal)
    # ____________________________________________________________
    moduleName = args[0]
    targetName = args[1]
    module = loadModule(moduleName)
    model = None
    if module != None:
        model = internalize(module, targetName)
    else:
        print "Error, could not load module %s." % moduleName
    # ____________________________________________________________
    if graphical:
        from basil.visuals.TreeBox import showTree
        factory = module.getModelFactory()()
        tree = factory.externalizeTree(model)
        if __DEBUG__:
            pprint.pprint(tree)
        showTree(tree).mainloop()
    if __DEBUG__:
        print "Done. model =", `model`

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of internalize.py
