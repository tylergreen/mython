#! /usr/bin/env python
# ______________________________________________________________________
"""Script mycmodulesetup.py

Example of how to build mycmodule.c using distutils.  Usage:
    $ python mycmodulesetup.py build

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

from distutils.core import setup, Extension

# ______________________________________________________________________
# Module data

mycmodule_ext = Extension('mycmodule', sources = ['mycmodule.c'])

# ______________________________________________________________________
# Main (distutils) routine

if __name__ == "__main__":
    setup(name = 'mycmodule', version = '1.0',
          description = 'This is a test extension package.',
          ext_modules = [mycmodule_ext])

# ______________________________________________________________________
# End of mycmodulesetup.py
