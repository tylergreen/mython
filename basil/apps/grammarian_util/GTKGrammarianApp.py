#! /usr/bin/env python
# ______________________________________________________________________
"""Module GTKGrammarianApp

Defines a GTK-based front-end for Grammarian.

Jonathan Riehl

$Id$
"""
# ______________________________________________________________________
# Module imports

import pygtk
pygtk.require('2.0')
import gtk

from basil.apps.grammarian_util.misc import VERSION

# ______________________________________________________________________
# Utility functions

def make_gtk_menu (menu_obj):
    ret_val = None
    if type(menu_obj) == tuple:
        crnt_obj, child_obj = menu_obj
        container = None
        if crnt_obj is None:
            ret_val = gtk.MenuBar()
            container = ret_val
        else:
            ret_val = gtk.MenuItem(crnt_obj)
            if type(child_obj) != list:
                ret_val.connect("activate", child_obj, None)
            else:
                container = gtk.Menu()
                ret_val.set_submenu(container)
        if type(child_obj) == list:
            for child in child_obj:
                crnt_item = make_gtk_menu(child)
                container.append(crnt_item)
                crnt_item.show()
    return ret_val

# ______________________________________________________________________
# Class definitions

class GTKGramApp (object):
    # ____________________________________________________________
    def __init__ (self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Grammarian %s (GTK)" % VERSION)
        self.window.connect("delete_event", self.delete_event)

        self.vbox = gtk.VBox()
        self.window.add(self.vbox)

        self.menubar = make_gtk_menu((None,
                                      [("_File", [("_New", self.file_new),
                                                  ("_Open...", self.file_open),
                                                  ("_Save...", self.file_save),
                                                  ("Save _As...",
                                                   self.file_save_as),
                                                  ("_Quit", self.file_quit)]),
                                       ("_Help", [("_About",
                                                   self.help_about)]),
                                       ]))
        self.vbox.pack_start(self.menubar, False, False, 2)
        self.menubar.show()

        self.notebook = gtk.Notebook()
        self.notebook.set_tab_pos(gtk.POS_TOP)
        self.vbox.pack_start(self.notebook)
        self.notebook.show()

        self.prod_frame = gtk.Frame("Productions")
        label = gtk.Label("Production View")
        self.prod_frame.add(label)
        label.show()
        self.prod_frame.show()
        self.notebook.append_page(self.prod_frame, gtk.Label("Productions"))

        self.nonterm_frame = gtk.Frame("Nonterminals")
        label = gtk.Label("Nonterminal View")
        self.nonterm_frame.add(label)
        label.show()
        self.nonterm_frame.show()
        self.notebook.append_page(self.nonterm_frame,
                                  gtk.Label("Nonterminals"))

        self.term_frame = gtk.Frame("Terminals")
        label = gtk.Label("Terminal View")
        self.term_frame.add(label)
        label.show()
        self.term_frame.show()
        self.notebook.append_page(self.term_frame, gtk.Label("Terminals"))

        self.statusbar = gtk.Statusbar()
        self.vbox.pack_start(self.statusbar, False, False, 2)
        self.statusbar.show()

        self.vbox.show()
        self.window.show()

    # ____________________________________________________________
    def delete_event (self, widget, event, data = None):
        gtk.main_quit()
        return False

    # ____________________________________________________________
    def file_new (self, *args):
        if __debug__:
            print "file_new", args

    # ____________________________________________________________
    def file_open (self, *args):
        if __debug__:
            print "file_open", args

    # ____________________________________________________________
    def file_save (self, *args):
        if __debug__:
            print "file_save", args

    # ____________________________________________________________
    def file_save_as (self, *args):
        if __debug__:
            print "file_save_as", args

    # ____________________________________________________________
    def file_quit (self, *args):
        if __debug__:
            print "file_quit", args
        gtk.main_quit()

    # ____________________________________________________________
    def help_about (self, *args):
        if __debug__:
            print "help_about", args

    # ____________________________________________________________
    def main (self):
        gtk.main()

# ______________________________________________________________________
# Main routine

def main (*args):
    app = GTKGramApp()
    app.main()

# ______________________________________________________________________    

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of GTKGrammarianApp.py
