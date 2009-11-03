#! /usr/bin/env python
# ______________________________________________________________________
"""llvm/test2.py

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import time
import StringIO
import llvm
import llvm.core

# ______________________________________________________________________
# Module data

llvm_as_source = """@msg = internal constant [15 x i8] c"Hello, world.\\0A\\00"

declare i32 @puts(i8 *)

define i32 @not_really_main() {
    %cst = getelementptr [15 x i8]* @msg, i32 0, i32 0
    call i32 @puts(i8 * %cst)
    ret i32 0
}
"""

llvm_bitcode = None

# ______________________________________________________________________
# Function definitions

def test_module_from_source ():
    global llvm_as_source
    return llvm.core.Module.from_assembly(StringIO.StringIO(llvm_as_source))

# ______________________________________________________________________

def test_module_from_source_to_bitcode ():
    global llvm_as_source, llvm_bitcode
    llvm_module = test_module_from_source()
    fobj = StringIO.StringIO()
    llvm_module.to_bitcode(fobj)
    llvm_bitcode = fobj.getvalue()
    return llvm_bitcode

# ______________________________________________________________________

def test_module_from_bitcode ():
    global llvm_bitcode
    return llvm.core.Module.from_bitcode(StringIO.StringIO(llvm_bitcode))

# ______________________________________________________________________

def time_function (test_function, test_runs = 1000):
    test_results = []
    t0 = time.time()
    for test_run in xrange(test_runs):
        test_results.append(test_function())
    t1 = time.time()
    del test_results # Try to defer any deallocation to after times
                     # are measured.
    return t1 - t0

# ______________________________________________________________________
# Main (self-test) routine

def main (*args):
    testruns = xrange(100)
    naive_embedding_times = [time_function(test_module_from_source)
                             for testrun in testruns]
    compile_time_times = [time_function(test_module_from_source_to_bitcode)
                          for testrun in testruns]
    run_time_times = [time_function(test_module_from_bitcode)
                      for testrun in testruns]
    print ("Naive embedding summary: min=%g max=%g avg=%g" %
           (min(naive_embedding_times), max(naive_embedding_times),
            sum(naive_embedding_times) / len(naive_embedding_times)))
    print ("Compile-time summary: min=%g max=%g avg=%g" %
           (min(compile_time_times), max(compile_time_times),
            sum(compile_time_times) / len(compile_time_times)))
    print ("Run-time summary: min=%g max=%g avg=%g" %
           (min(run_time_times), max(run_time_times),
            sum(run_time_times) / len(run_time_times)))

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main (*sys.argv[1:])

# ______________________________________________________________________
# End of test2.py
