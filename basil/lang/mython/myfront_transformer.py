#! /usr/bin/env python
# ______________________________________________________________________
"""Module myfront_transformer.py

Partially automatically generated.

TODO: Integrate the simplification routine and make sure the
simplified CPT generates the same results.

TODO: Generalize this so it can be used as a native Python compiler,
given a concrete parse tree from the parser module.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.utils.Handler import *
from myfront_ast import *

import MyRealParser

# ______________________________________________________________________
# Class definitions

class ExprContextError (Exception):
    pass

# ______________________________________________________________________

class MyHandler (Handler):
    def __init__ (self, *args, **kws):
        Handler.__init__(self, *args, **kws)
        self.expr_context = Load

    def get_children (self, node):
        return None if self.is_token(node) else node[1]

    def get_nonterminal (self, node):
        return node[0]

    def is_token (self, node):
        return type(node[0]) == tuple

    def make_node (self, node_id, children):
        return (node_id, children)

    def handle_default (self, node):
        return node[0]

    def _handle_nontoken_children (self, node):
        return [self.handle_node(child) for child in self.get_children(node)
                if not self.is_token(child)]

    def _handle_only_child (self, node):
        children = self.get_children(node)
        assert len(children) == 1
        return self.handle_node(children[0])

    def _flatten_once (self, ast_list):
        ret_val = []
        for ast_elem in ast_list:
            if type(ast_elem) == list:
                ret_val += ast_elem
            else:
                ret_val.append(ast_elem)
        return ret_val

    def _handle_left_binop (self, node, construct_op):
        children = node[1]
        if len(children) > 1:
            child_results = [self.handle_node(child) for child in children]
            location = self._get_location(node)
            op = construct_op(child_results[1])
            ret_val = BinOp(child_results[0], op, child_results[2],
                            location[0], location[1])
            for child_index in range(4, len(child_results), 2):
                location = child_results[child_index - 1][2]
                op = construct_op(child_results[child_index - 1])
                ret_val = BinOp(ret_val, op, child_results[child_index],
                                location[0], location[1])
        else:
            ret_val = self.handle_node(children[0])
        return ret_val

    def _handle_logical_op (self, node, op_constructor):
        children = node[1]
        if len(children) > 1:
            child_results = [self.handle_node(child) for child in children]
            location = self._get_location(node)
            ret_val = BoolOp(op_constructor(),
                             [child for child in child_results
                              if isinstance(child, AST)],
                             location[0], location[1])
        else:
            ret_val = self.handle_node(children[0])
        return ret_val

    def _get_location (self, node):
        is_token = self.is_token
        while not is_token(node):
            node = node[1][0]
        return node[0][2]

    def _get_tokens (self, node):
        if self.is_token(node):
            yield node[0]
        else:
            child_stack = node[1][:]
            child_stack.reverse()
            while child_stack:
                crnt_node = child_stack.pop()
                if self.is_token(crnt_node):
                    yield crnt_node[0]
                else:
                    crnt_children = crnt_node[1][:]
                    crnt_children.reverse()
                    child_stack.extend(crnt_children)

    def _handle_comp_for (self, node):
        children = node[1]
        old_context = self.expr_context
        self.expr_context = Store
        target = self.handle_node(children[1])
        self.expr_context = old_context
        iter_expr = self.handle_node(children[3])
        child_ifs = []
        comprehensions = []
        if len(children) > 4:
            child_ifs, comprehensions = self.handle_node(children[4])
        comprehensions.insert(0, comprehension(target, iter_expr, child_ifs))
        return ([], comprehensions)

    def _handle_comp_if (self, node):
        children = node[1]
        if_expr = self.handle_node(children[1])
        peer_ifs = []
        comprehensions = []
        if len(children) > 2:
            peer_ifs, comprehensions = self.handle_node(children[2])
        peer_ifs.insert(0, if_expr)
        return (peer_ifs, comprehensions)

    def handle_and_expr (self, node):
        return self._handle_left_binop(node, lambda x : BitAnd())

    def handle_and_test (self, node):
        return self._handle_logical_op(node, And)

    def handle_arglist (self, node):
        """handle_arglist() - Should return a 4-element list with the
        argument related inputs to the Call constructor."""
        args = []
        keywords = []
        starargs = None
        kwargs = None
        children = self.get_children(node)
        child_count = len(children)
        child_index = 0
        while ((child_index < child_count) and
               (not self.is_token(children[child_index]))):
            child_result = self.handle_node(children[child_index])
            if isinstance(child_result, keyword):
                keywords.append(child_result)
                child_index += 2
                break
            args.append(child_result)
            child_index += 2
        while ((child_index < child_count) and
               (not self.is_token(children[child_index]))):
            child_result = self.handle_node(children[child_index])
            if not isinstance(child_result, keyword):
                # XXX Typical syntax error notes.
                raise SyntaxError("non-keyword arg after keyword arg")
            keywords.append(child_result)
            child_index += 2
        if ((child_index < child_count) and
            self.is_token(children[child_index]) and
            children[child_index][0][1] == "*"):
            starargs = self.handle_node(children[child_index + 1])
            child_index += 3
        if ((child_index < child_count) and
            self.is_token(children[child_index]) and
            children[child_index][0][1] == "**"):
            kwargs = self.handle_node(children[child_index + 1])
            child_index += 3
        # XXX Additional checks required here?
        return [args, keywords, starargs, kwargs]

    def handle_argument (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            if children[1][0][1] == '=':
                # Keyword argument.
                assert len(children) == 3
                lhs = self.handle_node(children[0])
                if not isinstance(lhs, Name):
                    # XXX This error message is what Python says.
                    raise SyntaxError("keyword can't be an expression")
                lhs_keyword = lhs.id
                rhs = self.handle_node(children[2])
                ret_val = keyword(lhs_keyword, rhs)
            else:
                # Generator argument.
                location = self._get_location(children[0])
                target = self.handle_node(children[0])
                if_exprs, comprehensions = self.handle_node(children[1])
                assert len(if_exprs) == 0
                ret_val = GeneratorExp(target, comprehensions, *location)
        return ret_val

    def handle_arith_expr (self, node):
        def arith_op (tok):
            return Add() if tok[1] == "+" else Sub()
        return self._handle_left_binop(node, arith_op)

    def handle_assert_stmt (self, node):
        children = node[1]
        assert self.is_token(children[0])
        location = children[0][0][2]
        child_results = self._handle_nontoken_children(node)
        if len(child_results) == 1:
            test = child_results[0]
            msg = None
        else:
            test, msg = child_results
        return Assert(test, msg, location[0], location[1])

    def handle_atom (self, node):
        ret_val = None
        children = node[1]
        assert self.is_token(children[0])
        token_text = children[0][0][1]
        token_location = children[0][0][2]
        if token_text == "(":
            if self.is_token(children[1]) and children[1][0][1] == ")":
                if self.expr_context is not Load:
                    # XXX Figure out how to push stack frame for
                    # traceback from Python.
                    raise ExprContextError()
                ret_val = Tuple([], Load(), token_location[0],
                                token_location[1])
            else:
                # NOTE: This puts the burden of detecting a tuple and
                # constructing it on handle_testlist_gexp().
                ret_val = self.handle_node(children[1])
        elif token_text == "[":
            if self.is_token(children[1]) and children[1][0][1] == "]":
                if self.expr_context is not Load:
                    # XXX Figure out how to push stack frame for
                    # traceback from Python.
                    raise ExprContextError()
                ret_val = List([], Load(), *token_location)
            else:
                ret_val = self.handle_node(children[1])
                if hasattr(ret_val, "lineno") and ret_val.lineno is None:
                    ret_val.lineno, ret_val.col_offset = token_location
        elif token_text == "{":
            if self.expr_context is not Load:
                raise ExprContextError()
            if self.is_token(children[1]) and children[1][0][1] == "}":
                ret_val = Dict([], [], token_location[0], token_location[1])
            else:
                ret_val = self.handle_node(children[1])
                if hasattr(ret_val, "lineno"):
                    ret_val.lineno = token_location[0]
                if hasattr(ret_val, "col_offset"):
                    ret_val.col_offset = token_location[1]
        elif token_text == "`":
            assert children[2][0][1] == "`"
            ret_val = Repr(self.handle_node(children[1]), token_location[0],
                           token_location[1])
        else:
            token_kind = children[0][0][0]
            if token_kind == MyRealParser.STRING:
                ret_string = eval(token_text)
                for child in children[1:]:
                    ret_string += eval(child[0][1])
                ret_val = Str(ret_string, token_location[0], token_location[1])
            elif token_kind == MyRealParser.NUMBER:
                ret_val = Num(eval(token_text), token_location[0],
                              token_location[1])
            else:
                assert token_kind == MyRealParser.NAME
                ret_val = Name(token_text, self.expr_context(),
                               token_location[0], token_location[1])
        return ret_val

    def handle_augassign (self, node):
        children = node[1]
        token_text = children[0][0][1]
        return {'+=' : Add,
                '-=' : Sub,
                '*=' : Mult,
                '/=' : Div,
                '%=' : Mod,
                '&=' : BitAnd,
                '|=' : BitOr,
                '^=' : BitXor,
                '<<=' : LShift,
                '>>=' : RShift,
                '**=' : Pow,
                '//=' : FloorDiv}[token_text]()

    def handle_break_stmt (self, node):
        location = node[1][0][0][2]
        return Break(location[0], location[1])

    def handle_classdef (self, node):
        children = node[1]
        location = children[0][0][2]
        class_name = children[1][0][1]
        bases = []
        if self.is_token(children[2]) and children[2][0][1] == "(":
            if not self.is_token(children[3]):
                bases = self.handle_node(children[3])
                if type(bases) != Tuple:
                    # No comma, causing handle_testlist() to return
                    # the sole child.
                    # XXX Should handle_testlist() return a list
                    # unconditionally, and be added to the list of
                    # nodes that can't be simplified?
                    bases = [bases]
                else:
                    bases = bases.elts
        return ClassDef(class_name, bases, self.handle_node(children[-1]),
                        location[0], location[1])

    def handle_comp_op (self, node):
        children = node[1]
        token_text = children[0][0][1]
        if len(children) == 1:
            ret_val = {'<': Lt,
                       '>': Gt,
                       '==': Eq,
                       '>=': GtE,
                       '<=': LtE,
                       '<>': NotEq,
                       '!=': NotEq,
                       'in': In,
                       'is' : Is}[token_text]()
        elif token_text == "is":
            ret_val = IsNot()
        else:
            assert token_text == "not"
            ret_val = NotIn()
        return ret_val

    def handle_comparison (self, node):
        children = node[1]
        left = self.handle_node(children[0])
        if len(children) == 1:
            ret_val = left
        else:
            ops = []
            comparators = []
            for child_index in xrange(1, len(children), 2):
                ops.append(self.handle_node(children[child_index]))
                comparators.append(self.handle_node(children[child_index + 1]))
            lineno = None
            col_offset = None
            if hasattr(left, "lineno"):
                lineno = left.lineno
                col_offset = left.col_offset
            ret_val = Compare(left, ops, comparators, lineno, col_offset)
        return ret_val

    handle_compound_stmt = _handle_only_child

    def handle_continue_stmt (self, node):
        location = node[1][0][0][2]
        return Continue(location[0], location[1])

    def handle_decorator (self, node):
        children = node[1]
        ret_val = self.handle_node(children[1])
        child_count = len(children)
        if child_count > 3:
            location = children[0][0][2]
            args = [ret_val]
            if child_count > 5:
                args += self.handle_node(children[3])
            else:
                args += [[], [], None, None]
            args += location
            ret_val = Call(*args)
        return ret_val

    handle_decorators = Handler.handle_children

    def handle_del_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        old_context = self.expr_context
        self.expr_context = Del
        targets = self.handle_node(children[1])
        self.expr_context = old_context
        if type(targets) != Tuple:
            # XXX This has a similar flavor to the handle_testlist()
            # notes; see handle_classdef() in the base class handling.
            targets = [targets]
        else:
            targets = targets.elts
        return Delete(targets, location[0], location[1])

    def handle_dictmaker (self, node):
        children = node[1]
        keys = []
        values = []
        assert len(children) > 2
        for child_index in xrange(0, len(children), 4):
            keys.append(self.handle_node(children[child_index]))
            values.append(self.handle_node(children[child_index + 2]))
        # Note: The location is going to be set by handle_atom().
        return Dict(keys, values)

    def handle_dotted_as_name (self, node):
        children = node[1]
        module_name = ""
        for token in self._get_tokens(children[0]):
            module_name += token[1]
        module_alias = None
        if len(children) > 1:
            # XXX Unsure about where 'dotted_name NAME NAME' is legal...
            assert children[1][0][1] == "as"
            module_alias = children[2][0][1]
        return alias(module_name, module_alias)

    handle_dotted_as_names = _handle_nontoken_children

    def handle_dotted_name (self, node):
        """Note: This is circumvented by handle_dotted_as_name()!"""
        # XXX Not sure this has the 100% fidelity I want.
        children = node[1]
        first_name = children[0][0][1]
        first_location = children[0][0][2]
        ret_val = Name(first_name, Load(), first_location[0],
                       first_location[1])
        for child_index in xrange(2, len(children), 2):
            location = children[child_index - 1][0][2]
            ret_val = Attribute(ret_val, children[child_index][0][1], Load(),
                                *location)
        return ret_val

    def handle_encoding_decl (self, node):
        raise NotImplementedError("should not be reachable in grammar!")

    def handle_eval_input (self, node):
        ret_val = self.handle_node(node[1][0])
        return ret_val

    def handle_except_clause (self, node):
        ret_val = []
        children = node[1][1:]
        if len(children) > 0:
            ret_val.append(self.handle_node(children[0]))
            if len(children) > 1:
                old_context = self.expr_context
                self.expr_context = Store
                ret_val.append(self.handle_node(children[2]))
                self.expr_context = old_context
        return ret_val

    def handle_exec_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        body = self.handle_node(children[1])
        global_expr = None
        local_expr = None
        if len(children) > 2:
            global_expr = self.handle_node(children[3])
            if len(children) > 4:
                local_expr = self.handle_node(children[5])
        return Exec(body, global_expr, local_expr, *location)

    def handle_expr (self, node):
        return self._handle_left_binop(node, lambda tok : BitOr())

    def handle_expr_stmt (self, node):
        children = node[1]
        if len(children) == 1:
            location = self._get_location(children[0])
            ret_val = Expr(self.handle_node(children[0]), location[0],
                           location[1])
        elif not self.is_token(children[1]):
            assert len(children) == 3
            # Augmented assignment
            location = self._get_location(children[0])
            old_context = self.expr_context
            self.expr_context = Store
            lhs = self.handle_node(children[0])
            self.expr_context = old_context
            aug_op = self.handle_node(children[1])
            rhs = self.handle_node(children[2])
            ret_val = AugAssign(lhs, aug_op, rhs, location[0], location[1])
        else:
            location = self._get_location(children[0])
            old_context = self.expr_context
            self.expr_context = Store
            targets = [self.handle_node(child) for child in children[:-1]
                       if not self.is_token(child)]
            self.expr_context = old_context
            value = self.handle_node(children[-1])
            ret_val = Assign(targets, value, location[0], location[1])
        return ret_val

    def handle_exprlist (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            location = self._get_location(children[0])
            tup_elems = self._handle_nontoken_children(node)
            ret_val = Tuple(tup_elems, self.expr_context(), location[0],
                            location[1])
        return ret_val

    def handle_factor (self, node):
        children = node[1]
        if len(children) > 1:
            token = children[0][0]
            token_text = token[1]
            token_location = token[2]
            unary_op_constructor = {"+" : UAdd,
                                    "-" : USub,
                                    "~" : Invert}[token_text]
            ret_val = UnaryOp(unary_op_constructor(),
                              self.handle_node(children[1]),
                              token_location[0], token_location[1])
        else:
            ret_val = self.handle_node(children[0])
        return ret_val

    def handle_file_input (self, node):
        child_results = self._handle_nontoken_children(node)
        return Module(self._flatten_once(child_results))

    handle_flow_stmt = _handle_only_child

    def handle_for_stmt (self, node):
        children = node[1]
        location = self._get_location(children[0])
        old_context = self.expr_context
        self.expr_context = Store
        target = self.handle_node(children[1])
        self.expr_context = old_context
        # XXX Compatibility hack to comply with Python - which seems
        # to only apply in a weird situations...WTF, yo?
        if isinstance(target, Tuple):
            target.col_offset = location[1]
        iter_expr = self.handle_node(children[3])
        body_stmts = self.handle_node(children[5])
        orelse_stmts = []
        if len(children) > 6:
            orelse_stmts = self.handle_node(children[-1])
        return For(target, iter_expr, body_stmts, orelse_stmts, *location)

    def handle_fpdef (self, node):
        children = node[1]
        if len(children) == 1:
            child_data = children[0][0]
            location = child_data[2]
            ret_val = Name(child_data[1], self.expr_context(), location[0],
                           location[1])
        else:
            assert len(children) == 3 and children[0][0][1] == "("
            ret_val = self.handle_node(children[1])
        return ret_val

    def handle_fplist (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            old_context = self.expr_context
            self.expr_context = Store
            tup_elems = [self.handle_node(child) for child in children
                         if not self.is_token(child)]
            self.expr_context = old_context
            ret_val = Tuple(tup_elems, Store(), location[0], location[1])
        return child_results

    def handle_funcdef (self, node):
        children = node[1]
        location = self._get_location(children[0])
        name_index = 1
        decorators = []
        if not self.is_token(children[0]):
            name_index = 2
            decorators = self.handle_node(children[0])
        name = children[name_index][0][1]
        params = self.handle_node(children[name_index + 1])
        body = self.handle_node(children[name_index + 3])
        return FunctionDef(name, params, body, decorators, location[0],
                           location[1])

    def handle_gen_for (self, node):
        return self._handle_comp_for(node)

    def handle_gen_if (self, node):
        return self._handle_comp_if(node)

    handle_gen_iter = _handle_only_child

    def handle_global_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        global_names = [child[0][1] for child in children[1::2]]
        return Global(global_names, *location)

    def handle_if_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        test = self.handle_node(children[1])
        body_stmts = self.handle_node(children[3])
        orelse_stmts = []
        elifs = []
        child_index = 4
        while ((child_index < len(children)) and
               (children[child_index][0][1] == "elif")):
            # XXX Another questionable location source (I would have
            # used the elif token location...)
            elifs.append((self._get_location(children[child_index + 1]),
                          self.handle_node(children[child_index + 1]),
                          self.handle_node(children[child_index + 3])))
            child_index += 4
        if child_index < len(children):
            assert children[child_index][0][1] == "else"
            orelse_stmts = self.handle_node(children[child_index + 2])
        if len(elifs) > 0:
            elifs.reverse()
            for elif_location, elif_test, elif_body in elifs:
                orelse_stmts = [If(elif_test, elif_body, orelse_stmts,
                                   *elif_location)]
        return If(test, body_stmts, orelse_stmts, *location)

    def handle_import_as_name (self, node):
        children = node[1]
        name = children[0][0][1]
        as_name = None
        if len(children) > 1:
            # XXX Same 'as' weirdness as in handle_dotted_as_name()...
            assert len(children) == 3
            as_name = children[2][0][1]
        return alias(name, as_name)

    handle_import_as_names = _handle_nontoken_children

    def handle_import_from (self, node):
        children = node[1]
        child_count = len(children)
        location = children[0][0][2]
        level = 0
        child_index = 1
        while ((child_index < child_count) and
               (self.is_token(children[child_index])) and
               (children[child_index][0][1] == ".")):
            level += 1
            child_index += 1
        module_name = ""
        if ((child_index < child_count) and
            (not self.is_token(children[child_index]))):
            module_name = "".join(token[1] for token in
                                  self._get_tokens(children[child_index]))
            child_index += 1
        assert ((child_index < child_count) and
                (children[child_index][0][1] == "import"))
        child_index += 1
        names = []
        if ((child_index < child_count) and
            (self.is_token(children[child_index]))):
            if children[child_index][0][1] == "*":
                names.append(alias("*", None))
            else:
                assert children[child_index][0][1] == "("
                names = self.handle_node(children[child_index + 1])
        else:
            names = self.handle_node(children[child_index])
        return ImportFrom(module_name, names, level, *location)

    def handle_import_name (self, node):
        children = node[1]
        location = children[0][0][2]
        return Import(self.handle_node(children[1]), *location)

    handle_import_stmt = _handle_only_child

    def handle_lambdef (self, node):
        children = node[1]
        location = children[0][0][2]
        args = arguments([], None, None, [])
        if len(children) > 3:
            args = self.handle_node(children[1])
        body = self.handle_node(children[-1])
        return Lambda(args, body, *location)

    def handle_list_and_or_kw_args (self, node):
        children = node[1]
        vararg_name = None
        kwarg_name = None
        kw_index = 1
        if children[0][0][1] == "*":
            vararg_name = children[1][0][1]
            kw_index = 4
        if kw_index < len(children):
            kwarg_name = children[kw_index][0][1]
        return ([], vararg_name, kwarg_name, [])

    def handle_list_for (self, node):
        return self._handle_comp_for(node)

    def handle_list_if (self, node):
        return self._handle_comp_if(node)

    handle_list_iter = _handle_only_child

    def handle_listmaker (self, node):
        children = node[1]
        first_elem = self.handle_node(children[0])
        if len(children) == 1:
            ret_val = List([first_elem], self.expr_context())
        else:
            if self.is_token(children[1]):
                # Comma separated list.
                child_elems = [first_elem] + [self.handle_node(child)
                                              for child in children[2::2]]
                ret_val = List(child_elems, self.expr_context())
            else:
                # List comprehension
                location = self._get_location(children[0])
                comp_ifs, comprehensions = self.handle_node(children[1])
                assert len(comp_ifs) == 0
                # XXX Okay, this is just messed up.  I have to set the
                # position here, but must set it in the caller for
                # lists?!?
                ret_val = ListComp(first_elem, comprehensions, *location)
        return ret_val

    def handle_not_test (self, node):
        children = node[1]
        if len(children) > 1:
            assert len(children) == 2
            location = children[0][0][2]
            ret_val = UnaryOp(Not(), self.handle_node(children[1]),
                              location[0], location[1])
        else:
            ret_val = self.handle_node(children[0])
        return ret_val

    # This is groovy because old_lambdef and lambdef have the same
    # shape despite having different nonterminal contents.  This is
    # only reachable from list comprehensions anyway...
    handle_old_lambdef = handle_lambdef

    handle_old_test = _handle_only_child

    def handle_or_test (self, node):
        return self._handle_logical_op(node, Or)

    def handle_parameters (self, node):
        children = node[1]
        if len(children) > 2:
            ret_val = self.handle_node(children[1])
        else:
            ret_val = arguments([], None, None, [])
        return ret_val

    def handle_pass_stmt (self, node):
        children = node[1]
        assert len(children) == 1
        location = children[0][0][2]
        return Pass(location[0], location[1])

    def _process_trailer (self, value, trailer, location):
        ret_val = self.handle_node(trailer)
        if hasattr(ret_val, "value"):
            ret_val.value = value
        elif hasattr(ret_val, "func"):
            ret_val.func = value
        # XXX I'm not really happy about this position convention.
        ret_val.lineno = location[0]
        ret_val.col_offset = location[1]
        return ret_val

    def handle_power (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            location = self._get_location(children[0])
            starstar_flag = self.is_token(children[-2])
            power_rhs = None
            if self.is_token(children[-2]):
                assert children[-2][0][1] == "**"
                power_rhs = children[-1]
                children = children[:-2]
            if len(children) == 1:
                ret_val = self.handle_node(children[0])
            else:
                old_context = self.expr_context
                self.expr_context = Load
                crnt_val = self.handle_node(children[0])
                for child in children[1:-1]:
                    crnt_val = self._process_trailer(crnt_val, child, location)
                self.expr_context = old_context
                ret_val = self._process_trailer(crnt_val, children[-1],
                                                location)
            if power_rhs:
                ret_val = BinOp(ret_val, Pow(), self.handle_node(power_rhs),
                                location[0], location[1])
        return ret_val

    def handle_print_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        children = children[1:]
        dest = None
        values = []
        newline = True
        if children:
            if self.is_token(children[0]) and children[0][0][1] == ">>":
                dest = self.handle_node(children[1])
                children = children[2:]
            values = [self.handle_node(child) for child in children
                      if not self.is_token(child)]
            if children:
                newline = not (self.is_token(children[-1]) and
                               children[-1][0][1] == ",")
        return Print(dest, values, newline, *location)

    def handle_qsuite (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = children[0][0][1]
        else:
            ret_val = children[2][0][1]
        return ret_val

    def handle_quotedef (self, node):
        children = node[1]
        location = children[0][0][2]
        lang_expr = None
        child_index = 1
        if (self.is_token(children[child_index]) and
            children[child_index][0][1] == '['):
            lang_expr = self.handle_node(children[child_index + 1])
            child_index += 3
        name = None
        if ((child_index < len(children)) and
            self.is_token(children[child_index]) and
            (children[child_index][0][1] != ':')):
            name = children[child_index][0][1]
            child_index += 1
        body_str = self.handle_node(children[-1])
        return QuoteDef(lang_expr, name, body_str, *location)

    def handle_raise_stmt (self, node):
        children = node[1]
        child_count = len(children)
        location = children[0][0][2]
        exn_type = None
        exn_inst = None
        exn_tback = None
        if child_count > 1:
            exn_type = self.handle_node(children[1])
            if child_count > 3:
                exn_inst = self.handle_node(children[3])
                if child_count > 5:
                    exn_tback = self.handle_node(children[5])
        return Raise(exn_type, exn_inst, exn_tback, *location)

    def handle_return_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        value = None
        if len(children) > 1:
            value = self.handle_node(children[1])
        return Return(value, location[0], location[1])

    def handle_shift_expr (self, node):
        def shift_op (tok):
            return LShift() if tok[1] == "<<" else RShift()
        return self._handle_left_binop(node, shift_op)

    handle_simple_stmt = _handle_nontoken_children

    def handle_single_input (self, node):
        child_results = self.handle_children(node)
        return child_results

    def handle_sliceop (self, node):
        children = node[1]
        if len(children) == 1:
            # XXX Is this right?  This is what the Python compiler returns...
            location = self._get_location(children[0])
            ret_val = Name("None", Load(), *location)
        else:
            ret_val = self.handle_node(children[1])
        return ret_val

    handle_small_stmt = _handle_only_child

    handle_start = _handle_only_child

    handle_stmt = _handle_only_child

    def handle_subscript (self, node):
        children = node[1]
        if len(children) == 1:
            # XXX Would really like to hand up an Index() instance,
            # but unfortunately, handle_subscriptlist() must be able
            # to determine if the index is a tuple and not an extended
            # slice.
            if self.is_token(children[0]):
                assert children[0][0][1] == ":"
                ret_val = Slice(None, None, None)
            else:
                ret_val = self.handle_node(children[0])
        elif ((len(children) == 3) and
              self.is_token(children[0]) and
              (children[0][0][1] == ".")):
            ret_val = Ellipsis()
        else:
            lower = None
            upper = None
            step = None
            child_index = 0
            if not self.is_token(children[child_index]):
                lower = self.handle_node(children[child_index])
                child_index += 1
            assert (self.is_token(children[child_index]) and
                    children[child_index][0][1] == ":")
            child_index += 1
            # XXX Would like better way of determining what kind of
            # nonterminal a node is...
            if ((child_index < len(children)) and
                (children[child_index][0] == "test")):
                upper = self.handle_node(children[child_index])
                child_index += 1
            if child_index < len(children):
                step = self.handle_node(children[child_index])
            ret_val = Slice(lower, upper, step)
        return ret_val

    def _is_slice_type (self, obj):
        return type(obj) in (Ellipsis, Slice, ExtSlice, Index)

    def handle_subscriptlist (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            child_elems = [self.handle_node(child) for child in children
                           if not self.is_token(child)]
            is_slice = False
            for child in child_elems:
                if self._is_slice_type(child):
                    is_slice = True
                    break
            if is_slice:
                child_elems = [child_elem
                               if self._is_slice_type(child_elem) else
                               Index(child_elem)
                               for child_elem in child_elems]
                ret_val = ExtSlice(child_elems)
            else:
                location = self._get_location(children[0])
                ret_val = Tuple(child_elems, self.expr_context(), location[0],
                                location[1])
        if not self._is_slice_type(ret_val):
            ret_val = Index(ret_val)
        return ret_val

    def handle_suite (self, node):
        return self._flatten_once(self._handle_nontoken_children(node))

    def handle_term (self, node):
        def term_op (tok):
            return {"*" : Mult,
                    "/" : Div,
                    "%" : Mod,
                    "//" : FloorDiv}[tok[1]]()
        return self._handle_left_binop(node, term_op)

    def handle_test (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            location = self._get_location(children[0])
            true_expr = self.handle_node(children[0])
            pred_expr = self.handle_node(children[2])
            false_expr = self.handle_node(children[4])
            ret_val = IfExp(pred_expr, true_expr, false_expr, *location)
        return ret_val

    def handle_testlist (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = self.handle_node(children[0])
        else:
            location = self._get_location(children[0])
            tup_elems = self._handle_nontoken_children(node)
            ret_val = Tuple(tup_elems, self.expr_context(), *location)
        return ret_val

    handle_testlist1 = handle_testlist

    def handle_testlist_gexp (self, node):
        children = node[1]
        ret_val = self.handle_node(children[0])
        if len(children) > 1:
            location = self._get_location(children[0])
            if self.is_token(children[1]):
                # Tuple
                tuple_elems = [ret_val] + [self.handle_node(child)
                                           for child in children[2:]
                                           if not self.is_token(child)]
                ret_val = Tuple(tuple_elems, self.expr_context(), *location)
            else:
                # Generator
                assert len(children) == 2
                if_exprs, comprehensions = self.handle_node(children[1])
                assert len(if_exprs) == 0
                ret_val = GeneratorExp(ret_val, comprehensions, *location)
        return ret_val

    # This is cool, since testlist_safe and testlist still have the same shape.
    handle_testlist_safe = handle_testlist

    def handle_trailer (self, node):
        children = node[1]
        assert self.is_token(children[0])
        token_data = children[0][0]
        token_text = token_data[1]
        location = token_data[2]
        if token_text == "(":
            call_args = [[], [], None, None]
            if len(children) == 3:
                call_args = self.handle_node(children[1])
            ret_val = Call(None, *call_args)
        elif token_text == "[":
            old_context = self.expr_context
            self.expr_context = Load
            child_slice = self.handle_node(children[1])
            self.expr_context = old_context
            ret_val = Subscript(None, child_slice, self.expr_context(),
                                location[0], location[1])
        elif token_text == ".":
            ret_val = Attribute(None, children[1][0][1], self.expr_context(),
                                location[0], location[1])
        return ret_val

    def handle_try_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        if self.is_token(children[3]):
            body_stmts = self.handle_node(children[2])
            final_stmts = self.handle_node(children[-1])
            ret_val = TryFinally(body_stmts, final_stmts, *location)
        else:
            child_count = len(children)
            body_stmts = self.handle_node(children[2])
            handlers = []
            child_index = 3
            while ((child_index < child_count) and
                   (not self.is_token(children[child_index]))):
                except_location = self._get_location(children[child_index])
                except_results = self.handle_node(children[child_index])
                except_type = None
                if len(except_results) > 0:
                    except_type = except_results[0]
                except_name = None
                if len(except_results) > 1:
                    except_name = except_results[1]
                except_body = self.handle_node(children[child_index + 2])
                handlers.append(excepthandler(except_type, except_name,
                                              except_body, *except_location))
                child_index += 3
            orelse_stmts = []
            if ((child_index < child_count) and
                self.is_token(children[child_index]) and
                (children[child_index][0][1] == "else")):
                orelse_stmts = self.handle_node(children[child_index + 2])
                child_index += 3
            ret_val = TryExcept(body_stmts, handlers, orelse_stmts, *location)
            if ((child_index < child_count) and
                self.is_token(children[child_index]) and
                (children[child_index][0][1] == "finally")):
                finally_stmts = self.handle_node(children[child_index + 2])
                ret_val = TryFinally([ret_val], finally_stmts, *location)
        return ret_val

    def _handle_varargs (self, children):
        if children[0][0] == "fpdef":
            old_context = self.expr_context
            self.expr_context = Param
            fpdef_result = [self.handle_fpdef(children[0])]
            self.expr_context = old_context
            default_value = []
            tail_result = None
            if len(children) > 1:
                tail_index = 1
                if self.is_token(children[tail_index]):
                    default_value = [self.handle_node(children[2])]
                    tail_index = 3
                if tail_index < len(children):
                    tail_result = self.handle_node(children[tail_index])
            if tail_result is None:
                arg_args = (fpdef_result, None, None, default_value)
            else:
                if (len(default_value) > 0 and
                    (len(tail_result[3]) < len(tail_result[0]))):
                    # XXX
                    raise SyntaxError("non-default argument follows default "
                                      "argument")
                arg_args = (fpdef_result + tail_result[0],
                            tail_result[1], tail_result[2],
                            default_value + tail_result[3])
        else:
            # Should be list_and_or_kw_args...
            assert len(children) == 1
            arg_args = self.handle_node(children[0])
        return arg_args

    def handle_varargslist (self, node):
        children = node[1]
        arg_args = self._handle_varargs(children)
        return arguments(*arg_args)

    def handle_varargslist_end (self, node):
        children = node[1]
        if len(children) == 1:
            ret_val = ([], None, None, [])
        else:
            ret_val = self._handle_varargs(children[1:])
        return ret_val

    def handle_while_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        test_expr = self.handle_node(children[1])
        body_stmts = self.handle_node(children[3])
        orelse_stmts = []
        if len(children) > 4:
            orelse_stmts = self.handle_node(children[-1])
        return While(test_expr, body_stmts, orelse_stmts, *location)

    def handle_with_stmt (self, node):
        children = node[1]
        location = children[0][0][2]
        context_expr = self.handle_node(children[1])
        optional_vars = None
        if not self.is_token(children[2]):
            optional_vars = self.handle_node(children[2])
        body_stmts = self.handle_node(children[-1])
        return With(context_expr, optional_vars, body_stmts, *location)

    def handle_with_var (self, node):
        # XXX Not sure this is correct; the with statement doesn't
        # compile w/o future import.  (Need to read the PEP.)
        children = node[1]
        assert len(children) == 2
        old_context = self.expr_context
        self.expr_context = Store
        ret_val = self.handle_node(children[1])
        self.expr_context = old_context
        return ret_val

    def handle_xor_expr (self, node):
        return self._handle_left_binop(node, lambda x : BitXor())

    def handle_yield_expr (self, node):
        children = node[1]
        location = children[0][0][2]
        value = None
        if len(children) > 1:
            value = self.handle_node(children[1])
        return Yield(value, *location)

    def handle_yield_stmt (self, node):
        children = node[1]
        assert len(children) == 1
        child_result = self.handle_node(children[0])
        return Expr(child_result, child_result.lineno, child_result.col_offset)

# ______________________________________________________________________
# Self-test routine

def build_test_environment ():
    """build_test_environment() - Create an environment for testing
    this transformer against the native Python transformer.  Returned
    as a dictionary."""
    import StringIO
    import operator
    import tokenize
    import MyRealParser
    import myfront_transformer
    import myfront_ast
    import _ast
    import ASTUtils
    import pprint
    # ____________________________________________________________
    ast_to_tuple = ASTUtils.mk_ast_to_tuple(myfront_ast.AST)
    pyast_to_tuple = ASTUtils.mk_pyast_to_tuple(myfront_ast.__dict__)
    # ____________________________________________________________
    def myparse (text):
        sio = StringIO.StringIO(text)
        tok = tokenize.generate_tokens(sio.readline)
        parser = MyRealParser.MyRealParser(tok)
        cpt = parser()
        hdlr = myfront_transformer.MyHandler()
        return hdlr.handle_node(cpt)
    # ____________________________________________________________
    def theirparse (text):
        return compile(text, '<stdin>', 'exec', _ast.PyCF_ONLY_AST)
    # ____________________________________________________________
    def dotest (text, comparator = None):
        if comparator is None:
            comparator = operator.__eq__
        tup1 = ast_to_tuple(myparse(text))
        tup2 = pyast_to_tuple(theirparse(text))
        assert comparator(tup1, tup2), ("For %s,\n%s\n!=\n%s" %
                                        (`text`, pprint.pformat(tup1),
                                         pprint.pformat(tup2)))
    # ____________________________________________________________
    test_strings = ["pass\n",
                    "pass\npass\n",
                    "a & 3 & 2\n",
                    "a | 2 | 1\n",
                    "x + 3 - 2\n",
                    "assert True\n",
                    "assert False, 'message!'\n",
                    "x += 2\n",
                    "x -= 3\n",
                    "x *= 2\n",
                    "y /= 55\n",
                    "z %= 3\n",
                    "duh &= 99\n",
                    "dur |= 99\n",
                    "dee ^= 0\n",
                    "zounds <<= 3\n",
                    "zends >>= 4\n",
                    "powzer **= 3.2\n",
                    "drowzer //= _\n",
                    "royalty.sir.nukesalot |= 99\n",
                    "freed[99] ^= 105\n",
                    "frood[99][2] &= 203\n",
                    "while 1:\n break\n",
                    "while 1:\n continue\n",
                    "class Goo:\n pass\n\n",
                    "class Goo:\n pass\n pass\n",
                    "class Goo ():\n pass\n\n",
                    "class Goo (Gah):\n pass\n\n",
                    "class Spum (Egg, Baconish):\n pass\n\n",
                    "3 < 4\n",
                    "3 > 4\n",
                    "3 == 4\n",
                    "3 >= 4\n",
                    "3 <= 4\n",
                    "3 != 4\n",
                    "3 <> 4\n",
                    "3 in (3,4)\n",
                    "3 not in (1,2)\n",
                    "None is None\n",
                    "None is not None\n",
                    "3 <= x <= 9\n",
                    "def egg ():\n pass\n\n",
                    "def sporm ():\n return\n\n",
                    "@thingy\ndef egg ():\n pass\n\n",
                    "def second (x, y):\n return y\n\n",
                    "def f (*a):\n return a\n\n",
                    "def f (**kws):\n return kws\n\n",
                    "def f (*a, **kws):\n return a, kws\n\n",
                    "def f (x = 23, y = 99):\n return x,y\n\n",
                    "1,2,3\n",
                    "True or False\n",
                    "True and True\n",
                    "not not not False\n",
                    "2 << 4 << 5\n",
                    "5 >> 2 >> 3\n",
                    "+ x\n",
                    "-y, ~z\n",
                    "del xzyyz\n",
                    "del x[4]\n",
                    "del x,z,y\n",
                    "{'egg' : drop, 'soup' : 99}\n",
                    "import foo\n",
                    "import flum.bloor\n",
                    "import flum.bloor as blixy\n",
                    "(x,y) = (z,q) = (1,2)\n",
                    "2 ** 8 ** 1\n",
                    "f(1,2,3)\n",
                    "f(1,2,z = 99, n = 2)\n",
                    "f(*a)\n",
                    "f(**kws)\n",
                    "f(*a, **kws)\n",
                    "f(1, 2, x= 22, *a, **kws)\n",
                    "org[ogg], crim[4,5,6], crum[3,4:]\n",
                    "crazy_copy = crazy[:]\n",
                    "crobs[3,nimz] = 99\n",
                    "del x[4:3:]\n",
                    "del x[4::]\n",
                    "del x[::]\n",
                    "del x[:]\n",
                    "x[:] = 8\n",
                    "x[::] = 8\n",
                    "x[::5] = 8\n",
                    "exec 'print 99'\n",
                    "exec f.func_code in {'a' : 23, 'b' : 99}\n",
                    "exec f.func_code in {}, {'v' : 'ictory'}\n",
                    "print 'The answer is blowing in the %s' % 'shower'\n",
                    "print 'Or something like the number', 99,\n",
                    "print spam_msg.get()\n",
                    "print\n",
                    "print >> stderr\n",
                    "print >>stderr, 'Your stuff is all effed.'\n",
                    "for x,n in y:\n z\n w, w\nelse:\n w\n\n",
                    "for x,n in y:\n z\n w, w\n\n",
                    "(x + 22 / y for x in range(10) if x % 3 == 0 for y in "\
                     "range(10) if y % 2 == 0)\n",
                    "if x:\n y\n\n",
                    "if x:\n y\nelse:\n z\n",
                    "if x:\n y\nelif ~x:\n w\nelse:\n z\n",
                    "if x:\n y\nelif ~x:\n z\nelif x > 4:\n w**2\n",
                    "if x:\n y\nelif ~x:\n z\nelif x > 4:\n w**2\nelse:\n 9\n",
                    "lambda x : x\n",
                    "lambda : x\n",
                    "lambda : x, 7\n",
                    "lambda x, y, z  = 99: x, 7\n",
                    "from module import *\n",
                    "from .. import thingy\n",
                    "from ...module import thingy\n",
                    "from module.blah.blort import nip as nosh, torque\n",
                    "from module.blah.blort import (nip as nosh, torque)\n",
                    "from module.blah.blort import nip, torque\n",
                    "from module.blah.blort import *\n",
                    "[1]\n", "[]\n",
                    "[2,]\n",
                    "[1,2,3,4]\n",
                    "[x, y] = [0.2, 0.999]\n",
                    "[x + 2 for x in range(10)]\n",
                    "[x + 3 for x in 1,2,3]\n",
                    "[x + 3 for x in 1,2,3 if x % 2 == 0]\n",
                    "{99 : quip,}\n",
                    "`123`\n", "`1,2,3`\n",
                    "x = 1\nwhile x < 10:\n x+= 1\n\n",
                    "x = 1\nwhile x < 10:\n x+= 1\nelse:\n print x\n\n",
                    "def x():\n for y in range(10):\n  yield y\n\n",
                    "yield 23\n",
                    "yield\n",
                    "x = yield 23\n",
                    "23 if x > 99 else 32\n",
                    "try:\n 23\nexcept:\n 45\n\n",
                    "try:\n 23\nfinally:\n 45\n\n",
                    "try:\n 23\nexcept:\n 45\nfinally:\n 67\n\n",
                    "try:\n 4928\nexcept StupidError:\n print 'you stupid'\n"\
                    "else:\n 99\n\n",
                    "try:\n 4928\nexcept StuErr, s:\n print 'you stupid'\n"\
                    "except:\n bad_things_happened()\nelse:\n 99\n\n",
                    "def f (**b):\n def g ():\n  return b\n return a, b\n\n",
                    "def z (a):\n return lambda b : (a,b)\n\n",
                    ]
    return locals()

# ______________________________________________________________________

def test ():
    test_env = build_test_environment()
    dotest = test_env["dotest"]
    for test_str in test_env["test_strings"]:
        dotest(test_str)

# ______________________________________________________________________
# Main routine

def main (*args):
    """main()
    """
    import os, tokenize, MyRealParser, pprint, ASTUtils, _ast
    if len(args) > 0:
        ast_to_tuple = ASTUtils.mk_ast_to_tuple(AST)
        pyast_to_tuple = ASTUtils.mk_pyast_to_tuple(globals())
        for file_name in args:
            tokenizer = tokenize.generate_tokens(open(file_name).readline)
            parser = MyRealParser.MyRealParser(tokenizer)
            parse_tree = parser()
            handler = MyHandler()
            pprint.pprint(parse_tree)
            ast = handler.handle_node(parse_tree)
            ast_tuple = ast_to_tuple(ast)
            pprint.pprint(ast_to_tuple(ast))
            if os.path.splitext(file_name)[1] == ".py":
                pyast = compile(open(file_name).read(), file_name, 'exec',
                                _ast.PyCF_ONLY_AST)
                pyast_tuple = pyast_to_tuple(pyast)
                pprint.pprint(pyast_tuple)
                assert ast_tuple == pyast_tuple
    else:
        test()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of myfront_transformer.py
