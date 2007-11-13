#! /usr/bin/env python
# ______________________________________________________________________
"""Module mybuiltins.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import os as _os
import struct as _struct
import marshal as _marshal
import imp as _imp
import new as _new
import StringIO as _StringIO
import tokenize as _tokenize
import pprint as _pprint

import ASTUtils as _ASTUtils
import MyRealParser as _myparser
import myfront_transformer as _myabs
import MythonRewriter as _myrw
import MyCodeGen as _mycodegen
import myfront_ast as _ast

# ______________________________________________________________________
# Function definitions

def myfrontend (text, env):
    """myfrontend()
    """
    abstract_tree, env = myparse(text, env)
    #ast_to_tuple = _ASTUtils.mk_ast_to_tuple(_ast.AST)
    #_pprint.pprint(ast_to_tuple(abstract_tree))
    return _myrw.rewriteToPython(abstract_tree, env)

# ______________________________________________________________________

def mybackend (tree, env):
    """mybackend()
    Given what is presumably a Python abstract syntax tree, generate a
    code object for that tree."""
    assert isinstance(tree, _ast.AST)
    codegen_obj = _mycodegen.MyCodeGen(env.get("filename", "<string>"))
    codegen_obj.handle(tree)
    return codegen_obj.get_code(), env

# ______________________________________________________________________

def myparse (text, env):
    """myparse(text, env)
    Parse the given string into an abstract syntax tree.  The
    environment argument is used to pass information such as filename,
    and starting line number."""
    assert isinstance(text, str)
    # XXX - There is going to be some line number mismatch stuff here;
    # look into it and fix it.
    tokenizer_readline = _StringIO.StringIO(text).readline
    tokenizer = _tokenize.generate_tokens(tokenizer_readline)
    filename = env.get("filename", "<string>")
    parser = _myparser.MyRealParser(tokenizer, filename)
    concrete_tree = parser()
    return _myabs.MyHandler().handle_node(concrete_tree), env

# ______________________________________________________________________

def myeval (code, env = None):
    """myeval(code, env)
    Evaluate the given abstract syntax tree, ast, in the environment, env.
    Returns the evaluation result."""
    if env is None:
        env = globals()
    ret_val = None
    # This is a hack that works because the Mython expression language
    # is identical to Python's.
    # XXX Consider splitting the myeval() and myexec() (contrary to
    # the original Mython paper).
    if isinstance(code, str):
        ret_val = eval(code, env)
    else:
        assert isinstance(code, _ast.AST)
        env = env.copy()
        code_obj, env = mybackend(code, env)
        ret_val = eval(code_obj, env)
    return ret_val, env

# ______________________________________________________________________

def myescape (obj):
    """myescape(obj)
    Translate the given Mython AST into a Python AST that can be
    evaluated to construct the given Mython AST."""
    if isinstance(obj, _ast.AST):
        ast_type = type(obj)
        esc_args = [myescape(getattr(obj, ctor_arg))
                    for ctor_arg in ast_type.__init__.func_code.co_names]
        ret_val = _ast.Call(_ast.Name(ast_type.__name__, _ast.Load()),
                            esc_args, [], None, None)
    elif isinstance(obj, list):
        ret_val = _ast.List([myescape(subobj) for subobj in obj], _ast.Load())
    elif isinstance(obj, tuple):
        ret_val = _ast.Tuple([myescape(subobj) for subobj in obj], _ast.Load())
    elif isinstance(obj, int):
        ret_val = _ast.Num(obj)
    elif isinstance(obj, str):
        ret_val = _ast.Str(obj)
    elif obj is None:
        ret_val = _ast.Name("None", _ast.Load())
    else:
        raise NotImplementedError("Don't know how to escape `%r`!" % (obj))
    return ret_val

# ______________________________________________________________________

def mython (name, code, env0):
    """mython(name, code, env0)
    Quotation function for Mython."""
    stmt_lst = []
    ast, env1 = myparse(code, env0)
    esc_ast = myescape(ast)
    if name is not None:
        env1[name] = ast
        # XXX Add line and position information to the constructed syntax.
        stmt_lst = [_ast.Assign([_ast.Name(name, _ast.Store())], esc_ast)]
    else:
        stmt_lst = [_ast.Expr(esc_ast)]
    return stmt_lst, env1

# ______________________________________________________________________

def myfront (name, code, env0):
    """myfront(name, code, env0)
    Pragma function for MyFront."""
    ast, env = myparse(code, env0)
    env = env.copy()
    if name is not None:
        env[name] = ast
    _, env = myeval(ast, env)
    return [], env

# ______________________________________________________________________

def output_module_co (name, code_obj, env):
    """output_module_co()
    """
    assert isinstance(code_obj, _new.code)
    if name is not None:
        outfile = open(name, "wb")
        outfile.write(_imp.get_magic())
        if "filename" in env:
            mtime = _os.path.getmtime(env["filename"])
        else:
            mtime = 0
        outfile.write(_struct.pack("<i", mtime))
        outfile.write(_marshal.dumps(code_obj))
        outfile.close()
    return env

# ______________________________________________________________________

def initial_environment ():
    ret_val = {}
    for key, value in globals().items():
        if key[0] != "_":
            ret_val[key] = value
    return ret_val

# ______________________________________________________________________
# End of mybuiltins.py
