#! /usr/bin/env python
# ______________________________________________________________________
"""Module Handler.py

Defines the Handler class, an abstract base class for handling
concrete (and possibly abstract) parse trees.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

# ______________________________________________________________________
# Class definition

class Handler (object):
    """Class Handler
    """
    # ____________________________________________________________
    def __init__ (self):
        """Handler.__init__()
        """
        self.special_nonterminals = []

    # ____________________________________________________________
    def get_nonterminal (self, node):
        """Handler.get_nonterminal()
        This should be overloaded to return the nonterminal identifier
        or None, if the node is terminal."""
        raise NotImplementedError("Overload me!")

    # ____________________________________________________________
    def get_children (self, node):
        """Handler.get_children()
        """
        raise NotImplementedError("Overload me!")

    # ____________________________________________________________
    def make_node (self, node_id, children):
        """Handler.make_node()
        """
        raise NotImplementedError("Overload me!")

    # ____________________________________________________________
    def handle_default (self, node):
        """Handler.handle_default()
        """
        raise NotImplementedError("Overload me!")

    # ____________________________________________________________
    def is_token (self, node):
        """Handler.is_token()
        """
        ret_val = False
        return ret_val

    # ____________________________________________________________
    def get_handler_name (self, node):
        """Handler.get_handler_name()
        """
        return "handle_%s" % (str(self.get_nonterminal(node)))

    # ____________________________________________________________
    def handle_node (self, node):
        """Handler.handle_node()
        Possibly overload to dispatch."""
        handler_name = self.get_handler_name(node)
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            ret_val = handler(node)
        else:
            ret_val = self.handle_default(node)
        return ret_val

    # ____________________________________________________________
    def handle_children (self, node):
        """Handler.handle_children()
        Utility method that returns a list of post-processed children."""
        children = self.get_children(node)
        return [self.handle_node(child) for child in children]

    # ____________________________________________________________
    def simplify_tree (self, node):
        """Handler.simplify_tree()
        """
        ret_val = node
        nonterminal = self.get_nonterminal(node)
        if nonterminal is not None:
            children = self.get_children(node)
            if ((nonterminal in self.special_nonterminals) or
                (len(children) > 1)):
                new_children = [self.simplify_tree(child)
                                for child in children]
                ret_val = self.make_node(nonterminal, new_children)
            else:
                ret_val = self.simplify_tree(children[0])
        return ret_val

# ______________________________________________________________________
# Main routine

def main (*args):
    """main() - Unit test for the handler class."""
    import parser, token, pprint
    # ____________________________________________________________
    class PySTHandler (Handler):
        """Class PySTHandler
        Simple class illustrating how the Handler class may be
        specialized to handle Python syntax trees."""
        # __________________________________________________
        def get_nonterminal (self, node):
            ret_val = None
            if not self.is_token(node):
                ret_val = node[0]
            return ret_val
        # __________________________________________________
        def get_children (self, node):
            ret_val = []
            if not self.is_token(node):
                ret_val = node[1:]
            return ret_val
        # __________________________________________________
        def is_token (self, node):
            return node[0] < token.NT_OFFSET
        # __________________________________________________
        def make_node (self, node_id, children):
            return tuple([node_id] + children)
        # __________________________________________________
        def handle_default (self, node):
            print node
            ret_val = self.handle_children(node)
            return ret_val
        # __________________________________________________
        def handle_317 (self, node):
            print "!!! ATOM !!!", node
            ret_val = node
            return ret_val
    # ____________________________________________________________
    for infilename in args:
        intext = open(infilename).read()
        cst = parser.suite(intext).totuple()
        handler = PySTHandler()
        pprint.pprint(handler.handle_node(cst))
        simplified_tree = handler.simplify_tree(cst)
        pprint.pprint(simplified_tree)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of Handler.py
