#! /usr/bin/env python
# ______________________________________________________________________
"""Stepper.py

A toy stepper GUI for a toy language.  Usage:

Stepper.py [-c] [-i <file>]

-c         Read initial textual ATerm from stdin.
-i <file>  Read initial textual ATerm from <file>.

Jonathan Riehl

$Id: Stepper.py,v 1.1 2007/06/22 00:11:33 jriehl Exp $
"""
# ______________________________________________________________________
# Module imports

import sys
import getopt
import Tkinter
import commands
import string

# ______________________________________________________________________
# Utility functions

def skip_whitespace (text, index):
    while index < len(text) and text[index] in string.whitespace:
        index += 1
    return index

# ______________________________________________________________________

def match_to_balance (balancer, delimiter, text, index):
    if __debug__:
        print "match_to_balance():", `balancer`, `text[index:]`
    subs = []
    while index < len(text) and text[index] != balancer:
        index, sub = parse_aterm(text, index)
        subs.append(sub)
        index = skip_whitespace(text, index)
        if index < len(text) and text[index] == delimiter:
            index += 1
    if index < len(text):
        index += 1
    return (index, subs)

# ______________________________________________________________________

def parse_aterm (text, index = None):
    """parse_aterm()
    Crude and incomplete ATerm parser.
    """
    if __debug__:
        print "parse_aterm():", `text[index:]`
    if index is None:
        index = 0
    index = skip_whitespace(text, index)
    ret_val = None
    if index >= len(text):
        ret_val = (index, None)
    if text[index] == "(":
        index, subs = match_to_balance(")", ",", text, index + 1)
        ret_val = (index, tuple(subs))
    elif text[index] == "[":
        ret_val = match_to_balance("]", ",", text, index + 1)
    elif text[index] == '"':
        string_start = index
        index += 1
        while (index < len(text) and text[index] != '"' and
               text[index - 1] != "\\"):
            index += 1
        if index < len(text):
            index += 1
        ret_val = (index, text[string_start + 1: index - 1])
    elif text[index] in string.digits:
        num_start = index
        index += 1
        while (index < len(text) and text[index] in string.digits):
            index += 1
        ret_val = (index, int(text[num_start:index]))
    else:
        id_start = index
        index += 1
        id_set = string.ascii_letters + string.digits + "_"
        while index < len(text) and text[index] in id_set:
            index += 1
        id_end = index
        if index < len(text) and text[index] == "(":
            # Constructor
            index, subs = match_to_balance(")", ",", text, index + 1)
        else:
            subs = []
        ret_val = (index, (text[id_start:id_end], subs))
    if __debug__:
        print "parse_aterm =>", ret_val
    return ret_val

# ______________________________________________________________________

def unparse_aterm (py_term):
    """unparse_aterm()
    A crude and incomplete unparser for ATerms processed using
    parse_aterm().
    """
    py_term_ty = type(py_term)
    ret_val = None
    if py_term_ty in (str, int):
        ret_val = `py_term`
    elif py_term_ty == tuple:
        if (len(py_term) == 2 and type(py_term[0]) == str and
            type(py_term[1]) == list):
            if len(py_term[1]) > 0:
                subterm_strs = [unparse_aterm(subterm)
                                for subterm in py_term[1]]
                constructor_args = ", ".join(subterm_strs)
                ret_val = "%s(%s)" % (py_term[0], constructor_args)
            else:
                ret_val = py_term[0]
        else:
            subterm_strs = [unparse_aterm(subterm) for subterm in py_term]
            ret_val = "(%s)" % (", ".join(subterm_strs))
    elif py_term_ty == list:
        subterm_strs = [unparse_aterm(subterm) for subterm in py_term]
        ret_val = "[%s]" % (", ".join(subterm_strs))
    else:
        ret_val = "???"
    return ret_val

# ______________________________________________________________________
# Class definition

class StepperApp (object):
    # ____________________________________________________________
    def __init__ (self, master, initial_text = None):
        """StepperApp.__init__()
        """
        self.master = master
        self.frame = Tkinter.Frame(master)
        self.frame.pack(fill = Tkinter.BOTH)
        self.text_area = Tkinter.Text(self.frame, width = 60,
                                      state = Tkinter.DISABLED)
        self.text_area.pack(fill = Tkinter.BOTH)
        # __________________________________________________
        text_row = Tkinter.Frame(self.frame)
        text_row.pack(fill = Tkinter.X)
        text_area_pack_opts = {"side" : Tkinter.LEFT,
                               "fill" : Tkinter.X,
                               "expand" : Tkinter.TRUE}
        self.crnt_term_area = Tkinter.Text(text_row, width = 20,
                                           state = Tkinter.DISABLED)
        self.crnt_term_area.pack(**text_area_pack_opts)
        self.crnt_env_area = Tkinter.Text(text_row, width = 20,
                                          state = Tkinter.DISABLED)
        self.crnt_env_area.pack(**text_area_pack_opts)
        self.crnt_stack_area = Tkinter.Text(text_row, width = 20,
                                            state = Tkinter.DISABLED)
        self.crnt_stack_area.pack(**text_area_pack_opts)
        # __________________________________________________
        button_row = Tkinter.Frame(self.frame)
        button_row.pack()
        self.step_button = Tkinter.Button(button_row, text = "Step",
                                          command = self.do_step)
        self.step_button.pack(side = Tkinter.LEFT)
        self.reset_button = Tkinter.Button(button_row, text = "Reset",
                                           command = self.do_reset)
        self.reset_button.pack(side = Tkinter.LEFT)
        self.quit_button = Tkinter.Button(button_row, text = "Quit",
                                          command = self.do_quit)
        self.quit_button.pack(side = Tkinter.LEFT)
        # __________________________________________________
        if initial_text is None:
            initial_text = 'Int("0")'
        self.initial_text = initial_text
        self.update_state('([],[],%s)' % initial_text)

    # ____________________________________________________________
    def update_state (self, state):
        """StepperApp.update_state()
        """
        self.insert_text("%s\n\n" % state)
        self.crnt_state = state
        py_state = parse_aterm(state)[1]
        print py_state
        if len(py_state) == 2:
            self.set_term(py_state[0])
            self.set_env(None)
            self.set_stack(py_state[1])
        elif len(py_state) == 3:
            self.set_term(py_state[2])
            self.set_env(py_state[1])
            self.set_stack(py_state[0])
        else:
            self.set_term(None)
            self.set_env(None)
            self.set_stack(None)

    # ____________________________________________________________
    def insert_text (self, text):
        """StepperApp.insert_text()
        """
        self.text_area.config(state = Tkinter.NORMAL)
        self.text_area.insert(Tkinter.END, text)
        self.text_area.see(Tkinter.END)
        self.text_area.config(state = Tkinter.DISABLED)

    # ____________________________________________________________
    def clear_text (self):
        """StepperApp.clear_text()
        """
        self.text_area.config(state = Tkinter.NORMAL)
        self.text_area.delete(1.0, Tkinter.END)
        self.text_area.config(state = Tkinter.DISABLED)

    # ____________________________________________________________
    def set_term (self, term):
        """StepperApp.set_term()
        """
        if term is None:
            term_str = "???"
        else:
            term_str = unparse_aterm(term)
        self._set_textarea(self.crnt_term_area, term_str)

    # ____________________________________________________________
    def set_env (self, env):
        """StepperApp.set_env()
        """
        # Should be a list of pairs.
        if env is None:
            env_str = "N/A"
        elif len(env) > 0:
            env_str = "\n".join(["%s : %s" % (label, unparse_aterm(val))
                                 for (label, val) in env])
        else:
            env_str = "EMPTY"
        self._set_textarea(self.crnt_env_area, env_str)

    # ____________________________________________________________
    def set_stack (self, stack):
        """StepperApp.set_stack()
        """
        if stack is None:
            stack_str = "???"
        elif len(stack) > 0:
            stack_str = "\n---\n".join([unparse_aterm(context)
                                        for context in stack])
        else:
            stack_str = "EMPTY"
        self._set_textarea(self.crnt_stack_area, stack_str)

    # ____________________________________________________________
    def _set_textarea (self, area, text):
        """StepperApp._set_textarea()
        """
        area.config(state = Tkinter.NORMAL)
        area.delete(1.0, Tkinter.END)
        area.insert(Tkinter.END, text)
        area.config(state = Tkinter.DISABLED)

    # ____________________________________________________________
    def do_step (self):
        """StepperApp.do_step()
        """
        command = ('echo "%s" | ToyEvalStep' %
                   (self.crnt_state.replace('"', '\\"')))
        result, next_state = commands.getstatusoutput(command)
        if result == 0:
            self.update_state(next_state)
        else:
            self.insert_text(next_state)
            self.step_button.config(state = Tkinter.DISABLED)

    # ____________________________________________________________
    def do_reset (self):
        """StepperApp.do_reset()
        """
        self.clear_text()
        self.update_state('([],[],%s)' % self.initial_text)
        self.step_button.config(state = Tkinter.NORMAL)

    # ____________________________________________________________
    def do_quit (self):
        """StepperApp.do_quit()
        """
        sys.exit(0)

# ______________________________________________________________________
# Main routine

def main ():
    """main()
    """
    initial_text = None
    text_file = None
    opts, args = getopt.getopt(sys.argv[1:], "ci:")
    for opt_key, opt_val in opts:
        if opt_key == "-c":
            text_file = sys.stdin
        elif opt_key == "-i":
            text_file = open(opt_val)
    if text_file is not None:
        initial_text = text_file.read()
    # ____________________________________________________________
    tk = Tkinter.Tk()
    app = StepperApp(tk, initial_text)
    tk.mainloop()

# ______________________________________________________________________

if __name__ == "__main__":
    main()

# ______________________________________________________________________
# End of Stepper.py
