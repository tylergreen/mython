#! /usr/bin/env python
# ______________________________________________________________________
"""Module asrl_utils

Jonathan Riehl"""
# ______________________________________________________________________
# Exception class definition(s)

class ASRLFailure (Exception):
    """Base exception class for ASRL exceptions."""

# ______________________________________________________________________

class ASRLMatchFailure (ASRLFailure):
    """Exception class for failures to match."""

# ______________________________________________________________________

class ASRLBuildFailure (ASRLFailure):
    """Exception class for failures to construct an object from ASRL
    abstract syntax."""

# ______________________________________________________________________
# Function definition(s)

def asrlassert (pred):
    if not pred:
        raise ASRLMatchFailure()

# ______________________________________________________________________
# End of asrl_utils.py
