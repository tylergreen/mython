#! /usr/bin/env python
# ______________________________________________________________________
"""basil/setup.py - Distutils script for the Basil platform.

$Id: setup.py 2537 2004-01-11 00:12:42Z jriehl $
"""
# ______________________________________________________________________

from distutils.core import setup, Extension
import os.path

# ______________________________________________________________________

CParserSources = map(lambda x : os.path.join("lang","c",x),
                     ["cparser.tab.c",
                      "lex.cparser.c",
                      "cparserutils.c",
                      "namespace.c",
                      "cparsermodule.c"])

CParserExtension = Extension("basil.lang.c._cparser",
                             define_macros = [("MAJOR_VERSION", "0"),
                                              ("MINOR_VERSION", "1")],
                             include_dirs = [os.path.join("lang", "c")],
                             sources = CParserSources)

# ______________________________________________________________________

PgenExtension = Extension("basil.parsing.pgen",
                          define_macros = [("MAJOR_VERSION", "0"),
                                           ("MINOR_VERSION", "1")],
                          sources = [os.path.join("parsing", "pgenmodule.c")])

# ______________________________________________________________________

setup(name = "Basil",
      version = "0.1",
      description = "Basil cross language support framework.",
      author = "Jon Riehl",
      author_email = "jriehl@spaceship.com",
      url = "http://wildideas.org/basil/",
      package_dir = {"basil" : ""},
      packages = ["basil",
                  "basil.xml",
                  "basil.utils",
                  "basil.visuals",
                  "basil.parsing",
                  "basil.modeling",
                  "basil.models",
                  "basil.models.uml",
                  "basil.models.grammar",
                  "basil.lang",
                  "basil.lang.c",
                  "basil.lang.python"],
      ext_modules = [PgenExtension, CParserExtension])

# ______________________________________________________________________
# End of basil/setup.py
