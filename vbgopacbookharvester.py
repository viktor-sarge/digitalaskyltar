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
import re

import itemharvester
from common import resizeImage, getTextNodeValue, getCDataNodeValue
from item import BookItem

#OpacBookItem
attr_author = 'Author'

#RSS feed
el_channel = 'channel'
el_rssitem = 'item'
el_link = 'link'
el_pubdate = 'pubDate'
el_rssdesc = 'description'

#This text appears at the end of the shelves in the youth department
_youthdepartmentextension = 'Ung'

def isInYouthDepartment(shelf):
    """Check if a shelf is located in the youth department

    Argument
    shelf -- the shelf to check

    """
    return shelf.upper().endswith(_youthdepartmentextension.upper())

class OpacBookItem(BookItem):
    """A BookItem harvested from the Varberg OPAC RSS feed."""
    def __init__(self, (dir, dims, smalldims, library), xmlnode = None, url = None):
        """Initiate the OpacBookItem. Either xmlnode xor url shall be specified. 
        
        Arguments
        dir -- the cache directory
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        library -- if not None only books from this library will be considered
        xmlnode -- if not None the  OpacBookItem will be loaded from this cache node
        url -- if not None the OpacBookItem will be loaded from this url
        
        """
        BookItem.__init__(self, dims, smalldims)

        if(xmlnode is not None):
            self._loadfromcache(xmlnode, dir)
            self.author = xmlnode.attributes[attr_author].value
            self._loadimage(dims, smalldims)
        elif(url is not None):
            try:
                data = itemharvester.harvestBookInfo(url, library)
            except:
                self.valid = False
                return
            
            self._rawtitle = data.title
            self.author =  data.author
            self._rawtext =  data.rawtext
            self.uid =  data.isbn
            self._selectShelf(data.shelves)
            self.section = data.section
            self.subjects = data.subjects
            
            if(self.uid == ''):
                self.valid = False
                return
            else:
                self._imagename = os.path.join(dir, self.uid + ".jpg")
                self._imgsrcisbn = data.isbn

            if(self._rawtext == ''):
                self.valid = False
                return

        self._formattext()

    def getXml(self, doc, name):
        """"Return an XML representation of this OpacBookItem.
        
        Arguments
        doc -- the XML doc in which to create the node
        name -- the name of the node
        
        """
        element = BookItem.getXml(self, doc, name)        
        element.setAttribute(attr_author, self.author)

        return element

    def _loadfromcache(self, xmlnode, dir):
        """Load the OpacBookItem from cache
        
        Argument
        xmlnode -- XML node describing this item
        
        """
        BookItem._loadfromcache(self, xmlnode, dir)
        self.author = xmlnode.attributes[attr_author].value

class OpacYouthBookItem(OpacBookItem):
    """This is an OpacBookItem where the shelf is set to the first shelf 
    found in the youth department

    """
    def _selectShelf(self, shelves):
        """Select which shelf this BookItem belongs to

        Select the first shelf found in the youth department if any, 
        otherwise the first shelf. 

        Argument
        shelves -- all shelves where this book exists

        """
        if(shelves != []):
            self.shelf = shelves[0]

            for i in shelves:
                if(isInYouthDepartment(i)):
                    self.shelf = i
                    return

            self.shelf = shelves[0]
        else:
            self.shelf = ''

class VarbergOpacHarvester:
    """Harvest books from the OPAC RSS feed."""
    def __init__(self, dsd, settings, addandcheckfunc):
        """Initiate harvester
        
        Arguments
        dsd -- datasource description
        settings -- settings
        addandcheckfunc -- function that checks if the harvester needs to harvest more items
        
        """
        self._url = dsd.link
        self.newestId = ''
        self._addandcheckfunc = addandcheckfunc
        self._library = settings.library
        self._itemclass = OpacBookItem
        
        #TBD debug
        self.id = dsd.cacheid

    def update(self):
        """Look for new books."""
        print(self.id + ': I will look for new books')
        
        self._readRssChannel(self._url)

    def _readRssChannel(self, url):
        """Extract books from an OPAC RSS channel until no more books need 
        to be extracted
        
        Argument
        url -- url to the RSS channel
        
        """
        #Get rss data
        try:
            rssobj = urllib.urlopen(url)
        except IOError:
            print('Error: Could not read url ' + url)
            return

        try:
            rssdoc = parse(rssobj)
        except xml.dom.DOMException:
            print('Error: Could not read RSS')
            return
        finally:
            rssobj.close()
        
        nodes = rssdoc.getElementsByTagName(el_channel)
        
        if(nodes.length < 0):
            raise Exception('No channel found in rss feed')
        
        chnode = nodes[0]
        ctr = 0
        newItems = []
        nodes = chnode.getElementsByTagName(el_rssitem)

        if(nodes.length > 0):
            id = self._getId(nodes.item(0))
            
            if(id == self.newestId):
                print(self.id + ': No more new items')
            else:
                newestId = id

                #Extract items from rss data
                for i in nodes:
                    if(i.nodeType == i.ELEMENT_NODE):
                        id = self._getId(i)
                        
                        #Check if the element is new
                        if(id == self.newestId):
                            print(self.id + ': No more new items')
                            break
                        
                        #Check if the element comes from the correct library
                        desc = getCDataNodeValue(i, el_rssdesc)
                        library = self._getlibrary(desc)
                        
                        if(library == self._library):
                            url = getTextNodeValue(i, el_link)
                            
                            try:
                                item = self._itemclass(self.itemarg, url = url.strip())
                            except:
                                print('VarbergOpacHarvester: Could not create OpacBookItem')
                                continue

                            done = self._addandcheckfunc(item)
            
                            if(done):
                                print(self.id + ': I don''t need to read more items\n')
                                break

                self.newestId = newestId

    def _getlibrary(self, desc):
        """Get a library from an OPAC description
        
        Argument
        desc -- an OPAC description
        
        """
        key = 'Biblioteksenhet:'
        pos1 = desc.find(key)
        pos2 = desc.find('<', pos1)
        library = desc[pos1 + len(key):pos2]

        return library.strip()

    def _getId(self, node):
        """Get an id for an OPAC RSS item.
        
        Argument
        node -- the RSS XML node to extract the id from
        
        """
        for i in node.childNodes:
            if(i.nodeType == i.ELEMENT_NODE):
                if(i.nodeName == el_pubdate):
                    for j in i.childNodes:
                        if(j.nodeType == j.TEXT_NODE):
                            timestamp = j.nodeValue.strip()
                elif(i.nodeName == el_link):
                    for j in i.childNodes:
                        if(j.nodeType == j.TEXT_NODE):
                            link = j.nodeValue.strip()
                            
        return timestamp + '_' + link

_subjectKey = r'@SUBJECT@'
_opacRssSearchBase = r'searchtype=advanced&txtSubject=' + _subjectKey + r'&ComboSortorder=1&RadioDisplayResult=3'
_subjectListDelim = r'|'
_subjectValueDelim = r'^'

class VarbergOpacSubjectSearchHarvester(VarbergOpacHarvester):
    """Harvest books from an OPAC RSS feed generated by searching for all subjects"""
    def __init__(self, dsd, settings, addandcheckfunc):
        """Initiate harvester
        
        Arguments
        dsd -- datasource description
        settings -- settings
        addandcheckfunc -- function that checks if the harvester needs to harvest more items
        
        """
        VarbergOpacHarvester.__init__(self, dsd, settings, addandcheckfunc)
        self._itemclass = OpacYouthBookItem
        self.doesUpdate = False
        self._subjects = []

        for subject in settings.subjects:
            self._subjects.append((subject, self._getEncodedSubject(subject)))

    def update(self):
        """Look for new books
        
        One search will be made for each subject.
        
        """
        self.doesUpdate = True

        #Extract newest id for all subjects
        uidTable = dict()
        subjectlist = self.newestId.split(_subjectListDelim)
        
        for i in subjectlist:
            l = i.split(_subjectValueDelim)
            
            if(len(l) == 2):
                uidTable[l[0]] = l[1]

        #Check for new books
        for (subject, escSubject) in self._subjects:
            try:
                self.newestId = uidTable[subject]
            except KeyError:
                self.newestId = ''
            
            self.currentSubject = subject
            url = self._url + re.sub(_subjectKey, escSubject, _opacRssSearchBase)
            self._readRssChannel(url)
            print('  ...subject ' + subject.encode('utf-8') + ' done!')
            
            uidTable[subject] = self.newestId

        #Create newest id string to store in cache
        self.newestId = ''
        newestId = ''
        
        for (subject, escSubject) in self._subjects:
            newestId = subject + _subjectValueDelim
            
            try:
                id = uidTable[subject]
            except:
                id = ''
            
            newestId = newestId + id + _subjectListDelim
            self.newestId = self.newestId + newestId
        
        #Remove last delimiter
        self.newestId = self.newestId[:-1]
        self.doesUpdate = False

    def _getEncodedSubject(self, subject):
        """Return the argument with all non-ASCII characters escaped
        
        Argument
        subject -- the subject to escape
        
        """
        result = ''

        for c in subject:
            value = ord(c)
            
            #Is it an ASCII character? 
            if(value < 128):
                result = result + c
            else:
                result = result + r'%%u%04x' % value

        return result

    def _getlibrary(self, desc):
        """Always return desired library
        
        Since there is no library data in the search RSS stream where this 
        function is called it will always assume that the book is present 
        at the desired library. 
        
        Argument
        desc -- an OPAC description
        
        """
        return self._library

    def _getId(self, node):
        """Get an id for an OPAC RSS item.
        
        Argument
        node -- the RSS XML node to extract the id from
        
        """
        for i in node.childNodes:
            if(i.nodeType == i.ELEMENT_NODE):
                if(i.nodeName == el_link):
                    for j in i.childNodes:
                        if(j.nodeType == j.TEXT_NODE):
                            return j.nodeValue.strip()
                            
        raise Exception('VarbergOpacSubjectSearchHarvester: RSS item has no link')
