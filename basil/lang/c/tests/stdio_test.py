#! /usr/bin/env python
# ______________________________________________________________________
"""Script stdio_test.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.lang.c import cppString, parseString

# ______________________________________________________________________
# Main routine

def main ():
    start_code = "#include <stdio.h>\n\n"
    # On Linux, this should get rid of GCC specific extensions.
    # XXX Should these be pushed into the grammar?  Cross reference
    # from current GCC syntax.
    preprocessed_code = cppString(start_code,
                                  "-std=c99",
                                  "-D__extension__=",
                                  "-D__const=const",
                                  "-D__attribute__(x)=",
                                  "-D__restrict=")
    print parseString(preprocessed_code)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of stdio_test.py
