#!/usr/bin/env python
# ______________________________________________________________________
"""Module handle.py

Process a model data file using the specified model, model handler and
model file.  Command line usage:
        % handle.py <model> <handler> <datafile> [args]

<model> - Python model module name.  Should be specified as a file
          path to the model module without the .py at the end.
<handler> - Python model handler name.  The chosen handler should be compatible
            with the specified model.  The handler should be specified as a
            file path the model handler module without the .py at the end.
<datafile> - Data file to internalize.  Internalization routine
             determined by the data file extension and model library
             implementation.
[args] - Optional arguments specific to the handler invoked.

$Id: handle.py 2537 2004-01-11 00:12:42Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import sys
from basil.modeling import internalize

# ______________________________________________________________________

def main ():
    if len(sys.argv) < 4:
        print __doc__
        sys.exit(-1)
    modelModuleName = sys.argv[1]
    handlerModuleName = sys.argv[2]
    datafileName = sys.argv[3]
    args = tuple(sys.argv[4:])
    modelModule = internalize.loadModule(modelModuleName)
    handlerModule = internalize.loadModule(handlerModuleName)
    if modelModule != None:
        model = internalize.internalize(modelModule, datafileName)
        if handlerModule != None and model != None:
            handler = handlerModule.getModelHandler()()
            handler.handleModel(model, args)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of handle.py
