#! /usr/bin/env python
# ______________________________________________________________________
"""llvm/test0.py

Simple example of embedding LLVM assembly in Python.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import StringIO
import llvm
import llvm.core

# ______________________________________________________________________
# Module data

llvm_source = """@msg = internal constant [15 x i8] c"Hello, world.\\0A\\00"
declare i32 @puts(i8 *)
define i32 @not_really_main() {
    %cst = getelementptr [15 x i8]* @msg, i32 0, i32 0
    call i32 @puts(i8 * %cst)
    ret i32 0
}
"""
llvm_module = llvm.core.Module.from_assembly(StringIO.StringIO(llvm_source))

# ______________________________________________________________________
# Main (self-test) routine

def main ():
    import llvm.ee
    print llvm_module
    print "_" * 60
    provider = llvm.core.ModuleProvider.new(llvm_module)
    llvm_engine = llvm.ee.ExecutionEngine.new(provider)
    not_really_main = llvm_module.get_function_named('not_really_main')
    retval = llvm_engine.run_function(not_really_main, [])
    print "_" * 60
    print "Returned", retval.as_int()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of test0.py
