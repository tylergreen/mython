#! /usr/bin/env python
# ______________________________________________________________________
"""Module AST

Defines a set of base classes for ASDL abstract syntax data types.

Jonathan Riehl"""
# ______________________________________________________________________
# Class definition(s)

class ASTError (Exception):
    """Base class for AST related exceptions."""

# ______________________________________________________________________

class ASTFieldMappingError (ASTError):
    """Exception class for problems related to instantiating a sequence of
    fields."""

# ______________________________________________________________________

class ASTInitError (Exception):
    """Exception class for AST instantiation violations."""

# ______________________________________________________________________

class AST (object):
    """Abstract base class for reprenting abstract syntax."""
    # ____________________________________________________________
    __asdl_meta__ = None
    # ____________________________________________________________
    # XXX This seems like taking the long road to get there.  My
    # options are to just stick with the original plan (generate
    # custom code for each constructor), or refine this.
    def map_fields (self, field_list, match_tup, mapping = None):
        if mapping is None:
            mapping = {}
        field_len = len(field_list)
        match_len = len(match_tup)
        if field_len == 0:
            if match_len > 0:
                raise ASTFieldMappingError()
        else:
            field_name, field_type, field_opt, field_seq = field_list[0]
            if field_opt == 0:
                if len(match_tup) == 0:
                    raise ASTFieldMappingError()
                mapping[field_name] = match_tup[0]
                mapping = self.map_fields(field_list[1:], match_tup[1:],
                                          mapping)
            else:
                try:
                    mapping = mapping.copy()
                    mapping[field_name] = match_tup[0]
                    mapping = self.map_fields(field_list[1:], match_tup[1:],
                                              mapping)
                except ASTFieldMappingError:
                    mapping = self.map_fields(field_list[1:], match_tup,
                                              mapping)
        return mapping
    # ____________________________________________________________
    def get_attributes (self):
        ret_val = []
        md = self.__asdl_meta__
        if "attributes" not in md:
            # ASSUMES: super type is either this class or a sum type.
            md = super(type(self), self).__asdl_meta__
        if "attributes" in md:
            ret_val = md["attributes"]
        return ret_val
    # ____________________________________________________________
    def __init__ (self, *args, **kws):
        if "types" in self.__asdl_meta__:
            raise ASTInitError("Can not directly instantiate a sum type "
                               "(trying to create a %s)." %
                               type(self).__name__)
        # Come up with a plausible map from fields to arguments.
        if "fields" in self.__asdl_meta__:
            field_map = self.map_fields(self.__asdl_meta__["fields"], args)
            for key, val in field_map.items():
                setattr(self, key, val)
        # Now handle attributes.
        attributes = self.get_attributes()
        for key, val in kws.items():
            if key not in attributes:
                raise ASTInitError("Not an attribute of %s: %s." %
                                   (type(self).__name__, key))
            setattr(self, key, val)
    # ____________________________________________________________
    def __eq__ (self, other):
        return ((type(self) == type(other)) and
                (self.__dict__ == other.__dict__))
    # ____________________________________________________________
    def __repr__ (self):
        if "fields" in self.__asdl_meta__:
            fields = self.__asdl_meta__["fields"]
            fields_str = ", ".join([repr(getattr(self,field[0]))
                                    for field in fields])
        return "%s(%s)" % (type(self).__name__, fields_str)

# ______________________________________________________________________
# Main (self-test) routine

def main ():
    # XXX Would like the property that eval(repr(a)) == a, given the
    # definitions of AST.__eq__ and AST.__repr__.  Write some tests
    # for that.
    pass

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of AST.py
