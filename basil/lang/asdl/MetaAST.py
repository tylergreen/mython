#! /usr/bin/env python
# ______________________________________________________________________
"""Module MetaAST

Defines a flattened AST representation for ASDL AST's (originally
defined in asdl.py from the Python source).  Also defines a handler
class for flattening ASDL AST's.

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

from basil.thirdparty import asdl
from basil.lang.asdl import ASDLHandler
from basil.lang.mython import pgen2LL1

# ______________________________________________________________________
# Class definition(s)

class MetaAST (object):
    """Abstract base class for representing ASDL metadata.  Could be
    considered the root class of the metamodel."""
    # ____________________________________________________________
    def emit_md (self):
        "Emits metadata for the current ASDL metaobject (not the full code)."
        emit_dict = self.__dict__.copy()
        for key in self.__dict__.keys():
            if len(key) > 0 and key[0] == "_":
                del emit_dict[key]
        return repr(emit_dict)
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        if crnt_code == None:
            crnt_code = []
        return crnt_code
    # ____________________________________________________________
    def emit_class (self, class_name, base_class = None, fields = None):
        ret_val = []
        if base_class is None:
            base_class = "AST"
        ret_val.append("class %s (%s):" % (class_name, base_class))
        class_contents = ["__asdl_meta__ = %s" % self.emit_md(), ""]
        #if fields:
        #    class_contents += ["def __init__ (self, *args):",
        #                       ["pass"]]
        ret_val.append(class_contents)
        return ret_val
    # ____________________________________________________________
    def _handle_fields (self, fields):
        return [(field.name.value, field.type.value, field.opt,
                 field.seq) for field in fields]

# ______________________________________________________________________

class ASTModule (MetaAST):
    def __init__ (self, ast_node):
        self.name = ast_node.name.value
        self.version = ast_node.version.value
        self.dfns = [type_node.name.value for type_node in ast_node.dfns]
        self._types = []
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        if crnt_code == None:
            crnt_code = []
        module_code = self.emit_class(self.name, "object")
        for contained_type in self._types:
            contained_type.emit_code(module_code[-1])
            module_code[-1] += [""]
        crnt_code += module_code
        return crnt_code

# ______________________________________________________________________

class ASTType (MetaAST):
    def __init__ (self, type_node):
        self.name = type_node.name.value
        if isinstance(type_node.value, asdl.Sum):
            self.value = ASTSum(type_node.value)
            self.value._name = self.name
        else:
            self.value = ASTProduct(type_node.value)
            self.value._name = self.name
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        return self.value.emit_code(crnt_code)

# ______________________________________________________________________

class ASTSum (MetaAST):
    def __init__ (self, ast_node):
        self._name = None
        self.attributes = self._handle_fields(ast_node.attributes)
        self.types = [constructor.name.value for constructor in ast_node.types]
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        if crnt_code is None:
            crnt_code = []
        if self._name:
            crnt_code += self.emit_class(self._name, fields = self.attributes)
        return crnt_code

# ______________________________________________________________________

class ASTProduct (MetaAST):
    def __init__ (self, ast_node):
        self._name = None
        self.fields = self._handle_fields(ast_node.fields)
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        if crnt_code is None:
            crnt_code = []
        if self._name:
            crnt_code += self.emit_class(self._name, fields = self.fields)
        return crnt_code

# ______________________________________________________________________

class ASTConstructor (MetaAST):
    def __init__ (self, ast_node):
        self._parent = None
        self.name = ast_node.name.value
        self.fields = self._handle_fields(ast_node.fields)
    # ____________________________________________________________
    def emit_code (self, crnt_code = None):
        if crnt_code is None:
            crnt_code = []
        if self._parent:
            crnt_code += self.emit_class(self.name, self._parent._name,
                                         self.fields + self._parent.attributes)
        else:
            crnt_code += self.emit_class(self.name, fields = self.fields)
        return crnt_code

# ______________________________________________________________________

class MetaASDLHandler (ASDLHandler.ASDLHandler):
    # ____________________________________________________________
    def __init__ (self):
        ASDLHandler.ASDLHandler.__init__(self)
        self.init_types()
        self.modules = []
    # ____________________________________________________________
    def init_types (self):
        self.types = None
    # ____________________________________________________________
    def handle_Module (self, module_node):
        ret_val = ASTModule(module_node)
        self.types = ret_val._types
        for dfn in module_node.dfns:
            self.handle(dfn)
        self.modules.append(ret_val)
        return ret_val
    # ____________________________________________________________
    def handle_Type (self, type_node):
        ret_val = ASTType(type_node)
        self.types.append(ret_val)
        self.handle(type_node.value)
        return ret_val
    # ____________________________________________________________
    def handle_Sum (self, sum_node):
        ret_val = None
        if isinstance(self.types[-1], ASTType):
            ret_val = self.types[-1].value
            assert isinstance(ret_val, ASTSum)
        for constructor in sum_node.types:
            child = self.handle(constructor)
            child._parent = ret_val
        return ret_val
    # ____________________________________________________________
    def handle_Product (self, product_node):
        ret_val = None
        if isinstance(self.types[-1], ASTType):
            ret_val = self.types[-1].value
            assert isinstance(ret_val, ASTProduct)
        return ret_val
    # ____________________________________________________________
    def handle_Constructor (self, constructor_node):
        ret_val = ASTConstructor(constructor_node)
        self.types.append(ret_val)
        return ret_val
    # ____________________________________________________________
    def emit_code (self, *args, **kws):
        code_lines = ["#! /usr/bin/env python", "",
                      "from basil.lang.asdl.AST import AST", ""]
        for module in self.modules:
            module.emit_code(code_lines)
        return "\n".join(pgen2LL1.gen_code_lines(code_lines))

# ______________________________________________________________________
# Main (self-test) routine.

def main (*args):
    import pprint
    handler = MetaASDLHandler()
    for arg in args:
        pt = asdl.parse(arg)
        module = handler.handle(pt)
        print module.emit_md()
        for ty in module._types:
            print ty.emit_md()
        print
        print "\n".join(pgen2LL1.gen_code_lines(module.emit_code()))

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MetaAST.py
