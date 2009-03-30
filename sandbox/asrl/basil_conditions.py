#! /usr/bin/env python
# ______________________________________________________________________
"""Module basil_conditions

Playing around with some ideas regarding property verfication of Basil
language implementations.

XXX See 'Verify non-pattern'.

Mython should eat its own dog food!  There should be a MyFront front s.t.

* is_language_integration(myfront_front) == True
* is_staging_integration(myfront_front) == True

This will uncomplicate code generation to some extent, right?  You can
then write MyFront fronts using concrete syntax.  Something like:

def myfrontend (name, text, env):
    env = env.copy()
    compile_time_val = transform(parse(text))
    env[name] = compile_time_val
    run_time_val = escape(compile_time_val)
    return [myfront_front.parse('%s = %r\n' % (name, run_time_val))], env

Jonathan Riehl"""
# ______________________________________________________________________
# Module imports

# ______________________________________________________________________
# Module exception(s)

class Counterexample (Exception):
    """Exception class for counterexamples of a language
    implementation not having some property."""

# ______________________________________________________________________
# Function definition(s)

def is_language_integration (source, implementation,
                             report_counterexample = None):
    ret_val = True
    try:
        for test_string in implementation.get_test_strings():
            ir0 = implementation.parse(test_string)
            proc_string = implementation.pretty_print(ir0)
            if not isinstance(proc_string, string):
                raise Counterexample((test_string, proc_string,
                                      "not a string"))
            else:
                ir1 = implementation.parse(proc_string)
                if ir1 != i0:
                    raise Counterexample((test_string, ir0, ir1))
    except Counterexample, counterexample:
        if report_counterexample is not None:
            report_counterexample(counterexample)
        ret_val = False
    return ret_val

# ______________________________________________________________________

def is_staged (source, implementation):
    ret_val = True
    for test_string in implementation.get_test_strings():
        ir0 = implementation.parse(test_string)
        if eval(python_impl.pretty_print(ir0.to_python())) != ir0:
            ret_val = False
            break
    return ret_val

# ______________________________________________________________________
# End of basil_conditions.py
