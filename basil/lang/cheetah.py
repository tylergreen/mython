from Cheetah.Template import Template

def mktemplate(src):
    def mktemp(ns):
        return Template(src, ns)
    return mktemp

def mkcheetah (rtsrc_format, name, src, env):
    imp = ("from Cheetah.Template import Template\n"
           "from basil.lang.cheetah import mktemplate\n")
    rtsrc = rtsrc_format % (name, src)
    ast, env = env['myfrontend'](imp + rtsrc, env)
    return ast.body , env

def echeetah(name, src, env):
    return mkcheetah("%s = Template(%r, [locals(), globals()])\n", name, src, env)

def cheetah(name, src, env):
    return mkcheetah('%s = mktemplate(%r)\n',name, src, env)

