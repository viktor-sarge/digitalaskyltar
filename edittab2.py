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
from Tkinter import Frame, W, N, NSEW
from edittab import EditTab
import editinputsections as eis

class EditTab2(EditTab):
    def __init__(self, filename, parentnotebook):
        EditTab.__init__(self, filename, parentnotebook)

        et = eis.EditInputTheme(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 0, column = 0, rowspan = 4, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputDataSource(self._mainframe, self, 'Blog')
        self._inputs.append(et)
        et.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputTopLeftText(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = NSEW)
        
        et = eis.EditInputCommon2(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputHorizontalPanel(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputItemView(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 0, column = 2, rowspan = 2, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputDimensions(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 2, column = 2, rowspan = 2, padx = 5, pady = 5, sticky = NSEW)
