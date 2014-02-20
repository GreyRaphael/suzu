import Tkinter as tk
import os

import matdb_frame

class Dialog(tk.Toplevel):

    def __init__(self, parent, opts, title = None):

        tk.Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        self.initial_focus = None
        self.bodyframe = matdb_frame.MatDBFrame(self, opts)

        self.bodyframe.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.buttonframe = tk.Frame(self)
        self.buttonbox(self.buttonframe)
        self.buttonframe.grid(row=1, column=0, sticky=tk.N+tk.S)

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

        self.initial_focus.focus_set()

    #
    # construction hooks
    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        pass

    def buttonbox(self, master):
        # add standard button box. override if you don't want the
        # standard buttons

        w = tk.Button(master, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(master, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    #
    # standard button semantics
    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks
    def validate(self):
        return 1 # override

    def apply(self):
        self.result = self.bodyframe.get_current_selection()

if __name__ == '__main__':
    app = tk.Tk()

    entries = [{'name':"A", 'summary':'summary of A'},
            {'name':"B", 'summary':'summary of B'},
            {'name':"C", 'summary':'summary of C'},
            {'name':"D", 'summary':'summary of D'},
            {'name':"E", 'summary':'summary of E'},
            {'name':"F", 'summary':'summary of F'},
            {'name':"G", 'summary':'summary of G'},
            {'name':"H", 'summary':'summary of H'},
            {'name':"I", 'summary':'summary of I'},
            {'name':"J", 'summary':'summary of J'},
            {'name':"K", 'summary':'summary of K'},
            {'name':"L", 'summary':'summary of L'},
            {'name':"M", 'summary':'summary of M'},
            {'name':"N", 'summary':
            '''\
            summary of N
            very very very long long long long summary
            0
            1
            2
            3
            4
            5
            6
            :
            a''' }]

    # test for less entries
    #del(entries[3:])

    d = Dialog(app, entries)

    app.wait_window(d)

    # print type(d)
    # print d.__dict__
    print d.result
