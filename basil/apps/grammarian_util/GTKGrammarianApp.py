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

import sys
import traceback

from basil.models.grammar import GrammarUtils
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
    def make_list_page (self, prefix, *cols):
        page = gtk.ScrolledWindow()
        store = gtk.ListStore(*((str,) * len(cols)))
        view = gtk.TreeView(store)
        cell_objs = []
        col_objs = []
        for col_name in cols:
            col = gtk.TreeViewColumn(col_name)
            view.append_column(col)
            cell = gtk.CellRendererText()
            col.pack_start(cell, True)
            col.add_attribute(cell, "text", len(col_objs))
            col.set_sort_column_id(len(col_objs))
            cell_objs.append(cell)
            col_objs.append(col)
        view.set_search_column(0)
        view.set_reorderable(True)
        page.add(view)
        view.show()
        page.show()
        setattr(self, "%s_page" % prefix, page)
        setattr(self, "%s_store" % prefix, store)
        setattr(self, "%s_view" % prefix, view)
        setattr(self, "%s_cols" % prefix, tuple(col_objs))
        setattr(self, "%s_cells" % prefix, tuple(cell_objs))
        return page

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

        self.model = None
        self.model_filename = None

        self.notebook.append_page(self.make_list_page("prod", "LHS", "RHS"),
                                  gtk.Label("Productions"))
        self.notebook.append_page(self.make_list_page("nonterm",
                                                      "Nonterminal"),
                                  gtk.Label("Nonterminals"))
        self.notebook.append_page(self.make_list_page("term", "Terminal"),
                                  gtk.Label("Terminals"))

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
        self.file_open_dialog = dialog = gtk.FileSelection("Open...")
        dialog.ok_button.connect("clicked", self.file_open_ok)
        dialog.cancel_button.connect("clicked", lambda w: dialog.destroy())
        dialog.show()

    # ____________________________________________________________
    def file_open_ok (self, *args):
        if __debug__:
            print "file_open_ok", args
        model_filename = self.file_open_dialog.get_filename()
        try:
            model = GrammarUtils.getModel(model_filename)
            self.model_filename = model_filename
            self.model = model
            self.update_views()
        except:
            print >> sys.stderr, "Failed to open model '%s'." % model_filename
            print >> sys.stderr, traceback.format_exc()
        self.file_open_dialog.destroy()
        self.file_open_dialog = None

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
    def update_views (self):
        self.prod_store.clear()
        self.nonterm_store.clear()
        self.term_store.clear()
        start, terms, nonterms, prods = self.model
        for term in terms:
            self.term_store.append([term.name])
        for nonterm in nonterms:
            self.nonterm_store.append([nonterm.name])
        for prod in prods:
            prod = list(prod)
            lhs, rhs = prod[-2:]
            lhs_str = " ".join([x.name for x in lhs])
            rhs_str = " ".join([x.name for x in rhs[0]])
            self.prod_store.append([lhs_str, rhs_str])

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
