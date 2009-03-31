#experiment for intergration between ply and basil grammars

import mycalcgrammar

myg = mycalcgrammar
tokens = mycalcgrammar.tokens

prodfns = [ getattr(myg,name) for name in myg.__dict__.keys()
            if name.startswith("p_")]

prodstrs = [ f.__doc__ for f in prodfns ]

nts = set() 
print nts
print prodfns
print prodstrs

