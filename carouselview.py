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
import tkFont

_maxitems = 5
_space = 5
_highlightwidth = 5
_minspareheight = 10

class CarouselView:
    """Contain a list of items, display them cyclically in a carousel view and 
    highlight one of the items. This class should not be instantiated directly; 
    it uses a function called _drawItem that should be implemented in any subclass. 
    
    """
    def __init__(self, parent, reqwidth, reqheight):
        """Initiate the carouselview

        Arguments
        parent -- the frame on which to layout the carousel view
        reqwidth - the width of the items to display
        reqheight - the height of the items to display
                
        """
        parent.rowconfigure(0, weight = 1)

        self._labels = []
        
        width = parent['width']
        height = parent['height']
        viewcount = _maxitems
        found = False
        spareheight = (height - reqheight) / 2
        
        if(spareheight < _minspareheight):
            print('Too little space for carousel view; required = ' + str(_minspareheight) +
                  ', available = ' + str(spareheight))
            raise Exception()

        while(viewcount >= 1):
            #TBD This value was added because there is a problem with the formula below. 
            margin = 0#viewcount * 4
            if((margin + 2 * _highlightwidth + viewcount * (2 * _space + reqwidth)) <= width):
                found = True
                break
            else:
                viewcount -= 2
        
        if(not found):
            print('Too little space for carousel view; required = ' + str(_space + 3 * (_space + reqwidth)) +
                  ', available = ' + str(width))
            raise Exception()
        
        self._viewcount = viewcount
        self._center = viewcount / 2
        color = bg = parent['bg']
        
        for i in range(viewcount):
            parent.columnconfigure(i, weight = 1)

            if(i == self._center):
                cwidth = reqwidth + 2 * _highlightwidth
                cheight = reqheight + 2 * spareheight
                c = tki.Canvas(parent, width = cwidth, height = cheight, bd = 0, highlightthickness = 0, bg = color)
                c.grid(row = 0, column = i, padx = _space)
                owidth = min(reqwidth / 2, 5 * spareheight / 3)
                oheight = 3 * owidth / 5
                oleft = (cwidth - owidth) / 2
                otop = spareheight - _highlightwidth - oheight / 2
                c.create_oval(oleft, otop, oleft + owidth, otop + oheight, fill = 'white', outline = 'white')
                rtop = (cheight - reqheight - 2 * _highlightwidth) / 2
                rheight = reqheight + 2 * _highlightwidth
                c.create_rectangle(0, rtop, cwidth, rtop + rheight, fill = 'white', outline = 'white')
                f = tki.Frame(parent, width = reqwidth, height = reqheight, bg = 'white')
                f.rowconfigure(0, weight = 1)
                f.columnconfigure(0, weight = 1)
                f.grid_propagate(0)
                l = tki.Label(f)
                l.grid()
                self._labels.append(l)
                c.create_window(cwidth / 2, cheight / 2, window = f)
            else:
                f = tki.Frame(parent, width = reqwidth, height = reqheight, bg = color)
                f.rowconfigure(0, weight = 1)
                f.columnconfigure(0, weight = 1)
                f.grid_propagate(0)
                l = tki.Label(f, bg = color)
                l.grid()
                f.grid(row = 0, column = i, padx = _space)
                self._labels.append(l)

    def setItemList(self, list, index):
        """Set the list of items and select the index to display initially
        
        Arguments
        list -- the list to display
        index -- the index to highlight
        
        """
        self._list = list
        self._listindex = index
        self._update()

    def next(self):
        """Browse to next item"""
        self._listindex += 1
        
        if(self._listindex >= len(self._list)):
            self._listindex = 0
        
        self._update()
        
    def prev(self):
        """Browse to previous item"""
        self._listindex -= 1
        
        if(self._listindex < 0):
            self._listindex = len(self._list) - 1

        self._update()

    def _update(self):
        """Update the contents of the carouselview."""        
        viewcount = min(self._viewcount, len(self._list))
        center = viewcount / 2
        
        for i in self._labels:
            i.grid_remove()
        
        if(self._viewcount > len(self._list)):
            viewcount = len(self._list)
            offset = (self._viewcount - len(self._list)) / 2
        else:
            viewcount = self._viewcount
            offset = 0

        for i in range(viewcount):
            index = self._listindex + i - center
            
            if(index < 0):
                index = index + len(self._list)
                
            if(index >= len(self._list)):
               index -= len(self._list)

            self._drawItem(offset + i, index)

class ImageCarouselView(CarouselView):
    """A CarouselView containing images"""
    def __init__(self, parent, imagewidth, imageheight):
        """Initiate the carouselview. 

        Arguments
        parent -- the frame on which to layout the carousel view
        imagewidth - the width of the images to display
        imageheight - the height of the images to display
                
        """
        CarouselView.__init__(self, parent, imagewidth, imageheight)

    def _drawItem(self, labelindex, itemindex):
        """Display one of the items. 
        
        Arguments
        labelindex -- the index of the label on which to display the item
        itemindex -- the index of the item to display
        
        """
        if(self._list[itemindex].smallimage is not None):
            self._labels[labelindex].config(image = self._list[itemindex].smallimage)
            self._labels[labelindex].grid()

class TextCarouselView(CarouselView):
    """Displays a list of images and highlights one item"""
    def __init__(self, parent, reqwidth, reqheight):
        """Initiate the carouselview. 

        Arguments
        parent -- the frame on which to layout the carousel view
        reqwidth - the width of the images to display
        reqheight - the height of the images to display
                
        """
        CarouselView.__init__(self, parent, reqwidth, reqheight)
        
        font = tkFont.Font(family="Arial", size=10)
        
        for i in self._labels:
            i.config(font = font, wraplength = reqwidth, bg = 'white')

    def _drawItem(self, graphicindex, itemindex):
        """Display one of the items. 
        
        Arguments
        labelindex -- the index of the label on which to display the item
        itemindex -- the index of the item to display
        
        """
        self._labels[graphicindex].config(text = self._list[itemindex])
        self._labels[graphicindex].grid()
