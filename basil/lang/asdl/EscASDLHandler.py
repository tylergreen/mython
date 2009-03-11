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
    # ____________________________________________________________
    def __init__ (self, verbose = False):
        ASDLHandler.ASDLHandler.__init__(self)
        self.verbose = verbose
    # ____________________________________________________________
    def handle_Module (self, module_node):
        if __DEBUG__:
            print "handle_Module():", module_node
            print
        return ("Module",
                {"version" : self.handle(module_node.version),
                 "name" : self.handle(module_node.name)},
                [self.handle(dfn) for dfn in module_node.dfns])
    # ____________________________________________________________
    def handle_Type (self, type_node):
        if __DEBUG__:
            print "handle_Type():", type_node, type_node.__dict__
            print
        return ("Type", {"name" : self.handle(type_node.name)},
                [self.handle(type_node.value)])
    # ____________________________________________________________
    def handle_Sum (self, sum_node):
        if __DEBUG__:
            print "handle_Sum():", sum_node, sum_node.__dict__
            print
        return ("Sum", {"attributes" : [self.handle(attribute)
                                        for attribute in sum_node.attributes]},
                [self.handle(child) for child in sum_node.types])
    # ____________________________________________________________
    def handle_Constructor (self, cons_node):
        if __DEBUG__:
            print "handle_Constructor():", cons_node, cons_node.__dict__
            print
        return ("Constructor", {"name" : self.handle(cons_node.name)},
                [self.handle(field) for field in cons_node.fields])
    # ____________________________________________________________
    def handle_Product (self, prod_node):
        if __DEBUG__:
            print "handle_Product():", prod_node, prod_node.__dict__
            print
        return ("Product", {}, [self.handle(field)
                                for field in prod_node.fields])
    # ____________________________________________________________
    def handle_Field (self, field_node):
        if __DEBUG__:
            print "handle_Field():", field_node, field_node.__dict__
            print
        return ("Field", {"opt" : field_node.opt, "seq" : field_node.seq},
                [self.handle(field_node.type), self.handle(field_node.name)])
    # ____________________________________________________________
    def handle_Id (self, id_node):
        if __DEBUG__:
            print "handle_Id():", id_node, id_node.__dict__
            print
        ret_val = id_node.value
        if self.verbose:
            ret_val = ("Id", {"value" : ret_val, "lineno" : id_node.lineno},
                       [])
        return ret_val
    # ____________________________________________________________
    def handle_String (self, string_node):
        ret_val = string_node.value
        if self.verbose:
            ret_val = ("String", {"value" : ret_val}, [])
        return ret_val

# ______________________________________________________________________
# Main (self-test) routine

def main (*args):
    global __DEBUG__
    from basil.thirdparty import asdl
    import pprint
    esc_handler = EscASDLHandler()
    for arg in args:
        if arg == "-d":
            __DEBUG__ = True
        elif arg == "-v":
            esc_handler = EscASDLHandler(True)
        else:
            pt = asdl.parse(arg)
            esc_pt = esc_handler.handle(pt)
            pprint.pprint(esc_pt)
            print

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of EscASDLHandler.py
