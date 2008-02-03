#! /usr/bin/env python
class AST (object):
    pass

class Assign (AST):
    def __init__ (self, lhs = None, rhs = None, lineno = None):
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno

class BVPClosure (AST):
    def __init__ (self, decs = None, body = None):
        self.decs = decs
        self.body = body

class Const (AST):
    def __init__ (self, val = None, lineno = None):
        self.val = val
        self.lineno = lineno

class Index (AST):
    def __init__ (self, iexpr = None, index = None, lineno = None):
        self.iexpr = iexpr
        self.index = index
        self.lineno = lineno

class LIndex (AST):
    def __init__ (self, expr = None, index = None, lineno = None):
        self.expr = expr
        self.index = index
        self.lineno = lineno

class LVar (AST):
    def __init__ (self, lvid = None, lineno = None):
        self.lvid = lvid
        self.lineno = lineno

class Loop (AST):
    def __init__ (self, loop_var = None, loop_iter = None, body = None, lineno = None):
        self.loop_var = loop_var
        self.loop_iter = loop_iter
        self.body = body
        self.lineno = lineno

class Mult (AST):
    def __init__ (self, exprs = None, lineno = None):
        self.exprs = exprs
        self.lineno = lineno

class Special (AST):
    def __init__ (self, sid = None, lineno = None):
        self.sid = sid
        self.lineno = lineno

class Sum (AST):
    def __init__ (self, loop_var = None, loop_iter = None, sexpr = None, lineno = None):
        self.loop_var = loop_var
        self.loop_iter = loop_iter
        self.sexpr = sexpr
        self.lineno = lineno

class SumAssign (AST):
    def __init__ (self, lhs = None, rhs = None, lineno = None):
        self.lhs = lhs
        self.rhs = rhs
        self.lineno = lineno

class VDec (AST):
    def __init__ (self, id = None, ty = None, dim = None, init = None, lineno = None):
        self.id = id
        self.ty = ty
        self.dim = dim
        self.init = init
        self.lineno = lineno

class Var (AST):
    def __init__ (self, vid = None, lineno = None):
        self.vid = vid
        self.lineno = lineno
