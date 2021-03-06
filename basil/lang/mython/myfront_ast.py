#! /usr/bin/env python
# ______________________________________________________________________
"""Module myfront_ast.py

Automatically generated by asdl_py.py.  Made some comments and extensions to the AST class.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Class definitions

class AST (object):
    pass

class Add (AST):
    def __init__ (self):
        pass

class And (AST):
    def __init__ (self):
        pass

class Assert (AST):
    def __init__ (self, test = None, msg = None, lineno = None, col_offset = None):
        self.test = test
        self.msg = msg
        self.lineno = lineno
        self.col_offset = col_offset

class Assign (AST):
    def __init__ (self, targets = None, value = None, lineno = None, col_offset = None):
        self.targets = targets
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class Attribute (AST):
    def __init__ (self, value = None, attr = None, ctx = None, lineno = None, col_offset = None):
        self.value = value
        self.attr = attr
        self.ctx = ctx
        self.lineno = lineno
        self.col_offset = col_offset

class AugAssign (AST):
    def __init__ (self, target = None, op = None, value = None, lineno = None, col_offset = None):
        self.target = target
        self.op = op
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class AugLoad (AST):
    def __init__ (self):
        pass

class AugStore (AST):
    def __init__ (self):
        pass

class BinOp (AST):
    def __init__ (self, left = None, op = None, right = None, lineno = None, col_offset = None):
        self.left = left
        self.op = op
        self.right = right
        self.lineno = lineno
        self.col_offset = col_offset

class BitAnd (AST):
    def __init__ (self):
        pass

class BitOr (AST):
    def __init__ (self):
        pass

class BitXor (AST):
    def __init__ (self):
        pass

class BoolOp (AST):
    def __init__ (self, op = None, values = None, lineno = None, col_offset = None):
        self.op = op
        self.values = values
        self.lineno = lineno
        self.col_offset = col_offset

class Break (AST):
    def __init__ (self, lineno = None, col_offset = None):
        self.lineno = lineno
        self.col_offset = col_offset

class Call (AST):
    def __init__ (self, func = None, args = None, keywords = None, starargs = None, kwargs = None, lineno = None, col_offset = None):
        self.func = func
        self.args = args
        self.keywords = keywords
        self.starargs = starargs
        self.kwargs = kwargs
        self.lineno = lineno
        self.col_offset = col_offset

class ClassDef (AST):
    def __init__ (self, name = None, bases = None, body = None, lineno = None, col_offset = None):
        self.name = name
        self.bases = bases
        self.body = body
        self.lineno = lineno
        self.col_offset = col_offset

class Compare (AST):
    def __init__ (self, left = None, ops = None, comparators = None, lineno = None, col_offset = None):
        self.left = left
        self.ops = ops
        self.comparators = comparators
        self.lineno = lineno
        self.col_offset = col_offset

class Continue (AST):
    def __init__ (self, lineno = None, col_offset = None):
        self.lineno = lineno
        self.col_offset = col_offset

class Del (AST):
    def __init__ (self):
        pass

class Delete (AST):
    def __init__ (self, targets = None, lineno = None, col_offset = None):
        self.targets = targets
        self.lineno = lineno
        self.col_offset = col_offset

class Dict (AST):
    def __init__ (self, keys = None, values = None, lineno = None, col_offset = None):
        self.keys = keys
        self.values = values
        self.lineno = lineno
        self.col_offset = col_offset

class Div (AST):
    def __init__ (self):
        pass

class Ellipsis (AST):
    def __init__ (self):
        pass

class Eq (AST):
    def __init__ (self):
        pass

class Exec (AST):
    def __init__ (self, body = None, globals = None, locals = None, lineno = None, col_offset = None):
        self.body = body
        self.globals = globals
        self.locals = locals
        self.lineno = lineno
        self.col_offset = col_offset

class Expr (AST):
    def __init__ (self, value = None, lineno = None, col_offset = None):
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class Expression (AST):
    def __init__ (self, body = None):
        self.body = body

class ExtSlice (AST):
    def __init__ (self, dims = None):
        self.dims = dims

class FloorDiv (AST):
    def __init__ (self):
        pass

class For (AST):
    def __init__ (self, target = None, iter = None, body = None, orelse = None, lineno = None, col_offset = None):
        self.target = target
        self.iter = iter
        self.body = body
        self.orelse = orelse
        self.lineno = lineno
        self.col_offset = col_offset

class FunctionDef (AST):
    def __init__ (self, name = None, args = None, body = None, decorators = None, lineno = None, col_offset = None):
        self.name = name
        self.args = args
        self.body = body
        self.decorators = decorators
        self.lineno = lineno
        self.col_offset = col_offset

class GeneratorExp (AST):
    def __init__ (self, elt = None, generators = None, lineno = None, col_offset = None):
        self.elt = elt
        self.generators = generators
        self.lineno = lineno
        self.col_offset = col_offset

class Global (AST):
    def __init__ (self, names = None, lineno = None, col_offset = None):
        self.names = names
        self.lineno = lineno
        self.col_offset = col_offset

class Gt (AST):
    def __init__ (self):
        pass

class GtE (AST):
    def __init__ (self):
        pass

class If (AST):
    def __init__ (self, test = None, body = None, orelse = None, lineno = None, col_offset = None):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.lineno = lineno
        self.col_offset = col_offset

class IfExp (AST):
    def __init__ (self, test = None, body = None, orelse = None, lineno = None, col_offset = None):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.lineno = lineno
        self.col_offset = col_offset

class Import (AST):
    def __init__ (self, names = None, lineno = None, col_offset = None):
        self.names = names
        self.lineno = lineno
        self.col_offset = col_offset

class ImportFrom (AST):
    def __init__ (self, module = None, names = None, level = None, lineno = None, col_offset = None):
        self.module = module
        self.names = names
        self.level = level
        self.lineno = lineno
        self.col_offset = col_offset

class In (AST):
    def __init__ (self):
        pass

class Index (AST):
    def __init__ (self, value = None):
        self.value = value

class Interactive (AST):
    def __init__ (self, body = None):
        self.body = body

class Invert (AST):
    def __init__ (self):
        pass

class Is (AST):
    def __init__ (self):
        pass

class IsNot (AST):
    def __init__ (self):
        pass

class LShift (AST):
    def __init__ (self):
        pass

class Lambda (AST):
    def __init__ (self, args = None, body = None, lineno = None, col_offset = None):
        self.args = args
        self.body = body
        self.lineno = lineno
        self.col_offset = col_offset

class List (AST):
    def __init__ (self, elts = None, ctx = None, lineno = None, col_offset = None):
        self.elts = elts
        self.ctx = ctx
        self.lineno = lineno
        self.col_offset = col_offset

class ListComp (AST):
    def __init__ (self, elt = None, generators = None, lineno = None, col_offset = None):
        self.elt = elt
        self.generators = generators
        self.lineno = lineno
        self.col_offset = col_offset

class Load (AST):
    def __init__ (self):
        pass

class Lt (AST):
    def __init__ (self):
        pass

class LtE (AST):
    def __init__ (self):
        pass

class Mod (AST):
    def __init__ (self):
        pass

class Module (AST):
    def __init__ (self, body = None):
        self.body = body

class Mult (AST):
    def __init__ (self):
        pass

class Name (AST):
    def __init__ (self, id = None, ctx = None, lineno = None, col_offset = None):
        self.id = id
        self.ctx = ctx
        self.lineno = lineno
        self.col_offset = col_offset

class Not (AST):
    def __init__ (self):
        pass

class NotEq (AST):
    def __init__ (self):
        pass

class NotIn (AST):
    def __init__ (self):
        pass

class Num (AST):
    def __init__ (self, n = None, lineno = None, col_offset = None):
        self.n = n
        self.lineno = lineno
        self.col_offset = col_offset

class Or (AST):
    def __init__ (self):
        pass

class Param (AST):
    def __init__ (self):
        pass

class Pass (AST):
    def __init__ (self, lineno = None, col_offset = None):
        self.lineno = lineno
        self.col_offset = col_offset

class Pow (AST):
    def __init__ (self):
        pass

class Print (AST):
    def __init__ (self, dest = None, values = None, nl = None, lineno = None, col_offset = None):
        self.dest = dest
        self.values = values
        self.nl = nl
        self.lineno = lineno
        self.col_offset = col_offset

class QuoteDef (AST):
    def __init__ (self, lang = None, name = None, body = None, body_ofs = None, lineno = None, col_offset = None):
        self.lang = lang
        self.name = name
        self.body = body
        self.body_ofs = body_ofs
        self.lineno = lineno
        self.col_offset = col_offset

class RShift (AST):
    def __init__ (self):
        pass

class Raise (AST):
    def __init__ (self, type = None, inst = None, tback = None, lineno = None, col_offset = None):
        self.type = type
        self.inst = inst
        self.tback = tback
        self.lineno = lineno
        self.col_offset = col_offset

class Repr (AST):
    def __init__ (self, value = None, lineno = None, col_offset = None):
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class Return (AST):
    def __init__ (self, value = None, lineno = None, col_offset = None):
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class Slice (AST):
    def __init__ (self, lower = None, upper = None, step = None):
        self.lower = lower
        self.upper = upper
        self.step = step

class Store (AST):
    def __init__ (self):
        pass

class Str (AST):
    def __init__ (self, s = None, lineno = None, col_offset = None):
        self.s = s
        self.lineno = lineno
        self.col_offset = col_offset

class Sub (AST):
    def __init__ (self):
        pass

class Subscript (AST):
    def __init__ (self, value = None, slice = None, ctx = None, lineno = None, col_offset = None):
        self.value = value
        self.slice = slice
        self.ctx = ctx
        self.lineno = lineno
        self.col_offset = col_offset

class Suite (AST):
    def __init__ (self, body = None):
        self.body = body

class TryExcept (AST):
    def __init__ (self, body = None, handlers = None, orelse = None, lineno = None, col_offset = None):
        self.body = body
        self.handlers = handlers
        self.orelse = orelse
        self.lineno = lineno
        self.col_offset = col_offset

class TryFinally (AST):
    def __init__ (self, body = None, finalbody = None, lineno = None, col_offset = None):
        self.body = body
        self.finalbody = finalbody
        self.lineno = lineno
        self.col_offset = col_offset

class Tuple (AST):
    def __init__ (self, elts = None, ctx = None, lineno = None, col_offset = None):
        self.elts = elts
        self.ctx = ctx
        self.lineno = lineno
        self.col_offset = col_offset

class UAdd (AST):
    def __init__ (self):
        pass

class USub (AST):
    def __init__ (self):
        pass

class UnaryOp (AST):
    def __init__ (self, op = None, operand = None, lineno = None, col_offset = None):
        self.op = op
        self.operand = operand
        self.lineno = lineno
        self.col_offset = col_offset

class While (AST):
    def __init__ (self, test = None, body = None, orelse = None, lineno = None, col_offset = None):
        self.test = test
        self.body = body
        self.orelse = orelse
        self.lineno = lineno
        self.col_offset = col_offset

class With (AST):
    def __init__ (self, context_expr = None, optional_vars = None, body = None, lineno = None, col_offset = None):
        self.context_expr = context_expr
        self.optional_vars = optional_vars
        self.body = body
        self.lineno = lineno
        self.col_offset = col_offset

class Yield (AST):
    def __init__ (self, value = None, lineno = None, col_offset = None):
        self.value = value
        self.lineno = lineno
        self.col_offset = col_offset

class alias (AST):
    def __init__ (self, name = None, asname = None):
        self.name = name
        self.asname = asname

class arguments (AST):
    def __init__ (self, args = None, vararg = None, kwarg = None, defaults = None):
        self.args = args
        self.vararg = vararg
        self.kwarg = kwarg
        self.defaults = defaults

class comprehension (AST):
    def __init__ (self, target = None, iter = None, ifs = None):
        self.target = target
        self.iter = iter
        self.ifs = ifs

class excepthandler (AST):
    def __init__ (self, type = None, name = None, body = None, lineno = None, col_offset = None):
        self.type = type
        self.name = name
        self.body = body
        self.lineno = lineno
        self.col_offset = col_offset

class keyword (AST):
    def __init__ (self, arg = None, value = None):
        self.arg = arg
        self.value = value

# ______________________________________________________________________
# FIXME: The following is currently human generated.  Beware.

expr_types = (BoolOp, BinOp, UnaryOp, Lambda, IfExp, Dict, ListComp,
              GeneratorExp, Yield, Compare, Call, Repr, Num, Str, Attribute,
              Subscript, Name, List, Tuple)

# ______________________________________________________________________
# End of myfront_ast.py
