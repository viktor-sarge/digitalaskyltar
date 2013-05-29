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
import urllib
import re

import itemharvester
import funcSaveCover
from common import textToCData, getTextNodeValue, getCDataNodeValue, textToFilename
from formattedtext import filterHtml, replaceEscapeSequences
from language import lang
import language as lng
from formattedtext import FormattedText
from item import ImageItem

#RSS feed
el_title = 'title'
el_rssitem = 'item'

el_channel = 'channel'
el_rssitem = 'item'
el_link = 'link'
el_pubdate = 'pubDate'
el_rssdesc = 'description'
el_rsscontent = 'content:encoded'

_idDelimiter = '#'
_issueDelimiters = ' /'
_yearDigits = 4
_yearRegexp = '[0-9][0-9][0-9][0-9]'

class WordPressItem(ImageItem):
    """A blog post harvested from Wordpress. Each of these blog posts is about 
    an issue of a magazine and they begin with a unique identifier 
    of the following format:
    
    [magazine name] #[issue number] [year] 
    
    """
    def __init__(self, (dir, dims, smalldims), cachexml = None, rssxml = None):
        """Create WordPressItem
        
        Arguments
        dir -- the cache directory
        dims -- tuple containing normal width and height of the image
        smalldims -- tuple containing small width and height of the image
        cachexml -- if not None the WordPressItem will be loaded from this cache node
        rssxml -- if not None the WordPressItem will be loaded from this RSS XML element
        
        """
        ImageItem.__init__(self, dims, smalldims)

        if(cachexml is not None):
            self._loadfromcache(cachexml, dir)
            self._setId()
            self._loadimage(dims, smalldims)
        elif(rssxml is not None):
            title = getTextNodeValue(rssxml, el_title)
            self._rawtitle = title
            self._rawtext = getCDataNodeValue(rssxml, el_rsscontent)
            self._setUid()
            self._setId()
            self._imagename = ''
            
        self._formattext()
        
        if(rssxml is not None):
            if(self._formattedtext is not None):
                imagesrc = self._formattedtext.getFirstImage()
                
                if(imagesrc is not None):
                    #TBD This is not good
                    imagesrc = imagesrc.split('?')[0]
                    self._imgsrcurl = imagesrc
                    filename = textToFilename(self.uid) + os.path.split(imagesrc)[1]
                    self._imagename = os.path.join(dir, filename)
            else:
                print('Could not get formatted text from ' + title)
                    
#    def loadData(self):
#        """If necessary, download and load the image associated with this WordPressItem."""
#        if((self._imagename != '') and (self.image is None)):
#            try:
#                funcSaveCover.saveGenericImage(self._url, self._imagename)
#                self._loadimage(self._dims, self._smalldims)
#            except IOError:
#                print('Could not get image ' + self._url)

    def _setUid(self):
        """Get the unique identifier for this blog post.
        The uid ends with the year and the parsed uid contains all text up to
        the first four consecutive digits. 
        
        """
        text = filterHtml(self._rawtext)
        myear = re.search(_yearRegexp, text)

        if(myear is None):
            raise Exception('Unable to parse year')
            
        year = myear.group(0)
        endpos = text.find(year) + _yearDigits
        self.uid = text[:endpos]

    def _setId(self):
        """Set the issue id of this blog post."""
        pos = self.uid.find(_idDelimiter)
        self.name = replaceEscapeSequences(self.uid[:pos].strip())
        issuetext = self.uid[pos + 1:]
        issuetext = issuetext[:len(issuetext) - _yearDigits]
        issuetext = issuetext.strip(_issueDelimiters)
        year = self.uid[len(self.uid) - _yearDigits:]
        #self.issue = lang[lng.txtIssue] + ' ' + issuetext + ' / ' + year
        self.issue = issuetext + ' / ' + year

class WordpressHarvester:
    """Harvest blog posts from a Wordpress blog."""
    def __init__(self, dsd, addandcheckfunc):
        """Create WordpressHarvester
        
        Arguments
        dsd -- data description source for the blog
        addandcheckfunc -- function that checks if the harvester needs to harvest more items
        
        """
        self.newestId = ''

        self._url = dsd.link
        self._addandcheckfunc = addandcheckfunc

    def update(self):
        """Look for new blog posts."""
        #url = r'http://' + self._blogname + '.blogspot.com/feeds/posts/default'

        try:
            blogobj = urllib.urlopen(self._url)
        except IOError:
            print('Error: could not read url ' + self._url)
            return
        
        try:
            rssdoc = parse(blogobj)
        except xml.dom.DOMException:
            print('Error: Could not read RSS')
            return
        finally:
            blogobj.close()
                
        nodes = rssdoc.getElementsByTagName(el_channel)
        
        if(nodes.length <= 0):
            raise Exception('No channel found in rss feed')
        
        chnode = nodes[0]
        nodes = chnode.getElementsByTagName(el_rssitem)
        newestId = getTextNodeValue(nodes.item(0), el_pubdate)
        
        if(self.newestId != newestId):
            for i in nodes:
                id = getTextNodeValue(i, el_pubdate)
    
                if(id == self.newestId):
                    break
    
                try:
                    item = WordPressItem(self.itemarg, rssxml = i)
                except:
                    print('WordpressHarvester: Could not create WordPressItem')
                    continue

                done = self._addandcheckfunc(item)
                
                if(done):
                    #print(self.id + ': I don''t need to read more blog posts\n')
                    break

            self.newestId = newestId
        else:
            print('There are no new items; newest item @ ' + self.newestId)
