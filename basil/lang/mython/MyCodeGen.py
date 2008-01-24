#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyCodeGen

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import myfront_ast
from compiler import pyassem, misc, consts, symbols
import ASTUtils

# ______________________________________________________________________

class MyCodeGenError (Exception):
    pass

# ______________________________________________________________________

myast_get_children = ASTUtils.mk_ast_get_children(myfront_ast)

class ASTVisitor (object):
    def __call__ (self, node):
        stack = [node]
        visited = set()
        while stack:
            crnt_node = stack[-1]
            if type(crnt_node) in (list, tuple):
                stack.pop()
                stack += list(crnt_node)
            elif crnt_node not in visited:
                self.enter(crnt_node)
                visited.add(crnt_node)
                stack += myast_get_children(crnt_node)
            else:
                self.leave(crnt_node)
                stack.pop()

    def enter (self, node):
        raise NotImplementedError("Implement me!")

    def leave (self, node):
        raise NotImplementedError("Implement me!")

class StackVisitor (ASTVisitor):
    def __init__ (self):
        self.stack = []

    def enter (self, node):
        self.stack.append(node)

    def leave (self, node):
        assert self.stack.pop() == node

class DelegatingVisitor (ASTVisitor):
    def delegate (self, method_prefix, node):
        node_type_name = type(node).__name__
        delegate_method_name = "%s_%s" % (method_prefix, node_type_name)
        delegate_method = getattr(self, delegate_method_name, None)
        if delegate_method is not None:
            delegate_method(node)

    def enter (self, node):
        self.delegate("enter", node)

    def leave (self, node):
        self.delegate("leave", node)

class PrintingVisitor (StackVisitor):
    def enter (self, node):
        super(PrintingVisitor, self).enter(node)
        print "%s->%s" % ("  " * len(self.stack), repr(node))

    def leave (self, node):
        print "%s<-%s" % ("  " * len(self.stack), repr(node))
        super(PrintingVisitor, self).leave(node)

def walk (node, visitor = None):
    if visitor is None:
        if __debug__:
            visitor = PrintingVisitor()
        else:
            visitor = StackVisitor()
    visited = set()
    stack = [node]
    while stack:
        crnt_node = stack[-1]
        if type(crnt_node) in (list, tuple):
            stack.pop()
            stack += list(crnt_node)
        elif crnt_node not in visited:
            visitor.enter(crnt_node)
            visited.add(crnt_node)
            stack += [val for val in crnt_node.__dict__.values()
                      if isinstance(val, myfront_ast.AST) or
                      (type(val) in (list, tuple) and len(val) > 0 and
                       isinstance(val[0], myfront_ast.AST))]
        else:
            visitor.leave(crnt_node)
            stack.pop()

class LocalNameFinder (DelegatingVisitor):
    def __init__ (self, names = None):
        self.names = set()
        self.globals = set()
        if names is not None:
            for name in names:
                self.names.add(name)

    # XXX Baggage inherited from compiler module: list comprehensions
    # and for loops.

    def enter_Global (self, node):
        for name in node.names:
            self.globals.add(name)

    def _enter_named_node (self, node):
        self.names.add(node.name)

    visit_Function = _enter_named_node
    visit_Class = _enter_named_node

    def enter_alias (self, node):
        if node.asname is None:
            self.names.add(node.name)
        else:
            self.names.add(node.asname)

    def enter_Name (self, node):
        if isinstance(node.ctx, myfront_ast.Store):
            self.names.add(node.id)

def find_locals (node):
    lnf = LocalNameFinder()
    lnf(node)
    return lnf.names - lnf.globals

# ______________________________________________________________________

class ASTHandler (ASTUtils.GenericASTHandler):
    def get_children (self, node):
        global myast_get_children
        return myast_get_children(node)

# ______________________________________________________________________

class ScopeHandler (ASTHandler):
    # XXX (TODO) Remove the underscored methods after verifying they
    # are not required.

    def __init__ (self):
        self.scopes = {}
        self.klass = None
        self.module = None
        self.crnt_scope = None

    def _handle_Add (self, node):
        pass

    def _handle_And (self, node):
        pass

    def _handle_Assert (self, node):
        pass

    def _handle_Assign (self, node):
        pass

    def _handle_Attribute (self, node):
        pass

    def _handle_AugAssign (self, node):
        pass

    def _handle_AugLoad (self, node):
        pass

    def _handle_AugStore (self, node):
        pass

    def _handle_BinOp (self, node):
        pass

    def _handle_BitAnd (self, node):
        pass

    def _handle_BitOr (self, node):
        pass

    def _handle_BitXor (self, node):
        pass

    def _handle_BoolOp (self, node):
        pass

    def _handle_Break (self, node):
        pass

    def _handle_Call (self, node):
        pass

    def handle_ClassDef (self, node):
        parent = self.crnt_scope
        parent.add_def(node.name)
        self.handle_list(node.bases)
        scope = symbols.ClassScope(node.name, self.module)
        if parent.nested or isinstance(parent, symbols.FunctionScope):
            scope.nested = 1
        # XXX Docstring support.
        scope.add_def("__module__")
        self.crnt_scope = self.scopes[node] = scope
        prev_klass = self.klass
        self.klass = node.name
        self.handle_list(node.body)
        self.klass = prev_klass
        parent.add_child(scope)
        scope.handle_children()
        self.crnt_scope = parent

    def _handle_Compare (self, node):
        pass

    def _handle_Continue (self, node):
        pass

    def _handle_Del (self, node):
        pass

    def _handle_Delete (self, node):
        pass

    def _handle_Dict (self, node):
        pass

    def _handle_Div (self, node):
        pass

    def _handle_Ellipsis (self, node):
        pass

    def _handle_Eq (self, node):
        pass

    def _handle_Exec (self, node):
        pass

    def _handle_Expr (self, node):
        pass

    def _handle_ExtSlice (self, node):
        pass

    def _handle_FloorDiv (self, node):
        pass

    def _handle_For (self, node):
        pass

    def handle_FunctionDef (self, node):
        self.handle_list(node.decorators)
        self.crnt_scope.add_def(node.name)
        self.handle_list(node.args.defaults)
        scope = symbols.FunctionScope(node.name, self.module, self.klass)
        parent = self.crnt_scope
        self.crnt_scope = self.scopes[node] = scope
        if parent.nested or isinstance(parent, symbols.FunctionScope):
            scope.nested = 1
        self.handle(node.args)
        self.handle_list(node.body)
        parent.add_child(scope)
        scope.handle_children()
        self.crnt_scope = parent

    def handle_GeneratorExp (self, node):
        scope = symbols.GenExprScope(self.module, self.klass)
        parent = self.crnt_scope
        self.crnt_scope = scope
        if (parent.nested or isinstance(parent, symbols.FunctionScope) or
            isinstance(parent, symbols.GenExprScope)):
            scope.nested = 1
        self.scopes[node] = scope
        self.handle(node.elt)
        self.handle_list(node.generators)
        parent.add_child(scope)
        scope.handle_children()
        self.crnt_scope = parent

    def _handle_Global (self, node):
        pass

    def _handle_Gt (self, node):
        pass

    def _handle_GtE (self, node):
        pass

    def _handle_If (self, node):
        pass

    def _handle_IfExp (self, node):
        pass

    def _handle_Import (self, node):
        pass

    def _handle_ImportFrom (self, node):
        pass

    def _handle_In (self, node):
        pass

    def _handle_Index (self, node):
        pass

    def _handle_Interactive (self, node):
        pass

    def _handle_Invert (self, node):
        pass

    def _handle_Is (self, node):
        pass

    def _handle_IsNot (self, node):
        pass

    def _handle_LShift (self, node):
        pass

    def handle_Lambda (self, node):
        self.handle_list(node.args.defaults)
        scope = symbols.LambdaScope(self.module, self.klass)
        parent = self.crnt_scope
        self.crnt_scope = self.scopes[node] = scope
        if parent.nested or isinstance(parent, symbols.FunctionScope):
            scope.nested = 1
        self.handle(node.args)
        self.handle(node.body)
        parent.add_child(scope)
        scope.handle_children()
        self.crnt_scope = parent        

    def _handle_List (self, node):
        pass

    def _handle_ListComp (self, node):
        pass

    def _handle_Load (self, node):
        pass

    def _handle_Lt (self, node):
        pass

    def _handle_LtE (self, node):
        pass

    def _handle_Mod (self, node):
        pass

    def handle_Module (self, node):
        scope = self.module = self.scopes[node] = symbols.ModuleScope()
        self.crnt_scope = scope
        self.handle_children(node)
        self.crnt_scope = None
        return scope

    handle_Expression = handle_Module

    def _handle_Mult (self, node):
        pass

    def handle_Name (self, node):
        ctx_type = type(node.ctx)
        if ctx_type == myfront_ast.Store:
            self.crnt_scope.add_def(node.id)
        elif ctx_type == myfront_ast.Param:
            self.crnt_scope.add_param(node.id)
        else:
            self.crnt_scope.add_use(node.id)

    def _handle_Not (self, node):
        pass

    def _handle_NotEq (self, node):
        pass

    def _handle_NotIn (self, node):
        pass

    def _handle_Num (self, node):
        pass

    def _handle_Or (self, node):
        pass

    def _handle_Param (self, node):
        pass

    def _handle_Pass (self, node):
        pass

    def _handle_Pow (self, node):
        pass

    def _handle_Print (self, node):
        pass

    def _handle_QuoteDef (self, node):
        pass

    def _handle_RShift (self, node):
        pass

    def _handle_Raise (self, node):
        pass

    def _handle_Repr (self, node):
        pass

    def _handle_Return (self, node):
        pass

    def _handle_Slice (self, node):
        pass

    def _handle_Store (self, node):
        pass

    def _handle_Str (self, node):
        pass

    def _handle_Sub (self, node):
        pass

    def _handle_Subscript (self, node):
        pass

    def _handle_Suite (self, node):
        pass

    def _handle_TryExcept (self, node):
        pass

    def _handle_TryFinally (self, node):
        pass

    def _handle_Tuple (self, node):
        pass

    def _handle_UAdd (self, node):
        pass

    def _handle_USub (self, node):
        pass

    def _handle_UnaryOp (self, node):
        pass

    def _handle_While (self, node):
        pass

    def _handle_With (self, node):
        pass

    def handle_Yield (self, node):
        self.crnt_scope.generator = 1
        if node.value is not None:
            self.handle(node.value)

    def _handle_alias (self, node):
        pass

    def handle_arguments (self, node):
        self.handle_list(node.args)
        if node.vararg is not None:
            self.crnt_scope.add_param(node.vararg)
        if node.kwarg is not None:
            self.crnt_scope.add_param(node.kwarg)

    def _handle_comprehension (self, node):
        pass

    def _handle_excepthandler (self, node):
        pass

    def _handle_keyword (self, node):
        pass

# ______________________________________________________________________

class MyCodeGen (ASTHandler):
    """Class MyCodeGen"""
    # ____________________________________________________________
    lambda_count = 0

    # ____________________________________________________________
    def __init__ (self, filename = None, co_name = None, args = None,
                  optimized = 0, klass = None, scope = None, scopes = None):
        if co_name is None:
            co_name = "<module>"
        if args is None:
            args = ()
        self.last_lineno = 0
        self.optimized = optimized
        self.class_name = klass
        self.slice_context = None
        # State variables for generator expressions (these shouldn't
        # require a stack since nested generators will have separate
        # code generator objects).
        self.comprehension_stack = None
        self.is_outmost = False
        # State variables for try-except.
        self.tryexcept_end_blocks = []
        # Other variables...
        self.setups = []
        self.scope = scope
        self.scopes = scopes
        self.locals = set(args)
        self.filename = str(filename)
        self.graph = pyassem.PyFlowGraph(co_name, self.filename, args,
                                         optimized, klass)

    # ____________________________________________________________
    def set_lineno (self, node, force = False):
        """Stolen from compile.pycodegen...(temporarily, hopefully)"""
        ret_val = False
        lineno = getattr(node, 'lineno', None)
        if lineno is not None and (lineno != self.last_lineno or force):
            self.graph.emit("SET_LINENO", lineno)
            self.last_lineno = lineno
            ret_val = True
        return ret_val

    ctx_dict = {
        myfront_ast.Load : "LOAD",
        myfront_ast.Store : "STORE",
        myfront_ast.Del : "DELETE",
        }

    def get_prefix_from_ctx (self, ctx_node):
        ctx_type = type(ctx_node)
        if self.ctx_dict.has_key(ctx_type):
            ret_val = self.ctx_dict[ctx_type]
        else:
            # XXX Un-funkify.
            raise RuntimeError, "Stuff be all funky."
        return ret_val

    def _mangle (self, name):
        ret_val = name
        if self.class_name is not None:
            ret_val = misc.mangle(name, self.class_name)
        return ret_val

    def _name_op (self, prefix, name):
        name = self._mangle(name)
        postfix = "NAME"
        name_scope = self.scope.check_name(name)
        if name_scope in (consts.SC_FREE, consts.SC_CELL):
            postfix = "DEREF"
        elif self.optimized:
            if name_scope == consts.SC_LOCAL:
                postfix = "FAST"
            elif name_scope == consts.SC_GLOBAL:
                postfix = "GLOBAL"
        self.graph.emit("%s_%s" % (prefix, postfix), name)

    def _implicit_name_op (self, prefix, name):
        postfix = "NAME"
        if self.optimized:
            postfix = "FAST"
        self.graph.emit("%s_%s" % (prefix, postfix), name)

    _subscript_op_dict = {
        myfront_ast.Load : "BINARY_SUBSCR",
        myfront_ast.AugLoad : "BINARY_SUBSCR",
        myfront_ast.Store : "STORE_SUBSCR",
        myfront_ast.AugStore : "STORE_SUBSCR",
        myfront_ast.Del : "DELETE_SUBSCR",
        }

    def _handle_subscr (self):
        op = self._subscript_op_dict[self.slice_context]
        if self.slice_context == myfront_ast.AugLoad:
            self.graph.emit("DUP_TOPX", 2)
        elif self.slice_context == myfront_ast.AugStore:
            self.graph.emit("ROT_THREE")
        self.graph.emit(op)

    _slice_op_dict = {
        myfront_ast.Load : "SLICE",
        myfront_ast.AugLoad : "SLICE",
        myfront_ast.Store : "STORE_SLICE",
        myfront_ast.AugStore : "STORE_SLICE",
        myfront_ast.Del : "DELETE_SLICE",
        }

    def _handle_simple_slice (self, node):
        """Should roughly correspond to compiler_simple_slice in compile.c"""
        slice_offset = 0
        stack_count = 0
        if node.lower is not None:
            slice_offset += 1
            stack_count += 1
            if self.slice_context != myfront_ast.AugStore:
                self.handle(node.lower)
        if node.upper is not None:
            slice_offset += 2
            stack_count += 1
            if self.slice_context != myfront_ast.AugStore:
                self.handle(node.upper)
        assert stack_count < 3
        if self.slice_context == myfront_ast.AugLoad:
            if stack_count == 0:
                self.graph.emit("DUP_TOP")
            else:
                self.graph.emit("DUP_TOPX", stack_count + 1)
        elif self.slice_context == myfront_ast.AugStore:
            if stack_count == 0:
                self.graph.emit("ROT_TWO")
            elif stack_count == 1:
                self.graph.emit("ROT_THREE")
            else:
                self.graph.emit("ROT_FOUR")
        self.graph.emit("%s+%d" % (self._slice_op_dict[self.slice_context],
                                   slice_offset))

    def _handle_slice (self, node):
        """Should roughly correspond to compiler_slice() in compile.c"""
        n = 2
        if node.lower is None:
            self.graph.emit("LOAD_CONST", None)
        else:
            self.handle(node.lower)
        if node.upper is None:
            self.graph.emit("LOAD_CONST", None)
        else:
            self.handle(node.upper)
        if node.step is not None:
            # XXX Weird behavior in Python compiler where an empty
            # step expands to load the name None rather than loading
            # the None constant.  See handle_sliceop() in
            # myfront_transformer.py.
            n += 1
            if ((type(node.step) == myfront_ast.Name) and
                (node.step.id == "None")):
                # XXX Hack (see above)
                self.graph.emit("LOAD_CONST", None)
            else:
                self.handle(node.step)
        self.graph.emit("BUILD_SLICE", n)

    def _handle_nested_slice (self, node):
        """Should roughly correspond to compiler_visit_nested_slice() in
        compile.c."""
        node_type = type(node)
        if node_type == myfront_ast.Ellipsis:
            self.graph.emit("LOAD_CONST", Ellipsis)
        elif node_type == myfront_ast.Slice:
            self._handle_slice(node)
        elif node_type == myfront_ast.Index:
            self.handle(node.value)
        else:
            raise SystemError("extended slice invalid in nested slice")

    def _make_closure (self, gen, args):
        frees = gen.scope.get_free_vars()
        if frees:
            for name in frees:
                self.graph.emit("LOAD_CLOSURE", name)
            self.graph.emit("BUILD_TUPLE", len(frees))
            self.graph.emit("LOAD_CONST", gen.graph)
            self.graph.emit("MAKE_CLOSURE", args)
        else:
            self.graph.emit("LOAD_CONST", gen.graph)
            self.graph.emit("MAKE_FUNCTION", args)

    def _flatten_args (self, expr_list):
        ret_val = []
        for expr in expr_list:
            if isinstance(expr, myfront_ast.Name):
                ret_val.append(expr.id)
            elif isinstance(expr, myfront_ast.Tuple):
                ret_val += self._flatten_args(expr.elts)
            else:
                raise NotImplementedError("Don't know how to flatten %s's!" %
                                          type(expr).__name__)
        return ret_val

    def _handle_ListComp_comprehension (self, comp):
        start = self.graph.newBlock()
        cont = None
        anchor = self.graph.newBlock()
        self.handle(comp.iter)
        self.graph.emit("GET_ITER")
        self.graph.nextBlock(start)
        self.set_lineno(comp.target, True)
        self.graph.emit("FOR_ITER", anchor)
        self.graph.nextBlock()
        self.handle(comp.target)
        for if_expr in comp.ifs:
            if cont is None:
                cont = self.graph.newBlock()
            self.set_lineno(if_expr, True)
            self.handle(if_expr)
            self.graph.emit("JUMP_IF_FALSE", cont)
            self.graph.newBlock()
            self.graph.emit("POP_TOP")
        return start, cont, anchor

    def _handle_GeneratorExp_inner (self, node):
        """Liberally interpreted from visitGenExprInner()"""
        self.comprehension_stack = []
        # Note that this should delegate to handle_comprehension().
        self.is_outmost = True
        self.handle(node.generators[0])
        self.is_outmost = False
        for gen in node.generators[1:]:
            self.handle(gen)
        self.comprehension_stack.reverse()
        self.handle(node.elt)
        self.graph.emit("YIELD_VALUE")
        self.graph.emit("POP_TOP")
        for start, cont, anchor, end in self.comprehension_stack:
            if cont is not None:
                skip_one = self.graph.newBlock()
                self.graph.emit("JUMP_FORWARD", skip_one)
                self.graph.startBlock(cont)
                self.graph.emit("POP_TOP")
                self.graph.nextBlock(skip_one)
            self.graph.emit("JUMP_ABSOLUTE", start)
            self.graph.startBlock(anchor)
            self.graph.emit("POP_BLOCK")
            self.setups.pop()
            self.graph.startBlock(end)
        self.graph.emit("LOAD_CONST", None)
        self.comprehension_stack = None

    # ____________________________________________________________
    def handle_children (self, node):
        pass

    def get_code (self):
        return self.graph.getCode()

    def handle_Add (self, node):
        self.graph.emit("BINARY_ADD")

    def handle_And (self, node):
        raise NotImplementedError("Should never directly visit an And node.")

    def handle_Assert (self, node):
        if __debug__:
            end = self.graph.newBlock()
            self.set_lineno(node)
            self.graph.nextBlock()
            self.handle(node.test)
            self.graph.emit("JUMP_IF_TRUE", end)
            self.graph.nextBlock()
            self.graph.emit("POP_TOP")
            self.graph.emit("LOAD_GLOBAL", "AssertionError")
            if node.msg is not None:
                self.handle(node.msg)
                self.graph.emit("RAISE_VARARGS", 2)
            else:
                self.graph.emit("RAISE_VARARGS", 1)
            self.graph.nextBlock(end)
            self.graph.emit("POP_TOP")

    def handle_Assign (self, node):
        self.set_lineno(node)
        self.handle(node.value)
        for target in node.targets[:-1]:
            self.graph.emit("DUP_TOP")
            self.handle(target)
        self.handle(node.targets[-1])

    def handle_Attribute (self, node):
        ctx_type = type(node.ctx)
        if ctx_type != myfront_ast.AugStore:
            self.handle(node.value)
        if ctx_type == myfront_ast.AugLoad:
            self.graph.emit("DUP_TOP")
            self.graph.emit("LOAD_ATTR", self._mangle(node.attr))
        elif ctx_type == myfront_ast.Load:
            self.graph.emit("LOAD_ATTR", self._mangle(node.attr))
        elif ctx_type == myfront_ast.AugStore:
            self.graph.emit("ROT_TWO")
            self.graph.emit("STORE_ATTR", self._mangle(node.attr))
        elif ctx_type == myfront_ast.Store:
            self.graph.emit("STORE_ATTR", self._mangle(node.attr))
        elif ctx_type == myfront_ast.Del:
            self.graph.emit("DELETE_ATTR", self._mangle(node.attr))
        else:
            raise SystemError, "param invalid in attribute expression"

    inplace_dict = {
        myfront_ast.Add : "INPLACE_ADD",
        myfront_ast.Sub : "INPLACE_SUBTRACT",
        myfront_ast.Mult : "INPLACE_MULTIPLY",
        myfront_ast.Div : "INPLACE_DIVIDE", # XXX No future division support.
        myfront_ast.Mod : "INPLACE_MODULO",
        myfront_ast.Pow : "INPLACE_POWER",
        myfront_ast.LShift : "INPLACE_LSHIFT",
        myfront_ast.RShift : "INPLACE_RSHIFT",
        myfront_ast.BitOr : "INPLACE_OR",
        myfront_ast.BitXor : "INPLACE_XOR",
        myfront_ast.BitAnd : "INPLACE_AND",
        myfront_ast.FloorDiv : "INPLACE_FLOOR_DIVIDE",
        }

    def handle_AugAssign (self, node):
        self.set_lineno(node)
        target = node.target
        target_type = type(target)
        auge = None
        op_name = self.inplace_dict[type(node.op)]
        if target_type == myfront_ast.Attribute:
            auge = myfront_ast.Attribute(target.value, target.attr,
                                         myfront_ast.AugLoad(), target.lineno,
                                         target.col_offset)
        elif target_type == myfront_ast.Subscript:
            auge = myfront_ast.Subscript(target.value, target.slice,
                                         myfront_ast.AugLoad(), target.lineno,
                                         target.col_offset)
        elif target_type == myfront_ast.Name:
            self._name_op("LOAD", target.id)
            self.handle(node.value)
            self.graph.emit(op_name)
            self._name_op("STORE", target.id)
        else:
            raise SystemError, ("invalid node type (%s) for augmented "
                                "assignment" % target_type.__name__)
        if auge is not None:
            self.handle(auge)
            self.handle(node.value)
            self.graph.emit(op_name)
            auge.ctx = myfront_ast.AugStore()
            self.handle(auge)

    def handle_AugLoad (self, node):
        pass

    def handle_AugStore (self, node):
        pass

    def handle_BinOp (self, node):
        self.handle(node.left)
        self.handle(node.right)
        self.handle(node.op)

    def handle_BitAnd (self, node):
        self.graph.emit("BINARY_AND")

    def handle_BitOr (self, node):
        self.graph.emit("BINARY_OR")

    def handle_BitXor (self, node):
        self.graph.emit("BINARY_XOR")

    def handle_BoolOp (self, node):
        end = self.graph.newBlock()
        jump_op = "JUMP_IF_TRUE"
        if isinstance(node.op, myfront_ast.And):
            jump_op = "JUMP_IF_FALSE"
        for child in node.values[:-1]:
            self.handle(child)
            self.graph.emit(jump_op, end)
            self.graph.nextBlock()
            self.graph.emit("POP_TOP")
        self.handle(node.values[-1])
        self.graph.nextBlock(end)

    def handle_Break (self, node):
        if not self.setups:
            raise SyntaxError, "'break' outside loop on line %d." % node.lineno
        self.set_lineno(node)
        self.graph.emit("BREAK_LOOP")

    _call_ops = {0 : "CALL_FUNCTION",
                 1 : "CALL_FUNCTION_VAR",
                 2 : "CALL_FUNCTION_KW",
                 3 : "CALL_FUNCTION_VAR_KW",
                 }

    def handle_Call (self, node):
        code = 0
        self.handle(node.func)
        n = len(node.args)
        self.handle_list(node.args)
        if len(node.keywords) > 0:
            self.handle_list(node.keywords)
            n |= len(node.keywords) << 8
        if node.starargs is not None:
            self.handle(node.starargs)
            code |= 1
        if node.kwargs is not None:
            self.handle(node.kwargs)
            code |= 2
        self.graph.emit(self._call_ops[code], n)

    def handle_ClassDef (self, node):
        self.set_lineno(node)
        scope = self.scopes[node]
        self.graph.emit("LOAD_CONST", node.name)
        for base in node.bases:
            self.handle(base)
        self.graph.emit("BUILD_TUPLE", len(node.bases))
        class_code_gen = MyCodeGen(self.filename, node.name, klass = 1,
                                   scope = scope, scopes = self.scopes)
        class_code_gen.locals.union(find_locals(node))
        class_code_gen.graph.setFlag(consts.CO_NEWLOCALS)
        class_code_gen.set_lineno(node)
        class_code_gen.graph.emit("LOAD_GLOBAL", "__name__")
        class_code_gen._name_op("STORE", "__module__")
        # XXX Handle doc strings!
        for stmt in node.body:
            class_code_gen.handle(stmt)
        class_code_gen.graph.startExitBlock()
        class_code_gen.graph.emit("LOAD_LOCALS")
        class_code_gen.graph.emit("RETURN_VALUE")
        self._make_closure(class_code_gen, 0)
        self.graph.emit("CALL_FUNCTION", 0)
        self.graph.emit("BUILD_CLASS")
        self._name_op("STORE", node.name)

    def handle_Compare (self, node):
        self.handle(node.left)
        op_count = len(node.ops)
        cleanup = None
        if op_count > 1:
            cleanup = self.graph.newBlock()
            for op, comparator in zip(node.ops[:-1], node.comparators[:-1]):
                self.handle(comparator)
                self.graph.emit("DUP_TOP")
                self.graph.emit("ROT_THREE")
                self.handle(op)
                self.graph.emit("JUMP_IF_FALSE", cleanup)
                self.graph.nextBlock()
                self.graph.emit("POP_TOP")
        self.handle(node.comparators[-1])
        self.handle(node.ops[-1])
        if op_count > 1:
            end = self.graph.newBlock()
            self.graph.emit("JUMP_FORWARD", end)
            self.graph.startBlock(cleanup)
            self.graph.emit("ROT_TWO")
            self.graph.emit("POP_TOP")
            self.graph.nextBlock(end)

    def handle_Continue (self, node):
        if not self.setups:
            raise SyntaxError, ("'continue' outside loop on line %d" %
                                node.lineno)
        self.set_lineno(node)
        kind, block = self.setups[-1]
        if kind == "LOOP":
            self.graph.emit("JUMP_ABSOLUTE", block)
        elif kind in ("EXCEPT", "TRY_FINALLY"):
            top = len(self.setups)
            while top > 0:
                top -= 1
                kind, loop_block = self.setups[top]
                if kind == "LOOP":
                    break
            if kind != "LOOP":
                raise SyntaxError, ("'continue' outside loop on line %d" %
                                    node.lineno)
            self.graph.emit("CONTINUE_LOOP", loop_block)
        elif kind == "END_FINALLY":
            raise SyntaxError, ("'continue' not allowed inside 'finally' "
                                "clause on line %d" % node.lineno)
        self.graph.nextBlock()

    def handle_Del (self, node):
        raise NotImplementedError("Should never directly visit a Del node.")

    def handle_Delete (self, node):
        self.set_lineno(node)
        self.handle_list(node.targets)

    def handle_Dict (self, node):
        self.graph.emit("BUILD_MAP", 0)
        for key_expr, value_expr in zip(node.keys, node.values):
            self.graph.emit("DUP_TOP")
            self.handle(key_expr)
            self.handle(value_expr)
            self.graph.emit("ROT_THREE")
            self.graph.emit("STORE_SUBSCR")

    def handle_Div (self, node):
        self.graph.emit("BINARY_DIVIDE")

    def handle_Ellipsis (self, node):
        if self.slice_context != myfront_ast.AugStore:
            self.graph.emit("LOAD_CONST", Ellipsis)
        self._handle_subscr()

    def handle_Eq (self, node):
        self.graph.emit("COMPARE_OP", "==")

    def handle_Exec (self, node):
        # XXX Note that compiler.parse gets locals and globals wrong,
        # causing another test failure.
        self.set_lineno(node)
        self.handle(node.body)
        if node.locals is None:
            self.graph.emit("LOAD_CONST", None)
        else:
            self.handle(node.locals)
        if node.globals is None:
            self.graph.emit("DUP_TOP")
        else:
            self.handle(node.globals)
        self.graph.emit("EXEC_STMT")

    def handle_Expr (self, node):
        self.set_lineno(node)
        self.handle(node.value)
        self.graph.emit("POP_TOP")

    def _handle_scope (self, node):
        scope_handler = ScopeHandler()
        scope_handler.handle(node)
        self.scopes = scope_handler.scopes
        self.scope = self.scopes[node]

    def handle_Expression (self, node):
        self._handle_scope(node)
        self.handle(node.body)
        self.graph.emit("RETURN_VALUE")

    def handle_ExtSlice (self, node):
        if self.slice_context != myfront_ast.AugStore:
            for dim in node.dims:
                self._handle_nested_slice(dim)
            self.graph.emit("BUILD_TUPLE", len(node.dims))
        self._handle_subscr()

    def handle_FloorDiv (self, node):
        self.graph.emit("BINARY_FLOOR_DIVIDE")

    def handle_For (self, node):
        start = self.graph.newBlock()
        anchor = self.graph.newBlock()
        after = self.graph.newBlock()
        self.setups.append(("LOOP", start))
        self.set_lineno(node)
        self.graph.emit("SETUP_LOOP", after)
        self.handle(node.iter)
        self.graph.emit("GET_ITER")
        self.graph.nextBlock(start)
        self.set_lineno(node, True)
        self.graph.emit("FOR_ITER", anchor)
        self.handle(node.target)
        self.handle_list(node.body)
        self.graph.emit("JUMP_ABSOLUTE", start)
        self.graph.nextBlock(anchor)
        self.graph.emit("POP_BLOCK")
        self.setups.pop()
        if len(node.orelse) > 0:
            self.handle_list(node.orelse)
        self.graph.nextBlock(after)

    def _handle_function_or_lambda (self, node):
        is_lambda = isinstance(node, myfront_ast.Lambda)
        scope = self.scopes[node]
        vararg = node.args.vararg
        kwarg = node.args.kwarg
        flags = []
        args = self._flatten_args(node.args.args)
        if vararg is not None:
            args.append(vararg)
            flags.append(consts.CO_VARARGS)
        if kwarg is not None:
            args.append(kwarg)
            flags.append(consts.CO_VARKEYWORDS)
        if scope.generator is not None:
            flags.append(consts.CO_GENERATOR)
        if not is_lambda:
            # Function
            name = node.name
        else:
            name = "<lambda.%d>" % MyCodeGen.lambda_count
            MyCodeGen.lambda_count += 1
        gen = MyCodeGen(self.filename, name, args, 1, self.class_name, scope,
                        self.scopes)
        gen.graph.setFreeVars(scope.get_free_vars())
        gen.graph.setCellVars(scope.get_cell_vars())
        # XXX Add documentation string support.
        gen.locals.union(find_locals(node))
        for flag in flags:
            gen.graph.setFlag(flag)
        gen.set_lineno(node)
        gen.handle(node.body)
        gen.graph.startExitBlock()
        if not is_lambda:
            gen.graph.emit("LOAD_CONST", None)
        gen.graph.emit("RETURN_VALUE")
        # XXX Special case here: there is going to be divergence in
        # the line number information for this code generator and the
        # compiler module because the new AST data drops the line
        # number of the "def" token (if I changed this, it would break
        # compatibility with the Python AST parser).
        self.set_lineno(node)
        for default in node.args.defaults:
            self.handle(default)
        self._make_closure(gen, len(node.args.defaults))

    def handle_FunctionDef (self, node):
        for decorator in node.decorators:
            self.handle(decorator)
        self._handle_function_or_lambda(node)
        for _ in xrange(len(node.decorators)):
            self.graph.emit("CALL_FUNCTION", 1)
        self._name_op("STORE", node.name)

    def handle_GeneratorExp (self, node):
        scope = self.scopes[node]
        # XXX Consider brining this in line with compile.c instead of
        # the compiler module.
        name = "<lambda.%d>" % MyCodeGen.lambda_count
        MyCodeGen.lambda_count += 1
        gen = MyCodeGen(self.filename, name, [".0"], 1, self.class_name,
                        scope, self.scopes)
        gen.graph.setFreeVars(scope.get_free_vars())
        gen.graph.setCellVars(scope.get_cell_vars())
        gen.graph.setFlag(consts.CO_GENERATOR)
        gen._handle_GeneratorExp_inner(node)
        gen.graph.startExitBlock()
        gen.graph.emit("RETURN_VALUE")
        self.set_lineno(node)
        self._make_closure(gen, 0)
        self.handle(node.generators[0].iter)
        self.graph.emit("GET_ITER")
        self.graph.emit("CALL_FUNCTION", 1)

    def handle_Global (self, node):
        pass

    def handle_Gt (self, node):
        self.graph.emit("COMPARE_OP", ">")

    def handle_GtE (self, node):
        self.graph.emit("COMPARE_OP", ">=")

    def handle_If (self, node):
        end_block = self.graph.newBlock()
        is_constant_false = (isinstance(node.test, myfront_ast.Num) and
                             (not node.test.n))
        if not is_constant_false:
            orelse_block = self.graph.newBlock()
            self.set_lineno(node.test)
            self.handle(node.test)
            self.graph.emit("JUMP_IF_FALSE", orelse_block)
            self.graph.emit("POP_TOP")
            self.handle_list(node.body)
            self.graph.emit("JUMP_FORWARD", end_block)
            self.graph.nextBlock(orelse_block)
            self.graph.emit("POP_TOP")
        self.handle_list(node.orelse)
        self.graph.nextBlock(end_block)

    def handle_IfExp (self, node):
        end_block = self.graph.newBlock()
        orelse_block = self.graph.newBlock()
        self.handle(node.test)
        self.graph.emit("JUMP_IF_FALSE", orelse_block)
        self.graph.emit("POP_TOP")
        self.handle(node.body)
        self.graph.emit("JUMP_FORWARD", end_block)
        self.graph.nextBlock(orelse_block)
        self.graph.emit("POP_TOP")
        self.handle(node.orelse)
        self.graph.nextBlock(end_block)

    def handle_Import (self, node):
        self.set_lineno(node)
        # XXX Ignoring CO_FUTURE_ABSIMPORT
        level = -1
        for alias in node.names:
            # XXX Assuming Python version > 1
            self.graph.emit("LOAD_CONST", level)
            self.graph.emit("LOAD_CONST", None)
            self.graph.emit("IMPORT_NAME", alias.name)
            elts = alias.name.split(".")
            mod = elts[0]
            if alias.asname is None:
                self._name_op("STORE", mod)
            else:
                for elt in elts[1:]:
                    self.graph.emit("LOAD_ATTR", elt)
                self._name_op("STORE", alias.asname)

    def handle_ImportFrom (self, node):
        self.set_lineno(node)
        # XXX Ignoring CO_FUTURE_ABSIMPORT
        if (node.level is None) or (node.level == 0):
            level = -1
        else:
            level = node.level
        fromlist = [alias.name for alias in node.names]
        # XXX Assming Python version > 1
        self.graph.emit("LOAD_CONST", level)
        self.graph.emit("LOAD_CONST", tuple(fromlist))
        self.graph.emit("IMPORT_NAME", node.module)
        assert len(node.names) > 0
        if node.names[0].name == "*":
            assert len(node.names) == 1
            if level != -1:
                raise SyntaxError("'import *' not allowed with 'from .'")
            self.graph.emit("IMPORT_STAR")
        else:
            for alias in node.names:
                self.graph.emit("IMPORT_FROM", alias.name)
                elts = alias.name.split(".")
                for elt in elts[1:]:
                    self.graph.emit("LOAD_ATTR", elt)
                if alias.asname is None:
                    self._name_op("STORE", alias.name)
                else:
                    self._name_op("STORE", alias.asname)
            self.graph.emit("POP_TOP")

    def handle_In (self, node):
        self.graph.emit("COMPARE_OP", "in")

    def handle_Index (self, node):
        if self.slice_context != myfront_ast.AugStore:
            self.handle(node.value)
        self._handle_subscr()

    def handle_Interactive (self, node):
        # XXX
        raise NotImplementedError("Not currently implemented.")

    def handle_Invert (self, node):
        self.graph.emit("UNARY_INVERT")

    def handle_Is (self, node):
        self.graph.emit("COMPARE_OP", "is")

    def handle_IsNot (self, node):
        self.graph.emit("COMPARE_OP", "is not")

    def handle_LShift (self, node):
        self.graph.emit("BINARY_LSHIFT")

    def handle_Lambda (self, node):
        self._handle_function_or_lambda(node)

    def handle_List (self, node):
        self.set_lineno(node)
        if isinstance(node.ctx, myfront_ast.Store):
            self.graph.emit("UNPACK_SEQUENCE", len(node.elts))
        self.handle_list(node.elts)
        if isinstance(node.ctx, myfront_ast.Load):
            self.graph.emit("BUILD_LIST", len(node.elts))

    __list_count = 0

    def handle_ListComp (self, node):
        self.set_lineno(node)
        append = "$append%d" % self.__list_count
        self.__list_count += 1
        self.graph.emit("BUILD_LIST", 0)
        self.graph.emit("DUP_TOP")
        self.graph.emit("LOAD_ATTR", "append")
        self._implicit_name_op("STORE", append)
        stack = [self._handle_ListComp_comprehension(comprehension)
                 for comprehension in node.generators]
        stack.reverse()
        self._implicit_name_op("LOAD", append)
        self.handle(node.elt)
        self.graph.emit("CALL_FUNCTION", 1)
        self.graph.emit("POP_TOP")
        for start, cont, anchor in stack:
            if cont is not None:
                skip_one = self.graph.newBlock()
                self.graph.emit("JUMP_FORWARD", skip_one)
                self.graph.startBlock(cont)
                self.graph.emit("POP_TOP")
                self.graph.nextBlock(skip_one)
            self.graph.emit("JUMP_ABSOLUTE", start)
            self.graph.startBlock(anchor)
        self._implicit_name_op("DELETE", append)
        self.__list_count -= 1

    def handle_Load (self, node):
        raise NotImplementedError("Should never directly visit a Load node.")

    def handle_Lt (self, node):
        self.graph.emit("COMPARE_OP", "<")

    def handle_LtE (self, node):
        self.graph.emit("COMPARE_OP", "<=")

    def handle_Mod (self, node):
        self.graph.emit("BINARY_MODULO")

    def handle_Module (self, node):
        self._handle_scope(node)
        self.graph.emit("SET_LINENO", 0)
        self.handle_list(node.body)
        self.graph.emit("LOAD_CONST", None)
        self.graph.emit("RETURN_VALUE")

    def handle_Mult (self, node):
        self.graph.emit("BINARY_MULTIPLY")

    def handle_Name (self, node):
        prefix = self.get_prefix_from_ctx(node.ctx)
        self._name_op(prefix, node.id)

    def handle_Not (self, node):
        self.graph.emit("UNARY_NOT")

    def handle_NotEq (self, node):
        self.graph.emit("COMPARE_OP", "!=")

    def handle_NotIn (self, node):
        self.graph.emit("COMPARE_OP", "not in")

    def handle_Num (self, node):
        self.graph.emit("LOAD_CONST", node.n)

    def handle_Or (self, node):
        raise NotImplementedError("Should never directly visit an Or node.")

    def handle_Param (self, node):
        pass

    def handle_Pass (self, node):
        self.set_lineno(node)

    def handle_Pow (self, node):
        self.graph.emit("BINARY_POWER")

    def handle_Print (self, node):
        self.set_lineno(node)
        n = len(node.values)
        dest = False
        if node.dest is not None:
            self.handle(node.dest)
            dest = True
        for value in node.values:
            if dest:
                self.graph.emit("DUP_TOP")
                self.handle(value)
                self.graph.emit("ROT_TWO")
                self.graph.emit("PRINT_ITEM_TO")
            else:
                self.handle(value)
                self.graph.emit("PRINT_ITEM")
        if node.nl:
            if dest:
                self.graph.emit("PRINT_NEWLINE_TO")
            else:
                self.graph.emit("PRINT_NEWLINE")
        elif dest:
            self.graph.emit("POP_TOP")

    def handle_QuoteDef (self, node):
        raise MyCodeGenError("File '%s', line %d: QuoteDef is not being "
                             "reduced prior to code generation." %
                             (self.filename, node.lineno))

    def handle_RShift (self, node):
        self.graph.emit("BINARY_RSHIFT")

    def handle_Raise (self, node):
        pass

    def handle_Repr (self, node):
        # XXX The compiler module indicates an incorrect line number
        # for code generated for a lone Repr node (maybe an issue with
        # compiler.parser).
        self.handle(node.value)
        self.graph.emit("UNARY_CONVERT")

    def handle_Return (self, node):
        self.set_lineno(node)
        if node.value is not None:
            self.handle(node.value)
        else:
            self.graph.emit("LOAD_CONST", None)
        self.graph.emit("RETURN_VALUE")

    def handle_Slice (self, node):
        if node.step is None:
            self._handle_simple_slice(node)
        else:
            if self.slice_context != myfront_ast.AugStore:
                self._handle_slice(node)
            self._handle_subscr()

    def handle_Str (self, node):
        self.graph.emit("LOAD_CONST", node.s)

    def handle_Sub (self, node):
        self.graph.emit("BINARY_SUBTRACT")

    def handle_Subscript (self, node):
        ctx_type = type(node.ctx)
        old_slice_context = self.slice_context
        self.slice_context = ctx_type
        if ctx_type != myfront_ast.AugStore:
            self.handle(node.value)
        if ctx_type != myfront_ast.Param:
            self.handle(node.slice)
        else:
            raise SystemError, "param invalid in attribute expression"
        self.slice_context = old_slice_context

    def handle_Suite (self, node):
        raise NotImplementedError("The Suite node is not used in CPython nor "
                                  "MyFront.")

    def handle_TryExcept (self, node):
        body_block = self.graph.newBlock()
        handlers_block = self.graph.newBlock()
        orelse_block = end_block = self.graph.newBlock()
        has_orelse = len(node.orelse) > 0
        if has_orelse:
            orelse_block = self.graph.newBlock()
        self.set_lineno(node)
        self.graph.emit("SETUP_EXCEPT", handlers_block)
        self.graph.nextBlock(body_block)
        self.setups.append(("EXCEPT", body_block))
        self.handle_list(node.body)
        self.graph.emit("POP_BLOCK")
        self.setups.pop()
        self.graph.emit("JUMP_FORWARD", orelse_block)
        self.graph.startBlock(handlers_block)
        self.tryexcept_end_blocks.append(end_block)
        self.handle_list(node.handlers)
        self.tryexcept_end_blocks.pop()
        self.graph.emit("END_FINALLY")
        if has_orelse:
            self.graph.nextBlock(orelse_block)
            self.handle_list(node.orelse)
        self.graph.nextBlock(end_block)

    def handle_TryFinally (self, node):
        body_block = self.graph.newBlock()
        final_block = self.graph.newBlock()
        self.set_lineno(node)
        self.graph.emit("SETUP_FINALLY", final_block)
        self.graph.nextBlock(body_block)
        self.setups.append(("TRY_FINALLY", body_block))
        self.handle_list(node.body)
        self.graph.emit("POP_BLOCK")
        self.setups.pop()
        self.graph.emit("LOAD_CONST", None)
        self.graph.nextBlock(final_block)
        self.setups.append(("END_FINALLY", final_block))
        self.handle_list(node.finalbody)
        self.graph.emit("END_FINALLY")
        self.setups.pop()

    def handle_Tuple (self, node):
        if isinstance(node.ctx, myfront_ast.Store):
            self.graph.emit("UNPACK_SEQUENCE", len(node.elts))
        for expr in node.elts:
            self.handle(expr)
        if isinstance(node.ctx, myfront_ast.Load):
            self.graph.emit("BUILD_TUPLE", len(node.elts))

    def handle_UAdd (self, node):
        self.graph.emit("UNARY_POSITIVE")

    def handle_USub (self, node):
        self.graph.emit("UNARY_NEGATIVE")

    def handle_UnaryOp (self, node):
        self.handle(node.operand)
        self.handle(node.op)

    def handle_While (self, node):
        self.set_lineno(node)
        loop = self.graph.newBlock()
        else_ = self.graph.newBlock()
        after = self.graph.newBlock()
        self.graph.emit("SETUP_LOOP", after)
        self.graph.nextBlock(loop)
        self.setups.append(("LOOP", loop))
        self.set_lineno(node, True)
        self.handle(node.test)
        self.graph.emit("JUMP_IF_FALSE", else_ or after)
        self.graph.nextBlock()
        self.graph.emit("POP_TOP")
        for body_node in node.body:
            self.handle(body_node)
        self.graph.emit("JUMP_ABSOLUTE", loop)
        self.graph.startBlock(else_)
        self.graph.emit("POP_TOP")
        self.graph.emit("POP_BLOCK")
        self.setups.pop()
        if node.orelse:
            for orelse_node in node.orelse:
                self.handle(orelse_node)
        self.graph.nextBlock(after)

    def handle_With (self, node):
        raise NotImplementedError("Not implementing from __future__ features.")

    def handle_Yield (self, node):
        # XXX (TODO) Perform proper error checking - however note that
        # the compiler package (2.5.1) allows a yield outside a function.
        if node.value is None:
            self.graph.emit("LOAD_CONST", None)
        else:
            self.handle(node.value)
        self.graph.emit("YIELD_VALUE")

    def handle_alias (self, node):
        raise NotImplementedError("Should never directly visit an alias node.")

    def handle_arguments (self, node):
        pass

    def handle_comprehension (self, node):
        start = self.graph.newBlock()
        cont = None
        anchor = self.graph.newBlock()
        end = self.graph.newBlock()
        self.setups.append(("LOOP", start))
        self.graph.emit("SETUP_LOOP", end)
        if self.is_outmost:
            self._name_op("LOAD", ".0")
        else:
            self.handle(node.iter)
            self.graph.emit("GET_ITER")
        self.graph.nextBlock(start)
        self.set_lineno(node.target, True)
        self.graph.emit("FOR_ITER", anchor)
        self.graph.nextBlock()
        self.handle(node.target)
        for if_expr in node.ifs:
            if cont is None:
                cont = self.graph.newBlock()
            self.set_lineno(if_expr, True)
            self.handle(if_expr)
            self.graph.emit("JUMP_IF_FALSE", cont)
            self.graph.newBlock()
            self.graph.emit("POP_TOP")
        self.comprehension_stack.append((start, cont, anchor, end))

    def handle_excepthandler (self, node):
        self.set_lineno(node)
        next_block = None
        if node.type is not None:
            self.graph.emit("DUP_TOP")
            self.handle(node.type)
            self.graph.emit("COMPARE_OP", "exception match")
            next_block = self.graph.newBlock()
            self.graph.emit("JUMP_IF_FALSE", next_block)
            self.graph.nextBlock()
            self.graph.emit("POP_TOP")
        self.graph.emit("POP_TOP")
        if node.name is not None:
            self.handle(node.name)
        else:
            self.graph.emit("POP_TOP")
        self.graph.emit("POP_TOP")
        self.handle_list(node.body)
        self.graph.emit("JUMP_FORWARD", self.tryexcept_end_blocks[-1])
        if node.type is not None:
            self.graph.nextBlock(next_block)
        else:
            self.graph.nextBlock()
        if node.type is not None:
            self.graph.emit("POP_TOP")

    def handle_keyword (self, node):
        self.graph.emit("LOAD_CONST", node.arg)
        self.handle(node.value)

# ______________________________________________________________________

def build_test_environment ():
    import pprint
    import operator
    import myfront_transformer
    import compiler
    ret_val = myfront_transformer.build_test_environment()
    # ____________________________________________________________
    myparse = ret_val["myparse"]
    ast_to_tuple = ret_val["ast_to_tuple"]
    def mycompile (text, filename):
        ast = myparse(text)
        my_coder = MyCodeGen(filename)
        my_coder.handle(ast)
        return my_coder.get_code()
    # ____________________________________________________________
    def compare_code (co1, co2, lvl = 0):
        ret_val = ""
        v1 = type(co1)
        v2 = type(co2)
        indent = "  " * lvl
        if v1 != v2:
            ret_val = "%sMismatched types (%r != %r)\n" % (indent, v1, v2)
        else:
            attrlist = [attrname for attrname in dir(co1)
                        if attrname[:2] != "__"]
            for attrname in attrlist:
                v1 = getattr(co1, attrname)
                v2 = getattr(co2, attrname)
                if v1 != v2:
                    ret_val += ("%sMismatched attribute %s:\n%s%s\n%s!=\n%s%s"
                                "\n" %
                                (indent, attrname, indent, pprint.pformat(v1),
                                 indent, indent, pprint.pformat(v2)))
                if attrname == "co_consts":
                    if len(v1) == len(v2):
                        for const1, const2 in zip(v1, v2):
                            if type(const1) == type(co1):
                                ret_val += compare_code(const1, const2,
                                                        lvl + 1)
        return ret_val
    # ____________________________________________________________
    def compiler_test (text, comparator = None, guess_why = None):
        if comparator is None:
            comparator = operator.__eq__
        if guess_why is None:
            guess_why = compare_code
        ast = myparse(text)
        MyCodeGen.lambda_count = 0
        my_coder = MyCodeGen("<test>")
        my_coder.handle(ast)
        co1 = my_coder.get_code()
        compiler.pycodegen.FunctionCodeGenerator.lambdaCount = 0
        co2 = compiler.compile(text, "<test>", "exec")
        assert comparator(co1, co2), ("Failed equality for %s:\n%s\n%s" %
                                      (`text`,
                                       pprint.pformat(ast_to_tuple(ast)),
                                       guess_why(co1, co2)))
    # ____________________________________________________________
    ret_val.update(locals())
    return ret_val

# ______________________________________________________________________

def test ():
    import sys, traceback
    test_env = build_test_environment()
    compiler_test = test_env["compiler_test"]
    test_strings = test_env["test_strings"]
    passed = 0
    for test_str in test_env["test_strings"]:
        try:
            compiler_test(test_str)
            passed += 1
        except:
            traceback.print_exc(file = sys.stdout)
    print "Passed %0.2f %% (%d of %d)." % (100*float(passed)/len(test_strings),
                                           passed, len(test_strings))

# ______________________________________________________________________
# Main routine

def main (*args):
    if len(args) > 0:
        import tokenize, MyRealParser, myfront_transformer, dis
        for file_name in args:
            tokenizer = tokenize.generate_tokens(open(file_name).readline)
            parser = MyRealParser.MyRealParser(tokenizer)
            parse_tree = parser()
            handler = myfront_transformer.MyHandler()
            ast = handler.handle_node(parse_tree)
            code_generator = MyCodeGen(file_name)
            code_generator.handle(ast)
            code = code_generator.get_code()
            dis.dis(code)
    else:
        test()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of MyCodeGen.py
