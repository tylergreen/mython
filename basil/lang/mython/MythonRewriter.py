#! /usr/bin/env python
# ______________________________________________________________________
"""Module MythonRewriter

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import myfront_ast

from MyCodeGen import ASTHandler

# ______________________________________________________________________
# Function definitions

class MyRewriter (ASTHandler):
    """Class MyRewriter
    Translate from a Mython AST into a Python AST.

    XXX I should so totally be able to automate the generation of this code,
    or just use stategy combinators."""
    # ____________________________________________________________
    def __init__ (self, env):
        """MyRewriter.__init__()
        Constructor for the rewriter class."""
        self.env = env
        self.env_stack = []
    # ____________________________________________________________
    def push_environment (self):
        self.env_stack.append(self.env)
        self.env = self.env.copy()
    # ____________________________________________________________
    def pop_environment (self):
        self.env = self.env_stack.pop()
    # ____________________________________________________________
    def handle_body (self, node):
        if hasattr(node, "body"):
            node.body = self.handle_stmts(node.body)
        return node
    # ____________________________________________________________
    handle_Interactive = handle_body
    handle_Suite = handle_body
    handle_With = handle_body
    handle_excepthandler = handle_body
    # ____________________________________________________________
    def handle_namespace (self, node):
        self.push_environment()
        node.body = self.handle_stmts(node.body)
        self.pop_environment()
        return node
    # ____________________________________________________________
    handle_Module = handle_namespace
    handle_FunctionDef = handle_namespace
    handle_ClassDef = handle_namespace
    # ____________________________________________________________
    def handle_body_and_orelse (self, node):
        node.body = self.handle_stmts(node.body)
        node.orelse = self.handle_stmts(node.orelse)
        return node
    # ____________________________________________________________
    handle_For = handle_body_and_orelse
    handle_While = handle_body_and_orelse
    handle_If = handle_body_and_orelse
    # ____________________________________________________________
    def handle_TryExcept (self, node):
        node.body = self.handle_stmts(node.body)
        self.handle(node.handlers)
        node.orelse = self.handle_stmts(node.orelse)
        return node
    # ____________________________________________________________
    def handle_TryFinally (self, node):
        node.body = self.handle_stmts(node.body)
        node.finalbody = self.handle_stmts(node.finalbody)
    # ____________________________________________________________
    def handle_stmts (self, nodes):
        ret_val = []
        for node in nodes:
            child_result = self.handle(node)
            if isinstance(child_result, list):
                ret_val += child_result
            elif isinstance(child_result, tuple):
                ret_val += list(child_result)
            else:
                ret_val.append(child_result)
        return ret_val
    # ____________________________________________________________
    def handle_QuoteDef (self, node):
        myeval = self.env["myeval"]
        if node.lang is None:
            lang = "mython"
        else:
            lang = myfront_ast.Expression(node.lang)
        quotefn, env = myeval(lang, self.env)
        ret_val, env = quotefn(node.name, node.body, env)
        self.env = env
        return ret_val
    # ____________________________________________________________
    def _warn (self, node, warning_str, include_traceback = True):
        # XXX Possibly make "include_traceback" be a compiler flag for
        # verbosity instead?
        if include_traceback:
            import traceback
            warning_str = "\n".join((warning_str, traceback.format_exc()))
        mywarn = self.env["warn"]
        self.env = mywarn(node, warning_str, self.env)
        return self.env
    # ____________________________________________________________
    def _import_module (self, module_name, node = None, from_list = None):
        """MyRewriter._import_module(module_name, node?) -> module?

        Use the Mython importer to load a module of the given name.
        Optional node argument is used to get line information."""
        module = None
        myimport = self.env["__myimport__"]
        try:
            # XXX Check import level semantics here...
            level = getattr(node, "level", None)
            # XXX I'm not sure we care about the environment here --
            # does __myimport__() really need to follow the explicit
            # store passing style of the rest of the built-ins?
            # Besides, I'm made Module a namespace, so it'll dup/push
            # and then pop the compile-time environment anyway.
            if level:
                module, self.env = myimport(module_name, self.env, {},
                                            from_list, level)
            else:
                module, self.env = myimport(module_name, self.env, {},
                                            from_list)
        except ImportError:
            self._warn(node, "Failed to import '%s', module will not be "
                       "available at compile time." % module_name)
        return module
    # ____________________________________________________________
    def handle_Import (self, node):
        """MyRewriter.handle_Import(node) -> node

        Import the given modules in an Import AST node into the
        current compile-time environment.  Unlike run-time import,
        this forces compilation of Mython modules."""
        for alias in node.names:
            module = self._import_module(alias.name, node)
            if not alias.asname:
                top = alias.name.split(".")[0]
                self.env[top] = module
            else:
                # XXX Is there an easier way to do this traversal?
                for submodule_name in alias.name.split(".")[1:]:
                    module = getattr(module, submodule_name)
                self.env[alias.asname] = module
        return node
    # ____________________________________________________________
    def handle_ImportFrom (self, node):
        """MyRewriter.handle_ImportFrom(node) -> node

        Import the given names in the ImportFrom AST node into the
        current compile-time environment.  Unlike run-time import,
        this forces compilation of Mython modules."""
        from_list = [alias.name for alias in node.names]
        module = self._import_module(node.module, node, from_list)
        if module:
            #for submodule_name in node.module.split(".")[1:]:
            #    module = getattr(module, submodule_name)
            update_env = {}
            if node.names[0].name == "*":
                assert len(node.names) == 1
                try:
                    module_keys = getattr(module, "__all__",
                                          module.__dict__.keys())
                    for module_key in module_keys:
                        update_env[module_key] = getattr(module, module_key)
                except:
                    self._warn(node, "Failed to import * from %s, names "
                               "are not bound and may cause compile-time "
                               "exceptions." % node.module)
            else:
                for alias in node.names:
                    if alias.asname:
                        local_name = alias.asname
                    else:
                        local_name = alias.name
                    try:
                        update_env[local_name] = getattr(module, alias.name)
                    except:
                        self._warn(node, "Failed to import %s from %s, name "
                                   "is not bound and may cause compile-time "
                                   "exceptions." % (local_name, node.module))
            self.env.update(update_env)
        return node

# ______________________________________________________________________

def rewriteToPython (ast, env):
    """rewriteToPython()
    Translate the given ast from Mython abstract syntax to Python abstract
    syntax."""
    rewriter = MyRewriter(env)
    ast = rewriter.handle(ast)
    return ast, rewriter.env

# ______________________________________________________________________
# End of MythonRewriter.py
