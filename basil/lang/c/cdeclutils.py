#! /usr/bin/env python
# ______________________________________________________________________
"""Module cdeclutils.py

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

from basil.lang.c._cparser import *
from basil.lang.c.CBaseHandler import CBaseHandler

from basil.utils import TreeUtils

if __debug__:
    import pprint

# ______________________________________________________________________
# Module data

IDENTIFIER = cTokenMap["IDENTIFIER"]
IDENTIFIER_LIST = cNonterminalMap["IDENTIFIER_LIST"]
PARAMETER_LIST = cNonterminalMap["PARAMETER_LIST"]
PARAMETER_TYPE_LIST = cNonterminalMap["PARAMETER_TYPE_LIST"]

# ______________________________________________________________________
# Function definitions

def isTypedef (pt):
    """isTypedef()
    Predicate function for determining if the current parse tree
    corresponds to a type definiton."""
    ret_val = False
    typedef_tok = cTokenMap["TYPEDEF"]
    for pt_payload in TreeUtils.prefix_tree_iter(pt):
        if type(pt_payload) == tuple and pt_payload[0] == typedef_tok:
            ret_val = True
            break
    return ret_val

# ______________________________________________________________________

def getTypedefMap (pt):
    """getTypeMap()
    Create a map from type names to type definitions based on an input
    C concrete parse tree."""
    decl_map = getDeclMap(pt)
    typedef_items = ((decl_key, decl_vals) for decl_key, decl_vals in
                     decl_map.iteritems()
                     if sum([isTypedef(decl_val) for decl_val in decl_vals]))
    ret_val = dict(typedef_items)
    return ret_val

# ______________________________________________________________________

def getFirstIdentifier (pt):
    """getFirstIdentifier()
    Get the first identifier token found in the given parse tree."""
    ret_val = None
    for pt_payload in TreeUtils.prefix_tree_iter(pt):
        if type(pt_payload) == tuple and pt_payload[0] == IDENTIFIER:
            ret_val = pt_payload
            break
    return ret_val

# ______________________________________________________________________

def getDeclMap (pt):
    """getDeclMap()
    Create a map from identifiers to type declarations based on a C
    concrete parse tree."""
    declaration = cNonterminalMap["DECLARATION"]
    function_definition = cNonterminalMap["FUNCTION_DEFINITION"]
    declaration_specifiers = cNonterminalMap["DECLARATION_SPECIFIERS"]
    su_specifier = cNonterminalMap["SU_SPECIFIER"]
    enum_specifier = cNonterminalMap["ENUM_SPECIFIER"]
    def recGetDeclMap (pt):
        ret_val = {}
        if type(pt[0]) == int:
            nt_number, children = pt
            if nt_number == declaration:
                ret_val.update(recGetDeclMap(children[0]))
                if len(children) > 1:
                    _, identifier_key, _, _ = getFirstIdentifier(children[1])
                    ret_val[identifier_key] = children
            elif nt_number == function_definition:
                check_index = 0
                if ((type(children[0][0]) == int) and
                    (children[0][0] == declaration_specifiers)):
                    ret_val.update(recGetDeclMap(children[0]))
                    check_index = 1
                check_child = children[check_index]
                _, identifier_key, _, _ = getFirstIdentifier(check_child)
                ret_val[identifier_key] = children[1:]
            elif nt_number == su_specifier:
                if len(children) > 4:
                    assert type(children[0][0]) == tuple
                    assert type(children[1][0]) == tuple
                    identifier_key = "%s %s" % (children[0][0][1],
                                                children[1][0][1])
                    ret_val[identifier_key] = children
            elif nt_number == enum_specifier:
                if len(children) > 4:
                    assert type(children[1][0]) == tuple
                    identifier_key = "enum " + children[1][0][1]
                    ret_val[identifier_key] = children
                # Other cases would have been anonymous enumeration or
                # reference to an enumeration type.
            else:
                for child_pt in children:
                    ret_val.update(recGetDeclMap(child_pt))
        return ret_val
    return recGetDeclMap(pt)

# ______________________________________________________________________

class CDeclHandler (CBaseHandler):
    # ____________________________________________________________
    def __init__ (self, factory):
        self.factory = factory
        # XXX Not sure I would want to use this state...
        self.ty_stack = []
        self.crnt_ty = None

    # ____________________________________________________________
    def _handle_default (self, node):
        print node
        return self.handle_children(node)

    handle_default = CBaseHandler.handle_children
    #handle_default = _handle_default

    # ____________________________________________________________
    def get_handler_name (self, node):
        """
        Modified version of Handler.get_handler_name(), which will do
        dispatch on token names as well as non-terminals."""
        node_payload, _ = node
        if type(node_payload) == int:
            symbol_name = cNonterminals[node_payload]
        else:
            symbol_name = cTokens[node_payload[0]]
        return "handle_%s" % symbol_name

    # ____________________________________________________________
    def handle_ASTERISK (self, node):
        return self.factory.cPointer(self.crnt_ty)

    # ____________________________________________________________
    def handle_CHAR (self, node):
        return self.factory.cChar(self.crnt_ty)

    # ____________________________________________________________    
    def handle_DECLARATION (self, node):
        _, children = node
        ret_val = self.handle_node(children[0])
        if len(children) > 1:
            self.pushTy(ret_val)
            ret_val = self.handle_node(children[1])
            self.popTy()
        return ret_val

    # ____________________________________________________________
    def handle_DECLARATION_SPECIFIERS (self, node):
        _, children = node
        ret_val = self.handle_node(children[-1])
        if len(children) > 1:
            self.pushTy(ret_val)
            ret_val = self.handle_node(children[0])
            self.popTy()
        return ret_val

    # ____________________________________________________________
    def handle_DECLARATOR (self, node):
        _, children = node
        assert len(children) == 2
        ret_val = self.handle_node(children[0])
        self.pushTy(ret_val)
        ret_val = self.handle_node(children[1])
        self.popTy()
        return ret_val

    # ____________________________________________________________
    def handle_DIRECT_DECLARATOR (self, node):
        _, children = node
        ret_val = None
        if self.is_token(children[0]) and children[0][0][1] == "(":
            ret_val = self.handle_node(children[1])
        else:
            assert self.is_token(children[1])
            if children[1][0][1] == '(':
                # function... return type should be the current type...
                params = []
                if len(children) > 3:
                    if (self.is_token(children[2]) and
                        children[2][0][0] == IDENTIFIER):
                        # Single parameter name...
                        self.pushTy(self.factory.cInt())
                        params.append(self.handle_node(children[2]))
                        self.popTy()
                    elif children[2][0] in (IDENTIFIER_LIST,
                                            PARAMETER_LIST,
                                            PARAMETER_TYPE_LIST):
                        # Multiple parameter names...
                        params = self.handle_node(children[2])
                    else:
                        params.append(self.handle_node(children[2]))
                ret_val = self.factory.cFunction(self.crnt_ty,
                                                 params)
                self.pushTy(ret_val)
                ret_val = self.handle_node(children[0])
                self.popTy()
            elif children[1][0][1] == '[':
                # array
                raise NotImplementedError("Arrays are not currently handled.")
            else:
                raise NotImplementedError("Unexpected direct declarator: %s" %
                                          node)
        return ret_val

    # ____________________________________________________________
    def handle_DOUBLE (self, node):
        return self.factory.cDouble(self.crnt_ty)

    # ____________________________________________________________
    def handle_EXTERN (self, node):
        return self.factory.cExtern(self.crnt_ty)

    # ____________________________________________________________
    def handle_IDENTIFIER (self, node):
        return self.factory.setName(node[0][1], self.crnt_ty)

    # ____________________________________________________________
    def handle_IDENTIFIER_LIST (self, node):
        # Flatten the list...
        ret_val = []
        while node[0] == IDENTIFIER_LIST:
            self.pushTy(self.factory.cInt())
            ret_val.append(self.handle_node(node[1][2]))
            self.popTy()
            node = node[1][0]
        self.pushTy(self.factory.cInt())
        ret_val.append(self.handle_node(node))
        self.popTy()
        ret_val.reverse()
        return ret_val

    # ____________________________________________________________
    def handle_INT (self, node):
        return self.factory.cInt(self.crnt_ty)

    # ____________________________________________________________
    def handle_FLOAT (self, node):
        return self.factory.cFloat(self.crnt_ty)

    # ____________________________________________________________
    def handle_FUNCTION_DEFINITION (self, node):
        _, children = node
        knr_decls = False
        declarator_index = 0
        ret_ty = None
        # XXX After a slight modification to the grammar, this is
        # another way to determine if we are playing with a K&R style
        # definition.
        # if self.get_nonterminal(children[-2]) == "DECLARATION_LIST":
        #     knr_decls = True
        # __________________________________________________
        # First figure out the return type.
        if self.get_nonterminal(children[0]) == "DECLARATION_SPECIFIERS":
            if len(children) == 4:
                knr_decls =  True
            ret_ty = self.handle_node(children[0])
            declarator_index = 1
        elif len(children) == 3:
            knr_decls = True
        else:
            ret_ty = self.factory.cInt()
        # __________________________________________________
        # Then handle the declarator node.
        self.pushTy(ret_ty)
        ret_val = self.handle_node(children[declarator_index])
        self.popTy()
        # __________________________________________________
        # Finally, handle K&R parameter declarations.
        if knr_decls:
            # This implies old school parameter type syntax.
            raise NotImplementedError("K&R parameter type declarations not "
                                      "currently supported.")
        if __debug__:
            print ret_val
        return ret_val

    # ____________________________________________________________
    def handle_LONG (self, node):
        return self.factory.cLong(self.crnt_ty)

    # ____________________________________________________________
    def handle_PARAMETER_DECLARATION (self, node):
        _, children = node
        ret_val = self.handle_node(children[0])
        self.pushTy(ret_val)
        ret_val = self.handle_node(children[1])
        self.popTy()
        return ret_val

    # ____________________________________________________________
    def handle_PARAMETER_LIST (self, node):
        # Flatten the list...
        ret_val = []
        while node[0] == PARAMETER_LIST:
            ret_val.append(self.handle_node(node[1][2]))
            node = node[1][0]
        ret_val.append(self.handle_node(node))
        ret_val.reverse()
        return ret_val

    # ____________________________________________________________
    def handle_PARAMETER_TYPE_LIST (self, node):
        _, children = node
        ret_val = self.handle_node(children[0])
        if type(ret_val) != list:
            ret_val = [ ret_val ]
        ret_val.append("...")
        return ret_val

    # ____________________________________________________________
    def handle_POINTER (self, node):
        _, children = node
        ret_val = self.handle_node(children[0])
        for child in children[1:]:
            self.pushTy(ret_val)
            ret_val = self.handle_node(child)
            self.popTy()
        return ret_val

    # ____________________________________________________________
    def handle_SHORT (self, node):
        return self.factory.cShort(self.crnt_ty)

    # ____________________________________________________________
    def handle_SIGNED (self, node):
        return self.factory.cSigned(self.crnt_ty)

    # ____________________________________________________________
    def handle_SU_SPECIFIER (self, node):
        _, children = node
        if len(children) > 2:
            fields = self.handle_node(children[-2])
        raise NotImplementedError()

    # ____________________________________________________________
    def handle_STRUCT_DECLARATION_LIST (self, node):
        _, children = node
        ret_val = self.handle_node(children[0])
        if len(children) > 1:
            ret_val += self.handle_node(children[1])
        return tuple(ret_val)

    # ____________________________________________________________
    def handle_STRUCT_DECLARATION (self, node):
        pprint.pprint(node)
        _, children = node
        ret_val = self.handle_node(children[0])
        assert len(children) == 3
        if len(children) > 1:
            self.pushTy(ret_val)
            ret_val = self.handle_node(children[1])
            self.popTy()
        return [ret_val]

    # ____________________________________________________________
    def handle_TRANSLATION_UNIT (self, node):
        _, children = node
        assert len(children) == 2
        ret_val = []
        node_stack = [node]
        while node_stack:
            crnt_node = node_stack.pop()
            if self.get_nonterminal(crnt_node) == "TRANSLATION_UNIT":
                _, children = crnt_node
                assert len(children) == 2
                # Note that this reverses them b/c the stack is LIFO
                node_stack.append(children[1])
                node_stack.append(children[0])
            else:
                ret_val.append(self.handle_node(crnt_node))
        return ret_val

    # ____________________________________________________________
    def handle_UNSIGNED (self, node):
        return self.factory.cUnsigned(self.crnt_ty)

    # ____________________________________________________________
    def handle_VOID (self, node):
        return self.factory.cVoid(self.crnt_ty)

    # ____________________________________________________________
    def is_translation_unit (self, node):
        return self.get_noterminal == "TRANSLATION_UNIT"

    # ____________________________________________________________
    def pushTy (self, ty_obj):
        self.ty_stack.append(self.crnt_ty)
        self.crnt_ty = ty_obj

    # ____________________________________________________________
    def popTy (self):
        self.crnt_ty = self.ty_stack.pop()

# ______________________________________________________________________

DECL_TEST_STRING = """char b; short c; int d; long e;
float f; double g;
signed h; unsigned i; unsigned long long g;
char * bp; short * cp; int * dp; long * ep;
float * fp; double * gp; signed * hp; unsigned * ip;
unsigned long long * gp;
char ** bpp; short ** cpp; int ** dpp; long ** epp;
float ** fpp; double ** gpp; signed ** hpp; unsigned ** ipp;
unsigned long long ** gpp;
void testfn1 (int a, int b) {
 return;
}
extern int testfn2 (float c);

struct point {
 float x;
 float y;
 float z;
};

typedef struct {
  struct point corners [2];
} volume;
"""
# XXX To add: 

# XXX Is there some way to eject the above code into a .so and cross
# validate with ctypes?

# ______________________________________________________________________
# Main routine

def main (*args):
    debug_flag = "-d" in args
    from basil.lang.c.CBaseHandler import CTestHandler
    from basil.lang.c.CTypeFactory import NaiveCTypeFactory
    # ____________________________________________________________
    class CDeclTestHandler(CDeclHandler, CTestHandler):
        def __init__ (self):
            CDeclHandler.__init__(self, NaiveCTypeFactory())

        def get_handler_name (self, node):
            ret_val = CDeclHandler.get_handler_name(self, node)
            if debug_flag:
                print ("CDeclTestHandler.get_handler_name(): %s %s" %
                       (ret_val, str(hasattr(self, ret_val))))
                if __debug__:
                    pprint.pprint(node)
            return ret_val
    # ____________________________________________________________
    handler = CDeclTestHandler()
    args = [arg for arg in args if arg[0] != "-"]
    # XXX: Add tests on the other functions in this module.
    if args:
        for arg in args:
            handler.handle_file(arg)
    else:
        handler.handle_str(DECL_TEST_STRING)

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of cdeclutils.py
