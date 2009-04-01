#! /usr/bin/env python
"""basil.apps.grammarian_util.misc

Miscellaneous Grammarian settings, etc.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.models.grammar import BasilGrammarModel

# ______________________________________________________________________
# Module data

__DEBUG__ = False

VERSION = "0.0.1"

grammarModelFactory = BasilGrammarModel.getModelFactory()()

# ______________________________________________________________________
# End of misc.py
