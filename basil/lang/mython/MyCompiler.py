#! /usr/bin/env python
"""MyCompiler
Toy compiler for a modified Python parser.
"""
import pprint, copy
from basil.parsing import PyPgen, PgenParser
from basil.lang.python import TokenUtils, StdTokenizer, DFAParser

g = PgenParser.parseFile("./svn/basil/trunk/basil/parsing/tests/test2.pgen")
p = PyPgen.buildParser(g)
testString = # This is a comment, ooooo!
def spam(egg : eggType) stupid eggType:
    moosh = egg.add(spamSpamAndMoreSpam)
    assert moosh : int
    return egg

p.setStart(257)
myTree = p.parseString(testString)

class SyntaxTreeWalker (object):
    def __init__ (self, symbolMap):
        """TreeWalker
        """
        self.symbolMap = symbolMap
    def _flatten (self, childLists):
        retVal = []
        for result in childLists:
            if type(result) == list:
                retVal.extend(result)
            else:
                retVal.append(result)
        return retVal
    def _getSymbolNum (self, node):
        return node[0][0]
    def _handle (self, node):
        """
        """
        if len(node[1]) == 0:
            return node[0]
        childResults = map(self._handle, node[1])
        symbolNum = self._getSymbolNum(node)
        if self.symbolMap.has_key(symbolNum):
            symbolName = self.symbolMap[symbolNum]
            if hasattr(self, symbolName):
                symbolMethod = getattr(self, symbolName)
                return symbolMethod(self, childResults)
        return self._flatten(childResults)
    def __call__ (self, node):
        return self._handle(node)

class PrefixSyntaxTreeWalker (SyntaxTreeWalker):
    def _handle(self, node):
        symbolNum = self._getSymbolNum(node)
        if self.symbolMap.has_key(symbolNum)
            symbolName = self.symbolMap[symbolNum]
            if hasattr(self, symbolName):
                symbolMethod = getattr(self, symbolName)
                symbolMethod(self, node)
                return
        for child in node[1]:
            self._handle(child)

class NativeSyntaxTreeWalker (SyntaxTreeWalker):
    def _getSymbolNum (self, node):
        return node[0]

walker = SyntaxTreeWalker(p.symbolToStringMap())
walker._handle(myTree)

class SubWalker (TreeWalker):
    def test (self, node, children):
        print "TEST TEST TEST TEST!", children
        return self._flatten(children)

w2 = SubWalker(p.symbolToStringMap())
w2(myTree)

