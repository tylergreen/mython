from mycalcgrammar import *

def ceval((op,args), env={}):
    if '+' == op:
        return ceval(args[0],env) + ceval(args[1],env) 
    if '-' == op:
        return ceval(args[0],env) - ceval(args[1],env) 
    elif '*' == op:
        return ceval(args[0],env) * ceval(args[1],env) 
    elif '/' == op:
        return ceval(args[0],env) / ceval(args[1],env) 
    elif '<-' == op:
        env[args[0][0]] = ceval(args[1],env) 
        return args[0]
    elif type(op) is str:
        return env[op] # make sure this is right
    else:
        return op 

def is_val(tree):
    return type(tree[0]) is int

def rewrite(tree):
    op,args = tree
    rwchildren = [rewrite(child) for child in args]
    constant_children = sum((1 if is_val(child) else 0 for child in rwchildren))
#    print tree, constant_children
    if is_val(tree):
        return tree
    elif op in  ['+','-','*','/'] and constant_children == 2:
        return (eval(str(rwchildren[0][0]) + op + str(rwchildren[1][0])), [])
    else:
        return (op,[rewrite(x) for x in args])

if __name__ == '__main__':
    env = {}
    while True:
       try:
           s = raw_input('calc-eval > ')
       except EOFError:
           break
       if not s: continue
       st = parser.parse(s)
       tenv = env.copy()
       result0 = ceval(st,env)
       result1 = ceval(rewrite(st),tenv)
       print "tree" , st
       print "rw" , rewrite(st)
       print "test1:" , result0 == result1 
       print "test2:" , env == tenv

       
       


