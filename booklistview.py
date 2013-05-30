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
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import itertools
from listview import ListView

evItemSelected = '<<ItemSelectedInBookListView>>'

_minspace = 20

class BooklistView(ListView):
    """This class displays a list of books in a given frame."""
        
    def __init__(self, previewx, previewy, frame):
        """Creates an indexed frame and adds it to the scrollbox 

        Arguments
        previewx -- width of preview images
        previewy -- height of preview images
        frame -- the frame on which to layout the widgets

        """
        ListView.__init__(self, evItemSelected)
        
        width = frame['width']
        height = frame['height']
        
        self._eventgenerator = frame
        
        columncount = (width - _minspace) / (_minspace + previewx)
        rowcount = (height - _minspace) / (_minspace + previewy)
        self._itemcount = rowcount * columncount
        
        for i in range(rowcount):
            frame.rowconfigure(i, weight = 1)
            
        for i in range(columncount):
            frame.columnconfigure(i, weight = 1)
            
        self._labels = []
        
        for i in range(rowcount):
            for j in range(columncount):
                l = tki.Label(frame)#, image = image1)#, text = 'bild ' + str(j) + ', ' + str(i))
                #print('bild ' + str(j) + ', ' + str(i))
                self._labels.append(l)
                l.grid(row = i, column = j, padx = _minspace, pady = _minspace)
                l.index = (i * columncount) + j
                l.bind("<Button-1>", self._ehClick)
                
    def _update(self):
        """Update the contents of the BooklistView."""
        ListView._update(self)

        for (i, l) in itertools.izip_longest(self._items, self._labels):
            if(l is None):
                break

            if(i is None):
                l.grid_remove()
            else:
                if(i.image is None):
                    l.grid_remove()
                else:
                    l.config(image = i.image)
                    l.grid()
