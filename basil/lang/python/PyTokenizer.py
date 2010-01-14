#! /usr/bin/env python
# ______________________________________________________________________
"""Module PyTokenizer

Another Python tokenizer, but implemented without using the regex module.
(This is more folly than anything else, please use tokenize in the standard
library, or at least my wrapper class, StdTokenizer.)

$Id: PyTokenizer.py,v 1.1 2003/07/23 19:52:55 jriehl Exp $
"""
# ______________________________________________________________________

from basil.lang.python import pytokenize, TokenUtils

# ______________________________________________________________________

class PyTokenizer (TokenUtils.Tokenizer):
    pass

# ______________________________________________________________________

pyTokenizerFactory = TokenUtils.TokenizerFactory(PyTokenizer,
                                                 TokenUtils.operationMap)

# ______________________________________________________________________

def main ():
    """main()
    Tokenize an input file or stdin, if no file given in script arguments.
    """
    TokenUtils.testTokenizer(PyTokenizer)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of PyTokenizer.py
