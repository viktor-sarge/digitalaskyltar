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
from xml.dom.minidom import Node
from PIL.Image import ANTIALIAS
import os.path
from tkFont import Font
import ConfigParser
import codecs
import StringIO

def getConfigParser(inifile):
    """Return a ConfigParser given a unicode config file. 
    
    Arguments
    inifile -- the name of the inifile
    
    """
    
    if(os.path.exists(inifile)):
        parser = ConfigParser.ConfigParser()
        
        file = (codecs.open(inifile, "r", "utf8"))
        contents = file.read()
        file.close()
        
        #Workaround to remove the BOM from the contents - 
        #if the file is saved in UTF-8 without BOM it will work anyway;
        #if it is saved in UTF-8 (as Windows Notepad does) it will fail 
        #without this workaround
        if(ord(contents[0]) == 0xFEFF):
            contents = contents[1:]
            
        file = StringIO.StringIO(contents)
        parser.readfp(file)
        file.close()
        
        return parser
    else:
        return None



def getFont(name, size, style):
    """Create a font object.
    
    Arguments
    name -- font name
    size -- font size
    style -- font style; any combination of b, i, u, s:
        b -> bold
        i -> italic
        u -> underline
        s -> strikeout
    
    """
    if('b' in style):
        weight = 'bold'
    else:
        weight = 'normal'
        
    if('i' in style):
        slant = 'italic'
    else:
        slant = 'roman'
    
    underline = ('u' in style)
    overstrike = ('s' in style)
    
    return Font(family = name, size = size, weight = weight, slant = slant, 
                underline = underline, overstrike = overstrike)

#TBD The same as in hylte datamodel; use one of them
def resizeImage(image, maxwidth, maxheight):
    """Resize an image within given boundaries and keep the aspect ratio. 
    
    Arguments
    
    image -- a PIL.Image object
    maxwidth -- the maximum width of the image
    maxheight -- the maximum height of the image
    
    """
    width = float(image.size[0])
    height = float(image.size[1])
    ratio = width / height
    displayratio = float(maxwidth) / float(maxheight)
    
    if(ratio > displayratio):
        newwidth = maxwidth
        newheight = int(maxwidth / ratio)
    else:
        newwidth = int(maxheight * ratio)
        newheight = maxheight

    return image.resize((newwidth, newheight), ANTIALIAS)

def _getNodeValue(parent, nodename, type):
    """Get the value of an XML sub node
    
    Arguments
    parent -- the node containing the sub node
    nodename -- the name of the sub node
    type -- the node type of the sub node
    
    """
    nodes = parent.getElementsByTagName(nodename)

    if(nodes.length != 1):
        raise Exception('Error: Unexpected number of ' + nodename + ' nodes')

    for i in nodes.item(0).childNodes:
        if(i.nodeType == type):
            return i.nodeValue

    return ''

def getTextNodeValue(parent, nodename):
    """Get the value of an XML text sub node
    
    Arguments
    parent -- the node containing the sub node
    nodename -- the name of the sub node
    
    """
    return _getNodeValue(parent, nodename, Node.TEXT_NODE)

def getCDataNodeValue(parent, nodename):
    """Get the value of an XML CDATA sub node
    
    Arguments
    parent -- the node containing the sub node
    nodename -- the name of the sub node
    
    """
    return _getNodeValue(parent, nodename, Node.CDATA_SECTION_NODE)

def textToCData(text):
    """Convert a text to an XML CDATA section."""
    if(text.find(']]>') >= 0):
        raise ValueError("']]>' not allowed in a CDATA section")
    
    return '<![CDATA[' + text + ']]>'

_illegalChars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def textToFilename(text):
    """Convert a text to filename by removing any illegal characters
    
    Arguments
    text -- input text
    
    """    
    result = ''

    for c in text:
        if(not c in _illegalChars):
            result = result + c

    return result
