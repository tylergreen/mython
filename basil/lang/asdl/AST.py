#! /usr/bin/env python
# ______________________________________________________________________
"""Module AST

Defines a set of base classes for ASDL abstract syntax data types.

Jonathan Riehl"""
# ______________________________________________________________________
# Class definition(s)

class AST (object):
    """Abstract base class for reprenting abstract syntax."""
    # ____________________________________________________________
    __asdl_meta__ = None
    # ____________________________________________________________
    def __eq__ (self, other):
        return ((type(self) == type(other)) and
                (self.__dict__ == other.__dict__))

# ______________________________________________________________________
# Main (self-test) routine

def main ():
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of AST.py
