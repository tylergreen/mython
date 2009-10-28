#! /usr/bin/env python
# ______________________________________________________________________
# Module imports

import ctypes

# ______________________________________________________________________
# This should be automatically generated by myctypes.

mycmodule = ctypes.CDLL("mycmodule")
mycmodule.increment = ctypes.c_int.in_dll(mycmodule, "increment")
mycmodule.inc.argtypes = [ctypes.c_int]
mycmodule.inc.restype = ctypes.c_int

# ______________________________________________________________________
# Function definitions

def test_increment_range (cmodule, verbose = False):
    for i in range(10):
        inc_result = cmodule.inc(i)
        assert inc_result == (i + cmodule.increment.value)
        if verbose:
            print inc_result

# ______________________________________________________________________

def test_cmodule (cmodule, verbose = False):
    test_increment_range(cmodule, verbose)
    # Change the increment.
    if verbose:
        print mycmodule.increment
    mycmodule.increment.value = 2
    test_increment_range(cmodule, verbose)

# ______________________________________________________________________
# Main (self-test) routine.

def main (*args):
    test_cmodule(mycmodule, "-q" not in args)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*(sys.argv[1:]))

# ______________________________________________________________________
# End of mycmodulewrap.py