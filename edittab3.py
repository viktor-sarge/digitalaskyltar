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

class EditTab3(EditTab):
    def __init__(self, filename, parentnotebook):
        EditTab.__init__(self, filename, parentnotebook)

        et = eis.EditInputTheme(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 0, column = 0, rowspan = 4, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputDataSource(self._mainframe, self, 'Blog')
        self._inputs.append(et)
        et.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputDataSource(self._mainframe, self, 'New')
        self._inputs.append(et)
        et.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputCommon3(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputBottomArea(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputItemView(self._mainframe, self, True)
        self._inputs.append(et)
        et.grid(row = 0, column = 2, rowspan = 3, padx = 5, pady = 5, sticky = NSEW)

        et = eis.EditInputScrollbuttons(self._mainframe, self)
        self._inputs.append(et)
        et.grid(row = 3, column = 2,  padx = 5, pady = 5, sticky = NSEW)

        right = Frame(self._mainframe)
        right.grid(row = 0, column = 3, rowspan = 4, padx = 5, pady = 5, sticky = NSEW)
        right.rowconfigure(1, weight = 1)

        et = eis.EditInputDimensions(right, self)
        self._inputs.append(et)
        et.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = NSEW)

        sm = eis.SubjectManager(right, self)
        self._inputs.append(sm)
        sm.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = NSEW)
