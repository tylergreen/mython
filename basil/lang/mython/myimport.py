#! /usr/bin/env python
# ______________________________________________________________________
"""myimport.py

Importer for Mython modules.

This was heavily 'inspired' by the MetaPython importer, but has been
hacked to never return a loader.  Instead, when it finds a Mython
file, it compiles it to a .pyc file which the Python importer will
pick up on.

Jonathan Riehl
"""
# ______________________________________________________________________
# Module imports

import os
import sys
import stat

from basil.lang.mython import mybuiltins

# ______________________________________________________________________
# Module functions

def install_import_hook ():
    """Install the Mython import hook into sys.meta_path."""
    if MythonImporter not in sys.meta_path:
        sys.meta_path.append(MythonImporter)

# ______________________________________________________________________

def try_compiling_file (my_file_basename):
    """Given an extensionless path to a Mython file, build a .pyc for
    it if it has changed.

    Returns the compile environment if MyFront was used, None otherwise.

    Caveats:

    * This does not pick up compile time dependencies.  Supporting
      this will require adding some metadata to Mython modules that
      records compile-time dependencies, and cross checking those.

    * This does not currently handle .pyo files, so it is expected to
      fail when the -O flag is used."""
    my_file_cand = os.path.extsep.join((my_file_basename, "my"))
    if os.path.exists(my_file_cand):
        pyc_file_name = os.path.extsep.join((my_file_basename, "pyc"))
        if os.path.exists(pyc_file_name):
            my_file_mtime = os.stat(my_file_cand)[stat.ST_MTIME]
            pyc_file_mtime = os.stat(pyc_file_name)[stat.ST_MTIME]
            if pyc_file_mtime <= my_file_mtime:
                return mybuiltins.mycompile_file_to_pyc(my_file_cand)
        else:
            return mybuiltins.mycompile_file_to_pyc(my_file_cand)
    return None

# ______________________________________________________________________
# Module classes

class MythonImporter (object):
    """A module finder class for locating .my files."""

    @staticmethod
    def find_module (fullname, path = None):
        # So here is a quick hack, just generate the .pyc file, and
        # say we didn't find anything.
        fullname_rsplit = fullname.rsplit(".", 1)
        if len(fullname_rsplit) == 2:
            parent_name, child_name = fullname.rsplit(".", 1)
            if parent_name in sys.modules:
                parent_package = sys.modules[parent_name]
                try_compiling_file(os.path.join(parent_package.__path__[0],
                                                child_name))
        else:
            for dir_path in sys.path:
                my_basename_cand = os.path.join(dir_path, fullname_rsplit[-1])
                if try_compiling_file(my_basename_cand) is not None:
                    break

# ______________________________________________________________________
# End of myimport.py
