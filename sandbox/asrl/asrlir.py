#! /usr/bin/env python

from basil.lang.asdl.AST import AST

class ASRL (object):
    __asdl_meta__ = {'version': '"0.0"', 'name': 'ASRL', 'dfns': ['unit', 'rwty', 'rwexp']}

    class unit (AST):
        __asdl_meta__ = {'attributes': [], 'types': ['Unit']}


    class Unit (unit):
        __asdl_meta__ = {'fields': [('asdl_file', 'string', 0, 0), ('rws', 'rwty', 0, 1)], 'name': 'Unit'}


    class rwty (AST):
        __asdl_meta__ = {'attributes': [('lineno', 'int', 0, 0)], 'types': ['Rewrite']}


    class Rewrite (rwty):
        __asdl_meta__ = {'fields': [('label', 'identifier', 0, 0), ('match', 'rwexp', 0, 0), ('build', 'rwexp', 0, 0), ('where_clause', 'string', 1, 0)], 'name': 'Rewrite'}


    class rwexp (AST):
        __asdl_meta__ = {'attributes': [('lineno', 'int', 0, 0)], 'types': ['Constructor', 'List', 'Tuple', 'Dots', 'Var', 'Const', 'Builtin']}


    class Constructor (rwexp):
        __asdl_meta__ = {'fields': [('label', 'identifier', 0, 0), ('args', 'rwexp', 0, 1)], 'name': 'Constructor'}


    class List (rwexp):
        __asdl_meta__ = {'fields': [('elems', 'rwexp', 0, 1)], 'name': 'List'}


    class Tuple (rwexp):
        __asdl_meta__ = {'fields': [('elems', 'rwexp', 0, 1)], 'name': 'Tuple'}


    class Dots (rwexp):
        __asdl_meta__ = {'fields': [('dot_index', 'int', 0, 0)], 'name': 'Dots'}


    class Var (rwexp):
        __asdl_meta__ = {'fields': [('vid', 'identifier', 0, 0)], 'name': 'Var'}


    class Const (rwexp):
        __asdl_meta__ = {'fields': [('val', 'object', 0, 0)], 'name': 'Const'}


    class Builtin (rwexp):
        __asdl_meta__ = {'fields': [('blabel', 'identifier', 0, 0)], 'name': 'Builtin'}

