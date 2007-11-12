#! /usr/bin/env python
# ______________________________________________________________________
"""Module Visitor

Implements the AbstractVisitor and TreeVisitor classes.

Jonathan Riehl

$Id: Visitor.py 12580 2005-05-19 20:10:21Z jriehl $
"""
# ______________________________________________________________________
# Module imports

# ______________________________________________________________________
# Module data

__DEBUG__ = False

flags = []

# ______________________________________________________________________
# Class definitions

class ENTER (object):
    """The ENTER class is used to send the signal that the element is being
    seen for the first time (acting as a cue for prefix.
    """
    pass

flags.append(ENTER)

# ______________________________________________________________________

class EXIT (object):
    """The EXIT class is used to signal that the element is being seen for
    the last time (acting as a cue for postfix actions.)
    """
    pass

flags.append(EXIT)

# ______________________________________________________________________

class DUPLICATE (object):
    """The DUPLICATE class is used to signal that the element is being seen
    again (and the elements being visited are either a DAG or a graph.)
    """
    pass

flags.append(DUPLICATE)

# ______________________________________________________________________

def only (*keepFlags):
    """only()
    Generate a flag mask that will only permit the passed flags through.
    """
    global flags
    retVal = []
    for flag in flags:
        if flag not in keepFlags:
            retVal.append(flag)
    return set(retVal)

# ______________________________________________________________________

class AbstractVisitor (object):
    """Class AbstractVisitor
    """
    # ____________________________________________________________
    def __init__ (self, target, mask = None):
        """AbstractVisitor.__init__()
        Constructor for the AbstractVisitor class. The mask argument should
        either be a set or a sequence that will be turned into a set.
        By default no visitation 'signals' are masked.
        """
        self.target = target
        if mask == None:
            mask = set()
        elif type(mask) in (list, tuple):
            mask = set(mask)
        self.mask = mask
        self.reset()

    # ____________________________________________________________
    def __iter__ (self):
        """AbstractVisitor.__iter__()
        Creates a generator that calls self.next() until the StopIteration
        exception is raised (which must be done by child classes.)
        """
        while True:
            yield self.next()

    # ____________________________________________________________
    def next (self):
        """AbstractVisitor.next()
        """
        raise NotImplementedError("Child must override next().")

    # ____________________________________________________________
    def up (self):
        """AbstractVisitor.up()
        """
        raise NotImplementedError("Child must override up().")

    # ____________________________________________________________
    def reset (self):
        """AbstractVisitor.reset()
        """
        raise NotImplementedError("Child must override reset().")

# ______________________________________________________________________

class IterVisitor (AbstractVisitor):
    """Class IterVisitor
    """
    # ____________________________________________________________
    def reset (self):
        """IterVisitor.reset()
        """
        self.visited = set()
        self.cursor = [(None, self.target)]

    # ____________________________________________________________
    def getIterForElem (self, elem):
        """IterVisitor.getIterForElem()
        By default, just calls iter() on the passed element.  Can be
        overridden by subclasses to handle specific kinds of elements,
        or ignore elements that aren't iterable.
        """
        return iter(elem)

    # ____________________________________________________________
    def _next (self):
        """IterVisitor._next()
        """
        if __DEBUG__:
            print "IterVisitor._next():", self.cursor
        retVal = None
        if len(self.cursor) > 0:
            cIter, cTarget = self.cursor[-1]
            if cIter == None:
                # This should only happen just after a reset.
                cIter = self.getIterForElem(cTarget)
                self.cursor[-1] = (cIter, cTarget)
                retVal = ([ENTER], cTarget)
            else:
                try:
                    nextTarget = cIter.next()
                    retVal = ([ENTER], nextTarget)
                    self.cursor.append((iter(nextTarget), nextTarget))
                    if nextTarget in self.visited:
                        retVal[0].append(DUPLICATE)
                    else:
                        self.visited.add(nextTarget)
                except StopIteration:
                    if __DEBUG__:
                        print "IterVisitor._next(): StopIteration", cIter
                    del self.cursor[-1]
                    retVal = ([EXIT], cTarget)
        else:
            raise StopIteration
        if __DEBUG__:
            print "IterVisitor._next() -> ", retVal
        return retVal

    # ____________________________________________________________
    def next (self):
        """IterVisitor.next()
        Implements a next() method similar to the next() method of an iter
        object.  This in turn calls the _next() method until an element is
        visited that is not masked.
        """
        if __DEBUG__:
            print "IterVisitor.next():", self.cursor
        while True:
            retVal = self._next()
            flags, target = retVal
            maskedFlags = self.mask.intersection(flags)
            if len(maskedFlags) == 0:
                break
            elif DUPLICATE in maskedFlags:
                # Silently back out of duplicated visitations.
                self.up()
        return retVal

    # ____________________________________________________________
    def up (self):
        """IterVisitor.up()
        """
        if len(self.cursor) > 0:
            del self.cursor[-1]
        else:
            raise StopIteration

# ______________________________________________________________________

class TreeVisitor (IterVisitor):
    """Class TreeVisitor
    Subclass of the IterVisitor class.  Overrides getIterForElem() to handle
    tree representation:
    tree := (payload, [tree...])
    """
    # ____________________________________________________________
    def getIterForElem (self, elem):
        """TreeVisitor.getIterForElem()
        """
        return iter(elem[1])

# ______________________________________________________________________

class SafeIterVisitor (IterVisitor):
    """Class SafeIterVisitor
    Subclass of the IterVisitor class.  Overrides getIterForElem() to handle
    elements that are not iterable.
    """
    # ____________________________________________________________
    def getIterForElem (self, elem):
        """SafeIterVisitor.getIterForElem()
        """
        try:
            return iter(elem)
        except:
            # Assume that the exception is:
            # TypeError("iteration over non-sequence")
            pass
        return iter([])

# ______________________________________________________________________
# Main (test) routine

def main ():
    # ____________________________________________________________
    class BasilList (list):
        def __repr__ (self):
            return "0x%x %s" % (id(self), list.__repr__(self))
        def __hash__ (self):
            return hash(id(self))
    # ____________________________________________________________
    def doVariousTests (target, *baseMask):
        print "_" * 70
        print "NORMAL"
        iv = IterVisitor(target, baseMask)
        for f, n in iv:
            print f, n
        print "_" * 70
        print "PREFIX"
        iv1 = IterVisitor(target, only(ENTER))
        for f, n in iv1:
            print f, n
        print "_" * 70
        print "POSTFIX"
        iv2 = IterVisitor(target, only(EXIT))
        for f, n in iv2:
            print f, n
        print "_" * 70
    # ____________________________________________________________
    # Tree test
    t0 = BasilList([])
    t1 = BasilList([])
    t2 = BasilList([])
    t1.append(t2)
    t3 = BasilList([])
    t1.append(t3)
    t0.append(t1)
    t4 = BasilList([])
    t0.append(t4)
    doVariousTests(t0)
    # ____________________________________________________________
    # DAG
    d0 = BasilList([])
    d1 = BasilList([])
    d0.append(d1)
    d2 = BasilList([])
    d0.append(d2)
    d3 = BasilList([])
    d1.append(d3)
    d2.append(d3)
    doVariousTests(d0)
    # ____________________________________________________________
    # Cycle
    c0 = BasilList([])
    c1 = BasilList([])
    c0.append(c1)
    c2 = BasilList([])
    c1.append(c2)
    c2.append(c1)
    doVariousTests(c0, DUPLICATE)

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of Visitor.py
