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
from xml.dom.minidom import parse, Document
import xml.dom
import os
import os.path
from Tkinter import END

import PIL.Image as Image
import PIL.ImageTk as ImageTk

from funcSaveCover import saveFrontcoverOfBook, saveGenericImage
from common import resizeImage, getTextNodeValue, getCDataNodeValue, textToFilename
from formattedtext import FormattedText, filterHtml, replaceEscapeSequences

#Item
el_rawtext = 'RawText'
attr_title = 'Title'
attr_uid = 'UID'

#BookItem
attr_image = 'Image'
el_subject = 'Subject'
attr_shelf = 'Shelf'
attr_id = 'Id'
attr_section = 'Section'

class Item:
    """Super class of all items that are harvested, cached and displayed."""
    def __init__(self):
        """Initiate the item."""
        self.valid = True

    def getXml(self, doc, name):
        """"Return an XML representation of this Item.
        
        Arguments
        doc -- the XML doc in which to create the node
        name -- the name of the node
        
        """
        element = doc.createElement(name)
        element.setAttribute(attr_title, self._rawtitle)
        element.setAttribute(attr_uid, self.uid)
        descelement = doc.createElement(el_rawtext)
        descelement.appendChild(doc.createTextNode(self._rawtext))
        element.appendChild(descelement)
        
        return element

    def addDescription(self, textwidget, font):
        """Add a description at the end of a Tkinter Text widget.
        If the description is formatted a formatted text will be added; 
        otherwise a plain text will be added. 
        
        Arguments
        textwidget -- the Tkinter Text widget where the description will be added
        font -- the font to use if the text is formatted
        
        """
        if(self._formattedtext is not None):
            self._formattedtext.addDescription(textwidget, font)
        else:
            textwidget.insert(END, self._strippedtext)

    def _loadfromcache(self, xmlnode):
        """Load the Item from cache
        
        Argument
        xmlnode -- XML node describing this item
        
        """
        self._rawtitle = xmlnode.attributes[attr_title].value
        self.uid = xmlnode.attributes[attr_uid].value
        self._rawtext = getTextNodeValue(xmlnode, el_rawtext)
        
    def loadData(self):
        """Load data associated with this Item."""
        pass
        
    def cleanup(self):
        """Clean up data associated with this Item."""
        pass
    
    def getPlainText(self):
        """Return an unformatted text representation of this Item."""
        return filterHtml(self._rawtext)

    def _formattext(self):
        """Format the texts of this Item."""
        self.title = replaceEscapeSequences(self._rawtitle)
        
        print('START '  + self.title)
        
        try:
            self._formattedtext = FormattedText(self._rawtext)
        except:
            #print('Error: Could not format text, falling back to plain text...')
            self._formattedtext = None
            self._strippedtext = filterHtml(self._rawtext)
            print('FELSLUT '  + self.title)
        else:
            print('SLUT '  + self.title)



    def __str__(self):
        return self.title

    def __repr__(self):
        return 'Item: ' + self.title

class ImageItem(Item):
    """An Item containing an image."""
    def __init__(self, dims, smalldims):
        """Initiate the ImageItem.
        
        Arguments
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        
        """
        Item.__init__(self)
        self._imagename = ''
        self._imgsrcisbn = None
        self._imgsrcurl = None
        self._dims = dims
        self._smalldims = smalldims
        self.image = None
        self.smallimage = None

    def getXml(self, doc, name):
        """"Return an XML representation of this ImageItem.
        
        Arguments
        doc -- the XML doc in which to create the node
        name -- the name of the node
        
        """
        element = Item.getXml(self, doc, name)
        element.setAttribute(attr_image, os.path.split(self._imagename)[1])

        return element

    def cleanup(self):
        """Clean up data associated with this item."""
        if(os.path.exists(self._imagename)):
            try:
                os.remove(self._imagename)
            except OSError:
                print('Could not delete ' + self._imagename)

    def _loadfromcache(self, xmlnode, dir):
        """Load the item from cache
        
        Argument
        xmlnode -- XML node describing this item
        dir -- the cache dir
        
        """
        Item._loadfromcache(self, xmlnode)
            
        if(xmlnode.attributes[attr_image].value == ''):
            self._imagename = ''
        else:
            self._imagename = os.path.join(dir, xmlnode.attributes[attr_image].value)

    def _loadimage(self, dims, smalldims):
        """Load the image in normal size and small size.
        
        Argument
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        
        """
        if(self._imagename == ''):
            self.image = None
            self.smallimage = None
        else:
            try:
                image = Image.open(self._imagename)
                previmage = resizeImage(image, dims[0], dims[1])
                self.image = ImageTk.PhotoImage(previmage)
                smallimage = resizeImage(image, smalldims[0], smalldims[1])
                self.smallimage = ImageTk.PhotoImage(smallimage)
            except IOError:
                print('Error: could not open ' + self._imagename)
                self.valid = False
                
    def _getFirstImageFromFormattedText(self, dir, id):
        """Find the first image, if any, and set the image filename and url accordingly
        
        Argument
        dir -- the directory where the image will be stored
        id -- a readable id of the item

        """
        if(self._formattedtext is not None):
            imagesrc = self._formattedtext.getFirstImage()
            
            if(imagesrc is not None):
                #TBD This is not good
                imagesrc = imagesrc.split('?')[0]
                self._imgsrcurl = imagesrc
                filename = textToFilename(self.uid) + os.path.split(imagesrc)[1]
                self._imagename = os.path.join(dir, filename)
        else:
            self._imgsrcurl = ''
            self._imagename = ''
            print('Could not get formatted text from ' + id)

    def loadData(self):
        """Load data associated with this BookItem."""
        if((self._imagename != '') and (self.image is None)):
            if(self._imgsrcisbn is not None):
                saveFrontcoverOfBook(self._imgsrcisbn, self._imagename)
            elif(self._imgsrcurl is not None):
                saveGenericImage(self._imgsrcurl, self._imagename)

            self._loadimage(self._dims, self._smalldims)

class BookItem(ImageItem):
    """An ImageItem containing additional book related information."""
    def __init__(self, dims, smalldims):
        """Initiate the BookItem.
        
        Arguments
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        
        """
        ImageItem.__init__(self, dims, smalldims)

    def getXml(self, doc, name):
        """"Return an XML representation of this ImageItem.
        
        Arguments
        doc -- the XML doc in which to create the node
        name -- the name of the node
        
        """
        element = ImageItem.getXml(self, doc, name)
        element.setAttribute(attr_shelf, self.shelf)
        element.setAttribute(attr_section, self.section)

        for i in self.subjects:
            node = doc.createElement(el_subject)
            node.setAttribute(attr_id, i)
            element.appendChild(node)

        return element
    
    def _loadfromcache(self, xmlnode, dir):
        """Load the item from cache
        
        Argument
        xmlnode -- XML node describing this item
        dir -- the cache dir
        
        """
        ImageItem._loadfromcache(self, xmlnode, dir)
        
        self.shelf = xmlnode.attributes[attr_shelf].value
        self.section = xmlnode.attributes[attr_section].value
            
        if(xmlnode.attributes[attr_image].value == ''):
            self._imagename = ''
        else:
            self._imagename = os.path.join(dir, xmlnode.attributes[attr_image].value)

        self.subjects = []
        cnodes = xmlnode.getElementsByTagName(el_subject)
        
        for node in cnodes:
            self.subjects.append(node.attributes[attr_id].value)

    def _selectShelf(self, shelves):
        """Select which shelf this BookItem belongs to
        
        Select the first shelf. 
        
        Argument
        shelves -- all shelves where this book exists
        
        """
        if(shelves != []):
            self.shelf = shelves[0]
        else:
            self.shelf = ''
