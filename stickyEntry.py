#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from tkinter import *
import rfTest

class StickyEntry(Entry):

 

    def __init__(self, parent, text, **kw):

        ''' If relwidth is set, then width is ignored '''

        #fa = super(self,StickyEntry)

        #fa.__init__(parent, **kw)

        Entry.__init__(self, parent, kw)

 

        self.insert(0, text)


        #self['state'] = 'readonly'

        self['readonlybackground'] = 'white'

        self['selectbackground'] = '#1BA1E2'

        self['exportselection'] = False

 

        self.focus_force()

        self.bind("<Control-a>", self.selectAll)

        self.bind("<Escape>", lambda *ignore: self.destroy())

        self.bind("<KeyPress-Return>",self.inputUpdate)

 

    def selectAll(self, *ignore):

        ''' Set selection on the whole text '''

        self.selection_range(0, 'end')

 

        # returns 'break' to interrupt default key-bindings

        return 'break'

    def inputUpdate(self,keyword):
        rfTest.treeViewMapUpd(self.get())
        self.destroy()
