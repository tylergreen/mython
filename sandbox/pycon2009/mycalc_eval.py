from mycalcgrammar import *

env = { }

def ceval((op,args)):
    if '+' == op:
        return sum((ceval(c) for c in args))
    elif '*' == op:
        return reduce(lambda x,y: x*y, [ ceval(c,env) for c in args])
    elif '<-' == op:
        env[args[0]] = ceval(args[1])
        return args[0]
    elif type(op) is str:
        return env[op]  
    else:
        return op  


if __name__ == '__main__':
    while True:
       try:
           s = raw_input('calc-eval > ')
       except EOFError:
           break
       if not s: continue
       print ceval(parser.parse(s))
