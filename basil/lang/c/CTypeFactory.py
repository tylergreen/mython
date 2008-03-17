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

    def cStruct (self, structName = None, **fieldDict):
        raise NotImplementedError()

    def cUnion (self, unionName = None, **fieldDict):
        raise NotImplementedError()

    def cEnum (self, enumName = None, *enumPairs):
        raise NotImplementedError()

    def cFunction (self, retTy, params, fnName = None):
        raise NotImplementedError()

# ______________________________________________________________________

class NaiveCTypeFactory (CTypeFactory):
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

    def cStruct (self, structName = None, **fieldDict):
        field_str = "\n".join(("%s %s;" % (k, v)
                               for k, v in fieldDict.iteritems()))
        if structName is None:
            structName = ""
        else:
            structName = " " + structName
        return "struct%s{\n%s}" % (structName, field_str)

    def cUnion (self, unionName = None, **fieldDict):
        field_str = "\n".join(("%s %s;" %  (k, v)
                               for k, v in fieldDict.iteritems()))
        if unionName is None:
            unionName = ""
        else:
            unionName = " " + unionName
        return "union%s{\n%s}" % (unionName, field_str)

    def cEnum (self, *args, **kw):
        raise NotImplementedError()

    def cFunction (self, retTy, params, fnName = None):
        raise NotImplementedError()

    def setName (self, name, tyObj):
        print name, tyObj
        assert type(tyObj) == dict
        tyObj["name"] = name
        return tyObj

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
