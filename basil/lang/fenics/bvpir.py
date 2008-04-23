#! /usr/bin/env python
class AST (object):
    pass

class closure (AST):
    pass

class decl (AST):
    pass

class expr (AST):
    pass

class lvalue (AST):
    pass

class stmt (AST):
    pass

class Add (expr):
    def __init__ (self, exprs = None, lineno = None):
        self.exprs = exprs
        self.lineno = lineno

class Assign (stmt):
    def __init__ (self, lhs = None, rhs = None, lineno = None, result = None):
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno
        self.result = result

class BVPClosure (closure):
    def __init__ (self, decs = None, body = None):
        self.decs = decs
        self.body = body

class Const (expr):
    def __init__ (self, val = None, lineno = None):
        self.val = val
        self.lineno = lineno

class Index (expr):
    def __init__ (self, iexpr = None, index = None, lineno = None):
        self.iexpr = iexpr
        self.index = index
        self.lineno = lineno

class LIndex (lvalue):
    def __init__ (self, expr = None, index = None, lineno = None):
        self.expr = expr
        self.index = index
        self.lineno = lineno

class LVar (lvalue):
    def __init__ (self, lvid = None, lineno = None):
        self.lvid = lvid
        self.lineno = lineno

class Loop (stmt):
    def __init__ (self, loop_var = None, loop_iter = None, body = None, lineno = None, result = None):
        self.loop_var = loop_var
        self.loop_iter = loop_iter
        self.body = body
        self.lineno = lineno
        self.result = result

class Mult (expr):
    def __init__ (self, exprs = None, lineno = None):
        self.exprs = exprs
        self.lineno = lineno

class Pow (expr):
    def __init__ (self, lexpr = None, exp_expr = None, lineno = None):
        self.lexpr = lexpr
        self.exp_expr = exp_expr
        self.lineno = lineno

class Special (stmt):
    def __init__ (self, sid = None, options = None, lineno = None, result = None):
        self.sid = sid
        self.options = options
        self.lineno = lineno
        self.result = result

class SpecialExpr (expr):
    def __init__ (self, sid = None, options = None, lineno = None):
        self.sid = sid
        self.options = options
        self.lineno = lineno

class Sub (expr):
    def __init__ (self, exprs = None, lineno = None):
        self.exprs = exprs
        self.lineno = lineno

class Sum (expr):
    def __init__ (self, loop_var = None, loop_iter = None, sexpr = None, lineno = None):
        self.loop_var = loop_var
        self.loop_iter = loop_iter
        self.sexpr = sexpr
        self.lineno = lineno

class SumAssign (stmt):
    def __init__ (self, lhs = None, rhs = None, lineno = None, result = None):
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno
        self.result = result

class VDec (decl):
    def __init__ (self, id = None, ty = None, dim = None, init = None, lineno = None):
        self.id = id
        self.ty = ty
        self.dim = dim
        self.init = init
        self.lineno = lineno

class Var (expr):
    def __init__ (self, vid = None, lineno = None):
        self.vid = vid
        self.lineno = lineno
