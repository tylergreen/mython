#! /usr/bin/env python
# ______________________________________________________________________
"""Module PyHandlerStrings

Defines strings used for handler generation.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.utils.CodeGen import methodSeparator, sectionSeparator

# ______________________________________________________________________
# Module data

header = """#! /usr/bin/env python
%s
# Note: Parts of this were automatically generated using %%s
%s

from basil.modeling.BaseModelHandler import BaseModelHandler""" % \
(sectionSeparator, sectionSeparator)

# ______________________________________________________________________

classFront = """
%s
class %%s (BaseModelHandler):""" % (sectionSeparator,)

# ______________________________________________________________________

methodFront = """    %s
    def handle%%s%s (self, modelElement, args = None):""" % (methodSeparator,)

# ______________________________________________________________________

childlessMethodBody = """        # Insert handler actions here.
        pass
"""

# ______________________________________________________________________

methodBody = """        # Insert prefix actions here.
        childResults = self._handleChildren(modelElement, args)
        # Insert postfix actions here.
        return childResults
"""

# ______________________________________________________________________

footer = """%s

def getModelHandler ():
    return %%s

%s
# End of %%s.py
""" % (sectionSeparator, sectionSeparator)

# ______________________________________________________________________

defaultCodeStrings = {
    "header" :  header,
    "classFront" : classFront,
    "methodFront" : methodFront,
    "childlessMethodBody" : childlessMethodBody,
    "methodBody" : methodBody,
    "footer" : footer
    }

# ______________________________________________________________________
# End of PyHandlerStrings.py
