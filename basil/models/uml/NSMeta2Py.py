#! /usr/bin/env python
# ______________________________________________________________________
"""Module NSMeta2Py.py

Meta-model handler built using DTD2PyHandler.py from the NovoSoft UML metamodel
DTD.  Generates Python source.

$Id: NSMeta2Py.py,v 1.2 2001/08/07 01:46:37 jriehl Exp $
"""
# ______________________________________________________________________

import os, os.path, string
import PyExternals
from basil.modeling.BaseModelHandler import BaseModelHandler

# ______________________________________________________________________
class NSMetaModelHandler (BaseModelHandler):
    # ____________________________________________________________
    def handleModel (self, rootModelElement, args = None):
        """NSMetaModelHandler.handleModel
        Overloads base class main handler routine to perform various pre- and
        post-processing operations.
        """
        # Initialize any state variables.
        self.stack = []
        self.rootDirectory = None
        self.modules = []
        self.elementTextList = []
        self.superNameLists = []
        self.elementNameMap = {}
        # Create a flat namespace for the model.
        references = []
        self.namespace = self.__processNamespace(rootModelElement, references)
        # Add associations as potential attributes.
        self.__processReferences(references)
        # Walk the model and generate the external model.
        self.handleModelElement(rootModelElement)
        # Generate a factory class.
        self.createModelFactory()
        # Emit the external model.
        if len(args) == 0:
            crntDir = os.getcwd()
        else:
            crntDir = args[0]
        if not os.path.exists(crntDir):
            os.makedirs(crntDir)
        self.rootDirectory.commitToFileSystem(crntDir)

    # ____________________________________________________________
    def __processNamespace (self, modelElement, refList):
        """NSMetaModelHandler.__processNamespace
        Sets up the namespace map for return, then uses the recursive method
        __innerProcessNamespace() to do all the dirty work.
        """
        ns = {}
        self.__innerProcessNamespace(modelElement, ns, refList)
        return ns

    # ____________________________________________________________
    def __innerProcessNamespace (self, modelElement, ns, refList):
        """NSMetaModelHandler.__innerProcessNamespace
        """
        if hasattr(modelElement, "name"):
            ns[modelElement.name] = modelElement
        if modelElement.elementName == "association":
            refList.append(modelElement)
        for childElement in modelElement:
            self.__innerProcessNamespace(childElement, ns, refList)

    # ____________________________________________________________
    def __processReferences (self, refList):
        """NSMetaModelHandler.__processReferences
        """
        for association in refList:
            role1 = association[0]
            role2 = association[1]
            if self.namespace.has_key(role1.type):
                type1 = self.namespace[role1.type]
                if role2 not in type1:
                    type1.append(role2)
            if self.namespace.has_key(role2.type):
                type2 = self.namespace[role2.type]
                if role1 not in type2:
                    type2.append(role1)
    
    # ____________________________________________________________
    def createModelFactory (self):
        """NSMetaModelHandler.createModelFactory
        """
        # __________________________________________________
        # Process the attribute map to account for inheritance.
        for superTuple in self.superNameLists:
            elementName, superNameList = superTuple
            for superName in superNameList:
                self.elementNameMap[elementName].update(
                    self.elementNameMap[superName])
        # __________________________________________________
        # Get the __init__ module for the root package.
        rootModule = None
        for module in self.rootDirectory.modules:
            if module.name == "__init__":
                rootModule = module
        assert rootModule != None
        # __________________________________________________
        # Create a new code segment for the factory class and make it dependent
        # upon everything in the module (assuring it will be emitted last.)
        factoryText = PyExternals.ExtText("ModelFactory", rootModule)
        for textItem in rootModule.texts:
            if textItem != factoryText:
                factoryText.addDependency(textItem)
        # Import everything in the model.
        data = "# %s\n\n" % ("_" * 70)
        self.modules.remove(rootModule)
        for module in self.modules:
            data = "%simport %s\n" % (data, module.fullName()[2:])
        # XXX Make this tie into the directory argument.
        factoryName = "ModelFactory"
        data = (data + ("from basil.modeling.BaseModelFactory import "
                        "BaseModelFactory\n\n# %s\nclass %s "
                        "(BaseModelFactory):\n" % ("_" * 70, factoryName)))
        # Generate the constructor that defines the element map.
        data = (data + ("    # %s\n    def __init__ (self):\n"
                        "        self.elements = %s\n\n" %
                        ("_" * 60, `self.elementNameMap`)))
        # Generate creation methods for eveything in the model.
        for textItem in self.elementTextList:
            # XXX Need to add some assurance against name space collisions
            # as documented in the log (not to mention make this really
            # work...)
            textName = textItem.name
            if textItem.module != rootModule:
                # XXX...that [2:] is a hack...something is generating two
                # extra periods in the full name.
                textName = "%s.%s" % (textItem.module.fullName()[2:], textName)
            data = ("%s    # %s\n    def create%s (self, elementData):\n"
                    "        return self.__processElement(%s, elementData)\n\n"
                    % (data, "_" * 60,
                       string.upper(textItem.name[0]) + textItem.name[1:],
                       textName))
        factoryText.data = (data + ("# %s\ndef getModelFactory():\n     return"
                                    " %s\n\n" % ("_" * 70, factoryName)))

    # ____________________________________________________________
    def handleElement (self, modelElement):
        # Sort through actual and artificial child elements.
        superclasses = []
        references = []
        attributes = []
        attributeMap = {}
        for childElement in modelElement:
            if childElement.elementName == "superclass":
                superclasses.append(childElement)
            elif childElement.elementName == "role":
                references.append(childElement)
            else:
                attributes.append(childElement)
        extText = PyExternals.ExtText(modelElement.name, self.stack[-1])
        # __________________________________________________
        # Generate the top level class along with its superclasses.
        text = "# %s\nclass %s " % ("_" * 70, modelElement.name)
        if len(superclasses) > 0:
            text = text + " ("
            superNameList = []
            for superclass in superclasses[:-1]:
                text = text + superclass.type + ", "
                # Note the superclass name so the factory can look them up
                # when computing the attribute map.
                superNameList.append(superclass.type)
            text = text + superclasses[-1].type + ")"
            self.superNameLists.append((modelElement.name, superNameList))
        else:
            # This class must be a root class and should be derived from
            # UserList so that it can be internalized/externalized.
            text = text + " (UserList)"
        text = text + (":\n   elementName = \"%s\"\n   def __init__ (self):\n"
                       % modelElement.name)
        if len(superclasses) > 0:
            for superclass in superclasses:
                text = text + ("      %s.__init__(self)\n" % superclass.type)
                extText.dependencyNames.append(superclass.type)
        else:
            text = text + "      UserList.__init__(self)\n"
        # __________________________________________________
        # Create holder attributes for all element attributes.
        for attribute in attributes:
            text = text + ("      self.%s = None\n" % attribute.name)
            attributeMap[attribute.name] = attribute.name # XXX
        # __________________________________________________
        # Create holder variables for any navigable references.
        for reference in references:
            if reference.navigable == "true":
                if reference.kind == "ref":
                    initVal = "None"
                else:
                    initVal = "[]"
                text = text + ("      self.%s = %s\n" % (reference.name,
                                                         initVal))
                attributeMap[reference.name] = reference.name # XXX
        text = text + "\n\n"
        extText.data = text
        # __________________________________________________
        # Update data used by the factory class.
        self.elementTextList.append(extText)
        self.elementNameMap[modelElement.name] = attributeMap

    # ____________________________________________________________
    def handleEnumeration (self, modelElement):
        extText = PyExternals.ExtText(modelElement.name, self.stack[-1])
        self.elementTextList.append(extText)
        text = "# %s\nclass %s:\n" % ("_" * 70, modelElement.name)
        value = 1
        postText = ""
        for literal in modelElement:
            # XXX...note that there is a namespace collision with the Python
            # reserved words in the enumerations defined in the NSUML
            # metamodel, as a stop gap measure, all enumeration names are
            # preceeded with an underscore for now.
            text = text + ("   _%s = %d\n" % (literal.name, value))
            postText = postText + ("_%s = %s._%s\n" % (literal.name,
                                                       modelElement.name,
                                                       literal.name))
            value = value + 1
        text = text + "\n" + postText + "\n\n"
        extText.data = text

    # ____________________________________________________________
    def handlePackage (self, modelElement):
        """NSMetaModelHandler.handlePackage

        Processing method for handling package instances in a NSUML meta-model.
        Note that the root directory is established by the first package
        processed.  This is because a NSUML meta-model is defined in the DTD
        to only contain a single package.  It is assumed that the root package
        is this initial package for the entire model.  For this reason, the
        handler may not be suitable for use as a partial processor (go make
        another handler then.)
        """
        subordinatePackages = []
        subordinateElements = []
        for childElement in modelElement:
            if childElement.elementName == modelElement.elementName:
                subordinatePackages.append(childElement)
            else:
                subordinateElements.append(childElement)
        if len(subordinatePackages) > 0:
            dirName = modelElement.name
            if dirName == "root":
                dirName = "."
            if self.rootDirectory == None:
                directory = PyExternals.ExtDirectory(dirName)
                self.rootDirectory = directory
            else:
                directory = PyExternals.ExtDirectory(dirName, self.stack[-1])
            self.stack.append(directory)
            module = PyExternals.ExtModule("__init__", directory)
            self.modules.append(module)
            self.stack.append(module)
            importText = PyExternals.ExtText("imports", self.stack[-1])
            importText.data = "from UserList import UserList\n\n"
            for child in subordinateElements:
                self.handleModelElement(child)
            del self.stack[-1]
            for child in subordinatePackages:
                self.handleModelElement(child)
            del self.stack[-1]
        else:
            moduleName = modelElement.name
            if moduleName == "root":
                moduleName = "__init__"
            module = PyExternals.ExtModule(moduleName, self.stack[-1])
            self.modules.append(module)
            self.stack.append(module)
            importText = PyExternals.ExtText("imports", self.stack[-1])
            importText.data = "from UserList import UserList\n\n"
            for child in subordinateElements:
                self.handleModelElement(child)
            del self.stack[-1]
    
    # ____________________________________________________________
    def handleDatatype (self, modelElement):
        self.handleElement(modelElement)

    # ____________________________________________________________
    def handleMetamodel (self, modelElement):
        # Insert prefix actions here.
        for childElement in modelElement:
            self.handleModelElement(childElement)
        # Insert postfix actions here.

    # ____________________________________________________________
    def handlePrimitive (self, modelElement):
        extText = PyExternals.ExtText(modelElement.name, self.stack[-1])
        self.elementTextList.append(extText)
        extText.data = ("# %s\nclass %s (UserList):\n    elementName = \"%s\""
                        "\n\n\n" % ("_" * 70, modelElement.name,
                                    modelElement.name))

# ______________________________________________________________________
def getModelHandler ():
    return NSMetaModelHandler

# ______________________________________________________________________
# End of NSMetaModelHandler.py

