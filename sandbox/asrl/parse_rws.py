#!/usr/bin/env python
# ______________________________________________________________________
"""Script parse_rws.py

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

import os
import tokenize
import StringIO
from asrlir import ASRL
from basil.lang.mython import LL1Parser

# ______________________________________________________________________
# Debugging flags and other garbage...

__DEBUG__ = False

if __DEBUG__:
    import pprint

# ______________________________________________________________________
# Class definitions

class ListParserMixin (object):
    @staticmethod
    def mk_parse_delimited_list (nt, start, end, parse_fn):
        def _parse_list (self):
            ret_val = self.push(nt)
            self.expect(start)
            lookahead = self.get_lookahead()
            if lookahead[1] != end:
                parse_fn(self)
                lookahead = self.get_lookahead()
                while lookahead[1] != end:
                    self.expect(",")
                    parse_fn(self)
                    lookahead = self.get_lookahead()
            self.expect(end)
            self.pop()
            return ret_val
        return _parse_list

# ______________________________________________________________________

class ASRLParser (LL1Parser.LL1Parser, ListParserMixin):
    # ____________________________________________________________
    def __init__ (self, tokenizer, filename = None, env = None):
        LL1Parser.LL1Parser.__init__(self, tokenizer, filename)
        self.crnt_asdl_spec = None
        self.crnt_unit = None
        self.environment = env

    # ____________________________________________________________
    def tokenize (self):
        """Overloads LL1Parser.tokenize() in order to throw out whitespace."""
        ret_val = self.tokenizer.next()
        while ret_val[0] in (tokenize.INDENT, tokenize.DEDENT,
                             tokenize.NEWLINE, tokenize.NL):
            ret_val = self.tokenizer.next()
        return ret_val

    # ____________________________________________________________
    def parse_start (self):
        ret_val = []
        lookahead = self.get_lookahead()
        crnt_unit = None
        while lookahead[0] != tokenize.ENDMARKER:
            if lookahead[0] == tokenize.COMMENT:
                comment_result = self.parse_asdl_spec()
                if comment_result is not None:
                    crnt_unit = comment_result
                    ret_val.append(crnt_unit)
            else:
                assert crnt_unit is not None, "Need syntax specification!"
                rw_cst = self.parse_rw()
                crnt_unit.rws.append(self.cst_to_ast(rw_cst, self.environment))
            lookahead = self.get_lookahead()
        return ret_val

    # ____________________________________________________________
    def parse_asdl_spec (self):
        ret_val = None
        tok_ty, tok_str, _, _, _ = self.get_token()
        assert tok_ty == tokenize.COMMENT
        if tok_str.startswith("#syntax"):
            i0 = tok_str.find('"')
            i1 = tok_str.rfind('"')
            assert i0 < i1, ("Missing or malformed file name given in #syntax "
                             "declaration.")
            filename = tok_str[i0 + 1:i1]
            assert os.path.isfile(filename), ("Could not find syntax file, "
                                              "'%s'." % filename)
            self.crnt_asdl_spec = filename
            ret_val = ASRL.Unit(filename, [])
        return ret_val

    # ____________________________________________________________
    def parse_rw (self):
        ret_val = self.push("rw")
        self.expect(tokenize.NAME)
        self.expect(":")
        self.parse_rwexp()
        self.expect("-")
        self.expect(">")
        self.parse_rwexp()
        lookahead = self.get_lookahead()
        if lookahead[1] == "where":
            self.parse_where_clause()
        assert self.pop() == ret_val
        return ret_val

    # ____________________________________________________________
    def parse_rwexp (self):
        ret_val = None
        lookahead_ty, lookahead_str, _, _, _ = self.get_lookahead()
        if lookahead_ty == tokenize.NAME:
            self.push("rwexp")
            self.expect(tokenize.NAME)
            lookahead = self.get_lookahead()
            if lookahead[1] == "(":
                self.parse_args()
            ret_val = self.pop()
        elif lookahead_str == "[":
            ret_val = self.parse_list()
        elif lookahead_str == "(":
            ret_val = self.parse_tuple_or_paren()
        elif lookahead_str == ".":
            ret_val = self.parse_dots()
        else:
            # XXX Do some sanity checking...
            self.push("const")
            self.push(self.get_token())
            self.pop()
            ret_val = self.pop()
        return ret_val

    # ____________________________________________________________
    parse_list = ListParserMixin.mk_parse_delimited_list("list", "[", "]",
                                                         parse_rwexp)

    # ____________________________________________________________
    parse_args = ListParserMixin.mk_parse_delimited_list("args", "(", ")",
                                                         parse_rwexp)

    # ____________________________________________________________
    def parse_tuple_or_paren (self):
        ret_val = self.push("tuple")
        self.expect("(")
        lookahead = self.get_lookahead()
        if lookahead[1] != ")":
            self.parse_rwexp()
            lookahead = self.get_lookahead()
            if lookahead[1] == ")":
                ret_val = self.stack[-1][1][0]
            else:
                self.expect(",")
                lookahead = self.get_lookahead()
                while lookahead[1] != ")":
                    self.parse_rwexp()
                    lookahead = self.get_lookahead()
                    if lookahead[1] != ")":
                        self.expect(",")
        self.expect(")")
        self.pop()
        return ret_val

    # ____________________________________________________________
    def parse_dots (self):
        ret_val = self.push("dots")
        self.expect(".")
        self.expect(".")
        self.expect(".")
        self.pop()
        return ret_val

    # ____________________________________________________________
    def parse_where_clause (self):
        ret_val = self.push("where_clause")
        starts_at = self.expect("where")
        self.expect("{")
        nesting_level = 0
        lookahead = self.get_lookahead()
        while (nesting_level > 1) or (lookahead[1] != "}"):
            if lookahead[1] == "{":
                nesting_level += 1
            elif lookahead[1] == "}":
                nesting_level -= 1
            elif lookahead[0] == tokenize.ENDMARKER:
                raise SyntaxError("Unterminated where clause on line %d." %
                                  starts_at[0][2][1])
            self.push(self.get_token())
            self.pop()
            lookahead = self.get_lookahead()
        self.expect("}")
        assert ret_val == self.pop()
        return ret_val

    # ____________________________________________________________
    @staticmethod
    def cst_to_ast (cst, environment = None):
        if environment is None:
            environment = {}
        # __________________________________________________
        def _get_where_clause (cst):
            # XXX This hacked version might cause errors.  Should at least
            # reinject whitespace.
            nt, children = cst
            tok_strs = [tok[0][1] for tok in children[2:-1]]
            return "".join(tok_strs)
        # __________________________________________________
        ret_val = None
        nt, children = cst
        if nt == "rw":
            environment["$DOTS_COUNT"] = 0
            match_exp = ASRLParser.cst_to_ast(children[2], environment)
            environment["$DOTS_COUNT"] = 0
            build_exp = ASRLParser.cst_to_ast(children[5], environment)
            del environment["$DOTS_COUNT"]
            where_clause = (None if len(children) < 7
                            else _get_where_clause(children[6]))
            ret_val = ASRL.Rewrite(children[0][0][1], match_exp, build_exp,
                                   where_clause)
        elif nt == "rwexp":
            if len(children) > 1:
                arg_list = [ASRLParser.cst_to_ast(grandchild, environment)
                            for grandchild in children[1][1]
                            if type(grandchild[0]) != tuple]
                ret_val = ASRL.Constructor(children[0][0][1], arg_list)
            else:
                var_id = children[0][0][1]
                if var_id in environment:
                    ret_val = environment[var_id]
                else:
                    ret_val = ASRL.Var(children[0][0][1])
        elif nt == "list":
            list_args = [ASRLParser.cst_to_ast(child, environment)
                         for child in children
                         if type(child[0]) != tuple]
            ret_val = ASRL.List(list_args)
        elif nt == "tuple":
            tup_args = [ASRLParser.cst_to_ast(child, environment)
                        for child in children
                        if type(child[0]) != tuple]
            ret_val = ASRL.Tuple(tup_args)
        elif nt == "const":
            ret_val = ASRL.Const(eval(children[0][0][1]))
        elif nt == "dots":
            if "$DOTS_COUNT" in environment:
                dots_count = environment["$DOTS_COUNT"]
                environment["$DOTS_COUNT"] = dots_count + 1
            else:
                dots_count = 0
            ret_val = ASRL.Dots(dots_count)
        else:
            raise NotImplementedError("Not able to handle %s nonterminal!" %
                                      str(nt))
        return ret_val

    # ____________________________________________________________
    @staticmethod
    def parse_file (filename, start_symbol = None, environment = None):
        file_obj = open(filename)
        try:
            tokenizer = tokenize.generate_tokens(file_obj.readline)
            parser = ASRLParser(tokenizer, filename, environment)
            ret_val = parser(start_symbol)
        finally:
            file_obj.close()
        return ret_val

    # ____________________________________________________________
    @staticmethod
    def parse_string (source, start_symbol = None, environment = None):
        sio_obj = StringIO.StringIO(source)
        tokenizer = tokenize.generate_tokens(sio_obj.readline)
        parser = ASRLParser(tokenizer, "<string>", environment)
        return parser(start_symbol)

# ______________________________________________________________________
# Main routine

def main (*args):
    for arg in args:
        file_obj = open(arg)
        try:
            tokenizer = tokenize.generate_tokens(file_obj.readline)
            parser = ASRLParser(tokenizer, arg)
            rw_units = parser()
            for rw_unit in rw_units:
                print '#syntax "%s"' % rw_unit.asdl_file
                print
                for rw in rw_unit.rws:
                    print rw
                    print
        finally:
            file_obj.close()

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of parse_rws.py
