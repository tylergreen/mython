#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyAbstractor

I'm going to want to deprecate this in favor of a more automated transformer.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from compiler.ast import *
from compiler.consts import OP_ASSIGN, OP_DELETE, OP_APPLY

import MyRealParser
import pprint

# ______________________________________________________________________

def is_token ((cpt_id, cpt_children)):
    ret_val = False
    if type(cpt_id) == tuple:
        assert len(cpt_children) == 0, "Malformed terminal node."
        ret_val = True
    return ret_val

# ______________________________________________________________________

def simplify_tree ((cpt_id, cpt_children)):
    # Keep expr_stmt's around for discards.
    if len(cpt_children) == 1 and (cpt_id != "expr_stmt"): 
        if not is_token(cpt_children[0]):
            ret_val = simplify_tree(cpt_children[0])
        else:
            ret_val = (cpt_id, cpt_children)
    else:
        ret_val = (cpt_id, [simplify_tree(child) for child in cpt_children])
    return ret_val

# ______________________________________________________________________

def escape (obj):
    if isinstance(obj, Node):
        ret_val = Tuple((Const(obj.__class__.__name__),
                         escape(list(obj.getChildren()))))
        #ret_val = CallFunc(Name(obj.__class__.__name__),
        #                   tuple([escape(child)
        #                          for child in obj.getChildren()]))
    elif type(obj) == tuple:
        ret_val = Tuple(tuple([escape(child) for child in obj]))
    elif type(obj) == list:
        ret_val = List(tuple([escape(child) for child in obj]))
    else:
        # XXX Put some guards here?
        ret_val = Const(obj)
    return ret_val

# ______________________________________________________________________

def extract_names ((cpt_id, children)):
    ret_val = []
    if type(cpt_id) == tuple:
        if cpt_id[0] == MyRealParser.NAME:
            ret_val.append(cpt_id[1])
    else:
        for child in children:
            ret_val += extract_names(child)
    return ret_val

# ______________________________________________________________________
# Class definition

class MyAbstractor (object):
    """Class MyAbstractor

    This plays a similar function to the Transformer class in the
    compiler package: walk a concrete parse tree and create an
    abstract syntax tree.  However, it now supports parameterized
    quotation.
    """
    # ____________________________________________________________
    def __init__ (self, environment):
        """MyAbstractor.__init__()
        """
        self.environment = environment

    # ____________________________________________________________
    def get_docstring (self, (node_id, node_children)):
        """MyAbstractor.get_docstring()

        NOTE: I don't like this, but without access to an easy ASDL
        based bytecode compiler, this is needed to use the
        compiler.ast data structures.  Of course, here I am using
        strings to identify nonterminals in the concrete parse."""
        ret_val = None
        if node_id == "suite":
            if len(node_children) == 1:
                ret_val = self.get_docstring(node_children[0])
            else:
                for child in node_children:
                    if child[0] == "stmt":
                        ret_val = self.get_docstring(child)
                        break
        elif node_id == "file_input":
            for child in node_children:
                if child[0] == "stmt":
                    ret_val = self.get_docstring(child)
                    break
        elif node_id == "atom":
            if (is_token(node_children([0])) and
                node_children[0][0][0] == MyRealParser.STRING):
                ret_val = ""
                for (child_data, _) in node_children:
                    ret_val += eval(child_data[1])
        elif node_id in ("stmt", "simple_stmt", "small_stmt"):
            ret_val = self.get_docstring(node_children[0])
        elif node_id in ("expr_stmt",
                         "testlist",
                         "testlist_safe",
                         "test",
                         "or_test",
                         "and_test",
                         "not_test",
                         "comparison",
                         "expr",
                         "xor_expr",
                         "and_expr",
                         "shift_expr",
                         "arith_expr",
                         "term",
                         "factor",
                         "power") and len(node_children) == 1:
            ret_val = self.get_docstring(node_children[0])
        return ret_val

    # ____________________________________________________________
    def transform (self, tree):
        """MyAbstractor.transform()
        """
        assert tree[0] == "start" and len(tree[1]) == 1
        file_input_node = tree[1][0]
        assert file_input_node[0] == "file_input"
        node = simplify_tree(file_input_node)
        pprint.pprint(node)
        handler = getattr(self, node[0])
        return handler(node)

    # ____________________________________________________________
    def handle_node (self, node):
        handler = getattr(self, node[0])
        return handler(node)

    # ____________________________________________________________
    def file_input (self, node):
        # Thefted from Transformer more or less.
        doc = self.get_docstring(node)
        if doc is None:
            i = 0
        else:
            i = 1
        stmts = []
        for child in node[1][i:]:
            if not is_token(child):
                stmts.append(self.handle_node(child))
        return Module(doc, Stmt(stmts))

    # ____________________________________________________________
    def quotedef (self, (node_id, children)):
        # Step 0: Figure out if we need to package this directly into
        # abstract syntax.
        # XXX TODO
        name_index_opt = 1
        name_opt = None
        # Step 1: Compile and evaluate the processor.
        processor = self.environment["myfront"]
        if is_token(children[1]) and children[1][0][1] == '[':
            name_index_opt = 4
            raise NotImplementedError("FIXME")
        # Step 2: Determine the (optional) name of the object.
        if (is_token(children[name_index_opt]) and
            children[name_index_opt][0][0] == MyRealParser.NAME):
            name_opt = children[name_index_opt][0][1]
        # Step 3: Parse the quoted text and escape the abstracted result.
        env, obj = processor(self.environment, self.get_quote(children[-1]))
        self.environment = env
        if name_opt is not None:
            self.environment[name_opt] = obj
        return self.escape(name_opt, obj)

    # ____________________________________________________________
    def get_quote (self, (node_id, children)):
        """Scan a concrete parse tree for the text of the first QUOTED
        token found."""
        ret_val = None
        if type(node_id) == tuple:
            if node_id[0] == MyRealParser.QUOTED:
                ret_val = node_id[1]
        else:
            for child in children:
                ret_val = self.get_quote(child)
                if ret_val is not None:
                    break
        return ret_val

    # ____________________________________________________________
    def escape (self, name_opt, obj):
        """Translate a Python object in the current interpreter to
        abstract syntax that constructs that object."""
        # FIXME
        ret_val = escape(obj)
        if name_opt is not None:
            ret_val = Assign([AssName(name_opt, OP_ASSIGN)], ret_val)
        print ret_val
        return ret_val

    # ____________________________________________________________
    def simple_stmt (self, (_, children)):
        stmts = []
        for index in range(0, len(children), 2):
            stmts.append(self.handle_node(children[index]))
        return Stmt(stmts)

    # ____________________________________________________________
    def atom (self, (_, children)):
        assert is_token(children[0])
        ret_val = None
        token_text = children[0][0][1]
        token_line = children[0][0][2][0]
        if token_text == "(":
            if is_token(children[1]) and children[1][0][1] == ")":
                ret_val = Tuple((), lineno = token_line)
            else:
                ret_val = self.handle_node(children[1])
        elif token_text == "[":
            if is_token(children[1]) and children[1][0][1] == "]":
                ret_val = List((), lineno = token_line)
            else:
                ret_val = self.handle_node(children[1])
        elif token_text == "{":
            if is_token(children[1]) and children[1][0][1] == "}":
                ret_val = Dict((), lineno = token_line)
            else:
                ret_val = self.handle_node(children[1])
        elif token_text == "`":
            ret_val = Backquote(self.handle_node(children[1]))
        else:
            token_kind = children[0][0][0]
            if token_kind == MyRealParser.STRING:
                # XXX Ignoring encoding.
                result_string = eval(token_text)
                for child in children[1:]:
                    result_string += eval(child[0][1])
                ret_val = Const(result_string, lineno = token_line)
            elif token_kind == MyRealParser.NUMBER:
                ret_val = Const(eval(token_text), lineno = token_line)
            else:
                ret_val = Name(token_text, lineno = token_line)
        return ret_val

    # ____________________________________________________________
    def print_stmt (self, (_, children)):
        items = []
        dest = None
        start_index = 1
        if ((len(children) > 1) and (is_token(children[1])) and
            (children[1][0][1] == ">>")):
            dest = self.handle_node(children[2])
            start_index = 4
        for index in range(start_index, len(children), 2):
            items.append(self.handle_node(children[index]))
        if ((is_token(children[-1])) and (children[-1][0][1] == ",")):
            ret_val = Print(items, dest, lineno = children[0][0][2][0])
        else:
            ret_val = Printnl(items, dest, lineno = children[0][0][2][0])
        return ret_val

    # ____________________________________________________________
    def expr_stmt (self, (_, children)):
        expr_result = self.handle_node(children[-1])
        if len(children) == 1:
            ret_val = Discard(expr_result, expr_result.lineno)
        else:
            if children[1][0][1] == "=":
                nodesl = []
                for index in range(0, len(children) - 2, 2):
                    nodesl.append(self.assign_handle_node(children[index],
                                                          OP_ASSIGN))
                ret_val = Assign(nodesl, expr_result,
                                 lineno = children[1][0][2][0])
            else:
                raise NotImplementedError("FIXME")
        return ret_val

    # ____________________________________________________________
    def assign_handle_node (self, node, op_kind):
        handler = getattr(self, "assign_handle_%s" % node[0])
        return handler(node, op_kind)

    # ____________________________________________________________
    def assign_handle_atom (self, (_, children), op_kind):
        assert is_token(children[0])
        token_text = children[0][0][1]
        if token_text == "(":
            assert not is_token(children[1]), "can't assign to ()"
            ret_val = self.assign_handle_node(children[1], op_kind)
        elif token_text == "[":
            assert not is_token(children[1]), "can't assign to ()"
            ret_val = self.assign_handle_node(children[1], op_kind)
        else:
            assert token_text != "{", "can't assign to dictionaries"
            assert children[0][0][0] == MyRealParser.NAME, ("can't assign to "
                                                            "literals")
            ret_val = AssName(children[0][0][1], op_kind,
                              lineno = children[0][0][2][0])
        return ret_val

    # ____________________________________________________________
    def import_from (self, (_, children)):
        index = 1
        while is_token(children[index]) and children[index][0][1] == ".":
            index += 1
        level = index - 1
        if children[index][0] == "dotted_name":
            fromname = ".".join(extract_names(children[index]))
            index += 1
        else:
            fromname = ""
        if (is_token(children[index + 1]) and
            (children[index + 1][0][1] == "*")):
            as_names = [("*", None)]
        else:
            if is_token(children[index + 1]):
                assert children[index + 1][0][1] == "("
                as_names_node = children[index + 2]
            else:
                as_names_node = children[index + 1]
            as_names = self.handle_node(as_names_node)
        return From(fromname, as_names, level, lineno = children[0][0][2][0])

# ______________________________________________________________________
# End of MyAbstractor.py
