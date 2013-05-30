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
from itemview import ItemView, defaultpadding, strippadding, textpadding
import language as lng
from common import getFont
import htmlunit
from buttonscrollbar import ButtonScrollbar

class BookView(ItemView):
    """Contain a list of book items and display detailed information about one 
    of the books.
    
    """
    def __init__(self, frame, bgcolor, settings):
        """Initiate the bookview
        
        Arguments
        frame -- the frame on which to layout the displayed information
        bgcolor -- background color of the frame
        settings -- object containing font settings
        
        """
        ItemView.__init__(self, settings)
        
        self._svTitle = tki.StringVar()
        self._svAuthor = tki.StringVar()
        self._svLocation = tki.StringVar()
        
        fntAuthor = getFont(settings.authorfontname, settings.authorfontsize, 
                                  settings.authorfontstyle)

        fntShelf = getFont(settings.footerfontname, settings.footerfontsize, 
                                  settings.footerfontstyle)

        width = frame['width']
        frame.rowconfigure(3, weight = 1)
        frame.columnconfigure(0, weight = 1)
        
        if(settings.scrollenabled):
            bsb = ButtonScrollbar(frame, settings)
            bsb['bg'] = 'white'
            width -= bsb.getWidth()
            bsb.grid(row = 3, column = 1, sticky = tki.NS)

        l = tki.Label(frame)
        self._lblImage = l
        
        l.grid(row = 0, column = 0, pady = defaultpadding)
        l = tki.Label(frame, textvariable = self._svTitle, font = self._fntHeader, wraplength = width - (2 * textpadding), 
                      justify="left", bg="white")
        
        l.grid(row = 1, column = 0, pady = defaultpadding)
        l = tki.Label(frame, textvariable = self._svAuthor, font = fntAuthor, wraplength = width - (2 * textpadding), 
                      justify="left", bg="white")

        l.grid(row = 2, column = 0, pady = defaultpadding)

        t = tki.Text(frame, width = width - (2 * textpadding), height = 96, wrap = tki.WORD, bg="white", font = self._fntNormal, 
                     relief = tki.FLAT)
        t.grid(row = 3, column = 0, padx = textpadding, pady = defaultpadding, sticky = tki.W + tki.N)
        self._tDesc = t

        if(settings.scrollenabled):
            bsb.addScrollable(t)

        f = tki.Frame(frame, bg = bgcolor)
        f.grid(row = 4, column = 0, padx = strippadding, sticky = tki.W + tki.E)
        f.columnconfigure(0, weight = 1)
        
        l = tki.Label(f, textvariable = self._svLocation, bg = bgcolor, font = fntShelf, fg="white")
        l.grid(padx = defaultpadding, sticky = tki.E + tki.S)

    def toHtml(self):
        """Return an HTML representation of the currently displayed book"""
        if(self._currentitem is None):
            return ''
        
        defs = dict()
        defs[htmlunit.authorkey] = self._currentitem.author
        defs[htmlunit.imagekey] = self._currentitem._imagename
        defs[htmlunit.imagewidthkey] = str(self._currentitem.image.width())
        defs[htmlunit.imageheightkey] = str(self._currentitem.image.height())
        defs[htmlunit.titlekey] = self._currentitem.title
        defs[htmlunit.headlinekey] = self._currentitem.title
        defs[htmlunit.textkey] = self._currentitem.getPlainText()
        
        return htmlunit.createHtml(defs)

    def _displayItem(self, item):
        """Display a book item. 
        
        Arguments
        item -- the book item to display
        
        """
        ItemView._displayItem(self, item)

        self._svAuthor.set(item.author)
        self._svLocation.set(lng.lang[lng.txtLocatedAt] + ' ' + item.shelf)
