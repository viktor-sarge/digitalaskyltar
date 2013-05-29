#    Copyright 2013 Regionbibliotek Halland
#
#    This file is part of Digitala skyltar.
#
#    Digitala skyltar is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Digitala skyltar is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Digitala skyltar.  If not, see <http://www.gnu.org/licenses/>.
from Tkinter import *
from language import lang, txtUp, txtDown, txtDelete, txtTop, txtBottom, dlgDelFrameTitle, dlgDelFrame
import tkMessageBox

_defaultWidth = 200

class IndexedFrame(Frame):
    """The base class of a widget placed in a Scrollbox. 
    
    Do not instantiate subclasses directly; use Scrollbox.getWidget() instead. 
    The first argument of a subclass constructor must be directly passed to IndexedFrame. 
    Place any widgets in member _content. Member index will be set to the index in the list 
    by the containing Scrollbar.
    
    """
    def __init__(self, parent):
        """Create _content and a panel with control buttons
        
        Argument
        parent -- parent tkinter item
        
        """
        Frame.__init__(self, parent, bd = 1, relief = RAISED)
        
        #Create frame for the contents of this IndexedFrame
        self._content = Frame(self)
        self._content.grid(row = 0, column = 0, sticky = W + N + E + S)
        
        #Create control panel
        control = Frame(self)
        self._control = control
        control.grid(row = 1, column = 0)
        
        button = Button(control, text = lang[txtTop])
        button.ref = self
        button.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.btnTop = button

        button = Button(control, text = lang[txtUp])
        button.ref = self
        button.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.btnUp = button

        button = Button(control, text = lang[txtDown])
        button.ref = self
        button.grid(row = 0, column = 2, padx = 5, pady = 5)
        self.btnDown = button

        button = Button(control, text = lang[txtBottom])
        button.ref = self
        button.grid(row = 0, column = 3, padx = 5, pady = 5)
        self.btnBottom = button

        button = Button(control, text = lang[txtDelete])
        button.ref = self
        button.grid(row = 0, column = 4, padx = 5, pady = 5)
        self.btnDelete = button
        
    def update(self):
        """Gets called when the index has been updated"""
        pass

class Scrollbox(Frame):
    """A scrollbox containing indexed widgets that can be moved and removed."""
    def __init__(self, saveable, parent):
        """Initiate
        
        Arguments
        saveable -- object with a setDirty function - indicates if there are unsaved changes
        parent -- the parent tkinter item
        
        """
        Frame.__init__(self, parent)
        
        self._saveable = saveable
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        
        canvas = Canvas(self)
        canvas.grid(row=0, column=0, sticky=N + S + W + E)
        vscroll = Scrollbar(self, orient = VERTICAL, command = canvas.yview)
        self._vscroll = vscroll
        vscroll.grid(row=0, column=1, sticky=N+S)
        canvas["yscrollcommand"] = vscroll.set
        container = Frame(canvas, relief = RAISED)
        canvas.create_window(0, 0, window = container, anchor = N + W)

        self._canvas = canvas
        self._container = container
        self.widgets = []
        self._defaultWidth = _defaultWidth
        
    def getWidget(self, type, *args):
        """Create an indexed frame and add it to the scrollbox 

        Arguments
        type -- the type of the indexed frame to be created; must be a subclass of IndexedFrame
        *args -- arguments to the constructor of the indexed frame to be created
        
        """
        widget = type(self, *args)
        widget.index = len(self.widgets)
        widget.btnTop.bind("<Button-1>", self._ehTop)
        widget.btnUp.bind("<Button-1>", self._ehUp)
        widget.btnDown.bind("<Button-1>", self._ehDown)
        widget.btnBottom.bind("<Button-1>", self._ehBottom)
        widget.btnDelete.bind("<ButtonRelease-1>", self._ehDelete)
        
        widget.grid(in_ = self._container, row = widget.index, column = 0)
        self.widgets.append(widget)
        self._update()
        
        return widget

    def clear(self):
        """Clear the scrollbox"""
        for i in self.widgets:
            i.destroy()
            
        self.widgets = []

    def _update(self):
        """Relocate all widgets in the scrollbox"""
        for i in self.widgets:
            i.grid_remove()
            
        ctr = 0

        for i in self.widgets:
            i.grid(in_ = self._container, row = ctr, column = 0, pady = 1, sticky = W + E)
            i.index = ctr
            i.update()
            ctr += 1

        self._container.update_idletasks()
                
        if(len(self.widgets) > 0):
            self._canvas['width'] = self.widgets[0].winfo_reqwidth()
            self._defaultWidth = self.widgets[0].winfo_reqwidth()
        else:
            self._canvas['width'] = self._defaultWidth

        self._canvas["scrollregion"] = self._canvas.bbox(ALL)
        self._canvas.yview_moveto(1.0)

    def _swapFrames(self, index1, index2):
        """Swap two widgets in the scrollbox
        
        Arguments
        index1 -- index of the the first widget
        index2 -- index of the second widget
        
        """
        swap = self.widgets[index1]
        self.widgets[index1] = self.widgets[index2]
        self.widgets[index2] = swap
                
        self._update()  

    def _ehUp(self, event):
        """Event handler for moving a widget up in the scrollbox
        
        Argument
        event -- event object containing a reference to an IndexedFrame
        
        """
        index = event.widget.ref.index
        
        if(index == 0):
            return
        
        self._swapFrames(index, index - 1)
        self._saveable.setDirty(True)

    def _ehDown(self, event):
        """Event handler for moving a widget down in the scrollbox
        
        Argument
        event -- event object containing a reference to an IndexedFrame
        
        """
        index = event.widget.ref.index
        
        if(index >= (len(self.widgets) - 1)):
            return
        
        self._swapFrames(index, index + 1)
        self._saveable.setDirty(True)

    def _ehDelete(self, event):
        """Event handler for deleting a widget
        
        Argument
        event -- event object containing a reference to an IndexedFrame
        
        """
        response = tkMessageBox.askyesno(lang[dlgDelFrameTitle], lang[dlgDelFrame])
        
        if(not response):
            return

        index = event.widget.ref.index
        event.widget.ref.destroy()
        del self.widgets[index]
        self._update()
        self._saveable.setDirty(True)
        
    def _ehTop(self, event):
        """Event handler for moving a widget to the top in the scrollbox
        
        Argument
        event -- event object containing a reference to an IndexedFrame
        
        """
        index = event.widget.ref.index
        
        if(index == 0):
            return
        
        self._swapFrames(index, 0)
        self._saveable.setDirty(True)
        
    def _ehBottom(self, event):
        """Event handler for moving a widget to the bottom in the scrollbox
        
        Argument
        event -- event object containing a reference to an IndexedFrame
        
        """
        index = event.widget.ref.index
        
        last = len(self.widgets) - 1
        if(index == last):
            return

        self._swapFrames(index, last)
        self._saveable.setDirty(True)
