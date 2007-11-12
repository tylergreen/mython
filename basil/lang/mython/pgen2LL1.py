#! /usr/bin/env python
# ______________________________________________________________________
"""Script pgen2LL1.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import sys, getopt, pprint, token, string
from basil.common.python import PgenParser, PyPgen

# ______________________________________________________________________

def simplify_tree (tree):
    tree_data, tree_children = tree
    tree_children_1 = [simplify_tree(child) for child in tree_children]
    if len(tree_children) == 1:
        ret_val = tree_children_1[0]
    else:
        ret_val = (tree_data, tree_children_1)
    return ret_val

# ______________________________________________________________________

def flatten_pt (pt):
    ret_val = []
    pt_sym, children = pt
    if type(pt_sym) == tuple:
        ret_val.append(pt_sym)
    else:
        for child in children:
            ret_val += flatten_pt(child)
    return ret_val

# ______________________________________________________________________

def pt_to_keywords (pt):
    ret_val = set()
    pt_sym, children = pt
    if (pt_sym == PgenParser.ATOM) and (len(children) == 1):
        symbol_text = children[0][0][1]
        if symbol_text[0] == "'":
            symbol_string = symbol_text[1:-1]
            if symbol_string[0] in string.ascii_letters:
                ret_val.add(symbol_string)
    else:
        for child in children:
            ret_val = ret_val.union(pt_to_keywords(child))
    return ret_val

# ______________________________________________________________________

def pt_to_code (pt, rule_first_sets):
    pt_sym, children = pt
    if pt_sym == PgenParser.RHS:
        if len(children) == 1:
            ret_val = pt_to_code(children[0], rule_first_sets)
        else:
            ret_val = []
            child_data = [(child_pt, pt_to_first_set(child_pt,
                                                     rule_first_sets))
                          for child_pt in children
                          if type(child_pt[0]) != tuple]
            child_dispatch = {}
            warned = False
            for child_pt, child_firsts in child_data:
                has_none = False
                for start_symbol in child_firsts:
                    if start_symbol is None:
                        flat_pt = flatten_pt(child_pt)
                        line_no = flat_pt[0][2]
                        unparsed_rhs = " ".join([tok[1] for tok in flat_pt])
                        print ("Warning (line %d): None in first set for: %s" %
                               (line_no, unparsed_rhs))
                        has_none = True
                    elif child_dispatch.has_key(start_symbol) and not warned:
                        flat_pt = flatten_pt(pt)
                        line_no = flat_pt[0][2]
                        unparsed_rhs = " ".join([tok[1] for tok in flat_pt])
                        print ("Warning (line %d): Grammar is ambiguous: %s" %
                               (line_no, unparsed_rhs))
                        warned = True
                    else:
                        child_dispatch[start_symbol] = child_pt
                if has_none:
                    child_firsts.remove(None)
            # TODO: Consider either using the dispatch or sorting on
            # first set size.
            ret_val.append("if self.test_lookahead(%s):" %
                           ", ".join(child_data[0][1]))
            ret_val.append(pt_to_code(child_data[0][0], rule_first_sets))
            for child_pt, child_firsts in child_data[1:-1]:
                ret_val.append("elif self.test_lookahead(%s):" %
                               ", ".join(child_firsts))
                ret_val.append(pt_to_code(child_pt, rule_first_sets))
            ret_val.append("else:")
            ret_val.append(pt_to_code(child_data[-1][0], rule_first_sets))
    elif pt_sym == PgenParser.ALT:
        ret_val = pt_to_code(children[0], rule_first_sets)
        for child in children[1:]:
            ret_val += pt_to_code(child, rule_first_sets)
    elif pt_sym == PgenParser.ITEM:
        if len(children) == 3:
            assert children[0][0][0] == token.LSQB
            ret_val = ["if self.test_lookahead(%s):" %
                       ", ".join(pt_to_first_set(children[1],
                                                rule_first_sets))]
            ret_val.append(pt_to_code(children[1], rule_first_sets))
        else:
            child_code = pt_to_code(children[0], rule_first_sets)
            if len(children) == 2:
                # FIXME: Detect ambiguity in the grammar here.  There
                # are cases where the follows set is not mutually
                # exclusive with the first set of the recursive term.
                # Example:
                # arglist: (argument ',')* (argument [',']|
                #                           '*' test [',' '**' test] |
                #                           '**' test)
                # This must be refactored to avoid the while loop.
                test_code = ("while self.test_lookahead(%s):" %
                             ", ".join(pt_to_first_set(children[0],
                                                      rule_first_sets)))
                if children[1][0][0] == token.STAR:
                    ret_val = [test_code, child_code]
                else:
                    assert children[1][0][0] == token.PLUS
                    ret_val = child_code + [test_code, child_code]
            else:
                ret_val = child_code
    elif pt_sym == PgenParser.ATOM:
        if len(children) == 1:
            symbol_text = children[0][0][1]
            if rule_first_sets.has_key(symbol_text):
                ret_val = ["self.parse_%s()" % symbol_text]
            else:
                ret_val = ["self.expect(%s)" % symbol_text]
        else:
            assert len(children) == 3 and children[0][0][0] == token.LPAR
            ret_val = pt_to_code(children[1], rule_first_sets)
    return ret_val

# ______________________________________________________________________

def pt_to_first_set (pt, rule_first_sets = None):
    pt_sym, children = pt
    if pt_sym == PgenParser.RHS:
        ret_val = pt_to_first_set(children[0], rule_first_sets)
        index = 2
        while index < len(children):
            assert children[index - 1][0][0] == token.VBAR
            ret_val = ret_val.union(pt_to_first_set(children[index],
                                                    rule_first_sets))
            index += 2
    elif pt_sym == PgenParser.ALT:
        ret_val = pt_to_first_set(children[0], rule_first_sets)
        index = 1
        while (None in ret_val) and (index < len(children)):
            ret_val.remove(None)
            ret_val = ret_val.union(pt_to_first_set(children[index],
                                                    rule_first_sets))
            index += 1
    elif pt_sym == PgenParser.ITEM:
        if type(children[0][0]) == tuple:
            assert children[0][0][0] == token.LSQB
            ret_val = pt_to_first_set(children[1],
                                      rule_first_sets).union([None])
        else:
            ret_val = pt_to_first_set(children[0], rule_first_sets)
            if len(children) == 2:
                if children[1][0][0] == token.STAR:
                    ret_val = ret_val.union([None])
                else:
                    assert children[1][0][0] == token.PLUS
            else:
                assert len(children) == 1
    elif pt_sym == PgenParser.ATOM:
        if len(children) == 1:
            symbol_text = children[0][0][1]
            if ((rule_first_sets is not None) and
                (rule_first_sets.has_key(symbol_text))):
                ret_val = rule_first_sets[symbol_text]
            else:
                ret_val = set([symbol_text])
        else:
            assert len(children) == 3 and children[0][0][0] == token.LPAR
            ret_val = pt_to_first_set(children[1], rule_first_sets)
    return ret_val

# ______________________________________________________________________

def build_first_sets (rules):
    first_sets = {}
    for rule_name in rules.keys():
        first_sets[rule_name] = pt_to_first_set(rules[rule_name])
    changed = True
    work_list = rules.keys()
    while changed and work_list:
        changed = False
        next_list = []
        for rule_name in work_list:
            first_set = first_sets[rule_name]
            deps = [set_symbol for set_symbol in first_set
                    if set_symbol[0] != "'" and first_sets.has_key(set_symbol)]
            if deps:
                to_replace = [set_symbol for set_symbol in deps
                              if set_symbol not in work_list]
                if to_replace:
                    changed = True
                    for set_symbol in to_replace:
                        first_set.remove(set_symbol)
                        first_set = first_set.union(first_sets[set_symbol])
                    first_sets[rule_name] = first_set
                if len(to_replace) < len(deps):
                    next_list.append(rule_name)
        if len(next_list) < len(work_list):
            changed = True
        work_list = next_list
    return first_sets

# ______________________________________________________________________

def process_rules (pgenCPT):
    rulePTs = [child for child in pgenCPT[1] if child[0] == PgenParser.RULE]
    rules = {}
    for rule_symbol, rule_children in rulePTs:
        rule_name, colon, rule_rhs, newline = rule_children
        rule_name_str = rule_name[0][1]
        rules[rule_name_str] = rule_rhs
    return rules

# ______________________________________________________________________

def make_methods (rules, rule_first_sets):
    ret_val = {}
    for rule_name in rules.keys():
        if rule_name == "_IGNORE":
            tok_list = [tok[1] for tok in flatten_pt(rules[rule_name])]
            ret_val["tokenize"] = (["ret_val = self.tokenizer.next()",
                                    "while ret_val[0] in (%s):" %
                                    ", ".join(tok_list),
                                    ["ret_val = self.tokenizer.next()"],
                                    "return ret_val"])
        else:
            ret_val["parse_%s" % rule_name] = (["self.push('%s')" % rule_name]
                                               + pt_to_code(rules[rule_name],
                                                            rule_first_sets) +
                                               ["return self.pop()"])
    return ret_val

# ______________________________________________________________________

def make_class (methods, klass = None, start = None, keywords = None):
    if klass is None:
        klass = "MyParser"
    ret_val = ["#! /usr/bin/env python",
               "from tokenize import *", # FIXME: this is a hack, pending
                                         # better lexical abstraction
                                         # (currently assuming a Python
                                         # lexer).
               "from LL1Parser import LL1Parser, parser_main",
               "",
               "class %s (LL1Parser):" % klass]
    if keywords is not None:
        ret_val.append(["def __init__ (self, *args, **kws):",
                        ["LL1Parser.__init__(self, *args, **kws)",
                         "self.keywords = %s" % str(keywords)], ""])
    method_names = methods.keys()
    if "parse_start" in method_names:
        start_method = None
    elif start is None:
        start_method = method_names[0]
    else:
        start_method = "parse_%s" % start
    method_names.sort()
    for method_name in method_names:
        ret_val.append(["def %s (self):" % method_name,
                        methods[method_name], ""])
        if method_name == start_method:
            ret_val.append(["parse_start = %s" % method_name, ""])
    ret_val += ["",
                "if __name__ == '__main__':",
                ["parser_main(%s)" % klass],
                "", ""]
    return ret_val

# ______________________________________________________________________

def gen_code_lines (code_list, level = 0, indent = "    "):
    code_lines = []
    for code_elem in code_list:
        if type(code_elem) == list:
            code_lines += gen_code_lines(code_elem, level + 1, indent)
        elif code_elem != "":
            code_lines.append("%s%s" % (level * indent, code_elem))
        else:
            code_lines.append("")
    return code_lines

# ______________________________________________________________________
# Stuff

class PgenFrontEnd (object):
    """Class for parsing arguments and hold them for later processing."""
    # ____________________________________________________________
    def __init__ (self):
        self.infile = sys.stdin
        self.infilename = "<stdin>"
        self.outfile = sys.stdout
        self.outfilename = "<stdout>"
        self.klass_name = None
        self.quiet = False
        self.start = None
        self.cpt = None
        self.args = []
    # ____________________________________________________________
    def handle_args (self, *args):
        opts, args = getopt.getopt(args, "c:i:o:qs:")
        for opt_key, opt_val in opts:
            if opt_key == "-c":
                self.klass_name = opt_val
            elif opt_key == "-i":
                self.infilename = opt_val
                self.infile = open(self.infilename)
            elif opt_key == "-o":
                self.outfilename = opt_val
                self.outfile = open(self.outfilename, "w")
            elif opt_key == "-q":
                self.quiet = True
            elif opt_key == "-s":
                self.start = opt_val
        self.args = args
    # ____________________________________________________________
    def get_concrete_parse (self, close_file = True):
        ret_val = None
        try:
            ret_val = PgenParser.parseString(self.infile.read())
            self.cpt = ret_val
        finally:
            if close_file:
                self.infile.close()
        return ret_val
    # ____________________________________________________________
    def output_text (self, text, close_file = True):
        try:
            self.outfile.write(text)
        finally:
            self.outfile.close()

# ______________________________________________________________________
# Main routine definition

def main (*args):
    """main()
    """
    fe = PgenFrontEnd()
    fe.handle_args(*args)
    pgenCPT = fe.get_concrete_parse()
    assert pgenCPT[0] == PgenParser.MSTART
    if __debug__ and not fe.quiet:
        pprint.pprint(pgenCPT)
    rules = process_rules(pgenCPT)
    if __debug__ and not fe.quiet:
        print "_" * 70
        pprint.pprint(rules)
    rule_first_sets = build_first_sets(rules)
    if __debug__ and not fe.quiet:
        print "_" * 70
        pprint.pprint(rule_first_sets)
    if fe.start is None:
        first_rule = pgenCPT[1][0]
        assert first_rule[0] == PgenParser.RULE
        first_rule_name = first_rule[1][0][0]
        assert first_rule_name[0] == token.NAME
        fe.start = first_rule_name[1]
    # Now create a class that specializes LL1Parser and creates parse
    # methods for the various symbols
    methods = make_methods(rules, rule_first_sets)
    keywords = pt_to_keywords(pgenCPT)
    klass = make_class(methods, fe.klass_name, fe.start, keywords)
    code_lines = gen_code_lines(klass)
    fe.output_text("\n".join(code_lines))

# ______________________________________________________________________

if __name__ == "__main__":
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of pgen2LL1.py
