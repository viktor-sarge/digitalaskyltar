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
import shutil

_xmlname = 'cache.xml'
el_items = 'CachedItems'
el_item = 'Item'
el_desc = 'Desc'
el_newest = 'NewestId'
attr_id = 'Id'

class Cache:
    """Handle caching of items from a data source"""
    
    def __init__(self, dir, itemclass, itemarg):
        """Create Cache. 
        
        Arguments
        dir -- cache directory
        itemclass -- the class of the items that are stored in the cache; used when the cache is loaded from disk;
                     shall contain a function getXml that returns an xml element
        itemarg -- argument to the constructor of itemclass

        """
        self._cachedir = dir
        self._itemclass = itemclass
        self._itemarg = itemarg

        self.items = []
        self.newestId = ''
        
        self._load()

    def updateContents(self, items, newestId):
        """Update the contents of the cache
        
        Arguments
        items -- a list of items to cache
        newestId -- a tag representing the newest data item from the data source

        """        
        self.items = items
        self.newestId = newestId
        self._save()
    
    def _load(self):
        """Load cache."""
        #Initiate list by reading cache        
        filename = os.path.join(self._cachedir, _xmlname)
        
        try:
            xmldoc = parse(filename)
        except IOError:
            print('Error: Could not load cache from file ' + filename)
            return
        except xml.dom.DOMException:
            print('Error: Invalid cache xml file ' + filename)
            return
        except:
            print('Unexpected exception; could not load cache from file ' + filename)
            return

        nodes = xmldoc.documentElement.getElementsByTagName(el_item)
    
        for itemnode in nodes:
            try:
                item = self._itemclass(self._itemarg, itemnode)
                self.items.append(item)
            except:
                print('Cache: Could not create item')

        nodes = xmldoc.documentElement.getElementsByTagName(el_newest)
        
        self.newestId = nodes.item(0).attributes[attr_id].value
        print('newest id = ' + self.newestId)

    def _save(self):
        """Save cache."""
        xmldoc = Document()
        root = xmldoc.createElement(el_items)
        xmldoc.appendChild(root)
        
        node = xmldoc.createElement(el_newest)
        node.setAttribute(attr_id, self.newestId)
        root.appendChild(node)
        
        for i in self.items:
            node = i.getXml(xmldoc, el_item)
            root.appendChild(node)
            
        filename = os.path.join(self._cachedir, _xmlname)

        try:
            file = open(filename, "w")
            text = xmldoc.toxml("utf-8")
            file.write(text)
            file.close()
        except IOError, e:
            print('Could not save cache; ', e)
