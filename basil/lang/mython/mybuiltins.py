#! /usr/bin/env python
# ______________________________________________________________________
"""Module mybuiltins.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import sys as _sys
import os as _os
import stat as _stat
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
import LL1ParserUtil as _LL1ParserUtil

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

_myparse = _LL1ParserUtil.mkMyParser(_myparser.MyRealParser)

def myparse (text, env):
    """myparse(text, env)
    Parse the given string into an abstract syntax tree.  The
    environment argument is used to pass information such as filename,
    and starting line number."""
    assert isinstance(text, str)
    concrete_tree, env = _myparse(text, env)
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

myescape = _ASTUtils.mk_escaper(_ast)

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

def _load_file (filename, env):
    """_load_file()
    Given a file name, and an environment, load the file, and
    extend/modify the environment with information about the current
    file to be processed."""
    text = open(filename).read()
    env["filename"] = filename
    env["output_file"] = "%s.pyc" % (_os.path.splitext(filename)[0])
    return text, env

# ______________________________________________________________________

def mycompile_file (filename, env = None):
    """mycompile_file(filename, env) ->
    """
    if env is None:
        env = initial_environment()
    text, env = _load_file(filename, env)
    frontend = env.get("myfrontend", myfrontend)
    ast, env = frontend(text, env)
    backend = env.get("mybackend", mybackend)
    return backend(ast, env)

# ______________________________________________________________________

def _mycompile_file_to_pyc (filename, env = None):
    """_mycompile_file_to_pyc(filename, env) -> env

    Compile the given Mython file into Python bytecode, writing a .pyc
    file in the same directory.  Returns the modified, post
    compilation environment."""
    co, env = mycompile_file(filename, env)
    local_output_module_co = env.get("output_module_co", output_module_co)
    # XXX I'm not sure this is a good idea: keeping the output
    # filename in the environment.
    output_file = env.get("output_file",
                          "%s.pyc" % _os.path.splitext(filename)[0])
    env = local_output_module_co(output_file, co, env)
    return env

# ______________________________________________________________________

def warn (node, warning, env):
    """warn(node, warning, env) -> env

    Format and handle a warning message from the compiler."""
    lineno_str = "???"
    if hasattr(node, "lineno"):
        lineno_str = str(node.lineno)
    actual_warning = ('Warning, file "%s", line %s: %s\n' %
                      (env["filename"], lineno_str, warning))
    _sys.stderr.write(actual_warning)
    return env

# ______________________________________________________________________

def _check_my_file (parent_path, module_name):
    """_check_my_file(parent_path, module_name) -> string?

    Given a file path and base module file path (without a file
    extension given), check to see if a Mython module exists and needs
    to be recompiled.  Returns the path to the Mython module if so,
    None otherwise."""
    ret_val = None
    filename_base = _os.path.join(parent_path, module_name)
    my_filename = _os.path.extsep.join((filename_base, "my"))
    pyc_filename = _os.path.extsep.join((filename_base, "pyc"))
    try:
        my_filename_stat = _os.stat(my_filename)
        try:
            pyc_filename_stat = _os.stat(pyc_filename)
            my_mtime = my_filename_stat[_stat.ST_MTIME]
            pyc_mtime = pyc_filename_state[_stat.ST_MTIME]
            if pyc_mtime <= my_mtime:
                ret_val = my_filename
        except OSError:
            ret_val = my_filename
    except OSError:
        # XXX Maybe add a verbosity thing to say we checked...implying
        # an environment should be threaded along...
        pass
    return ret_val

# ______________________________________________________________________

def __myimport__ (name, global_env = None, local_env = None, from_list = None,
                  level = -1):
    """__myimport__(name, globals, locals, fromlist, level) -> module

    Compile-time import function.  Ideally this is compatible with
    Python's run-time __import__, with the exception that certain
    caveats apply to circular or non-existent imports (typically
    warnings will be generated, unless there is a compile-time
    circular dependency)."""
    # ____________________________________________________________
    # XXX I have no idea if this appropriate for __import__ compatibility.
    if global_env is None:
        global_env = initial_environment()
    if local_env is None:
        local_env = {}
    if from_list is None:
        from_list = []
    # ____________________________________________________________
    # Load parent modules
    module_path = name.split(".")
    parent_module = None
    if len(module_path) > 1:
        # XXX This is total puntage on the possibility of there being
        # an __init__.my.  Fix it.
        parent_module = __import__(".".join(module_path[:-1]),
                                   global_env.copy(),
                                   local_env, from_list, level)
    # ____________________________________________________________
    # Now see if the leaf module has a Mython file or not.
    mython_source = None
    parent_path = getattr(parent_module, "__path__", None)
    if parent_path is None:
        # XXX Could refine this to exclude paths that already have
        # importers sitting in sys.path_importer_cache.
        candidate_paths = _sys.path[:]
        mython_paths = _os.getenv("MYTHONPATH")
        if mython_paths:
            candidate_paths += mython_paths.split(_os.path.pathsep)
        # XXX This could circumvent requirements for a directory
        # being a Python package...what to do (besides get some wisdom)?
        module_dirpath = _os.path.join(*module_path)
        for candidate_path in candidate_paths:
            mython_source = _check_my_file(candidate_path, module_dirpath)
            if mython_source:
                break
    else:
        mython_source = _check_my_file(parent_path, module_path[-1])
    if mython_source:
        _mycompile_file_to_pyc(mython_source, global_env)
    # ____________________________________________________________
    # There should now be a .pyc there.  Let Python do it's thing.
    my_module = __import__(name, global_env, local_env, from_list, level)
    return my_module, global_env

# ______________________________________________________________________

def initial_environment ():
    ret_val = {}
    for key, value in globals().items():
        if (key[0] != "_") or (key in ("__myimport__",)):
            ret_val[key] = value
    return ret_val

# ______________________________________________________________________
# End of mybuiltins.py
