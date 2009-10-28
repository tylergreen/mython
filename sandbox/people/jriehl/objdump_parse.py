#! /usr/bin/env python
# ______________________________________________________________________
import array, re, ctypes

objdump_data = """00000000 <_addfunction>:
   0:	55                   	push   %ebp
   1:	89 e5                	mov    %esp,%ebp
   3:	8b 45 0c             	mov    0xc(%ebp),%eax
   6:	03 45 08             	add    0x8(%ebp),%eax
   9:	5d                   	pop    %ebp
   a:	c3                   	ret    

0000000b <_mulfunction>:
   b:	55                   	push   %ebp
   c:	89 e5                	mov    %esp,%ebp
   e:	8b 45 08             	mov    0x8(%ebp),%eax
  11:	0f af 45 0c          	imul   0xc(%ebp),%eax
  15:	5d                   	pop    %ebp
  16:	c3                   	ret    
  17:	90                   	nop    
"""

fn_start_pat = re.compile("(\\d|[a-fA-F])+ <([A-Za-z_]\\w*)>:")
bin_pat = re.compile("\\s*[0-9a-fA-F]+:\\s+(([0-9a-fA-F]+ )+).+")

def split_objdump_data (data):
    ret_val = []
    search_obj = fn_start_pat.search(data)
    while search_obj != None:
        next_search_obj = fn_start_pat.search(data, search_obj.end())
        if next_search_obj:
            ret_val.append(data[search_obj.start():next_search_obj.start()])
        else:
            ret_val.append(data[search_obj.start():])
        search_obj = next_search_obj
    return ret_val

def proc_fn_data (fn_data):
    fn_lns = fn_data.splitlines()
    fst_ln = fn_lns[0]
    fn_name = fn_start_pat.match(fst_ln).groups()[1]
    fn_data = array.array('B')
    data = []
    for ln in fn_lns[1:]:
        match_obj = bin_pat.match(ln)
        if match_obj is not None:
            for hexstr in match_obj.groups()[0].split():
                if len(hexstr) > 0:
                    fn_data.append(int(hexstr, 16))
    return fn_name, fn_data

c_int_fn_int_int = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)

def process_objdump_data (objdump_data, fn_cons = None):
    if fn_cons is None:
        fn_cons = c_int_fn_int_int
    for fn_name, fn_data in (proc_fn_data(fn_data) for fn_data in
                             split_objdump_data(objdump_data)):
        globals()[fn_name + "_data"] = fn_data
        globals()[fn_name] = fn_cons(fn_data.buffer_info()[0])
        print fn_name, fn_data

# Now need to figure out how to chain these together without Python's help.

def runObjdump (*args):
    ret_val = None
    from subprocess import Popen, PIPE
    cmd = ["objdump", "-d"] + list(args)
    subproc = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE,
                    close_fds = True)
    subproc.stdin.close()
    try:
        subproc.wait()
        if subproc.returncode == 0:
            ret_val = subproc.stdout.read()
        else:
            raise Exception(subproc.stderr.read())
    finally:
        subproc.stdout.close()
        subproc.stderr.close()
    return ret_val

if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        obj_dump_data = runObjdump(arg)
        process_objdump_data(obj_dump_data)
    else:
        obj_dump_data = runObjdump()
        process_objdump_data(obj_dump_data)

# ______________________________________________________________________
# End of objdump_parse.py
