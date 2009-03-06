#! /usr/bin/env python
# ______________________________________________________________________
"""Module ASDLHandler

Defines a base class for visiting ASDL parses.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Class definition(s)

class ASDLHandler (object):
    """Class ASDLHanlder - abstract walker for the ASDL abstract
    syntax tree."""
    # ____________________________________________________________
    def __init__ (self):
        """ASDLHanlder.__init__()"""
        self.crnt_type_name = None
    # ____________________________________________________________
    def handle (self, ast):
        ret_val = None
        attr_name = "handle_%s" % ast.__class__.__name__
        if hasattr(self, attr_name):
            handler = getattr(self, attr_name)
            ret_val = handler(ast)
        return ret_val
    # ____________________________________________________________
    def handle_Module (self, module_node):
        ret_val = None
        for type_name in module_node.types:
            type_node = module_node.types[type_name]
            self.crnt_type_name = type_name
            self.handle(type_node)
            self.crnt_type_name = None
        return ret_val
    # ____________________________________________________________
    def handle_Type (self, type_node):
        ret_val = None
        return ret_val
    # ____________________________________________________________
    def handle_Sum (self, sum_node):
        ret_val = None
        for type_node in sum_node.types:
            self.handle(type_node)
        return ret_val
    # ____________________________________________________________
    def handle_Constructor (self, cons_node):
        ret_val = None
        return ret_val
    # ____________________________________________________________
    def handle_Product (self, prod_node):
        ret_val = None
        return ret_val
    # ____________________________________________________________
    def handle_Field (self, field_node):
        ret_val = None
        return ret_val

# ______________________________________________________________________
# End of ASDLHandler.py
