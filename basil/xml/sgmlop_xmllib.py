#! /usr/env/bin python
# ______________________________________________________________________
"""Module sgmlop_xmllib.py

Orphaned step child of the XML-SIG, this module defines an sgmlop based XML
parser (which unlike the plain old xmllib or pyexpat allows DTD info in the
document.)  Requires the Python XML-SIG distribution. 

Originally by Fredrik Lundh

$Id: sgmlop_xmllib.py 2842 2004-01-20 07:44:52Z jriehl $
"""
# ______________________________________________________________________
# Module imports

import string, re

# XXX - Apparently one of my development machines is not configured to
# play well with where the XML-SIG stuff goes.  For now assume that sgmlop is
# in the Python path, and if that fails, look where the XML-SIG PC install put
# it...
try:
    import sgmlop
except ImportError:
    from xml.parsers import sgmlop

# standard entity defs

ENTITYDEFS = {
    'lt': '<',
    'gt': '>',
    'amp': '&',
    'quot': '"',
    'apos': '\''
    }

# XML parser base class -- find tags and call handler functions.
# Usage: p = XMLParser(); p.feed(data); ...; p.close().
# The dtd is defined by deriving a class which defines methods with
# special names to handle tags: start_foo and end_foo to handle <foo>
# and </foo>, respectively.  The data between tags is passed to the
# parser by calling self.handle_data() with some data as argument (the
# data may be split up in arbutrary chunks).  Entity references are
# passed by calling self.handle_entityref() with the entity reference
# as argument.

# --------------------------------------------------------------------
# accelerated XML parser

name = "[a-zA-Z_:][-a-zA-Z0-9._:]*"
ref = re.compile("[&%%](%s);" % name)

class FastXMLParser:

    # Interface -- initialize and reset this instance
    def __init__(self, verbose=0):
        self.verbose = verbose
        self.reset()

    # Interface -- reset this instance.  Loses all unprocessed data
    def reset(self):
        self.rawdata = ''
        self.stack = []
        self.lasttag = '???'
        self.nomoretags = 0
        self.literal = 0
        self.lineno = 1
        self.parser = sgmlop.XMLParser()
        self.feed = self.parser.feed
        self.parser.register(self)

    # For derived classes only -- enter literal mode (CDATA) till EOF
    def setnomoretags(self):
        self.nomoretags = self.literal = 1

    # For derived classes only -- enter literal mode (CDATA)
    def setliteral(self, *args):
        self.literal = 1

    # Interface -- feed some data to the parser.  Call this as
    # often as you want, with as little or as much text as you
    # want (may include '\n').  (This just saves the text, all the
    # processing is done by goahead().)
    def feed(self, data): # overridden by reset
        self.parser.feed(data)

    # Interface -- handle the remaining data
    def close(self):
        try:
            self.parser.close()
        finally:
            self.parser = None

    # Interface -- translate references
    def translate_references(self, data):
        newdata = []
        i = 0
        while 1:
            res = ref.search(data, i)
            if res is None:
                newdata.append(data[i:])
                return string.join(newdata, '')
            if data[res.end(0) - 1] != ';':
                self.syntax_error(self.lineno,
                                  '; missing after entity/char reference')
            newdata.append(data[i:res.start(0)])
            str = res.group(1)
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

    # Internal -- finish processing of start tag
    # Return -1 for unknown tag, 1 for balanced tag
    def finish_starttag(self, tag, attrs):
        self.stack.append(tag)
        try:
            method = getattr(self, 'start_' + tag)
        except AttributeError:
            self.unknown_starttag(tag, attrs)
            return -1
        else:
            self.handle_starttag(tag, method, attrs)
            return 1

    # Internal -- finish processing of end tag
    def finish_endtag(self, tag):
        if not tag:
            found = len(self.stack) - 1
            if found < 0:
                self.unknown_endtag(tag)
                return
        else:
            if tag not in self.stack:
                try:
                    method = getattr(self, 'end_' + tag)
                except AttributeError:
                    self.unknown_endtag(tag)
                return
            found = len(self.stack)
            for i in range(found):
                if self.stack[i] == tag: found = i
        while len(self.stack) > found:
            tag = self.stack[-1]
            try:
                method = getattr(self, 'end_' + tag)
            except AttributeError:
                method = None
            if method:
                self.handle_endtag(tag, method)
            else:
                self.unknown_endtag(tag)
            del self.stack[-1]

    # Overridable -- handle start tag
    def handle_starttag(self, tag, method, attrs):
        method(attrs)

    # Overridable -- handle end tag
    def handle_endtag(self, tag, method):
        method()

    # Example -- handle character reference, no need to override
    def handle_charref(self, name):
        try:
            if name[0] == 'x':
                n = string.atoi(name[1:], 16)
            else:
                n = string.atoi(name)
        except string.atoi_error:
            self.unknown_charref(name)
            return
        if not 0 <= n <= 255:
            self.unknown_charref(name)
            return
        self.handle_data(chr(n))

    # Definition of entities -- derived classes may override
    entitydefs = ENTITYDEFS

    # Example -- handle entity reference, no need to override
    def handle_entityref(self, name):
        table = self.entitydefs
        if table.has_key(name):
            self.handle_data(table[name])
        else:
            self.unknown_entityref(name)
            return

    # Example -- handle data, should be overridden
    def handle_data(self, data):
        pass

    # Example -- handle cdata, could be overridden
    def handle_cdata(self, data):
        pass

    # Example -- handle comment, could be overridden
    #def handle_comment(self, data):
    #   pass

    # Example -- handle processing instructions, could be overridden
    #def handle_proc(self, name, data):
    #   pass

    # Example -- handle special instructions, could be overridden
    #def handle_special(self, data):
    #   pass

    # Example -- handle relatively harmless syntax errors, could be overridden
    def syntax_error(self, lineno, message):
        raise RuntimeError, 'Syntax error at line %d: %s' % (lineno, message)

    # To be overridden -- handlers for unknown objects
    def unknown_starttag(self, tag, attrs): pass
    def unknown_endtag(self, tag): pass
    def unknown_charref(self, ref): pass
    def unknown_entityref(self, ref): pass

# ______________________________________________________________________
# There can be only one!

XMLParser = FastXMLParser

# --------------------------------------------------------------------
# test stuff

class TestXMLParser(XMLParser):

    def __init__(self, verbose=0):
        self.testdata = ""
        XMLParser.__init__(self, verbose)

    def handle_data(self, data):
        self.testdata = self.testdata + data
        if len(`self.testdata`) >= 70:
            self.flush()

    def flush(self):
        data = self.testdata
        if data:
            self.testdata = ""
            print 'data:', `data`

    def handle_cdata(self, data):
        self.flush()
        print 'cdata:', `data`

    def handle_proc(self, name, data):
        self.flush()
        print 'processing:',name,`data`

    def handle_special(self, data):
        self.flush()
        print 'special:',`data`

    def handle_comment(self, data):
        self.flush()
        r = `data`
        if len(r) > 68:
            r = r[:32] + '...' + r[-32:]
        print 'comment:', r

    def syntax_error(self, lineno, message):
        print 'error at line %d:' % lineno, message

    def unknown_starttag(self, tag, attrs):
        self.flush()
        if not attrs:
            print 'start tag: <' + tag + '>'
        else:
            print 'start tag: <' + tag,
            for name, value in attrs.items():
                print name + '=' + '"' + value + '"',
            print '>'

    def unknown_endtag(self, tag):
        self.flush()
        print 'end tag: </' + tag + '>'

    def unknown_entityref(self, ref):
        self.flush()
        print '*** unknown entity ref: &' + ref + ';'

    def unknown_charref(self, ref):
        self.flush()
        print '*** unknown char ref: &#' + ref + ';'

    def close(self):
        XMLParser.close(self)
        self.flush()

# ______________________________________________________________________

def test(args = None):
    import sys

    if not args:
        args = sys.argv[1:]

    if args and args[0] == '-s':
        args = args[1:]
        klass = XMLParser
    else:
        klass = TestXMLParser

    if args:
        file = args[0]
    else:
        file = 'test.xml'

    if file == '-':
        f = sys.stdin
    else:
        try:
            f = open(file, 'r')
        except IOError, msg:
            print file, ":", msg
            sys.exit(1)

    data = f.read()
    if f is not sys.stdin:
        f.close()

    x = klass()
    for c in data:
        x.feed(c)
    x.close()

# ______________________________________________________________________

if __name__ == '__main__':
    test()

# ______________________________________________________________________
# End of sgmlop_xmllib.py
