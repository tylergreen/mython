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
    def set_name (self, name):
        self.name = name

    def to_ctype (self):
        raise NotImplementedError("to_ctype() not implemented.")

    def to_wrapper (self, module_name):
        raise NotImplementedError("to_wrapper() not implemented.")

# ______________________________________________________________________

class MyCInt (MyCType):
    def to_ctype (self):
        return "ctypes.c_int"

    def to_wrapper (self, module_name):
        ret_val = None
        # XXX Check to see if this is static?
        if self.name:
            ret_val = ("%s.%s = ctypes.c_int.in_dll(%s, '%s')" %
                       (module_name, self.name, module_name, self.name))
        return ret_val

# ______________________________________________________________________

class MyCFunction (MyCType):
    def __init__ (self, ret_ty, params, fn_name = None):
        self.ret_ty = ret_ty
        self.params = params
        self.name = fn_name

    def to_wrapper (self, module_name):
        ret_val = None
        if self.name:
            arg_str = ",".join([arg_ty_obj.to_ctype() for arg_ty_obj in
                                self.params])
            ret_val = "%s.%s.argtypes = [%s]\n%s.%s.restype = %s" % (
                module_name, self.name, arg_str, module_name, self.name,
                self.ret_ty.to_ctype())
        return ret_val

# ______________________________________________________________________

class MyCTypeFactory (basil.lang.c.CTypeFactory.CTypeFactory):
    def cFunction (self, ret_ty, params, fn_name = None):
        return MyCFunction(ret_ty, params, fn_name)

    def cInt (self, base = None):
        return MyCInt()

    def setName (self, name, ty_obj):
        ty_obj.set_name(name)
        return ty_obj

# ______________________________________________________________________
# Main (self-test) routine.

def main ():
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of MyCTypeFactory.py
