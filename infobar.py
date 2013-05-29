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
import tkFont

class Infobar:
    """An observer that displays a text on a frame"""
    def __init__(self, parent):
        """
        Arguments
        parent -- the frame on which to layout the displayed information

        """
        self._svText = tki.StringVar()
        fntText = tkFont.Font(family="Arial", size = 18, weight="bold")
        
        parent.rowconfigure(0, weight = 1)
        parent.columnconfigure(0, weight = 1)
        l = tki.Label(parent, textvariable = self._svText, font = fntText, bg = parent['bg'])
        l.grid(row = 0, column = 0)
        
    def notify(self, datasrc):
        """Tell the Infobar that the displayed data shall be updated.
        
        Argument
        datasrc -- object containing a member subject
        
        """
        self._svText.set(datasrc.subject)
