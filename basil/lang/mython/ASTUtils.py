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
# End of ASTUtils.py
