#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyUglyPrinter

Defines a not-so-pretty printer for Python abstract syntax."""
# ______________________________________________________________________
# Module imports

from basil.lang.mython.mybuiltins import myfrontend
from basil.lang.mython.MyCodeGen import ASTHandler
from basil.lang.mython import myfront_ast

# ______________________________________________________________________
# Class definition(s)

# The methods for these were generated in part using:

# >>> from basil.lang.mython import ASTUtils, myfront_ast
# >>> ASTUtils.gen_py_handlers(myfront_ast)

# ...and then some copy/replace.  An example of using one of these is
# in .../basil/lang/mython/MyCodeGen.py

class MyUglyPrinter (ASTHandler):


    def handle_children(self, node):
        v = [self.handle(child) for child in self.get_children(node) ]
        print v
        return "".join(v)

    def handle_list(self, node):
        v = [self.handle(child) for child in node ]
        print v
        return "".join(v)

    handle_tuple = handle_list

    def handle_Add (self, node):
        return ""

    def handle_And (self, node):
        return ""

    def handle_Assert (self, node):
        return ""

    def handle_Assign (self, node):
        return ""

    def handle_Attribute (self, node):
        return ""

    def handle_AugAssign (self, node):
        return ""

    def handle_AugLoad (self, node):
        return ""

    def handle_AugStore (self, node):
        return ""

    def handle_BinOp (self, node):
        return ""

    def handle_BitAnd (self, node):
        return ""

    def handle_BitOr (self, node):
        return ""

    def handle_BitXor (self, node):
        return ""

    def handle_BoolOp (self, node):
        return ""

    def handle_Break (self, node):
        return ""

    def handle_Call (self, node):
        return ""

    def handle_ClassDef (self, node):
        return ""

    def handle_Compare (self, node):
        return ""

    def handle_Continue (self, node):
        return ""

    def handle_Del (self, node):
        return ""

    def handle_Delete (self, node):
        return ""

    def handle_Dict (self, node):
        return ""

    def handle_Div (self, node):
        return ""

    def handle_Ellipsis (self, node):
        return ""

    def handle_Eq (self, node):
        return ""

    def handle_Exec (self, node):
        return ""

    def handle_Expr (self, node):
        return '%s\n' % self.handle_children(node)
    
    def handle_Expression (self, node):
        return ""

    def handle_ExtSlice (self, node):
        return ""

    def handle_FloorDiv (self, node):
        return ""

    def handle_For (self, node):
        return ""

    def handle_FunctionDef (self, node):
        return ""

    def handle_GeneratorExp (self, node):
        return ""

    def handle_Global (self, node):
        return ""

    def handle_Gt (self, node):
        return ""

    def handle_GtE (self, node):
        return ""

    def handle_If (self, node):
        return ""

    def handle_IfExp (self, node):
        return ""

    def handle_Import (self, node):
        return ""

    def handle_ImportFrom (self, node):
        return ""

    def handle_In (self, node):
        return ""

    def handle_Index (self, node):
        return ""

    def handle_Interactive (self, node):
        return ""

    def handle_Invert (self, node):
        return ""

    def handle_Is (self, node):
        return ""

    def handle_IsNot (self, node):
        return ""

    def handle_LShift (self, node):
        return ""

    def handle_Lambda (self, node):
        return ""

    def handle_List (self, node):
        return ""

    def handle_ListComp (self, node):
        return ""

    def handle_Load (self, node):
        return ""

    def handle_Lt (self, node):
        return ""

    def handle_LtE (self, node):
        return ""

    def handle_Mod (self, node):
        return ""

    def _handle_Module (self, node):
        return ""

    def handle_Mult (self, node):
        return ""

    def handle_Name (self, node):
        return node.id

    def handle_Not (self, node):
        return ""

    def handle_NotEq (self, node):
        return ""

    def handle_NotIn (self, node):
        return ""

    def handle_Num (self, node):
        return ""

    def handle_Or (self, node):
        return ""

    def handle_Param (self, node):
        return ""

    def handle_Pass (self, node):
        return ""

    def handle_Pow (self, node):
        return ""

    def handle_Print (self, node):
        return ""

    def handle_QuoteDef (self, node):
        return ""

    def handle_RShift (self, node):
        return ""

    def handle_Raise (self, node):
        return ""

    def handle_Repr (self, node):
        return ""

    def handle_Return (self, node):
        return ""

    def handle_Slice (self, node):
        return ""

    def handle_Store (self, node):
        return ""

    def handle_Str (self, node):
        return ""

    def handle_Sub (self, node):
        return ""

    def handle_Subscript (self, node):
        return ""

    def handle_Suite (self, node):
        return ""

    def handle_TryExcept (self, node):
        return ""

    def handle_TryFinally (self, node):
        return ""

    def handle_Tuple (self, node):
        return ""

    def handle_UAdd (self, node):
        return ""

    def handle_USub (self, node):
        return ""

    def handle_UnaryOp (self, node):
        return ""

    def handle_While (self, node):
        return ""

    def handle_With (self, node):
        return ""

    def handle_Yield (self, node):
        return ""

    def handle_alias (self, node):
        return ""

    def handle_arguments (self, node):
        return ""

    def handle_comprehension (self, node):
        return ""

    def handle_excepthandler (self, node):
        return ""

    def handle_keyword (self, node):
        return ""


class MyUglierPrinter(ASTHandler):
    def __init__(self):
        self.level = 0
        self.indent = "  "
        
    def handle_children(self,node):
        print self.indent * self.level, type(node).__name__
        self.level += 1
        _val = super(type(self),self).handle_children(node)
        self.level -= 1
        return _val


# ______________________________________________________________________
# Main (self-test) routine.

test_strings = [
    "None\n",
    ]

def main (*args):
    global test_strings
    ugly_printer = MyUglyPrinter()    
    uglier_printer = MyUglierPrinter()    
    def handle_source (source, filename = "<string>"):
        ast, env = myfrontend(source, {"filename" : filename})
        uglier_printer.handle(ast)
        outstring = ugly_printer.handle(ast)
        print "outstring: ", outstring
        return myfrontend(outstring, env)[0] == ast # T(~T(T(s))) == T(s)
    if not args:
        for source in test_strings:
            print "_" * 70
            print source, handle_source(source)
    else:
        for arg in args:
            source = open(arg).read()
            print "_" * 70
            print source, handle_source(source, arg)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MyUglyPrinter.py
