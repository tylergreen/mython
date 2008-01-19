#! /usr/bin/env python
# ______________________________________________________________________
"""Module PushdownAutomaton.py

This is a reworking of the DFAParser code into a more object oriented
style.  This should replace LL1Parser as the output of an expanded
PyPgen.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________

E_OK = 0
E_DONE = 1
E_SYNTAX = 2

# ______________________________________________________________________
class DFAState (object):
    """Class DFA State
    Represents a state in a deterministic finite automaton (DFA)."""
    # ____________________________________________________________
    def __init__ (self, stateTup = None, parent = None):
        """DFAState.__init__()

        Constructor for a DFAState.  Takes an optional tuple argument
        of the form:
            ([Arc], Accel, Accept)

        Where Arc = (label : int, stateIndex : int)
        And Accel = (upper : int, lower :int, arr : int list)

        Additionally, a parent may be given, which should be a DFA
        instance that contains the state."""
        self.arcs = {}
        self.accelUpper = None
        self.accelLower = None
        self.accelTable = []
        self.accept = False
        if stateTup is not None:
            arcs, accel, accept = stateTup
            for arc in arcs:
                self.arcs[arc[0]] = arc[1]
            if accel is not None:
                self.accelUpper, self.accelLower, self.accelTable = accel
            self.accept = bool(accept)
        self.parent = parent

    # ____________________________________________________________
    def toTuple (self):
        """DFAState.toTuple()
        Convert the current DFA state into its tuple representation."""
        arcs = [(k,v) for k, v in self.arcs.items()]
        if self.accelUpper is None:
            accel = None
        else:
            accel = (self.accelUpper, self.accelLower, self.accelTable)
        accept = int(self.accept)
        return arcs, accel, accept

    # ____________________________________________________________
    def toString (self, fmt = None):
        """DFAState.toString([fmt])

        Returns a string representation of the given DFA state.  The
        optional fmt parameter is a string.  Currently only graphviz
        formatting is supported."""
        if fmt == "graphviz":
            assert ((self.parent is not None) and
                    (self in self.parent.states))
            nodeLabel = "%s_state%d" % (self.parent.name,
                                        self.parent.states.index(self))
            nodePeripheries = ""
            if self.accept:
                nodePeripheries = ", peripheries=2"
            nodeDecl = "%s [shape=ellipse%s];\n" % (nodeLabel, nodePeripheries)
            edgeDeclList = []
            grammar = self.parent.parent
            for arcIndex, arcState in self.arcs.items():
                labelTy, labelName = grammar.labels[arcIndex]
                if labelName is None:
                    arcLabel = str(labelTy)
                else:
                    arcLabel = labelName
                edgeDeclList.append('%s -> %s_state%d [label="%s"];\n' %
                                    (nodeLabel, self.parent.name, arcState,
                                     arcLabel))
            retVal = '%s%s' % (nodeDecl, "".join(edgeDeclList))
        elif fmt is None:
            retVal = "%s" % self.toTuple()
        else:
            retVal = "%r" % self
        return retVal

    # ____________________________________________________________
    def compareToTuple (self, tup):
        """DFAState.compareToTuple(tup)

        Compare the current object to the input tuple state
        representation.  Raises an exception if they are not
        equivalent.  Otherwise, None is returned.  Used for self
        testing.
        """
        theirArcs, theirAccel, theirAccept = tup
        myArcSet = set(self.arcs.items())
        theirArcSet = set(theirArcs)
        if myArcSet != theirArcSet:
            raise Exception("Arc mismatch, %s != %s" % (myArcSet, theirArcSet))
        myAccel = None
        if self.accelUpper is not None:
            myAccel = (self.accelUpper, self.accelLower, self.accelTable)
        if myAccel != theirAccel:
            raise Exception("Accel mismatch, %s != %s" % (myAccel, theirAccel))
        if int(self.accept) != theirAccept:
            raise Exception("Accept mismatch, %d != %d" % (int(self.accept),
                                                           theirAccept))

# ______________________________________________________________________
class DFA (object):
    """Class DFA
    Represents a deterministic finite-state automaton."""
    # ____________________________________________________________
    def __init__ (self, dfaTup = None, parent = None):
        """DFA.__init__([dfaTup, [parent]])

        Constructor for the DFA class. Accepts an optional DFA tuple of the
        form:
            (type : int, name : string, initial : int, states : state list,
            first : string)
        or
            (type : int, name : string, initial : int, states : state list)
        Where the second form is assumed to have accelerators defined in the
        state list.  See DFAState.__init__()'s docstring for the state tuple
        format.

        A final grammar instance may be optionally passed in as well."""
        self.typeIndex = None
        self.name = None
        self.initial = None
        self.states = []
        self.first = None
        if dfaTup is not None:
            self.typeIndex, self.name, self.initial, stateList = dfaTup[:4]
            if len(dfaTup) > 4:
                assert len(dfaTup) == 5
                self.first = dfaTup[-1]
            self.states = [DFAState(stateTup, self) for stateTup in stateList]
        self.parent = parent

    # ____________________________________________________________
    def toTuple (self):
        """DFA.toTuple()
        Convert the current DFA into its tuple representation."""
        stateList = [dfaState.toTuple() for dfaState in self.states]
        if self.first is None:
            retVal = (self.typeIndex, self.name, self.initial, stateList)
        else:
            retVal = (self.typeIndex, self.name, self.initial, stateList,
                      self.first)
        return retVal

    # ____________________________________________________________
    def toString (self, fmt = None):
        """DFA.toString([fmt])

        Returns a string representation of the given DFA.  The
        optional fmt parameter is a string.  Currently only graphviz
        formatting is supported."""
        if fmt == "graphviz":
            stateDecls = "".join([state.toString(fmt) for state in
                                  self.states])
            # FIXME: Don't know why dot isn't drawing labelled boxes
            # around subgraphs.
            retVal = ('subgraph "%s" {\n%slabel="%s_%d";\ncolor=black;\n}\n' %
                      (self.name, stateDecls, self.name, self.typeIndex))
        elif fmt is None:
            retVal = "%s" % self.toTuple()
        else:
            retVal = "%r" % self
        return retVal

    # ____________________________________________________________
    def compareToTuple (self, tup):
        """DFA.compareToTuple(tup)

        Compare the current object to the input tuple DFA
        representation.  Raises an exception if they are not
        equivalent.  Otherwise, None is returned.  Used for self
        testing.
        """
        myStateCount = len(self.states)
        if myStateCount != len(tup[3]):
            raise Exception("State count mismatch, %d != %d" %
                            (myStateCount, len(tup[3])))
        for index in xrange(myStateCount):
            self.states[index].compareToTuple(tup[3][index])
        if self.typeIndex != tup[0]:
            raise Exception("DFA type index mismatch, %d != %d" %
                            (self.typeIndex, tup[0]))
        if self.name != tup[1]:
            raise Exception("DFA name mismatch, %s != %s" %
                            (self.name, tup[1]))
        if self.initial != tup[2]:
            raise Exception("Initial state mismatch, %d != %d" %
                            (self.initial, tup[2]))
        if self.first is None:
            if len(tup) == 5:
                raise Exception("First set present in tuple, but not in DFA "
                                "object.")
        elif len(tup) == 4:
            raise Exception("First set present in DFA, but not in tuple.")
        elif self.first != tup[4]:
            raise Exception("First set mismatch, %s != %s" % (self.first,
                                                              tup[4]))

# ______________________________________________________________________
class PushdownGrammar (object):
    """Class PushdownGrammar
    Represents a pushdown automaton."""
    # ____________________________________________________________
    def __init__ (self, grammarTup = None):
        """PushdownGrammar.__init__([grammarTup])

        Constructor for a pushdown automaton's grammar, represented as
        a state machine.  Optionally accepts a tuple, representing the
        grammar, of the following form:

        (dfas : DFA list, labels : (int * string) list, start :int,
        accel : int)

        Where the DFA tuple form is defined in the DFA class constructor.
        """
        self.dfas = []
        self.labels = []
        self.start = None
        self.accel = False
        if grammarTup is not None:
            dfaList, self.labels, self.start, accelVal = grammarTup
            self.dfas = [DFA(dfaTup, self) for dfaTup in dfaList]
            self.accel = bool(accelVal)

    # ____________________________________________________________
    def toTuple (self):
        """PushdownGrammar.toTuple()
        Convert the current pushdown automaton back into its tuple
        representation."""
        return ([dfa.toTuple() for dfa in self.dfas], self.labels,
                self.start, int(self.accel))

    # ____________________________________________________________
    def toString (self, fmt = None):
        """PushdownGrammar.toString([fmt])

        Returns a string representation of the given grammar.  The
        optional fmt parameter is a string.  Currently only graphviz
        formatting is supported."""
        if fmt == "graphviz":
            dfaDecls = "\n".join([dfa.toString(fmt) for dfa in self.dfas])
            retVal = ('digraph G {\n%s\n}\n' % dfaDecls)
        elif fmt is None:
            retVal = "%s" % self.toTuple()
        else:
            retVal = "%r" % self
        return retVal

    # ____________________________________________________________
    def compareToTuple (self, tup):
        """PushdownGrammar.compareToTuple(tup)

        Compare the current object to the input tuple grammar
        representation.  Raises an exception if they are not
        equivalent.  Otherwise, None is returned.  Used for self
        testing.
        """
        myDFACount = len(self.dfas)
        if myDFACount != len(tup[0]):
            raise Exception("DFA count mismatch, %d != %d" %
                            (myDFACount, len(tup[0])))
        for index in xrange(myDFACount):
            self.dfas[index].compareToTuple(tup[0][index])

# ______________________________________________________________________
class PushdownAutomaton (object):
    """Class PushdownAutomaton
    """
    # ____________________________________________________________
    def __init__ (self, inital_nonterminal):
        """PushdownAutomaton.__init__()

        Attributes:
        initial_nonterminal - Name of the initial nonterminal.
        state_stack - Stack of nonterminal name and data pairs.
        node_stack - Stack of concrete parse tree nodes.
        handler_dict - Cache of parsing handler methods, indexed by
            nonterminal name.
        error_msg - State variable used to pass up syntax error messages.
        """
        self.initial_nonterminal = inital_nonterminal
        self.state_stack = []
        self.node_stack = []
        self.handler_dict = {}
        self.error_msg = None

    # ____________________________________________________________
    def __call__ (self, tokenizer):
        """PushdownAutomaton.__call__(tokenizer)
        Recognize the lexical stream tokenized by the given callable,
        tokenizer.  Returns a concrete parse tree.
        """
        self.tokenizer = tokenizer
        self.node_stack = [(self.initial_nonterminal)]
        self.state_stack = [(self.initial_nonterminal, None)]
        while result == E_OK:
            tok_data = tokenzier()
            result = self.handle(tok_data)
        if result == E_DONE:
            ret_val = self.node_stack[0]
        else:
            raise SyntaxError("Error in line %d%s" %
                              (self.get_lineno(tok_data), self.error_msg))
        return ret_val

    # ____________________________________________________________
    def get_lineno (self, tok_data):
        """PushdownAutomaton.get_lineno()
        """
        return tok_data[-1]

    # ____________________________________________________________
    def handle (self, tok_data):
        """PushdownAutomaton.handle()
        """
        handler_dict = self.handler_dict
        state_name, data = self.state_stack[-1]
        if state_name not in handler_dict:
            handler_name = "handle_%s" % state_name
            handler = getattr(self, handler_name)
            handler_dict[handler_name] = handler
        else:
            handler = handler_dict[state_name]
        return handler(data, tok_data)

# ______________________________________________________________________
# Main routine definition

def main (*args):
    """main() - Unit test routine for the PushdownAutomaton module."""
    from basil.lang.python import DFAParser
    from basil.parsing import PgenParser, PyPgen
    import sys, getopt
    # ____________________________________________________________
    opts, args = getopt.getopt(args, "o:")
    outFile = sys.stdout
    for optFlag, optArg in opts:
        if optFlag == "-o":
            outFile = open(optArg, "w")
    argc = len(args)
    if argc > 1:
        print "Usage:\n\tPushdownAutomaton.py [opts] <file.pgen>\n"
        sys.exit(-1)
    elif argc == 1:
        srcFile = args[0]
    else:
        srcFile = "./tests/test.pgen"
    grammarST = PgenParser.parseFile(srcFile)
    parser = PyPgen.buildParser(grammarST)
    grammarTup = parser.grammarObj
    # ____________________________________________________________
    # Round trip test
    myGrammarObj = PushdownGrammar(grammarTup)
    myGrammarObj.compareToTuple(grammarTup)
    grammarTup2 = myGrammarObj.toTuple()
    myGrammarObj.compareToTuple(grammarTup2)
    # Now with accelerators...
    grammarTup3 = DFAParser.addAccelerators(grammarTup)
    myGrammarObj2 = PushdownGrammar(grammarTup3)
    myGrammarObj2.compareToTuple(grammarTup3)
    grammarTup4 = myGrammarObj2.toTuple()
    myGrammarObj2.compareToTuple(grammarTup4)
    # ____________________________________________________________
    # Output tests.
    outFile.write("%s\n" % myGrammarObj2.toString("graphviz"))
    if outFile != sys.stdout:
        outFile.close()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of PushdownAutomaton.py
