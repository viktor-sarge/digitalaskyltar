# -*- coding: utf-8 -*-
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

import urllib
import os.path

def saveGenericImage(url, filename):
    """Download a file.
    
    Arguments
    url -- the url of the file
    filename -- the target file name
    
    """
    urllib.urlretrieve(url, filename)

def saveFrontcoverOfBook(isbn, filename):
    """Save the front cover image of a book from Adlibris. 
    
    Arguments
    isbn -- the isbn of the book
    filename -- the target file name
    
    """
    url = "http://www.adlibris.com/se/showimagesafe.aspx?isbn=" + isbn

    #Try to download the url five times
    for i in range(5):
        success = True
        
        try:
            urllib.urlretrieve(url, filename)
        except IOError, e:
            print('Error: Could not get ' + url + ';\n' + unicode(e))
            success = False
            
        if(success):
            break
    
    return
