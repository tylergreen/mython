#! /usr/bin/env python
# ______________________________________________________________________
"""basil.apps.grammarian_util.commands

The command module for the Grammarian application.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

# ______________________________________________________________________
# Module data

COMMANDS = {}

COMMAND_HELP = {}

# ______________________________________________________________________
# Command definitions
# ______________________________________________________________________

# ______________________________________________________________________
# Despecialize

def doDespecialize (inFile, grammarModel, outFile, args):
    """doDespecialize()
    """
    retVal = 0
    from basil.models.grammar import Despecializer
    DespecializerClass = Despecializer.getModelHandler()
    despecializer = DespecializerClass()
    despecializedModel = despecializer.handleModel(grammarModel)
    return doOutput(inFile, grammarModel, outFile, [])

COMMANDS['despecialize'] = doDespecialize
COMMAND_HELP['despecialize'] = """despecialize
    Remove extended Backus-Naur forms from grammar.
"""

# ______________________________________________________________________
# Make actions

def doMakeActions (inFile, grammarModel, outFile, args):
    """doMakeActions()
    """
    retVal = 0
    outFileObj = getOutFileObj(outFile)
    # ____________________________________________________________
    extendedActions = False
    opts, args = getopt.getopt(args, "e")
    for (optFlag, optArg) in opts:
        if optFlag == "-e":
            extendedActions = True
    # ____________________________________________________________
    handlerArgs = {"extendedActions" : extendedActions,
                   "inFile" : inFile,
                   "outFile" : outFile}
    from basil.models.grammar import PyPatActionizer
    handlerClass = PyPatActionizer.getModelHandler()
    handler = handlerClass()
    results = handler.handleModel(grammarModel, handlerArgs)
    print >>outFileObj, results
    # ____________________________________________________________
    releaseOutFileObj(outFileObj)
    return retVal

COMMANDS['makeactions'] = doMakeActions
COMMAND_HELP['makeactions'] = """makeactions [-e]
    Make a PyPat action description file for the input grammar.

Options:
    -e: Make an action for each sub-element of the top level oneOf element.
        (Default is to just make a handler for each non-terminal element.)
"""

# ______________________________________________________________________
# Make handler

def doMakeHandler (inFile, grammarModel, outFile, args):
    """doMakeHandler()
    """
    retVal = 0
    return retVal

COMMANDS['makehandler'] = doMakeHandler
COMMAND_HELP['makehandler'] = """makehandler
    Make an empty handler class for the input grammar.
"""

# ______________________________________________________________________
# Make model

def doMakeModel (inFile, grammarModel, outFile, args):
    """doMakeModel()
    """
    retVal = 0
    return retVal

COMMANDS['makemodel'] = doMakeModel
COMMAND_HELP['makemodel'] = """makemodel
    Make a tree style model from the elements of the input grammar.  Here, a
    model element class is created for each non-terminal, as well as a factory
    class.
"""

# ______________________________________________________________________
# Output Model

def doOutputModel (inFile, grammarModel, outFile, args):
    """doOutputModel()
    """
    retVal = 0
    output = grammarModelFactory.externalizeXML(grammarModel)
    outFileObj = getOutFileObj(outFile)
    outFileObj.write(output)
    releaseOutFileObj(outFileObj)
    return retVal

COMMANDS['output'] = doOutputModel
COMMAND_HELP['output'] = """output
    Output the grammar model in XML.
"""

# ______________________________________________________________________
# Test generation

def doTestGen (inFile, grammarModel, outFile, args):
    """doTestGen()
    """
    retVal = 0
    from basil.models.grammar import Testerizer
    TesterizerClass = Testerizer.getModelHandler()
    testerizer = TesterizerClass()
    # XXX Need to fix so that strings are output to outFile.
    testerizer.handleModel(grammarModel)
    return retVal

COMMANDS['testgen'] = doTestGen
COMMAND_HELP['testgen'] = """testgen
"""

# ______________________________________________________________________
# ML-Yacc output

def doMLYaccOut (inFile, grammarModel, outFile, args):
    """doMLYaccOut()
    """
    retVal = 0
    # ____________________________________________________________
    prefix = None
    if inFile != None:
        prefix = getPrefix(inFile)
    elif outFile != None:
        prefix = getPrefix(outFile)
    # ____________________________________________________________
    opts, args = getopt.getopt(args, "p:")
    for (optFlag, optArg) in opts:
        if optFlag == "-p":
            prefix = optArg
    # ____________________________________________________________
    
    # ____________________________________________________________
    return retVal

COMMANDS['mlyaccout'] = doMLYaccOut
COMMAND_HELP['mlyaccout'] = """mlyaccout
    Generate a ML-Yacc <PREFIX>.grm, syntax tree <PREFIX>-syntax.sml, driver
    <PREFIX>-parser.sml, and CM <PREFIX>.cm.

    Prefix is taken from the input file name or output file name (if input
    is stdin), with the directory and file extension stripped, unless the -p
    option is used.

    Options:
    -p <PREFIX>: Use the given prefix for all parser machinery.
"""

# ______________________________________________________________________
# End of commands.py
