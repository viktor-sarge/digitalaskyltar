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
import Tkinter as tki
import os.path
import PIL.Image as Image
import PIL.ImageTk as ImageTk



class ButtonScrollbar(tki.Frame):
    """A "scrollbar" consisting of two buttons"""
    
    def __init__(self, parent, settings):
        """Initiate the ButtonScrollbar
        
        Arguments
        parent -- parent Frame
        settings -- Settings object containing the up and down buttons
        
        """
        tki.Frame.__init__(self, parent)
       
        self._scrollable = None
        self._scrolling = False
        self._scrolldirUp = True
        self._donotthrow = []
        btnup = Image.open(settings.buttonup)
        self._width = btnup.size[0]
        btnup = ImageTk.PhotoImage(btnup)
        self._donotthrow.append(btnup)
        btndown = Image.open(settings.buttondown)
        btndown = ImageTk.PhotoImage(btndown)
        self._donotthrow.append(btndown)
                
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        
        color = 'white'
        btn = tki.Button(self, image = btnup, compound = tki.CENTER, 
                         bd = 0, highlightthickness = 0, bg = color, activebackground = color, foreground = color, activeforeground = color)
        btn.bind('<Button-1>', self._ehUp)
        btn.bind('<ButtonRelease-1>', self._ehStopScrolling)
        btn.grid(row = 0, column = 0, sticky = tki.N)
        btn = tki.Button(self, image = btndown, compound = tki.CENTER, 
                         bd = 0, highlightthickness = 0, bg = color, activebackground = color, foreground = color, activeforeground = color)
        btn.bind('<Button-1>', self._ehDown)
        btn.bind('<ButtonRelease-1>', self._ehStopScrolling)
        btn.grid(row = 1, column = 0, sticky = tki.S)
        
        

    def getWidth(self):
        return self._width

       
    
    def addScrollable(self, scrollable):
        self._scrollable = scrollable
       
    def _scroll(self):
        if(self._scrollable is not None and self._scrolling):
            if(self._scrolldirUp):
                dir = -1
            else:
                dir = 1
                
            self._scrollable.yview('scroll', dir, 'units')
            self.after(50, self._scroll)

    def _ehStopScrolling(self, event):
        self._scrolling = False

    def _ehUp(self, event):
        self._scrolldirUp = True
        self._scrolling = True
        self.after_idle(self._scroll)
   
    def _ehDown(self, event):
        self._scrolldirUp = False
        self._scrolling = True
        self.after_idle(self._scroll)
