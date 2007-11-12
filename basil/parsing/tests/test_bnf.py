#! /usr/bin/env python
# ______________________________________________________________________
"""test_bnf - Test the Basil BNF parser.

$Id: test_bnf.py,v 1.1 2003/07/10 22:08:16 jriehl Exp $
"""
# ______________________________________________________________________

import pprint
from basil.parsing import bnf

# ______________________________________________________________________

def main ():
    text = open("test.bnf").read()
    rVal = bnf.get_prods(text)
    pprint.pprint(rVal)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of test_bnf.py
