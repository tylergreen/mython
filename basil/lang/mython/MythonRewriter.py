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
    handle_Module = handle_body
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
    def handle_Import (self, node):
        for alias in node.names:
            module = None
            myimport = self.env["__myimport__"]
            # ________________________________________
            try:
                module = myimport(alias.name, self.env)
            except ImportError:
                import traceback
                warning = ("Failed to import '%s', module will not be "
                           "available at compile time.\n%s" %
                           (alias.name, traceback.format_exc()))
                self.env = self.env["warn"](node, warning, self.env)
            # ________________________________________
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
        warning = "ImportFrom not currently handled at compile time."
        self.env = self.env["warn"](node, warning, self.env)
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
