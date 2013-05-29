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
import os.path
import sys
import selector
from language import lang
import language as lng
from spmanager import spmanager

_windowoffset = 30
_taskbaroffset = 100


#Inifile constants
_searchpathfilename = 'paths.ini'

class AdminGui:
    
    def __init__(self):
        root = tki.Tk()
        self.root = root
        
        root.protocol("WM_DELETE_WINDOW", self._ehQuit)
        root.title(lang[lng.txtEditorTitle])
        root.rowconfigure(0, weight = 1)
        root.columnconfigure(0, weight = 1)

        nb = ttk.Notebook(root)
        self._nb = nb
        nb.grid(row = 0, column = 0, sticky = 'wnes')
        nt = selector.SelectorTab(nb)
        nb.add(nt, text = lang[lng.txtSelectFile])
        nb.select(0)
        

    def _ehQuit(self):
        """Terminate the application."""
        spmanager.save()
        self.root.destroy()
    
if __name__ == "__main__":
    #Workaround for unicode in exefiles
    if hasattr(sys,"setdefaultencoding"):
        sys.setdefaultencoding("utf-8")

    inidir = os.path.dirname(sys.argv[0])
    spmanager.load(os.path.normpath(os.path.join(inidir, _searchpathfilename)))
    ag = AdminGui()
    ag.root.mainloop()
