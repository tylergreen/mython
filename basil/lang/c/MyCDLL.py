#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyCDLL

XXX This is a broken attempt to add mutation to ctypes modules.  In
essence this is trying to make assignment to values in the CDLL mutate
the storage cell, rather than rebind the symbol in the Python wrapper
module (or in other words, give assignment in ctypes modules C
assignment semantics, instead of Python semantics).  See development
log for 2008.10.30 for some hint as to why this doesn't work (I think
ctypes.cast creates a new storage cell, and returns a pointer to the
copied cell, as opposed to the actual cell).  This module will be
removed in the next Subversion revision.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import ctypes

# ______________________________________________________________________
# Class definition

class MyCDLL(ctypes.CDLL):
    def __init__ (self, name, mode = ctypes.DEFAULT_MODE, handle = None):
        self.__dict__["_data"] = {}
        ctypes.CDLL.__init__(self, name, mode, handle)

    def set_data (self, key, data_type):
        """Tag the given DLL name as a data pointer instead of a
        function pointer."""
        kv = getattr(self, key)
        self._data[key] = data_type
        self.__dict__[key] = ctypes.cast(kv, ctypes.POINTER(data_type))

    def __setattr__ (self, key, value):
        if key in self._data:
            print key, value
            self.__dict__[key].contents = self._data[key](value)
        else:
            self.__dict__[key] = value
            # Could not get this to work properly, and I have no idea
            # why, since attribute assignment seems to work otherwise:
            # setattr(super(MyCDLL, self), key, value)

# ______________________________________________________________________
# Main (self-test) routine

def main ():
    from distutils.sysconfig import customize_compiler
    from distutils.ccompiler import new_compiler
    dll_name = "tests/mycmodule"
    # XXX There should be an easier way to get the shared library
    # extension from somewhere in the standard library.
    dummy_compiler = new_compiler()
    customize_compiler(dummy_compiler)
    shared_lib_ext = dummy_compiler.shared_lib_extension
    if shared_lib_ext:
        dll_name = "".join((dll_name, shared_lib_ext))
    mycmodule = MyCDLL(dll_name)
    mycmodule.set_data("increment", ctypes.c_int)
    mycmodule.inc.argtypes = [ctypes.c_int]
    mycmodule.inc.restype = ctypes.c_int
    assert mycmodule.inc(42) == 43
    mycmodule.increment = 2
    print mycmodule.inc(42)
    assert mycmodule.inc(42) == 44

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of MyCDLL.py
