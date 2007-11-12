#! /usr/bin/env python
# ______________________________________________________________________
"""Module SyntaxTupleHandler

Implements base class(es) for handling Pgen parser generated concrete syntax
trees (in the tuple representation).

XXX - This duplicates code that is similar to the BaseModelHandler.  Look
into refactoring w/BaseModelHandler.

XXX - What about the pgen C extension module?

Jonathan Riehl

$Id: SyntaxTupleHandler.py 13037 2005-06-03 17:23:46Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import token, string

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________
# Class definitions

class SyntaxTupleHandler (object):
    """Class SyntaxTupleHandler
    """
    # ____________________________________________________________
    def __init__ (self, symbolMap, handleTerminals = False):
        """SyntaxTupleHandler.__init__()
        Constructor for the SyntaxTupleHandler class.  The symbolMap
        argument provides the handler with a dictionary that should
        map from node type (the first integer in the st2tuple parse
        tree representation) to non-terminal name.
        """
        self.symbolMap = symbolMap
        self.handleTerminals = handleTerminals
        self.handlerMap = {}

    # ____________________________________________________________
    def getHandlerName (self, nodeType):
        """SyntaxTupleHandler.getHandlerName()
        Override this for other name conventions (such as
        handle_non_terminal_name_here).

        Note that a return value of None is used to signal to the
        handler that the nodeType should be ignored. (XXX Perhaps this
        functionality should be teased out of here?)
        """
        retVal = None
        if self.symbolMap.has_key(nodeType):
            symbolName = self.symbolMap[nodeType]
            retVal = "handle%s%s" % (string.upper(symbolName[0]),
                                     symbolName[1:])
        elif self.handleTerminals:
            tokenName = token.tok_name[nodeType]
            retVal = "handle%s%s" % (string.upper(tokenName[0]),
                                     tokenName[1:])
        if __DEBUG__:
            print "SyntaxTupleHandler.getHandlerName(): %d => %s" % (nodeType,
                                                                     retVal)
        return retVal

    # ____________________________________________________________
    def handle (self, node, *args, **kw):
        """SyntaxTupleHandler.handle()
        """
        if __DEBUG__:
            print "SyntaxTupleHandler.handle():", node
        retVal = None
        nodeType = node[0]
        if self.handlerMap.has_key(nodeType):
            retVal = self.handlerMap[nodeType](node, *args, **kw)
        else:
            handlerName = self.getHandlerName(nodeType)
            if handlerName != None:
                if hasattr(self, handlerName):
                    handler = getattr(self, handlerName)
                    retVal = handler(node, *args, **kw)
                    self.handlerMap[nodeType] = handler
                else:
                    retVal = self.defaultHandler(node, *args, **kw)
                    self.handlerMap[nodeType] = self.defaultHandler
        return retVal

    # ____________________________________________________________
    def getChildren (self, node):
        """SyntaxTupleHandler.getChildren()
        """
        retVal = []
        if node[0] >= token.NT_OFFSET:
            retVal = node[1:]
        return retVal

    # ____________________________________________________________
    def handleChildren (self, node, *args, **kw):
        """SyntaxTupleHandler.handleChildren()
        """
        children = self.getChildren(node)
        return [self.handle(child, *args, **kw) for child in children]

    # ____________________________________________________________
    def defaultHandler (self, node, *args, **kw):
        """SyntaxTupleHandler.defaultHandler()
        """
        return self.handleChildren(node, *args, **kw)

# ______________________________________________________________________
# Main routine

def main ():
    """main()
    Main routine for the SyntaxTupleHandler module.  Used to run
    rudimentary unit tests from the command line.
    """
    global __DEBUG__
    import sys, symbol, parser
    fileName = None
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if "-d" in args:
            __DEBUG__ = True
            args.remove("-d")
        if len(args) > 0:
            fileName = args[0]
    if fileName != None:
        text = open(fileName).read()
    else:
        text = sys.stdin.read()
    st = parser.suite(text)
    tup = parser.st2tuple(st)
    handler = SyntaxTupleHandler(symbol.sym_name, True)
    print handler.handle(tup)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of SyntaxTupleHandler.py
