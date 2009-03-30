#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyLangParser

Break out module for the toy language in demo.my.

Using this to determine if I've found a bug in the MyFront compiler.

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

import tokenize
import StringIO
from basil.lang.mython.LL1Parser import LL1Parser
from basil.lang.mython.mybuiltins import __myimport__

# ______________________________________________________________________
# Class definition(s)

class MyLangParser (LL1Parser):
    def parse_start (self):
        ret_val = self.push("+")
        self.parse_term()
        lookahead = self.get_lookahead()
        while lookahead[1] == "+":
            self.get_token()
            self.parse_term()
            lookahead = self.get_lookahead()
        self.pop()
        return ret_val

    def parse_term (self):
        ret_val = self.push("*")
        self.push(self.parse_number())
        self.pop()
        lookahead = self.get_lookahead()
        while lookahead[1] == "*":
            self.get_token()
            self.push(self.parse_number())
            self.pop()
            lookahead = self.get_lookahead()
        self.pop()
        return ret_val

    def parse_number (self):
        nr_tok = self.get_token()
        if nr_tok[0] != tokenize.NUMBER:
            raise SyntaxError("Line %d, expected number, got '%s'." %
                              (nr_tok[2][0], nr_tok[1]))
        return int(nr_tok[1])

    @staticmethod
    def parse_string (source, environment = None):
        if environment is None:
            environment = {}
        sio_obj = StringIO.StringIO(source)
        tokenizer = tokenize.generate_tokens(sio_obj.readline)
        filename = ("<string>" if "filename" not in environment
                    else environment["filename"])
        parser = MyLangParser(tokenizer, filename)
        return parser()

# ______________________________________________________________________
# Main (self-test) routine.

def main ():
    import pprint
    test_strings = ("1\n",
                    "2 + 3\n",
                    "4 * 5\n",
                    "6 + 7 * 8\n",
                    )
    myimport_result = __myimport__("demo")
    demo_module, _ = myimport_result
    for test_string in test_strings:
        py_pt = MyLangParser.parse_string(test_string)
        my_pt = demo_module.MyLangParser.parse_string(test_string)
        pprint.pprint((py_pt, my_pt, py_pt == my_pt))

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of MyLangParser.py
