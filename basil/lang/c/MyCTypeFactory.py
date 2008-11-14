#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyCTypeFactory.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import ctypes
import basil.lang.c.CTypeFactory

# ______________________________________________________________________
# Class definitions

class MyCType (object):
    pass

# ______________________________________________________________________

class MyCInt (MyCType):
    pass

# ______________________________________________________________________

class MyCFunction (MyCType):
    pass

# ______________________________________________________________________

class MyCTypeFactory (basil.lang.c.CTypeFactory.CTypeFactory):
    def cFunction (self, ret_ty, params, fn_name = None):
        return MyCFunction()

    def cInt (self, base = None):
        return MyCInt()

    def setName (self, name, ty_obj):
        ty_obj.name = name

# ______________________________________________________________________
# Main (self-test) routine.

def main ():
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of MyCTypeFactory.py
