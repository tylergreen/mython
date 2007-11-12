#! /usr/bin/env python
# ______________________________________________________________________
"""Module PyExternals

This module defines a class library for representing Python code on a file
system.  Models built with this library may be committed to the file system,
thus generating Python source code.  (Beware: will currently overwrite any
existing code.)

Jonathan Riehl

$Id: PyExternals.py 2537 2004-01-11 00:12:42Z jriehl $
"""
# ______________________________________________________________________
# Module constants.

__DEBUG__ = 1

# ______________________________________________________________________
# Module imports.

import string, os

# ______________________________________________________________________

class ExtDirectory:
    """Class ExtDirectory
    Represents a subdirectory on the file system (and therefore a Python
    module assuming an __init__ file is included.)
    Contains ExtDirectory and ExtModule instances, contained by an ExtDirectory
    instance.
    """
    # ____________________________________________________________
    def __init__ (self, data = None, parent = None):
        """ExtDirectory.__init__
        Constructor for ExtDirectory.  Accepts the string name of the
        subdirectory and the containing ExtDirectory instance for parameters.
        """
        self.name = data
        self.modules = []
        self.subDirectories = []
        self.superDirectory = parent
        if parent != None:
            parent.subDirectories.append(self)

    # ____________________________________________________________
    def commitToFileSystem (self, currentDirStr = None):
        """ExtDirectory.commitToFileSystem
        Recusively traverses a model hierarchy, generating directories and
        Python files.
        """
        if currentDirStr == None:
            currentDirStr = os.getcwd()
        # Coerce the name of the top level directory to be congruent with the
        # current working directory or the specified output directory.
        oldName = self.name
        currentDirStr, self.name = os.path.split(currentDirStr)
        self.__handleDependencies()
        self.__commitToFileSystem(currentDirStr)
        self.name = oldName

    # ____________________________________________________________
    def __commitToFileSystem (self, currentDirStr):
        """ExtDirectory.__commitToFileSystem
        Private, recursive portion of the commitToFileSystem() method.
        """
        currentDirStr = os.path.join(currentDirStr, self.name)
        if not os.path.exists(currentDirStr):
            os.makedirs(currentDirStr)
        for module in self.modules:
            module.commitToFileSystem(currentDirStr)
        for subdir in self.subDirectories:
            subdir.__commitToFileSystem(currentDirStr)        

    # ____________________________________________________________
    def getLeaves (self, leafMap = None):
        """ExtDirectory.getLeaves
        Builds a flat namespace, mapping from all contained text element names
        to the corresponding ExtText instance.
        """
        if leafMap == None:
            leafMap = {}
        for module in self.modules:
            module.getLeaves(leafMap)
        for subdir in self.subDirectories:
            subdir.getLeaves(leafMap)
        return leafMap

    # ____________________________________________________________
    def __handleDependencies (self):
        """ExtDirectory.__handleDependencies
        Flattens the namespace, using getLeaves, then builds dependency
        links between ExtText instances based on string name references.
        This operation should be performed globally (ie. at the top directory
        instance) once.  Subordinate module and text output use the generated
        data to determine module dependencies and text item order.
        """
        leafMap = self.getLeaves()
        leafItems = leafMap.items()
        keys = leafMap.keys()
        if __DEBUG__:
            keys.sort()
            print keys
        for leafItem in leafItems:
            textName, text = leafItem
            for dependencyName in text.dependencyNames:
                text.addDependency(leafMap[dependencyName])

# ______________________________________________________________________

class ExtModule:
    """Class ExtModule
    Represents a Python module, expressed as a source file.  Contains ExtText
    instances, contained by an ExtDirectory instance.
    """
    # ____________________________________________________________
    def __init__ (self, data = None, parent = None):
        """ExtModule.__init__
        Constructor for the ExtModule class.  Accepts the Python module name
        (with out the file extension,) and the parent ExtDirectory instance
        as parameters.
        """
        self.name = data
        self.dependencies = []
        self.texts = []
        self.directory = parent
        if parent != None:
            parent.modules.append(self)

    # ____________________________________________________________
    def commitToFileSystem (self, currentDirStr = None):
        """ExtModule.commitToFileSystem
        Writes the Python module and its contents to a file named after the
        module name with a .py suffix.
        """
        if currentDirStr == None:
            currentDirStr = os.getcwd()
        currentDirStr = os.path.join(currentDirStr, self.name + ".py")
        file = open(currentDirStr, "w")
        file.write("#! /usr/bin/env python\n")
        # Generate module dependencies (if any.)
        if self.dependencies:
            file.write("# %s\n" % ("_" * 70))
            file.write("# Module imports\n\n")
            for dependency in self.dependencies:
                file.write("from %s import *\n" % dependency.fullName())
            file.write("\n")
        # Sort module texts based on internal dependencies.
        self.__sortTexts()
        # Generate module text.
        for text in self.texts:
            file.write(text.data)
        file.write("# %s\n" % ("_" * 70))
        file.write("# End of %s\n\n" % self.name)
        file.close()

    # ____________________________________________________________
    def addDependency (self, module):
        """ExtModule.addDependency
        Creates an import dependency from the called instance to the passed
        module.
        """
        if module not in self.dependencies:
            self.dependencies.append(module)

    # ____________________________________________________________
    def fullName (self):
        """ExtModule.fullName
        Generates the full name of the module, assuming only the global
        container directory is the only module visible from the Python
        module path.
        """
        directories = []
        crntDir = self.directory
        while crntDir:
            dirName = os.path.split(crntDir.name)[1]
            if dirName:
                directories.append(crntDir.name)
                crntDir = crntDir.superDirectory
            else:
                break
        directories.reverse()
        if self.name != "__init__":
            directories.append(self.name)
        return string.join(directories, ".")

    # ____________________________________________________________
    def buildNamespace (self, leafMap = None):
        """ExtModule.buildNamespace
        Builds a map from contained text instance names to the actual
        ExtText instance.
        """
        namespace = {}
        for text in texts:
            namespace[text.name] = text.buildNamespace(leafMap)
        return namespace

    # ____________________________________________________________
    def getLeaves (self, leafMap = None):
        """ExtModule.getLeaves
        Used to flatten the namespace into the passed dictionary.
        """
        for text in self.texts:
            leafMap[text.name] = text

    # ____________________________________________________________
    def __sortTexts (self):
        """ExtModule.__sortTexts
        Sorts the order of the module contents based on intra-module
        dependencies.  This is used to prevent a child class from being
        emitted before the parent class has been emitted.
        """
        sorted = 0
        nextTexts = []
        count = 0
        textCount = len(self.texts)
        while count < textCount and textCount > len(nextTexts):
            for text in self.texts:
                if text not in nextTexts:
                    append = 1
                    for dependency in text.dependencies:
                        if dependency not in nextTexts:
                            append = 0
                            break
                    if append:
                        nextTexts.append(text)
            count = count + 1
        if textCount > len(nextTexts):
            raise self, "Circular dependency in text listing"
        else:
            self.texts = nextTexts

# ______________________________________________________________________

class ExtText:
    """Class ExtText
    Represents a segment of Python code, allowing a name or a tag to be
    associated with the contained source.  Contained by an ExtModule instance.
    """
    # ____________________________________________________________
    def __init__ (self, name = None, parent = None):
        """ExtText.__init__
        Constructor for the ExtText class.  Accepts a string name or tag for
        the text (source code) contained, and the containing ExtModule
        instance as parameters.        
        """
        self.name = name
        self.data = ""
        self.dependencyNames = []
        self.dependencies = []
        self.module = parent
        if parent != None:
            parent.texts.append(self)

    # ____________________________________________________________
    def addDependency (self, text):
        """ExtText.addDependency
        Used to instantiate both inter-module and intra-module dependencies on
        the passed ExtText instance.
        """
        if text.module == self.module:
            if text not in self.dependencies:
                self.dependencies.append(text)
        else:
            self.module.addDependency(text.module)

    # ____________________________________________________________
    def buildNamespace (self, leafMap = None):
        """ExtText.buildNamespace
        Maps the text name/tag to the ExtText instance via the passed
        dictionary.  Returns the current instance.
        """
        if leafMap != None:
            leafMap[self.name] = self
        return self

# ______________________________________________________________________
# End of PyExternals.py
