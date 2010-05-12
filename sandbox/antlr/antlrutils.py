#! /usr/bin/env python
# ______________________________________________________________________
"""Module antlrutils

Defines some utility functions for handling 
"""
# ______________________________________________________________________
# Module imports

from antlr3 import *

# ______________________________________________________________________
# Function definitions

def antlr_tree_to_tup (tree):
    return ((tree.getType(), tree.getText()),
            [antlr_tree_to_tup(child) for child in tree.getChildren()])

def mk_parse_file (lexer_class, parser_class):
    """Given an ANTLR3 lexer and parser class, build a function that
    takes a file object and returns a Pythonic representation of the
    AST.  Assumes that the parser outputs an ANTLR AST, and has a
    nonterminal called 'start'."""
    def parse_file (file_obj):
        char_stream = ANTLRInputStream(file_obj)
        lexer = lexer_class(char_stream)
        tokens = CommonTokenStream(lexer)
        parser = parser_class(tokens)
        return antlr_tree_to_tup(parser.start().tree)
    return parse_file

# ______________________________________________________________________
# End of antlrutils.py
