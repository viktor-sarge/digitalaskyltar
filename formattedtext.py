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
from Tkinter import END
from xml.dom.minidom import parse, parseString
from xml.dom import DOMException
import re

from videoframe import VideoFrame

_el_top = 'Top'
_ptid = 'PureText'

_bold = 'bold'
_italic = 'italic'
_strikeout = 'strikeout'
_underline = 'underline'

fntixFamily = 0
fntixSize = 1
fntixStyle = 2

_xmlescapeseqs = dict([('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', '\'')])
_htmlescapeseqs = dict([('&nbsp;', ' ')])
_numericseq = r'\&#[0-9]+;'
_headertagseq = r'^h[1-6]$'

def replaceXmlEscapeSequences(input):
    """Replace XML escape sequences
    
    Argument
    input -- the text in which to replace escape sequences
    
    """
    for k in _xmlescapeseqs.keys():
        input = re.sub(k, _xmlescapeseqs[k], input, flags = re.IGNORECASE)
        
    seqs = re.findall(_numericseq, input)
    
    for s in seqs:
        number = int(s[2:len(s)-1])
        subst = unichr(number)
        input = re.sub(s, subst, input)

    return input

def replaceHtmlEscapeSequences(input):
    """Replace HTML escape sequences
    
    Argument
    input -- the text in which to replace escape sequences
    
    """
    #Replace html space
    for k in _htmlescapeseqs.keys():
        input = re.sub(k, _htmlescapeseqs[k], input, flags = re.IGNORECASE)

    return input

def replaceEscapeSequences(input):
    """Replace escape sequences
    
    Argument
    input -- the text in which to replace escape sequences
    
    """
    input = replaceXmlEscapeSequences(input)
    input = replaceHtmlEscapeSequences(input)
    
    return input

def escapeXml(input):
    escapeseqs = dict(zip(_xmlescapeseqs.values(), _xmlescapeseqs.keys()))
    
    for k in escapeseqs.keys():
        input = re.sub(k, escapeseqs[k], input, flags = re.IGNORECASE)
    
    return input

def filterHtml(input):
    """Convert an HTML text to a readable text by stripping HTML elements, 
    replacing escape sequences and removing formatting of the HTML code.
    
    Argument
    input -- the HTML text to convert
    
    """
    #Remove all linebreaks
    input = re.sub('\n', '', input)
    
    #Replace html line break
    input = re.sub('<br/?>', '\n', input, flags = re.IGNORECASE)
    
    #Remove any remaining html element
    input = re.sub('<.*?>', '', input)
    
    #Remove tabs
    input = re.sub('\t', '', input, flags = re.IGNORECASE)

    #Replace escape sequences    
    input = replaceEscapeSequences(input)

    #Remove multiple linebreaks - only two in a row are allowed
#    input = re.sub('\n|\r\n{3,}', '\n\n', input, flags = re.IGNORECASE)
    
    return input

_basicxmlregexp = '@text@'
_basicxmldoc = r'<?xml version="1.0" encoding="utf-8"?><Node>' + _basicxmlregexp + '</Node>'

def repairMissingAmpersandEscape(input):
    """Add &amp; for each subsection between and including & and ; that is not parsable
    
    Argument
    input -- input XML string
    
    """
    result = ''
    prevpos = 0
    pos = input.find('&')
    
    if(pos < 0):
        return input

    while(pos >= 0):
        result = result + input[prevpos:pos]
        pos2 = input.find(';', pos + 1)
        
        if(pos2 < 0):
            pos3 = input.find('&', pos + 1)
            
            if(pos3 < 0):
                return result + '&amp;' + input[pos+1:]
            else:
                result = result + '&amp;' + input[pos+1:pos3]
                prevpos = pos3
                pos = pos3
                continue
        else:
            teststr = input[pos:pos2+1]
            testxml = re.sub(_basicxmlregexp, teststr, _basicxmldoc)

            try:
                parseString(testxml)
            except:
                print('Ogiltig xml ' + teststr)
                result = result + '&amp;'
                nextpos = pos+1
            else:
                result = result + teststr
                nextpos = pos2+1

        newpos = input.find('&', nextpos)
    
        if(newpos < 0):
            return result + input[nextpos:]
        else:
            prevpos = nextpos
            pos = newpos

    return result

_nsstartexp = r'<\w*:'
_nsstartrepl = r'<'
_nsendexp = r'<\/\w*:'
_nsendrepl = r'</'

def _removeNamespaceFromElements(text):
    """Remove namespace from xml elements
    
    Argument
    text -- an xml document
    
    """
    result = re.sub(_nsstartexp, _nsstartrepl, text)
    result = re.sub(_nsendexp, _nsendrepl, result)
    
    return result

class FormattedText:
    """A formatted text that can draw itself on a Tkinter Text widget."""
    def __init__(self, text):
        """Create a formatted text.
        
        Argument
        text -- the text to parse
        
        """
        self._items = []
        text =  replaceHtmlEscapeSequences(text)
        xml = r'<?xml version="1.0" encoding="utf-8"?><' + _el_top + '>' + text + '</' + _el_top + '>'
        xml = xml.encode('utf-8')
        xml = repairMissingAmpersandEscape(xml)
        xml = _removeNamespaceFromElements(xml)
        xmldoc = parseString(xml)
        
        for node in xmldoc.documentElement.childNodes:
            if(node.nodeType == node.ELEMENT_NODE):
                self._items.append(TextItem(xml = node))
            elif(node.nodeType == node.TEXT_NODE):
                self._items.append(TextItem(text = node.nodeValue))
                
    def addDescription(self, textwidget, font):
        """Add a description at the end of a Tkinter Text widget.
        If the description is formatted a formatted text will be added; 
        otherwise a plain text will be added. 
        
        Arguments
        textwidget -- the Tkinter Text widget where the description will be added
        font -- the font to use if the text is formatted
        
        """
        
        for i in self._items:
            i.addTextToTextWidget(textwidget, font)
            
    def getFirstImage(self):
        """Get the first image in the formatted text."""
        for i in self._items:
            imagesrc = i.getFirstImage()
            
            if(imagesrc != ''):
                return imagesrc
            
        return None

    def getFirstVideo(self):
        """Get the first video in the formatted text."""
        for i in self._items:
            videosrc = i.getFirstVideo()
            
            if(videosrc != ''):
                return videosrc

        return None

    def setFirstVideo(self, link):
        """If there are any videos, set the link to the first
        
        Argument
        link -- link to the video webpage
        
        """
        for i in self._items:
            videosrc = i.getFirstVideo()
            
            if(videosrc != ''):
                i.setFirstVideo(link)

class TextItem:
    """A TextItem is an object hierarchy representing a piece of formatted text.
    It is built up like an HTML structure. 
    
    """
    _ctr = 0
    
    def __init__(self, text = None, xml = None):
        """Create a TextItem.
        
        Arguments
        text -- a text block
        xml -- an XML element
        
        """
        self._style = ''
        self._imagesrc = ''
        self._videolink = ''
        self._rawvideolink = ''
        self._items = []
        self._text = text

        if(xml is not None):
            self._createFromXml(xml)

    def addTextToTextWidget(self, textwidget, font):
        """Add a description at the end of a Tkinter Text widget.
        If the description is formatted a formatted text will be added; 
        otherwise a plain text will be added. 
        
        Arguments
        textwidget -- the Tkinter Text widget where the description will be added
        font -- the font to use if the text is formatted
        
        """
        family = font[fntixFamily]
        size = font[fntixSize]
        style = font[fntixStyle]

        if(self._text is not None):
            id = _ptid + str(TextItem._ctr)
            textwidget.insert(END, replaceHtmlEscapeSequences(self._text), id)
            textwidget.tag_config(id, font = font)
            TextItem._ctr += 1
        elif(self._style != ''):
            if(self._style == _bold):
                style = style + ' bold'
            elif(self._style == _italic):
                style = style + ' italic'
            elif(self._style == _strikeout):
                style = style + ' overstrike'
            elif(self._style == _underline):
                style = style + ' underline'
            elif(self._style == 'video' and self._videolink != ''):
                print('Show video ' + self._videolink)
                try:
                    vf = VideoFrame(textwidget, self._videolink)
                    textwidget.window_create(END, window = vf, padx = 20)
                except:
                    print('Unable to start video')

        for i in self._items:
            i.addTextToTextWidget(textwidget, (family, size, style))

    def getFirstImage(self):
        """Return the first image, if any, in the sub elements"""
        if(self._imagesrc != ''):
            return self._imagesrc
        else:
            for i in self._items:
                image = i.getFirstImage()

                if(image != ''):
                    return image

        return ''

    def getFirstVideo(self):
        """Return the first video, if any, in the sub elements"""
        if(self._rawvideolink != ''):
            return self._rawvideolink
        else:
            for i in self._items:
                link = i.getFirstVideo()

                if(link != ''):
                    return link

        return ''

    def setFirstVideo(self, link):
        """If there are any videos, set the link to the first
        
        Argument
        link -- link to the video webpage
        
        """
        if(self._rawvideolink != ''):
            self._videolink = link
            return True
        else:
            for i in self._items:
                if(i.setFirstVideo(link)):
                    return True
                
        return False

    def _createFromXml(self, xmlnode):
        """Initiate properties from an XML node and parse its child nodes.
        
        Argument
        xmlnode the XML node to parse
        
        """
        if(xmlnode.nodeName.upper() == 'br'.upper()):
            self._items.append(TextItem(text = '\n'))
            return
        elif((xmlnode.nodeName.upper() == 'em'.upper()) or (xmlnode.nodeName.upper() == 'i'.upper())):
            self._style = _italic
        elif((xmlnode.nodeName.upper() == 'strong'.upper()) or (xmlnode.nodeName.upper() == 'b'.upper())):
            self._style = _bold
        elif((xmlnode.nodeName.upper() == 'strike'.upper()) or (xmlnode.nodeName.upper() == 's'.upper())):
            self._style = _strikeout
        elif(xmlnode.nodeName.upper() == 'u'.upper()):
            self._style = _underline
        elif(xmlnode.nodeName.upper() == 'blockquote'.upper()): 
            self._items.append(TextItem(text = '\n'))
        elif(xmlnode.nodeName.upper() == 'div'.upper()):
            pass
        elif(xmlnode.nodeName.upper() == 'object'.upper()):
            pass
        elif(xmlnode.nodeName.upper() == 'span'.upper()):
            pass
        elif(xmlnode.nodeName.upper() == 'p'.upper()):
            pass
        elif(re.search(_headertagseq, xmlnode.nodeName.upper(), re.IGNORECASE) is not None):
            self._style = _bold
        elif(xmlnode.nodeName.upper() == 'a'.upper()):
            for node in xmlnode.childNodes:
                if(node.nodeName.upper() == 'img'.upper()):
                    self._parseImageElement(node)

            return
        elif(xmlnode.nodeName.upper() == 'img'.upper()):
            self._parseImageElement(xmlnode)
        elif(xmlnode.nodeName.upper() == 'iframe'.upper() or 
             xmlnode.nodeName.upper() == 'embed'.upper()):
            self._style = 'video'
            self._parseVideoElement(xmlnode)
            return
        else:
            print('TextItem: Unknown tag ' + xmlnode.nodeName)
            return
            
        for node in xmlnode.childNodes:
            if(node.nodeType == node.ELEMENT_NODE):
                self._items.append(TextItem(xml = node))
            elif(node.nodeType == node.TEXT_NODE):
                self._items.append(TextItem(text = node.nodeValue))

    def _parseVideoElement(self, node):
        try:
            self._rawvideolink = str(node.attributes['src'].value)
            print('Found video ' + self._rawvideolink)
        except:
            print('Unable to extract video link')

    def _parseImageElement(self, node):
        """Get the source of an image.
        
        Argument
        node -- the node in which to look
        
        """
        imagesrc = node.attributes['src'].value
        
        if(not imagesrc.endswith('/')):
            self._imagesrc = imagesrc

        return None
