#! /usr/bin/env python
# ______________________________________________________________________
"""Module basil.apps.grammarian_util.files

Utilities for dealing with files.

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

import sys

# ______________________________________________________________________
# Function definition(s)

def getOutFileObj (outFile, mode = None):
    """getOutFileObj()
    Get an actual file object for the given output file.
    """
    retVal = None
    if mode == None:
        mode = "w"
    if outFile == None:
        retVal = sys.stdout
    else:
        retVal = open(outFile, mode)
    return retVal

# ______________________________________________________________________

def releaseOutFileObj (outFileObj):
    """releaseOutFileObj()
    Safe call to close for the passed stream object (compares it to stdout).
    If stdout is passed, a newline is sent and the buffer is then flushed.
    """
    if outFileObj == sys.stdout:
        outFileObj.write("\n")
        outFileObj.flush()
    else:
        outFileObj.close()

# ______________________________________________________________________
# End of files.py
