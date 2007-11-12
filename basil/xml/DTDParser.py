#! /usr/bin/env python
# ______________________________________________________________________
"""Module DTDParser.py

Defines a parser for extracting document type definition information from
either a DTD or XML document.

Test usage:
        % DTDParser.py [-v|-g] <document.dtd>

        -v Prints the map of element names to element declaration parse trees.
        -g Opens a graphical tree display of the DTD data.

Jonathan Riehl

$Id: DTDParser.py 2537 2004-01-11 00:12:42Z jriehl $
"""
# ______________________________________________________________________
# Module constants.

__DEBUG__ = 0

# ______________________________________________________________________
# Module imports.

import string, re
from basil.xml.sgmlop_xmllib import XMLParser

if __DEBUG__:
    import pprint

# ______________________________________________________________________

class DTDMatchStrings:
    """Class DTDMatchStrings
    Container namespace for a set of regular expression matching various
    XML special tag substrings (where special tags begin with <!...)
    """
    # ____________________________________________________________
    # XML BASICS
    S = "[ \t\r\n]+"
    Sopt = "[ \t\r\n]*"
    reSopt = re.compile(Sopt)
    NameChar = "[-a-zA-Z0-9._:]"
    Name = "[a-zA-Z_:]%s*" % NameChar
    reName = re.compile(Name)
    Nmtoken = "%s+" % NameChar
    reNmtoken = re.compile(Nmtoken)
    Nmtokens = "%s(%s%s)*" % (Nmtoken, S, Nmtoken)
    # ____________________________________________________________
    # ENTITIES
    EntityRef = "&%s;" % Name
    PEReference = "%%%s;" % Name
    Reference = "(%s|%s)" % (EntityRef, PEReference)
    reReference = re.compile(Reference)
    # ____________________________________________________________
    # ATTRS
    StringType = "CDATA"
    TokenizedType = "ID|IDREF|IDREFS|ENTITY|ENTITIES|NMTOKEN|NMTOKENS"
    reTokenizedType = re.compile(TokenizedType)
    Enumeration = "\(%s%s(%s\|%s%s)*%s\)" % (Sopt, Nmtoken, Sopt, Sopt,
                                               Nmtoken, Sopt)
    NotationType = "NOTATION%s\(%s%s(%s\|%s%s)*%s\)" % (S, Sopt, Name,
                                                        Sopt, Sopt, Name,
                                                        Sopt)
    reNotationType = re.compile(NotationType)
    EnumeratedType = "%s|%s" % (NotationType, Enumeration)
    AttType = "(%s|%s|%s)" % (StringType, TokenizedType, EnumeratedType)
    reAttType = re.compile(AttType)
    AttValue = "\"([^<&\"]|%s)*\"|'([^<&']|%s)*'" % (Reference, Reference)
    DefaultDecl = "#REQUIRED|#IMPLIED|((#FIXED%s)?%s)" % (S, AttValue)
    reDefaultDecl = re.compile(DefaultDecl)
    AttDef = "%s(%s)%s(%s)%s(%s)" % (S, Name, S, AttType, S, DefaultDecl)
    reAttDef = re.compile(AttDef)
    AttlistDecl = "%s(%s)((%s)*)%s" % (Sopt, Name, AttDef, Sopt)
    reAttlistDecl = re.compile(AttlistDecl)
    # ____________________________________________________________
    # ELEMENTS
    ContentPostfix = "[?*+]"
    reContentPostfix = re.compile(ContentPostfix)
    Mixed = "[(]%s#PCDATA((.|\n)*)" % Sopt
    reMixed = re.compile(Mixed)
    ContentSpec = "EMPTY|ANY|%s|([(](.|\n)*)" % (Name,)
    reContentSpec = re.compile(ContentSpec)
    ElementDecl = "%s(%s)%s(%s)" % (Sopt, Name, S, ContentSpec)
    reElementDecl = re.compile(ElementDecl)

# ______________________________________________________________________

class DTDParser (XMLParser):
    """Class DTDParser
    """
    # ____________________________________________________________
    def __init__ (self):
        """DTDParser.__init__
        Happy little constructor of the DTDParser class.  No inputs.
        """
        XMLParser.__init__(self)
        self.name = DTDMatchStrings.reName
        self.ref = DTDMatchStrings.reReference
        self.quote = re.compile("[\"']")

    # ____________________________________________________________
    def reset (self):
        """DTDParser.reset
        Note that this overloads the XMLParser.reset() method.
        Called by the base class constructor, this method adds a private
        stack for the DTD element parse tree, and a map for the DTD
        elements.
        """
        XMLParser.reset(self)
        self.__stack = []
        self.elements = {}

    # ____________________________________________________________
    # Interface -- translate references
    def translate_references(self, data):
        """DTDParser.translate_references
        Overloads the XMLParser.translate_references() method.
        Adds debugging information, and matches the reference differently
        than XMLParser.translate_references().
        """
        newdata = []
        i = 0
        while 1:
            res = self.ref.search(data, i)
            if res is None:
                newdata.append(data[i:])
                return string.join(newdata, '')
            if data[res.end(0) - 1] != ';':
                self.syntax_error(self.lineno,
                                  '; missing after entity/char reference')
            newdata.append(data[i:res.start(0)])
            str = res.group(0)[1:-1]
            if __DEBUG__:
                print "translate_references()", str
            if str[0] == '#':
                if str[1] == 'x':
                    newdata.append(chr(string.atoi(str[2:], 16)))
                else:
                    newdata.append(chr(string.atoi(str[1:])))
            else:
                try:
                    newdata.append(self.entitydefs[str])
                except KeyError:
                    # can't do it, so keep the entity ref in
                    newdata.append('&' + str + ';')
            i = res.end(0)

    # ____________________________________________________________
    # PRIVATE STACK OPERATORS
    def __name (self, data):
        """DTDParser.__name
        Pushes and pops a leaf Name node, thus adding it as a child node of the
        top node.  Accepts the string data of the name, return the leaf tree
        node created.
        """
        node = ("Name", data)
        self.__push(node)
        return self.__pop()

    # ____________________________________________________________
    def __push (self, nodeData):
        """DTDParser.__push
        Pushes a node onto the private DTD stack.  Input node data is expected
        to be a tuple of strings.  Returns None.
        """
        node = (nodeData, [])
        self.__stack[-1][1].append(node)
        self.__stack.append(node)

    # ____________________________________________________________
    def __pop (self):
        """DTDParser.__pop
        Pops a node off the top of the private DTD stack.  No inputs, returns
        the popped node tuple.
        """
        top = self.__stack[-1]
        del self.__stack[-1]
        return top

    # ____________________________________________________________
    def __set (self, nodeData):
        """DTDParser.__set
        Resets the private stack using the input node data (a tuple of
        strings.)  Returns None.
        """
        self.__stack = [(nodeData, [])]

    # ____________________________________________________________
    # ENTITY DECLARATION HANDLER
    def handle_entity (self, data):
        """DTDParser.handle_entity
        """
        matchName = self.name.search(data).group(0)
        stringStop = stringStart = self.quote.search(data).start() + 1
        quoteMatch = self.quote.search(data, stringStop)
        while quoteMatch != None:
            stringStop = quoteMatch.start()
            quoteMatch = self.quote.search(data, stringStop + 1)
        self.entitydefs[matchName] = data[stringStart:stringStop]

    # ____________________________________________________________
    # ELEMENT DECLARATION HANDLING METHODS
    def contentParticle (self, data, index):
        """DTDParser.contentParticle
        Parse a content particle (as defined in the XML 1.0 spec.)
        """
        childNodes = []
        if data[index] == "(":
            primaryChild, index = self.choiceOrSequence(data, index)
        else:
            nameObj = DTDMatchStrings.reName.search(data, index)
            assert nameObj != None
            primaryChild = (("Name", nameObj.group(0)), [])
            index = nameObj.end()
        childNodes.append(primaryChild)
        if data[index] in "*?+":
            childNodes.append(((data[index],),[]))
            index = index + 1
        return (("cp",), childNodes), index

    # ____________________________________________________________
    def choiceOrSequence (self, data, index):
        """DTDParser.choiceOrSequence
        Parse an element declarator substring that may either be a sequence of
        content particles or a choice of content particles.
        """
        childNodes = []
        nodeType = None
        assert data[index] == "("
        index = index + 1
        done = None
        while (index < len(data)):
            index = DTDMatchStrings.reSopt.match(data, index).end()
            childNode, index = self.contentParticle(data, index)
            childNodes.append(childNode)
            index = DTDMatchStrings.reSopt.match(data, index).end()
            assert data[index] in ")|,"
            if data[index] == "|":
                assert nodeType in [None, "Choice"]
                nodeType = "Choice"
                index = index + 1
            elif data[index] == ",":
                assert nodeType in [None, "Sequence"]
                nodeType = "Sequence"
                index = index + 1
            else:
                if nodeType == None:
                    nodeType = "Sequence"
                index = index + 1
                break
        assert index <= len(data)
        return ((nodeType,), childNodes), index

    # ____________________________________________________________
    def children (self, data):
        """DTDParser.children
        Process element content when that content consists of child nodes.
        Warning - here we stop doing recursive descent and start taking in
        string data instead of regular expression match objects.
        """
        childNodes = []
        childNode, index = self.choiceOrSequence(data, 0)
        childNodes.append(childNode)
        tailMatch = DTDMatchStrings.reContentPostfix.search(data, index)
        if tailMatch != None:
            childNodes.append(((tailMatch.group(0),), []))
        return (("Children",), childNodes)

    # ____________________________________________________________
    def mixed (self, matchObj):
        """DTDParser.mixed
        Parse mixed element content declarations.  Note that the * is not
        parsed since it is implicit if the Mixed AST node has more than one
        child.
        """
        self.__push(("Mixed",))
        self.__push(("#PCDATA",))
        self.__pop()
        data = matchObj.group(1)
        index = DTDMatchStrings.reSopt.match(data).end()
        while (index < len(data)) and (data[index] == "|"):
            index = index + 1
            nameSearch = DTDMatchStrings.reName.search(data, index)
            assert nameSearch != None
            self.__name(nameSearch.group(0))
            index = nameSearch.end()
            index = DTDMatchStrings.reSopt.match(data, index).end()
        assert data[index] == ")"
        return self.__pop()

    # ____________________________________________________________
    def contentSpec (self, matchObj):
        """DTDParser.contentSpec
        Parse the content specification for an element declaration.
        """
        self.__push(("ContentSpec",))
        data = matchObj.group(0)
        if data[0] == '(':
            matchObj1 = DTDMatchStrings.reMixed.search(data)
            if matchObj1 != None:
                self.mixed(matchObj1)
            else:
                # Manually add the child to the top node.
                self.__stack[-1][1].append(self.children(data))
        else:
            self.__push((data, ))
            self.__pop()
        return self.__pop()

    # ____________________________________________________________
    def elementDecl (self, matchObj):
        """DTDParser.elementDecl
        Parse an element declaration.
        """
        data = matchObj.group(2)
        self.__set(("ElementDecl",))
        matchObj1 = DTDMatchStrings.reContentSpec.search(data)
        self.contentSpec(matchObj1)
        return self.__pop()
        
    # ____________________________________________________________
    def handle_element (self, data):
        """DTDParser.handle_element
        """
        if __DEBUG__:
            print "handle_element():", data
        data = self.translate_references(data)
        matchObj = DTDMatchStrings.reElementDecl.search(data)
        if matchObj != None:
            elementName = matchObj.group(1)
            elementData = self.elementDecl(matchObj)
            if __DEBUG__:
                print "handle_element():", elementName
                pprint.pprint(elementData)
            self.addElementData(elementName, elementData)

    # ____________________________________________________________
    # ELEMENT ATTRIBUTE DECLARATION HANDLING METHODS
    def attlistDecl (self, matchObj):
        """DTDParser.attlistDecl
        """
        data = matchObj.group(2)
        if __DEBUG__:
            print "attlistDecl():", data
        self.__set(('AttlistDecl',))
        matchObj = DTDMatchStrings.reAttDef.search(data)
        while matchObj != None:
            self.attDef(matchObj)
            matchObj = DTDMatchStrings.reAttDef.search(data, matchObj.end())
        return self.__pop()

    # ____________________________________________________________
    def attDef (self, matchObj):
        """DTDParser.attDef
        """
        if __DEBUG__:
            print "attDef()", matchObj.group(0)
        self.__push(("AttDef",))
        self.__name(matchObj.group(1))
        matchObj1 = DTDMatchStrings.reAttType.search(matchObj.string,
                                                     matchObj.end(1))
        self.attType(matchObj1)
        matchObj2 = DTDMatchStrings.reDefaultDecl.search(matchObj.string,
                                                         matchObj1.end())
        self.defaultDecl(matchObj2)
        self.__pop()

    # ____________________________________________________________
    def attType (self, matchObj):
        """DTDParser.attType
        """
        data = matchObj.group(0)
        if __DEBUG__:
            print "attType()", data
        self.__push(("AttType",))
        if data == "CDATA":
            self.stringType(matchObj)
        else:
            matchObj1 = DTDMatchStrings.reTokenizedType.search(data)
            if matchObj1 != None:
                self.tokenizedType(matchObj1)
            else:
                self.enumeratedType(matchObj)
        self.__pop()

    # ____________________________________________________________
    def stringType (self, matchObj):
        """DTDParser.stringType
        """
        self.__push(("StringType", "CDATA"))
        self.__pop()

    # ____________________________________________________________
    def tokenizedType (self, matchObj):
        """DTDParser.tokenizedType
        """
        self.__push(("TokenizedType", matchObj.group(0)))
        self.__pop()

    # ____________________________________________________________
    def enumeratedType (self, matchObj):
        """DTDParser.enumeratedType
        """
        data = matchObj.group(0)
        if __DEBUG__:
            print "enumeratedType()", data
        self.__push(("EnumeratedType",))
        matchObj1 = DTDMatchStrings.reNotationType.search(data)
        if matchObj1 != None:
            self.notationType(matchObj1)
        else:
            self.enumeration(matchObj)
        self.__pop()
        
    # ____________________________________________________________
    def notationType (self, matchObj):
        """DTDParser.notationType
        """
        data = matchObj.group(0)
        if __DEBUG__:
            print "notationType()", data
        # XXX Punt for now.
        self.__push(("NotationType", data))
        self.__pop()

    # ____________________________________________________________
    def enumeration (self, matchObj):
        """DTDParser.enumeration
        """
        data = matchObj.group(0)
        if __DEBUG__:
            print "enumeration()", data
        self.__push(("Enumeration",))
        nmtokenMatch = DTDMatchStrings.reNmtoken.search(data)
        while nmtokenMatch != None:
            if __DEBUG__:
                print "enumeration() -- Nmtoken", nmtokenMatch.group(0)
            self.__push(("Nmtoken", nmtokenMatch.group(0)))
            self.__pop()
            end = nmtokenMatch.end(0)
            nmtokenMatch = DTDMatchStrings.reNmtoken.search(data, end)
        self.__pop()
    
    # ____________________________________________________________
    def defaultDecl (self, matchObj):
        """DTDParser.defaultDecl
        """
        data = matchObj.group(0)
        if __DEBUG__:
            print "defaultDecl()", data
        self.__push(("DefaultDecl", data))
        self.__pop()

    # ____________________________________________________________
    def handle_attlist (self, data):
        """DTDParser.handle_attlist
        """
        if __DEBUG__:
            print "handle_attlist():", data
        data = self.translate_references(data)
        matchObj = DTDMatchStrings.reAttlistDecl.search(data)
        if matchObj != None:
            elementName = matchObj.group(1)
            if __DEBUG__:
                print "handle_attlist():", elementName
            elementData = self.attlistDecl(matchObj)
            self.addElementData(elementName, elementData)

    # ____________________________________________________________
    def addElementData (self, elementName, elementData):
        """DTDParser.addElementData
        """
        if self.elements.has_key(elementName):
            self.elements[elementName].append(elementData)
        else:
            self.elements[elementName] = [elementData]
    
    # ____________________________________________________________
    # DISPATCH HANDLER FOR ANY SPECIAL XML CODE (such as DTD data...)
    specialDispatch = {
        "ENTITY" : handle_entity,
        "ELEMENT" : handle_element,
        "ATTLIST" : handle_attlist}

    # ____________________________________________________________
    def handle_special (self, data):
        """DTDParser.handle_special
        """
        firstSpace = string.find(data, " ")
        if firstSpace:
            specialType = data[:firstSpace]
            if self.specialDispatch.has_key(specialType):
                self.specialDispatch[specialType](self, data[firstSpace+1:])

# ______________________________________________________________________

def main ():
    import sys, time
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    args = sys.argv[1:]
    text = open(args[-1]).read()
    t0 = time.time()
    parser = DTDParser()
    parser.feed(text)
    parser.close()
    t1 = time.time()
    lines = string.count(text, "\n")
    sys.stderr.write("Choked down %d lines in %f sec(s.)\n" % (lines,
                                                               (t1 - t0)))
    sys.stderr.flush()
    # ____________________________________________________________
    if "-g" in args:
        # Process the element map into a list of tree nodes.
        childNodes = []
        items = parser.elements.items()
        for item in items:
            childNodes.append((item[0], item[1]))
        # Now show it.
        import Tkinter
        from basil.visuals import TreeBox
        tk = Tkinter.Tk()
        can = TreeBox.TreeBox(tk, (args[-1], childNodes))
        can.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        can.enableDefaultHandlers()
        tk.mainloop()
    elif "-v" in args:
        import pprint
        pprint.pprint(parser.elements)
    
# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of DTDParser.py
