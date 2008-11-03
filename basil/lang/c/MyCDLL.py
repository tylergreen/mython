#! /usr/bin/env python
# ______________________________________________________________________
"""Module MyCDLL

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
            self.__dict__[key].contents = self._data[key](value)
        else:
            self.__dict__[key] = value
            # Could not get this to work properly, and I have no idea
            # why, since attribute assignment seems to work otherwise:
            # setattr(super(MyCDLL, self), key, value)

# ______________________________________________________________________
# Main (self-test) routine

def main ():
    mycmodule = MyCDLL("tests/mycmodule")
    mycmodule.set_data("increment", ctypes.c_int)
    mycmodule.inc.argtypes = [ctypes.c_int]
    mycmodule.inc.restype = ctypes.c_int
    assert mycmodule.inc(42) == 43
    mycmodule.increment = 2
    assert mycmodule.inc(42) == 44

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of MyCDLL.py
