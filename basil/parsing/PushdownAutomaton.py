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
        self.node_stack = [(self.initial_nonterminal
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
# End of PushdownAutomaton.py
