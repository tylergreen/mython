#! /usr/bin/env python
# ______________________________________________________________________
"""Module trampoline.py

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import re
import token

# ______________________________________________________________________
# Compatibility layer

if "next" not in __builtins__.keys():
    def next (obj):
        return obj.next()

# ______________________________________________________________________
# Function definitions

class TokenStream (object):
    def __init__ (self, tokenizer):
        self.tokenizer = tokenizer
        self.next_token = None

    def tokenize (self):
        return next(self.tokenizer)

    def get_token (self):
        ret_val = None
        if self.next_token is None:
            ret_val = self.tokenize()
        else:
            ret_val = self.next_token
            self.next_token = None
        return ret_val

    def get_lookahead (self):
        ret_val = None
        if self.next_token is None:
            ret_val = self.tokenize()
            self.next_token = ret_val
        else:
            ret_val = self.next_token
        return ret_val

    def test_lookahead (self, *tokens):
        ret_val = False
        lookahead = self.get_lookahead()
        if (lookahead[0] in tokens):
            ret_val = True
        elif lookahead[1] in tokens:
            ret_val = True
        return ret_val

    def expect (self, token):
        crnt_token = self.get_token()
        if (crnt_token[0] != token) and (crnt_token[1] != token):
            raise SyntaxError("Got %s, expected %s." % (str(crnt_token),
                                                        str(token)))
        return crnt_token

# ______________________________________________________________________

class ExclusiveTokenStream (TokenStream):
    def __init__ (self, tokenizer, exclusion_set):
        TokenStream.__init__(self, tokenizer)
        self.excludes = exclusion_set

    def tokenize (self):
        ret_val = next(self.tokenizer)
        while ret_val[0] in self.excludes:
            ret_val = next(self.tokenizer)
        return ret_val

# ______________________________________________________________________

class TreeBuilder (object):
    def __init__ (self):
        self.tree = ('start', [])
        self.stack = [self.tree]

    def push (self, elem):
        node = (elem, [])
        self.stack[-1][1].append(node)
        self.stack.append(node)
        return node

    def pop (self):
        return self.stack.pop()

    def pushpop (self, elem):
        node = (elem, [])
        self.stack[-1][1].append(node)
        return node

# ______________________________________________________________________

def trampoline_parse (handlers, instream, outtree):
    generator_stack = [handlers['start'](instream, outtree)]
    while generator_stack:
        try:
            next_gen = next(generator_stack[-1])
            generator_stack.append(handlers[next_gen](instream, outtree))
        except StopIteration:
            del generator_stack[-1]
    return outtree

# ______________________________________________________________________

def pgen_grammar_to_handlers (grammar, handlers):
    dfas, labels, start, accel = grammar
    label_map = {}
    i = 0
    for label in labels:
        label_map[label] = i
        i += 1
    # Note that the old version of classify() (see
    # basil.lang.python.DFAParser) was very inefficient, doing a
    # linear search through the grammar labels.  Using a dictionary
    # should be faster.
    def classify (intoken):
        tok_type, tok_name, tok_start, tok_stop, tok_line = intoken
        if (tok_type == token.NAME) and ((tok_type, tok_name) in label_map):
            return label_map[(tok_type, tok_name)]
        return label_map.get((tok_type, None), -1)
    # TODO: Check for and add accelerators...
    assert accel
    for dfa in dfas:
        handler = dfa_to_handler(classify, dfa, labels)
        handlers[dfa[0]] = handler
        handlers[dfa[1]] = handler
    return handlers

# ______________________________________________________________________

def dfa_to_handler (classify, dfa, symbol_tab = None):
    dfa_num, dfa_name, dfa_initial, states = (dfa[0], dfa[1], dfa[2], dfa[3])
    def _parse_dfa (instream, outtree):
        if __debug__:
            print("Parse:%s" % dfa_name)
        outtree.push(dfa_name)
        state = states[dfa_initial]
        while 1:
            arcs, (accel_upper, accel_lower, accel_table), accept = state
            crnt_token = instream.get_lookahead()
            ilabel = classify(crnt_token)
            if __debug__:
                symbol_str = ""
                if symbol_tab:
                    symbol_str = " %r" % (symbol_tab[ilabel],)
                print("%r %r%s %r" % (crnt_token, ilabel, symbol_str,
                                      ilabel-accel_lower))
            if (accel_lower <= ilabel) and (ilabel < accel_upper):
                accel_result = accel_table[ilabel - accel_lower]
                if -1 != accel_result:
                    if (accel_result & (1<<7)):
                        # PUSH
                        nt = (accel_result >> 8) + token.NT_OFFSET
                        if __debug__:
                            print("PUSH %d" % nt)
                        yield nt
                        state = states[accel_result & ((1<<7) - 1)]
                    else:
                        # SHIFT
                        if __debug__:
                            print("SHIFT %r" % (crnt_token,))
                        outtree.pushpop(instream.get_token())
                        state = states[accel_result]
                        if state[2] and len(state[0]) == 1:
                            break
                    continue
            if accept:
                break
            else:
                # TODO: Make the error string more instructive, like
                # the older DFAParser stuff did.
                if __debug__:
                    label_index = accel_lower
                    for accel_result in accel_table:
                        if accel_result != -1:
                            symbol_str = ""
                            if symbol_tab:
                                symbol_str = " %r" % (symbol_tab[label_index],)
                            print("%r%s => %d" % (label_index, symbol_str,
                                                  accel_result))
                        label_index += 1
                    print("len(%r) = %d" % (accel_table, len(accel_table)))
                raise SyntaxError("Unexpected %s" % str(crnt_token))
        if __debug__:
            print("POP %s" % dfa_name)
        outtree.pop()
        return
    return _parse_dfa

# ______________________________________________________________________

def test_pgen_bits (pprint_tree = False):
    # Parse the MyFront grammar, create a set of automata for it (like
    # pgen does), and then convert the automata to generators for the
    # treepoline.
    from basil.parsing import PgenParser, PyPgen
    import basil.lang.python
    g_st = PgenParser.parseFile(basil.lang.python.__path__[0] +
                                '/python26/Grammar')
    g_obj = PyPgen.buildParser(g_st)
    g_tup0 = g_obj.toTuple()
    from basil.lang.python import DFAParser, TokenUtils
    g_tup1 = DFAParser.addAccelerators(g_tup0)
    handlers = pgen_grammar_to_handlers(g_tup1, {})
    # ____________________________________________________________
    # Override the start special nonterminal to just do what it is
    # supposed to:
    def parse_start (instream, outtree):
        yield 'file_input'
    handlers['start'] = parse_start
    # ____________________________________________________________
    # Build a tokenizer that ignores COMMENT and NL tokens, while
    # properly converting OP tokens.
    import tokenize
    class MyFrontTokenStream (TokenStream):
        def tokenize (self):
            ret_val = next(self.tokenizer)
            while ret_val[0] in (tokenize.NL, tokenize.COMMENT):
                ret_val = next(self.tokenizer)
            if ((ret_val[0] == tokenize.OP) and
                (ret_val[1] in TokenUtils.operatorMap)):
                # This is a workaround for using the Python tokenize module.
                _, tok_str, tok_start, tok_end, tok_ln = ret_val
                tok_type = TokenUtils.operatorMap[tok_str]
                ret_val = (tok_type, tok_str, tok_start, tok_end, tok_ln)
            return ret_val
    # ____________________________________________________________
    # Now tokenize and parse myself.
    token_stream = MyFrontTokenStream(
        tokenize.generate_tokens(open("trampoline.py").readline))
    tb = trampoline_parse(handlers, token_stream, TreeBuilder())
    if pprint_tree:
        import pprint
        pprint.pprint(tb.tree)
    return tb

# ______________________________________________________________________

class MythonReadliner (object):
    def __init__ (self, readline):
        self.readline = readline
        self.last_line_count = 0
        self.stored_line = None
        self.empty_line_pattern = re.compile("\\A\\s*\\Z")
        self.ws_pattern = re.compile("\\A(\\s)+")

    def __call__ (self):
        # TODO Note that the read readline function takes an optional
        # size argument.  This should ideally be modified to be 100%
        # readline compatible.
        ret_val = "\n"
        if self.last_line_count > 0:
            assert self.stored_line != None
            self.last_line_count -= 1
            if self.last_line_count == 0:
                ret_val = self.stored_line
                self.stored_line = None
        elif self.stored_line != None:
            # This handles EOF in the presence of an empty quote
            # block.
            ret_val = self.stored_line
        else:
            ret_val = self.readline()
        return ret_val

    def scan_quote_block (self):
        ret_val = []
        crnt_line = self.readline()
        while ((crnt_line != '') and
               (self.empty_line_pattern.match(crnt_line) != None)):
            ret_val.append(crnt_line)
            crnt_line = self.readline()
        if crnt_line != '':
            match_obj = self.ws_pattern.match(crnt_line)
            indent_whitespace = match_obj.groups(1)
            # XXX It seems easier to read this code if we check for a
            # proper indentation level here instead of in the caller.
            while crnt_line.startswith(indent_whitespace):
                ret_val.append(crnt_line)
                crnt_line = self.readline()
                while ((crnt_line != '') and
                       (self.empty_line_pattern.match(crnt_line) != None)):
                    ret_val.append(crnt_line)
                    crnt_line = self.readline()
        self.last_line_count = len(ret_val)
        self.stored_line = crnt_line
        return ret_val

# ______________________________________________________________________

class MythonTokenStream (TokenStream):
    def __init__ (self, tokenizer, readliner):
        TokenStream.__init__(self, tokenizer)
        self.readliner = readliner

    def scan_quote_block (self):
        # Assume the token stream just generated a valid NEWLINE
        # token, hijack the readliner.
        return "".join(self.readliner.scan_quote_block())

    def tokenize (self):
        from basil.lang.python import TokenUtils
        ret_val = next(self.tokenizer)
        while ret_val[0] in (NL, COMMENT):
            ret_val = next(self.tokenizer)
        if (ret_val[0] == OP) and (ret_val[1] in TokenUtils.operatorMap):
            # This is a workaround for using the Python tokenize module.
            _, tok_str, tok_start, tok_end, tok_ln = ret_val
            tok_type = TokenUtils.operatorMap[tok_str]
            ret_val = (tok_type, tok_str, tok_start, tok_end, tok_ln)
        return ret_val

# ______________________________________________________________________

def scan_mython_file (file_obj):
    ret_val = []
    readliner = MythonReadliner(file_obj.readline)
    tokenizer = generate_tokens(readliner)
    token_stream = MythonTokenStream(tokenizer, readliner)
    crnt_token = token_stream.get_token()
    ret_val.append(crnt_token)
    while crnt_token[0] != ENDMARKER:
        if crnt_token[:2] == (NAME, 'quote'):
            # TODO: Actually scan to the newline and see if we're in
            # an indented quote and if we're not.  (This seems to work
            # on the tests in the Basil repos, tho.)
            ret_val.append((token_stream.scan_quote_block(),))
        crnt_token = token_stream.get_token()
        ret_val.append(crnt_token)
    return ret_val

# ______________________________________________________________________
# End of trampoline.py
