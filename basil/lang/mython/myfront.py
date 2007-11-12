#! /usr/bin/env python
# ______________________________________________________________________
"""Script myfront.py

XXX This is a deprecated proof of concept!  Use MyFront.py, per the paper.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________

import os
import sys
import getopt
import imp
import marshal
import struct
import StringIO
import tokenize
import MyRealParser
import MyAbstractor
import compiler

# ______________________________________________________________________

class MyFront (object):
    """Class MyFront
    """
    # ____________________________________________________________
    def __init__ (self, input_file = None, processors = None,
                  output_file = None):
        """MyFront.__init__()
        """
        if processors is None:
            processors =  [self.myfront, self.code_generator, self.output_code]
        self.input_file = input_file
        self.processors = processors
        self.output_file = output_file
        self.environment = {"input_file" : input_file,
                            "output_file" : output_file,
                            "myfront" : self.myfront,
                            "myfront_eval" : self.myfront_eval,
                            None : self.myfront} # default front end,
                                                 # not visible except
                                                 # to the abstractor.

    # ____________________________________________________________
    def myfront (self, environment, input_data):
        """MyFront.myfront()
        environment x string -> environment x abstract parse tree"""
        # In this implementation, the lexer and parser do not modify
        # the environment.  However, the abstractor does.
        tokenizer_readline = StringIO.StringIO(input_data).readline
        tokenizer = tokenize.generate_tokens(tokenizer_readline)
        parser = MyRealParser.MyRealParser(tokenizer, self.input_file)
        concrete_tree = parser()
        ret_val = self.abstractor(environment, concrete_tree)
        input_file_name = self.input_file
        if input_file_name is None:
            input_file_name = "<stdin>"
        compiler.misc.set_filename(input_file_name, ret_val[1])
        compiler.syntax.check(ret_val[1])
        return ret_val

    # ____________________________________________________________
    def myfront_eval (self, environment, input_data):
        """MyFront.myfront_eval()
        environment x abstract parse tree -> environment x abstract parse tree
        """
        environment1, ast = self.myfront(environment, input_data)
        next_environment = environment1.copy()
        generator = compiler.pycodegen.ModuleCodeGenerator(ast)
        exec generator.getCode() in next_environment
        return (next_environment, ast)

    # ____________________________________________________________
    def abstractor (self, environment, input_data):
        """MyFront.abstractor()
        environment x concrete parse tree ->
        environment x abstract parse tree"""
        abstractor = MyAbstractor.MyAbstractor(environment)
        abstract_tree = abstractor.transform(input_data)
        ret_val = (environment, abstract_tree)
        return ret_val

    # ____________________________________________________________
    def code_generator (self, environment, input_data):
        """MyFront.code_generator()
        environment x abstract parse tree -> environment x code object"""
        generator = compiler.pycodegen.ModuleCodeGenerator(input_data)
        ret_val = (environment, generator.getCode())
        return ret_val

    # ____________________________________________________________
    def output_code (self, environment, input_data):
        """MyFront.output_code()
        environment x bytecode -> environment x unit"""
        ret_val = (environment, None)
        if self.output_file is not None:
            outfile = open(environment["output_file"], "wb")
        else:
            outfile = StringIO.StringIO()
        outfile.write(imp.get_magic())
        if self.input_file is not None:
            mtime = os.path.getmtime(self.input_file)
        else:
            mtime = 0
        outfile.write(struct.pack('<i', mtime))
        outfile.write(marshal.dumps(input_data))
        if self.output_file is None:
            # XXX Write an escaped string to stdout.
            print `outfile.getvalue()`
        outfile.close()
        return ret_val

    # ____________________________________________________________
    def __call__ (self):
        """MyFront.__call__() Do a fold over the processor pipeline,
        stringing the enviornment between the functions."""
        environment = self.environment.copy()
        if self.input_file is None:
            data = sys.stdin.read()
        else:
            data = open(self.input_file).read()
        for processor in self.processors:
            environment, data = processor(environment, data)
        return (environment, data)

# ______________________________________________________________________

def main (*args):
    """main()
    """
    input_file = None
    processors = None
    output_file = None
    opts, args = getopt.getopt(args, "o:")
    for opt_key, opt_val in opts:
        if opt_key == "-o":
            output_file = opt_val
    if len(args) > 0:
        input_file = args[-1]
    if input_file is not None and output_file is None:
        output_file = "%s.pyc" % (os.path.splitext(input_file)[0])
    app = MyFront(input_file, processors, output_file)
    app()

# ______________________________________________________________________

if __name__ == "__main__":
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of myfront.py
