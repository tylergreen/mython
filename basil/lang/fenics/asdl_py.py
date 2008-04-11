#! /usr/bin/env python
# ______________________________________________________________________
"""Script asdl_py.py

Translate an ASDL module into a set of Python classes.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import getopt
import sys

# NOTE: To get at this, I've simply added .../Parser to my PYTHONPATH,
# where ... is the top of the Python source tree.
import asdl

from basil.lang.mython import pgen2LL1

# ______________________________________________________________________
# Module data

__DEBUG__ = False

# ______________________________________________________________________

def parse_string (text):
    """parse_string()
    Hack of the parse() function in asdl, made to handle a string
    input."""
    ret_val = None
    scanner = asdl.ASDLScanner()
    parser = asdl.ASDLParser()
    tokens = scanner.tokenize(text)
    try:
        ret_val = parser.parse(tokens)
    except asdl.ASDLSyntaxError, err:
        print err
        lines = text.split("\n")
        print lines[err.lineno - 1]
    return ret_val

# ______________________________________________________________________

class ASDLHandler (object):
    """Class ASDLHanlder - walker for the ASDL abstract syntax tree."""
    # ____________________________________________________________
    def __init__ (self):
        """ASDLHanlder.__init__()"""
        self.classes = {}
        self.base_classes = []
        self.crnt_sum_name = None
        self.crnt_attrs = []
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
    def handle_Field (self, field_node):
        ret_val = None
        return ret_val
    # ____________________________________________________________
    def emit_classes (self):
        code_list = ["#! /usr/bin/env python",
                      "class AST (object):",
                      ["pass"],
                      "",
                      ]
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
# Main routine

def main (*args):
    infilename = "<stdin>"
    infile = sys.stdin
    outfilename = "<stdout>"
    outfile = sys.stdout
    global __DEBUG__
    # ____________________________________________________________
    opts, args = getopt.getopt(args, "di:o:")
    for opt_key, opt_val in opts:
        if opt_key == "-i":
            infilename = opt_val
            infile = open(infilename)
        elif opt_key == "-o":
            outfilename = opt_val
            outfile = open(outfilename, "w")
        elif opt_key == "-d":
            __DEBUG__ = True
    # ____________________________________________________________
    text = infile.read()
    infile.close()
    asdl_pt = parse_string(text)
    if __DEBUG__:
        import pprint
        pprint.pprint(asdl_pt.types)
        print
    handler = ASDLHandler()
    handler.handle(asdl_pt)
    if __DEBUG__:
        pprint.pprint(handler.classes)
    code_text = handler.emit_classes()
    outfile.write(code_text)
    outfile.close()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of asdl_py.py
