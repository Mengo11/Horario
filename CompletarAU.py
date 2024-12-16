from tkinter import *
import re

class AutocompleteEntry(Entry):
    def __init__(self, lista, ar, Defaultplus=0):
        Entry.__init__(self, ar)
        self.defaultp = Defaultplus
        self.lista = lista
        self.var = self["textvariable"]
        if not self.var:
            self.var = self["textvariable"] = StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)
        self.bind("<FocusIn>", self.show_listbox)
        self.lb_up = False
        self.lb = None

    def show_listbox(self, event=None):
        self.changed(None, None, None)

    def hide_listbox(self, window):
        widget_con_enfoque = window.focus_get()
        if isinstance(widget_con_enfoque, Listbox):
            return
        if self.lb_up:
            self.lb.destroy()
            self.lb_up = False

    def changed(self, name, index, mode):
        words = self.comparison()
        if words:
            if not self.lb_up:
                x, y, width, height = self.winfo_x(), self.winfo_y(), self.winfo_width(), self.winfo_height()
                self.lb = Listbox(self.winfo_toplevel())
                self.lb.bind("<Double-Button-1>", self.selection)
                self.lb.place(x=x, y=y + height + self.defaultp, width=width, height=100)
                self.lb_up = True

            self.lb.delete(0, END)
            for w in words:
                self.lb.insert(END, w)
        else:
            if self.lb_up:
                self.lb.destroy()
                self.lb_up = False

    def selection(self, event):
        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + re.escape(self.var.get()) + '.*', re.IGNORECASE)
        return [w for w in self.lista if re.match(pattern, w)]