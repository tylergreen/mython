#! /usr/bin/env python
# ______________________________________________________________________
"""Module mylexer

Lexical scanner for the Mython language.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import re
import tokenize

from basil.parsing.trampoline import TokenStream
from basil.lang.python import TokenUtils

# ______________________________________________________________________
# Compatibility layer 2.5/2.6

if "next" not in __builtins__.keys():
    def next (obj):
        return obj.next()

# ______________________________________________________________________
# Class definitions.

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

# ______________________________________________________________________
# Utility function(s).

def scan_mython_file (file_obj):
    """Simple Mython scanner, returns a list of tokens, given a file object."""
    ret_val = []
    readliner = MythonReadliner(file_obj.readline)
    tokenizer = tokenize.generate_tokens(readliner)
    token_stream = MythonTokenStream(tokenizer, readliner)
    crnt_token = token_stream.get_token()
    ret_val.append(crnt_token)
    while crnt_token[0] != tokenize.ENDMARKER:
        if crnt_token[:2] == (tokenize.NAME, 'quote'):
            # TODO: Actually scan to the newline and see if we're in
            # an indented quote and if we're not.
            ret_val.append((token_stream.scan_quote_block(),))
        crnt_token = token_stream.get_token()
        ret_val.append(crnt_token)
    return ret_val

# ______________________________________________________________________
# End of mylexer.py
