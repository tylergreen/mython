#! /usr/bin/env python
# ______________________________________________________________________
"""Module StdTokenizer

Implements the StdTokenizer class, which serves as a wrapper for Ping's
tokenizer in the Python distribution.

$Id: StdTokenizer.py,v 1.2 2003/07/23 19:52:55 jriehl Exp $
"""
# ______________________________________________________________________

import tokenize
from basil.lang.python import TokenUtils

# ______________________________________________________________________

class StdTokenizer (TokenUtils.AbstractTokenizer):
    """Class StdTokenizer
    Wrapper class (along with maintaining state and whatnot) for the
    Python tokenizer in the standard library.

    This is targetted as being an acceptable tokenizer for the DFAParser,
    and therefore is a callable object that returns tuples containing
    the following token information: (type, name, lineno)
    Note that some information is lost, as the token generator returns
    more information than the parser needs (XXX should this change?)
    """
    # ____________________________________________________________
    def __init__ (self, filename = None, linereader = None):
        """StdTokenizer.__init__()
        Args:
        self - Object instance
        linereader - Callable readline()-compatible object that can be passed
        directly to the generate_tokens() function.
        """
        TokenUtils.AbstractTokenizer.__init__(self, tokenize, filename,
                                              linereader)

# ______________________________________________________________________

stdTokenizerFactory = TokenUtils.TokenizerFactory(StdTokenizer,
                                                  TokenUtils.operatorMap)

# ______________________________________________________________________

def main ():
    """main()
    Run a silly little test on the tokenizer class.
    """
    testTokenizer(StdTokenizer)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of StdTokenizer.py
