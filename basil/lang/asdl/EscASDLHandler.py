#! /usr/bin/env python
# ______________________________________________________________________
"""Module EscASDLHandler

Defines a visitor class that constructs a loosely equivalent parse
tree using only objects that Mython knows how to escape out of the
box.

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

import ASDLHandler

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________
# Class definition(s)

class EscASDLHandler (ASDLHandler.ASDLHandler):
    def handle_Module (self, module_node):
        if __DEBUG__:
            print module_node
        children = []
        ret_val = ("Module", children)
        for type_name in module_node.types:
            type_node = module_node.types[type_name]
            self.crnt_type_name = type_name
            children.append(self.handle(type_node))
            self.crnt_type_name = None
        return ret_val
    # XXX Implement more here...

# ______________________________________________________________________
# End of EscASDLHandler.py
