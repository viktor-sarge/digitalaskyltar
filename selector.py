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
import ttk
import tkFileDialog
from tkMessageBox import showerror
import os.path
from language import lang
import language as lng
from varbergtabselector import getTab, getNewTab, displaytypes
import spmanager as spm

_iniextension = '.ini'
_inifiletypes = [(lang[lng.txtInifiles], '*.ini')]

class SelectorTab(tki.Frame):
    
    def __init__(self, nbparent):
        tki.Frame.__init__(self, nbparent)

        self._notebook = nbparent

        lfopen = ttk.Labelframe(self, text = ' ' + lang[lng.txtSelectExisting] + ' ')
        lfopen.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = tki.W + tki.E)
        
        b = tki.Button(lfopen, text = lang[lng.txtOpen] + '...', command = self._ehOpen)
        b.grid(padx = 10, pady = 10)

        lfnew = ttk.Labelframe(self, text = ' ' + lang[lng.txtCreateNew] + ' ')
        lfnew.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = tki.W + tki.E)
        
        cb = ttk.Combobox(lfnew, values = displaytypes, state = "readonly")
        self._cb = cb
        cb.set(displaytypes[0])
        cb.grid(row = 0, column = 0, padx = 10, pady = 10)
        b = tki.Button(lfnew, text = lang[lng.txtSelectName] + '...', command = self._ehNew)
        b.grid(row = 0, column = 1, padx = 10, pady = 10)

    def _ehOpen(self):
        initdir = spm.spmanager.getFirstPath([spm.ConfigFolder, 
                                              spm.MostRecentFolder])

        filename = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = _inifiletypes)
        
        if(filename != ''):
            spm.spmanager.setPath(spm.ConfigFolder, os.path.dirname(filename))

            try:
                et = getTab(filename, self._notebook)
                et.load()
            except IOError:
                showerror('Load Config File', 'Could not load {}. Please make sure the file exists and you have permission; then and try again'.format(filename))
            except Exception as e:
                showerror('Load config file', 'Could not load {}: {}, try recreating it from scratch.'.format(filename, str(e)))
            else:
                self._notebook.select(et)

    def _ehNew(self):
        initdir = spm.spmanager.getFirstPath([spm.ConfigFolder, 
                                              spm.MostRecentFolder])
        dirpath = tkFileDialog.askdirectory(initialdir = initdir)

        if(dirpath != ''):
            spm.spmanager.setPath(spm.ConfigFolder, dirpath)
            filename = displaytypes[self._cb.current()] + _iniextension
            filename = os.path.join(dirpath, filename)
            filename = os.path.normpath(filename)
            
            et = getNewTab(displaytypes[self._cb.current()], filename, self._notebook)
