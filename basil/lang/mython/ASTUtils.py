#! /usr/bin/env python
# ______________________________________________________________________
"""Module ASTUtils.py

Utility library for playing around with various kinds of abstract
syntax trees.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import myfront_ast

# ______________________________________________________________________
# Function definitions

def mk_ast_to_tuple (ast_class):
    """mk_ast_to_tuple() - Given a class, create a closue that
    converts from the given AST class to nested tuple/list
    representation of the abstract tree constructors.
    Note that this won't work for the wrapped AST objects."""
    def ast_to_tuple (ast_elem):
        ret_val = ast_elem
        elem_type = type(ast_elem)
        if issubclass(elem_type, ast_class):
            node_constructor_co = elem_type.__init__.im_func.func_code
            constructor_args = node_constructor_co.co_varnames[1:]
            constructor_vals = [ast_to_tuple(getattr(ast_elem, arg))
                                for arg in constructor_args]
            ret_val = (elem_type.__name__, constructor_vals)
        elif elem_type in (list, tuple):
            ret_val = [ast_to_tuple(child_elem) for child_elem in ast_elem]
            if elem_type == tuple:
                ret_val = tuple(ret_val)
        return ret_val
    return ast_to_tuple

# ______________________________________________________________________
# Note: An alternate way to get the constructor arguments would be to
# parse the ASDL file again (this goes the long way around by using
# asdl_py, then introspecting the resulting Python module/classes).

def mk_pyast_to_tuple (ast_dict):
    """mk_pyast_to_tuple() - Given a namespace for determining the
    constructor order, return a function that converts from Python
    AST's to a nested tuple/list representation."""
    import _ast
    def pyast_to_tuple (ast_elem):
        ret_val = ast_elem
        elem_type = type(ast_elem)
        if issubclass(elem_type, _ast.AST):
            elem_type_name = elem_type.__name__
            elem_type_analog = ast_dict[elem_type_name]
            analog_constructor_co = elem_type_analog.__init__.im_func.func_code
            constructor_args = analog_constructor_co.co_varnames[1:]
            constructor_vals = [pyast_to_tuple(getattr(ast_elem, arg))
                                for arg in constructor_args]
            ret_val = (elem_type_name, constructor_vals)
        elif elem_type in (list, tuple):
            ret_val = [pyast_to_tuple(child_elem) for child_elem in ast_elem]
            if elem_type == tuple:
                ret_val = tuple(ret_val)
        return ret_val
    return pyast_to_tuple

# ______________________________________________________________________

def mk_ast_get_children (ast_module):
    """mk_ast_get_children()"""
    def ast_get_children (node):
        return [val for val in node.__dict__.values()
                if isinstance(val, ast_module.AST) or
                (type(val) in (list, tuple) and len(val) > 0 and
                 isinstance(val[0], ast_module.AST))]
    return ast_get_children

# ______________________________________________________________________

def gen_py_handlers (ast_module):
    """gen_py_handlers() - returns Python code for a handler class,
    given a asdl_py.py generated module (formerly
    MyCodeGen.__gen_handlers())."""
    nodetypes = [x for x in dir(ast_module)
                 if type(getattr(ast_module, x)) == type and
                 issubclass(getattr(ast_module, x),
                            getattr(ast_module, "AST"))]
    nodetypes.sort()
    nodetypes.remove("AST")
    return "\n".join(["    def handle_%s (self, node):\n        pass\n" %
                     nodetype for nodetype in nodetypes])

# ______________________________________________________________________

def mk_escaper (ast_module):
    def myescape (obj):
        """myescape(obj) Translate the given AST into a Python AST
        that can be evaluated to construct the given AST."""
        if isinstance(obj, ast_module.AST):
            ast_type = type(obj)
            esc_args = [myescape(getattr(obj, ctor_arg))
                        for ctor_arg in ast_type.__init__.func_code.co_names]
            ret_val = myfront_ast.Call(myfront_ast.Name(ast_type.__name__,
                                                        myfront_ast.Load()),
                                       esc_args, [], None, None)
        elif isinstance(obj, list):
            ret_val = myfront_ast.List([myescape(subobj) for subobj in obj],
                                       myfront_ast.Load())
        elif isinstance(obj, tuple):
            ret_val = myfront_ast.Tuple([myescape(subobj) for subobj in obj],
                                        myfront_ast.Load())
        elif isinstance(obj, int):
            ret_val = myfront_ast.Num(obj)
        elif isinstance(obj, float):
            ret_val = myfront_ast.Num(obj)
        elif isinstance(obj, str):
            ret_val = myfront_ast.Str(obj)
        elif obj is None:
            ret_val = myfront_ast.Name("None", myfront_ast.Load())
        else:
            raise NotImplementedError("Don't know how to escape '%r'!" % (obj))
        return ret_val
    return myescape

# ______________________________________________________________________
# Class definitions

class GenericASTHandler (object):
    def get_children (self, node):
        raise NotImplementedError("Override me!")

    def handle_children (self, node):
        children = self.get_children(node)
        for child in children:
            self.handle(child)
        return node

    def handle_list (self, node_seq):
        for node in node_seq:
            self.handle(node)
        return node_seq

    handle_tuple = handle_list

    def handle (self, node):
        handler_method_name = "handle_%s" % type(node).__name__
        handler_method = getattr(self, handler_method_name,
                                 self.handle_children)
        return handler_method(node)

# ______________________________________________________________________
# End of ASTUtils.py
