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
import os.path
import urllib
import uuid
from Tkinter import END
import PIL.Image as Image
import PIL.ImageTk as ImageTk

from common import getTextNodeValue
from itemharvester import harvestBookInfo, CouldNotReadBookError
from formattedtext import filterHtml
from item import BookItem
from video import createVideo

#Identifiers in RSS blog contents
el_published = 'published'
el_entry = 'entry'
el_id = 'id'
el_content = 'content'
el_category = 'category'
el_title = 'title'
attr_term = 'term'

#Identifiers in cached content
el_video = 'Video'
attr_video = 'Video'
attr_id = 'Id'
attr_filename = 'Filename'

#Identifiers in RSS search contents
el_item = 'item'
el_link = 'link'


_isbnkey = 'ISBN'
_isbnseparators = ':'

class BlogPostData:
    """Data about one blog post"""
    def __init__(self, entrynode):
        """Create BlogPostData
        
        Argument
        entrynode -- XML node containing the data that will be extracted
        
        """
        self.subjects = []
        
        self.id = getTextNodeValue(entrynode, el_id)
        self.title = getTextNodeValue(entrynode, el_title)
        self.content = getTextNodeValue(entrynode, el_content)
        
        categorynodes = entrynode.getElementsByTagName(el_category)
        
        for i in categorynodes:
            self.subjects.append(i.attributes[attr_term].value)
            
class BlogspotItem(BookItem):
    """
    A generic blog post harvested from Blogspot. Subclass BlogspotItemWithImage is used in the Hylte display; 
    subclass BlogspotItemWithIsbn is used in the third Varberg display. 
    
    """
    def __init__(self, (dir, dims, smalldims, library), xmlnode = None, blogpostdata = None):
        """Create BlogspotItem.
        
        Arguments
        dir -- the cache directory
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        library -- if not None only books from this library will be considered
        xmlnode -- if not None the BlogspotItem will be loaded from this cache node
        blogpostdata -- if not None the BlogspotItem will be loaded from this BlogPostData
        
        """
        BookItem.__init__(self, dims, smalldims)
        self._video = ''

        if(xmlnode is not None):
            self._loadfromcache(xmlnode, dir)
            self._loadimage(dims, smalldims)
            self._formattext()
        elif(blogpostdata is not None):
            self.uid = str(uuid.uuid1())
            self._rawtitle = blogpostdata.title
            self.section = ''
            self.shelf = ''
            self.subjects = blogpostdata.subjects
            rawtext = blogpostdata.content
            self._rawtext = rawtext
            self._formattext()
            self._createVideoIfAvailable(dir)

        self._setVideo()

    def getXml(self, doc, name):
        """"Return an XML representation of this BlogspotItem.
        
        Arguments
        doc -- the XML doc in which to create the node
        name -- the name of the node
        
        """
        element = BookItem.getXml(self, doc, name)
        element.setAttribute(attr_video, os.path.basename(self._video))
        return element

    def cleanup(self):
        """Clean up data associated with this item."""
        
        if(self._video != ''):
            try:
                os.remove(self._video)
            except OSError:
                print('Could not delete ' + self._video)

        BookItem.cleanup(self)

    def _loadfromcache(self, xmlnode, dir):
        """Load the BlogspotItem from cache
        
        Argument
        xmlnode -- XML node describing this item
        
        """
        BookItem._loadfromcache(self, xmlnode, dir)
        
        if((xmlnode.attributes[attr_video] is not None) and
            (xmlnode.attributes[attr_video].value != '')):
            self._video = os.path.join(dir, xmlnode.attributes[attr_video].value)
        else:
            self._video = ''

    def _createVideoIfAvailable(self, dir):
        """If this blog item has an associated video, create a html page for it
        
        Argument
        dir -- the directory where the video web page will be stored 

        """        
        if(self._formattedtext is None):
            return

        videosrc = self._formattedtext.getFirstVideo()

        if(videosrc is not None):
            try:
                self._video = createVideo(videosrc, dir, self.uid)
            except:
                self._video = ''

    def _setVideo(self):
        """Assign the associated video. if any, to the formatted text"""
        if(self._video != '' and self._formattedtext is not None):
            self._formattedtext.setFirstVideo(self._video)
            
class BlogspotItemWithImage(BlogspotItem):
    """A blog post harvested from Blogspot. If the blog post contains an image, that image 
    will be displayed as the main image of the blog post.  
    
    """
    def __init__(self, (dir, dims, smalldims, library), xmlnode = None, blogpostdata = None):
        BlogspotItem.__init__(self, (dir, dims, smalldims, library), xmlnode, blogpostdata)

        if(xmlnode is not None):
            self._imgsrcurl = ''
        elif(blogpostdata is not None):
            self._getFirstImageFromFormattedText(dir, blogpostdata.title)

class BlogspotItemWithIsbn(BlogspotItem):
    """A blog post harvested from Blogspot. The topic of each blog post is a book
    and each blog post shall contain and ISBN number of the format ISBN [number].
    
    """
    def __init__(self, (dir, dims, smalldims, library, searchprefix, searchsuffix), xmlnode = None, blogpostdata = None):
        """Create BlogspotItemWithIsbn.
        
        Arguments
        dir -- the cache directory
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        library -- if not None only books from this library will be considered
        xmlnode -- if not None the BlogspotItemWithIsbn will be loaded from this cache node
        blogpostdata -- if not None the BlogspotItemWithIsbn will be loaded from this BlogPostData
        
        """
        BlogspotItem.__init__(self, (dir, dims, smalldims, library), xmlnode, blogpostdata)
        self._searchprefix = searchprefix
        self._searchsuffix = searchsuffix

        if(xmlnode is not None):
            self._imgsrcisbn = ''
        elif(blogpostdata is not None):
            isbn = self._findISBN(self._rawtext)
            #self.uid = isbn
            self._imgsrcisbn = isbn

            if(isbn == ''):
                try:
                    print('Can\'t read isbn from blog post ' + self._rawtitle)
                except:
                    print('Can\'t read isbn')

                self.valid = False
                return
        
            self._imagename = os.path.join(dir, isbn + ".jpg")
            
            if(not self._tryGetBookInfo(isbn, library)):
                self.valid = False
                return

    def _tryGetBookInfo(self, isbn, library):
        url = self._searchprefix + isbn + self._searchsuffix

        try:
            rssobj = urllib.urlopen(url)
        except IOError:
            print('Error: Could not read url ' + url)
            return False

        try:
            rssdoc = parse(rssobj)
        except xml.dom.DOMException:
            print('Error: Could not read RSS')
            return False
        finally:
            rssobj.close()

        nodes = rssdoc.getElementsByTagName(el_item)

        if(nodes.length < 0):
            return False

        for i in nodes:
            link = getTextNodeValue(i, el_link)
            
            try:
                data = harvestBookInfo(link, library)
            except Exception as e:
                print('BlogPostItem ' + self._rawtitle + ':\n  ' + e.value)
            else:
                self._selectShelf(data.shelves)
                self.section = data.section
                return True

        return False

    def _findISBN(self, rawtext):
        """Find an ISBN in a text. 
        
        Argument
        rawtext -- the text to search for ISBN
        
        """
        isbn = ''
        rawtext = filterHtml(rawtext)
        isbnindex = rawtext.rfind(_isbnkey)
        
        if(isbnindex >= 0):
            index = isbnindex + len(_isbnkey)
            
            try:
                while(rawtext[index].isspace() or rawtext[index] in _isbnseparators):
                    index += 1
            
                while((index < len(rawtext)) and (rawtext[index].isdigit() or rawtext[index].isspace())):
                    if(rawtext[index].isdigit()):
                        isbn = isbn + rawtext[index]
                    index += 1
                
                rawtext = rawtext[:isbnindex] + rawtext[index:]
            except IndexError:
                print('Illegal format in ISBN in blog post ' + self._rawtitle)
                isbn = ''

        return isbn

class BlogspotHarvester:
    """Harvest blog posts from a Blogspot blog."""
    def __init__(self, dsd, addandcheckfunc, itemtype):
        """Create BlogspotHarvester
        
        Arguments
        dsd -- data description source for the blog
        addandcheckfunc -- function that checks if the harvester needs to harvest more items
        
        """
        self.newestId = ''

        self._url = dsd.link
        self._addandcheckfunc = addandcheckfunc
        self._itemtype = itemtype

    def update(self, amount = 0):
        """Look for new blog posts.
        
        Argument
        amount -- if specified, amount blog posts will be harvested
        
        """
        #url = r'http://' + self._blogname + '.blogspot.com/feeds/posts/default'
        
        if(amount > 0):
            url = self._url + r'?redirect=false&max-results=' + amount
        else:
            url = self._url

        try:
            blogobj = urllib.urlopen(url)
        except IOError:
            print('Error: could not read url ' + url)
            return
        
        try:
            rssdoc = parse(blogobj)
        except xml.dom.DOMException:
            print('Error: Could not read RSS')
            return
        finally:
            blogobj.close()
                
        nodes = rssdoc.getElementsByTagName(el_entry)
        newestId = getTextNodeValue(nodes.item(0), el_published)
        
        if(self.newestId != newestId):
            for i in nodes:
                id = getTextNodeValue(i, el_published)
    
                if(id == self.newestId):
                    break
    
                try:
                    bpd = BlogPostData(i)
                    bpi = self._itemtype(self.itemarg, blogpostdata = bpd)
                except Exception as e:
                    print('BlogspotHarvester: Could not create BlogspotItem; ' + str(e))
                    continue
                
                done = self._addandcheckfunc(bpi)
                
                if(done):
                    print(self.id + ': I don''t need to read more blog posts\n')
                    break

            self.newestId = newestId
        else:
            print('There are no new items; newest item @ ' + self.newestId)
