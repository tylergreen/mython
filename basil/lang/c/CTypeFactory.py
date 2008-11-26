#! /usr/bin/env python
# ______________________________________________________________________
"""Module CTypeFactory

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module includes

# None.

# ______________________________________________________________________
# Class definition

class CTypeError (Exception):
    pass

# ______________________________________________________________________

class CTypeFactory (object):
    """Abstract base class for creating objects (or calling actions)
    that correspond to C types."""

    def __init__ (self):
        self.typename_map = {"void" : self.cVoid,
                             "char" : self.cChar,
                             "short" : self.cShort,
                             "int" : self.cInt,
                             "long" : self.cLong,
                             "float" : self.cFloat,
                             "double" : self.cDouble,
                             "signed" : self.cSigned,
                             "unsigned" : self.cUnsigned,
                             }

    def cVoid (self, baseTy = None):
        raise NotImplementedError()

    def cChar (self, baseTy = None):
        raise NotImplementedError()

    def cShort (self, baseTy = None):
        raise NotImplementedError()

    def cInt (self, baseTy = None):
        raise NotImplementedError()

    def cLong (self, baseTy = None):
        raise NotImplementedError()

    def cFloat (self, baseTy = None):
        raise NotImplementedError()

    def cDouble (self, baseTy = None):
        raise NotImplementedError()

    def cSigned (self, baseTy = None):
        raise NotImplementedError()

    def cUnsigned (self, baseTy = None):
        raise NotImplementedError()

    def cPointer (self, baseTy):
        raise NotImplementedError()

    def cStruct (self, structName = None, fieldPairs = None):
        raise NotImplementedError()

    def cUnion (self, unionName = None, fieldPairs = None):
        raise NotImplementedError()

    def cEnum (self, enumName = None, enumPairs = None):
        raise NotImplementedError()

    def cFunction (self, retTy, params, fnName = None):
        raise NotImplementedError()

    def setName (self, name, ty):
        raise NotImplementedError()

    def pushParamNaming (self):
        raise NotImplementedError()

    def pushTypedefNaming (self):
        raise NotImplementedError()

    def pushSUMemberNaming (self):
        raise NotImplementedError()

    def pushEnumNaming (self):
        raise NotImplementedError()

    def popMode (self):
        raise NotImplementedError()

# ______________________________________________________________________

class NaiveCTypeFactory (CTypeFactory):
    """The purpose of the NaiveCTypeFactory is to roughly reconstruct
    the C type as a string, given a construction sequence."""
    def __init__ (self):
        CTypeFactory.__init__(self)
        self.modeStack = []
        self.namespace = []

    def cVoid (self, baseTy = None):
        return {"ty" : "void"}

    def cChar (self, baseTy = None):
        return {"ty" : "char"}

    def cShort (self, baseTy = None):
        return {"ty" : "short"}

    def cInt (self, baseTy = None):
        return {"ty" : "int"}

    def cLong (self, baseTy = None):
        if baseTy is None:
            ret_val = {"ty" : "long"}
        else:
            ret_val = baseTy.copy()
            ret_val["ty"] = "long %s" % ret_val["ty"]
        return ret_val

    def cFloat (self, baseTy = None):
        return {"ty" : "float"}

    def cDouble (self, baseTy = None):
        return {"ty" : "double"}

    def __annotate_ty (self, tyAnnotation, baseTy = None):
        if baseTy is None:
            ret_val = {"ty" : "%s int" % tyAnnotation}
        else:
            ret_val = baseTy.copy()
            ret_val["ty"] = " ".join((tyAnnotation, ret_val["ty"]))
        return ret_val

    def cSigned (self, baseTy = None):
        return self.__annotate_ty("signed", baseTy)

    def cUnsigned (self, baseTy = None):
        return self.__annotate_ty("unsigned", baseTy)

    def cPointer (self, baseTy):
        ret_val = baseTy.copy()
        ret_val["ty"] = "%s *" % ret_val["ty"]
        return ret_val

    def cStruct (self, structName = None, fieldPairs = None):
        if fieldPairs is None:
            fieldPairs = []
        field_str = "\n".join(("%s %s;" % fieldPair
                               for fieldPair in fieldPairs))
        if structName is None:
            structName = ""
        else:
            structName = " " + structName
            if fieldPairs:
                raise NotImplementedError("Need to set struct in namespace.")
            else:
                raise NotImplementedError("Need to get struct from namespace.")
        return "struct%s{\n%s}" % (structName, field_str)

    def cUnion (self, unionName = None, fieldPairs = None):
        if fieldPairs is None:
            fieldParis = []
        field_str = "\n".join(("%s %s;" %  fieldPair
                               for fieldPair in fieldPairs))
        if unionName is None:
            unionName = ""
        else:
            unionName = " " + unionName
            if fieldPairs:
                raise NotImplementedError("Need to set union in namespace.")
            else:
                raise NotImplementedError("Need to get union from namespace.")
        return "union%s{\n%s}" % (unionName, field_str)

    def cEnum (self, enumName = None, enumPairs = None):
        raise NotImplementedError()

    def cFunction (self, retTy, params, fnName = None):
        ret_val = {"ty" : "%s -> %s" % (str(tuple(params)), retTy["ty"])}
        if retTy.has_key("extern"):
            ret_val["extern"] = retTy["extern"]
        if fnName is not None:
            ret_val["name"] = fnName
        return ret_val

    def setName (self, name, tyObj):
        assert type(tyObj) == dict
        tyObj["name"] = name
        return tyObj

    def cExtern (self, baseTy = None):
        if baseTy is None:
            ret_val = {"ty" : "int"}
        else:
            ret_val = baseTy.copy()
        ret_val["extern"] = True
        return ret_val

    def pushParamNaming (self):
        raise NotImplementedError()

    def pushTypedefNaming (self):
        raise NotImplementedError()

    def pushSUMemberNaming (self):
        raise NotImplementedError()

    def pushEnumNaming (self):
        raise NotImplementedError()

    def popMode (self):
        raise NotImplementedError()

# ______________________________________________________________________
# Main routine (self test)

def main (*args):
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])

# ______________________________________________________________________
# End of CTypeFactory
