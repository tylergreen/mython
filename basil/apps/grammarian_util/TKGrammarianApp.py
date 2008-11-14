#! /usr/bin/env python
# ______________________________________________________________________
"""TKGrammarianApp

Defines the Tkinter based front-end for Grammarian, implemented in the
TKGrammarianApp class.

XXX Not sure how much love this is going to get...

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import Tkinter

from basil.apps.grammarian_util.misc import VERSION

# ______________________________________________________________________
# Class definition

class TKGrammarianApp (object):
    """Class TKGrammarianApp
    """
    # ____________________________________________________________
    def __init__ (self, top):
        """GrammarianApp.__init__()
        """
        self.top = top
        self.top.title("Grammarian %s" % VERSION)
        self.frame = Tkinter.Frame(self.top)
        self.frame.pack(expand = Tkinter.YES, fill = Tkinter.BOTH)
        Tkinter.Label(self.frame, text = "Not finished!").pack()

# ______________________________________________________________________
# Main routine.

def main (*args):
    tk = Tkinter.Tk()
    app = TKGrammarianApp(tk)
    tk.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of TKGrammarianApp.py
