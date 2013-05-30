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

from common import getFont
import htmlunit

defaultpadding = 10
strippadding = 20
textpadding = 30

class ItemView:
    """Contain a list of items and display detailed information about one of the items."""
    def __init__(self, settings):
        """Initiate the itemview
        
        Arguments
        settings -- object containing font settings
        
        """
        self._currentitem = None
        self._normalfontname = settings.normalfontname
        self._normalfontsize = settings.normalfontsize

        self._fntHeader = getFont(settings.headerfontname, settings.headerfontsize, 
                                  settings.headerfontstyle)
        
        self._fntNormal = getFont(settings.normalfontname, settings.normalfontsize, 
                                  settings.normalfontstyle)

    def setContent(self, list, index):
        """Set the content and the displayed index
        
        Arguments
        list -- a list containing the content
        index -- the currently active index
        
        """
        self._list = list
        self._index = index
        self._displayItem(self._list[self._index])
        
    def next(self):
        """Browse to next item"""
        self._index += 1
        
        if(self._index >= len(self._list)):
            self._index = 0
        
        self._displayItem(self._list[self._index])
        
    def prev(self):
        """Browse to previous item"""
        self._index -= 1
        
        if(self._index < 0):
            self._index = len(self._list) - 1

        self._displayItem(self._list[self._index])

    def toHtml(self):
        """Return an HTML representation of the currently displayed item"""
        if(self._currentitem is None):
            return ''
        
        defs = dict()

        defs[htmlunit.imagekey] = self._currentitem._imagename
        defs[htmlunit.imagewidthkey] = str(self._currentitem.image.width())
        defs[htmlunit.imageheightkey] = str(self._currentitem.image.height())
        defs[htmlunit.titlekey] = self._currentitem.title
        defs[htmlunit.headlinekey] = self._currentitem.title
        defs[htmlunit.textkey] = self._currentitem.getPlainText()
        
        return htmlunit.createHtml(defs)

    def clear(self):
        """Clear the contents of the Text component
        
        The primary use for this function is to shut down any 
        multimedia content in the Text component. 

        """
        self._tDesc.config(state = tki.NORMAL)
        self._tDesc.delete(1.0, tki.END)
        self._tDesc.config(state = tki.DISABLED)

    def _displayItem(self, item):
        """Display an item. 
        
        Arguments
        item -- the item to display
        
        """
        self._currentitem = item

        if(item.image is not None):
            self._lblImage.config(image = item.image)
            self._lblImage.grid()
        else:
            self._lblImage.grid_remove()
            
        self._svTitle.set(item.title)
        self._tDesc.config(state = tki.NORMAL)
        self._tDesc.delete(1.0, tki.END)
        #Don't specify font style here; it will be specified from the formatted text
        item.addDescription(self._tDesc, (self._normalfontname, self._normalfontsize, ''))
        self._tDesc.config(state = tki.DISABLED)
