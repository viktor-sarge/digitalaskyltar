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
import os.path
from common import getConfigParser
from Tkinter import Frame, Canvas, Scrollbar, Button, NORMAL, DISABLED, W, N, E, S, NSEW, VERTICAL, HORIZONTAL, ALL
from tkMessageBox import showwarning, showerror, askyesnocancel

from configfilewriter import ConfigFileWriter
import language as lng
from language import lang

class EditTab(Frame):
    """A tab that represents a config file"""
    
    def __init__(self, filename, parentnotebook):
        """Create a new EditTab
        
        Argument
        filename -- name and path to the file being edited
        parentnotebook -- the NoteBook in which this tab will be added
        
        """
        Frame.__init__(self)
        self._filename = filename
        self._parentnotebook = parentnotebook
        self._inputs = []
        self.path = os.path.dirname(filename)
        self._dirty = False
        parentnotebook.add(self, state = 'normal')
        self._setLabel()

        #Set up GUI
        self.rowconfigure(0, weight = 1)        
        self.columnconfigure(0, weight = 1)
        
        vscroll = Scrollbar(self, orient = VERTICAL)
        self._vscroll = vscroll
        vscroll.grid(row=0, column=1, sticky=N+S)
        hscroll = Scrollbar(self, orient = HORIZONTAL)
        self._hscroll = hscroll
        hscroll.grid(row=1, column=0, sticky=E+W)

        canvas = Canvas(self, yscrollcommand = vscroll.set, xscrollcommand = hscroll.set)
        self._canvas = canvas
        canvas.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = NSEW)

        vscroll['command'] = canvas.yview
        hscroll['command'] = canvas.xview

        scrollframe = Frame(canvas)
        self._scrollframe = scrollframe
        canvas.create_window(0, 0, window = scrollframe, anchor = N + W)

        scrollframe.rowconfigure(0, weight = 1)        
        scrollframe.columnconfigure(0, weight = 1)
                
        self._mainframe = Frame(scrollframe)
        self._mainframe.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = NSEW)
        
        cf = Frame(scrollframe)
        self._control_frame = cf
        cf.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = E)
        b = Button(cf, text = lang[lng.txtCopyImages], command = self._ehCopyImages)
        self._btnCopy = b
        b.grid(row = 0, column = 0, padx = 5, pady = 5)
        b = Button(cf, text = lang[lng.txtSave], command = self._ehSave, state = DISABLED)
        self._btnSave = b
        b.grid(row = 0, column = 1, padx = 5, pady = 5)
        b = Button(cf, text = lang[lng.txtClose], command = self._ehClose)
        b.grid(row = 0, column = 2, padx = 5, pady = 5)

        parentnotebook.after_idle(self._setCanvas)

    def load(self):
        """If the config file exists, try to load it"""
        if(os.path.exists(self._filename)):
            cfgp = getConfigParser(self._filename)

            for input in self._inputs:
                input.readValue(cfgp)

    def setDirty(self, dummy = None):
        self._dirty = True
        self._btnCopy.config(state = NORMAL)
        self._btnSave.config(state = NORMAL)
        self._setLabel()

    def _setCanvas(self):
        self._parentnotebook.update_idletasks()
        self._canvas.config(scrollregion = self._canvas.bbox(ALL))

    def _save(self):
        """Save configuration to file"""

        cfw = ConfigFileWriter()
        
        for input in self._inputs:
            input.writeValue(cfw)

        try:            
            cfw.writeToFile(self._filename)
        except IOError:
            showerror('Save to File', 'Could not save {}; please make sure you have permission and try again'.format(self._filename))
        except Exception as e:
            showerror('Save to File', 'Could not save {}; an unknown error occurred'.format(self._filename) + ': ' + str(e))
        else:
            self._dirty = False
            self._btnSave.config(state = DISABLED)
            self._setLabel()

    def _setLabel(self):
        """Set the label of this tab"""
        text = os.path.basename(self._filename)

        if(self._dirty):
            text = text + '*'

        self._parentnotebook.tab(self, text = text)
        
    def _ehCopyImages(self):
        for input in self._inputs:
            input.copyImages()

        self.setDirty()
        self._btnCopy.config(state = DISABLED)

    def _ehClose(self):
        if(self._dirty):
            result = askyesnocancel('Unsaved Changes', 'There are unsaved changes. Do you want to save them before closing this tab?')
            
            if(result is None):
                return
            elif(result):
                self._save()

        self._parentnotebook.forget(self)

    def _ehSave(self):
        self._save()
