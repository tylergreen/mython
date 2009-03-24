#! /usr/bin/env python
# ______________________________________________________________________
"""Module PyASDLHandler

Defines a visitor class for ASDL parses that constructs Python code.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import ASDLHandler

# XXX This is only being used for a code generation utility function.
# Move that function elsewhere.
from basil.lang.mython import pgen2LL1

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________
# Class definition(s)

class PyASDLHandler (ASDLHandler.ASDLHandler):
    """Class PyASDLHandler - walker for the ASDL abstract syntax tree."""
    # ____________________________________________________________
    def __init__ (self):
        """ASDLHanlder.__init__()"""
        ASDLHandler.ASDLHandler.__init__(self)
        self.classes = {}
        self.base_classes = []
        self.crnt_sum_name = None
        self.crnt_attrs = []
    # ____________________________________________________________
    def handle_Sum (self, sum_node):
        ret_val = None
        self.crnt_sum_name = self.crnt_type_name
        self.base_classes.append(self.crnt_type_name)
        # XXX Can sum types be nested?  If so, need to push and pop crnt_attrs.
        self.crnt_attrs = sum_node.attributes
        for type_node in sum_node.types:
            self.handle(type_node)
        self.crnt_attrs = []
        self.crnt_sum_name = None
        return ret_val
    # ____________________________________________________________
    def make_class (self, klass_name, fields):
        ret_val = []
        base_class = self.crnt_sum_name
        constructor_arg_names = [field.name.value for field in fields]
        constructor_args = ""
        if constructor_arg_names:
            constructor_args = (", %s = None" %
                                (" = None, ".join(constructor_arg_names)))
        ret_val.append("def __init__ (self%s):" % constructor_args)
        if constructor_arg_names:
            ret_val.append(["self.%s = %s" % (constructor_arg, constructor_arg)
                            for constructor_arg in constructor_arg_names])
        else:
            ret_val.append(["pass"])
        self.classes[klass_name] = (base_class, ret_val)
        return ret_val        
    # ____________________________________________________________
    def handle_Constructor (self, cons_node):
        if __DEBUG__:
            print cons_node
        return self.make_class(cons_node.name.value,
                               cons_node.fields + self.crnt_attrs)
    # ____________________________________________________________
    def handle_Product (self, prod_node):
        if __DEBUG__:
            print prod_node
        assert self.crnt_type_name is not None
        return self.make_class(self.crnt_type_name, prod_node.fields)
    # ____________________________________________________________
    def emit_classes (self, self_contained = False):
        code_list = ["#! /usr/bin/env python"]
        if self_contained:
            code_list += ["class AST (object):",
                          ["def __eq__ (self, other):",
                           ["return ((type(self) == type(other))",
                            ["and (self.__dict__ == other.__dict__))"]],
                           ],
                          "",
                          ]
        else:
            code_list += ["from basil.lang.asdl.AST import AST",
                          ""]
        # __________________________________________________
        self.base_classes.sort()
        for base_class_name in self.base_classes:
            code_list += ["class %s (AST):" % base_class_name,
                          ["pass"], ""]
        # __________________________________________________
        class_names = self.classes.keys()
        class_names.sort()
        for class_name in class_names:
            base_class, class_body = self.classes[class_name]
            if base_class is None:
                base_class = "AST"
            code_list += ["class %s (%s):" % (class_name, base_class),
                          class_body, ""]
        return "\n".join(pgen2LL1.gen_code_lines(code_list))

# ______________________________________________________________________
# End of PyASDLHandler.py
