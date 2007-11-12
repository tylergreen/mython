#! /usr/bin/env python
# ______________________________________________________________________
"""Module XML2Tree.py

Defines an XML parser based on pyexpat that converts input XML into an
AST-like format of nested tuples and lists.  Inspired by Greg Stein's
qp_xml (but this lacks the overhead of constructing and interfacing with
objects.)

Test usage:
        % XML2Tree.py [-v|-g] <document.xml>

        -v Pretty prints the XML AST generated for the input document.
        -g Opens a graphical tree display of the XML AST.

Jonathan Riehl

$Id: XML2Tree.py,v 1.2 2001/08/07 01:47:33 jriehl Exp $
"""
# ______________________________________________________________________
# Module imports

try:
    import pyexpat
except:
    from xml.parsers import pyexpat
import string

# ______________________________________________________________________

class XML2TreeParser:
    """Class XML2TreeParser
    """
    # ____________________________________________________________
    def __init__ (self):
        """XML2TreeParser.__init__
        """
        self.reset()

    # ____________________________________________________________
    def reset (self):
        """XML2TreeParser.reset
        """
        self.treeRoot = ((None, {}), [])
        self.stack = [self.treeRoot]

    # ____________________________________________________________
    def start (self, name, attrs):
        """XML2TreeParser.start
        """
        # XXX Check to see if attrs is a list or a dictionary.
        # Is this a version thing with pyexpat or am I just on crack?
        if type(attrs) == type([]):
            index = 0
            attrDict = {}
            while index < len(attrs):
                attrDict[attrs[index]] = attrs[index + 1]
                index = index + 2
            attrs = attrDict
        treeNode = ((name, attrs), [])
        self.stack[-1][1].append(treeNode)
        self.stack.append(treeNode)

    # ____________________________________________________________
    def end (self, name):
        """XML2TreeParser.end
        """
        del self.stack[-1]

    # ____________________________________________________________
    def cdata (self, data):
        """XML2TreeParser.cdata
        """
        data = string.strip(data)
        if len(data) > 0:
            nodeAttrs = self.stack[-1][0][1]
            if not nodeAttrs.has_key("#CDATA"):
                nodeAttrs["#CDATA"] = data[:]
            else:
                nodeAttrs["#CDATA"] = "%s%s" % (nodeAttrs["#CDATA"], data)

    # ____________________________________________________________
    def parse (self, input):
        """XML2TreeParser.parse
        """
        self.reset()
        p = pyexpat.ParserCreate()
        p.StartElementHandler = self.start
        p.EndElementHandler = self.end
        p.CharacterDataHandler = self.cdata
        if type(input) == type(""):
            p.Parse(input, 1)
        else:
            text = input.read()
            p.Parse(text, 1)
        return self.stack[0]

# ______________________________________________________________________

def main ():
    import sys, time
    if len(sys.argv) < 2:
        print __doc__
        sys.exit(1)
    args = sys.argv[1:]
    text = open(args[-1]).read()
    sys.stderr.write("Please wait, processing file...")
    sys.stderr.flush()
    t0 = time.time()
    parser = XML2TreeParser()
    parser.parse(text)
    t1 = time.time()
    sys.stderr.write("finished (%d lines in %f seconds.)\n" %
                     (string.count(text,"\n"),(t1 - t0)))
    sys.stderr.flush()
    # ____________________________________________________________
    # Display anything, if asked to.
    if "-g" in args:
        import Tkinter
        from basil.visuals import TreeBox
        tk = Tkinter.Tk()
        can = TreeBox.TreeBox(tk, parser.treeRoot)
        can.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        can.enableDefaultHandlers()
        tk.mainloop()
    elif "-v" in args:
        import pprint
        pprint.pprint(parser.treeRoot)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of XML2Tree.py
