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
from formattedtext import filterHtml

subjectstrip = ' .'

class CouldNotReadBookError(Exception):
    """Can be thrown when it is not possible to get information about a book """
    def __init__(self, value):
        """Initiate the exception.
        
        Argument
        value -- message for the exception
        
        """
        self.value = value
    def __str__(self):
        return 'Could not read book data: ' + self.value

    def __repr__(self):
        return self.__str__()

def _getTextTag(content, index):
    """Return the text data of an XML element
    
    Argument
    content -- the XML string where the text is
    index -- the next text element after this index will be returned
    
    """
    startindex = content.find(">", index)
    stopindex = content.find("<", startindex)

    return content[startindex + 1:stopindex]

class BookInfo:
    """Information about a book harvested from Libra."""
    def __init__(self, content, reqlibrary = None):
        """Parse the information about the book. Optionally the book must be available at
        library reqlibrary or else a CouldNotReadBookError will be thrown.
        
        Arguments
        content -- XML string describing the book
        reqlibrary -- if specified, a book will only be parsed if it is available at this library 
        
        """
        # Extracting the description text
        if content.find("ctl00_lblDescr") != -1:
            startindex = content.find("ctl00_lblDescr")
            stopindex = content[startindex:].find("</span>")
            bookDescription = content[startindex+16:startindex + stopindex]
        else: 
            raise CouldNotReadBookError('Can\'t read book from Libra: No description found')
        
        self.rawtext = bookDescription
    
        # Extracting author metadata
        if content.find("/ff") != -1:
            startindex = content.find("/ff")    
            stopindex = content[startindex+5:].find("</a>")
            author = content[startindex+5:startindex + stopindex + 5]
        else: 
            author = ""
            
        self.author = author
        
        # Extracting the title - upgrade with regex
        if content.find("<td>Titel:</td>") != -1:
            startindex = content.find("<td>Titel:</td>")
            stopindex = content[startindex+15:].find("</td>")
            title = content[startindex+15:startindex + stopindex + 15]
            startindex = title.find(">")
            title = title[startindex+1:]
            while title[-1] == '/' or title[-1] == ' ':
                title = title[0:len(title)-1]
    
        else: 
            title = ""
            
        self.title = title
        
        # Saving the ISBN of the title in question
        startindex = content.find("ctl00_imgCover")
        stopindex = content[startindex+21:].find('"')
        imageUrl = content[startindex+21:stopindex+startindex+21]
    
        startindex = imageUrl.find("isbn=")
        stopindex = imageUrl[startindex+5:].find("&")
        self.isbn = imageUrl[startindex+5:startindex+5+stopindex]
    
    
        # Extract the location of the title in the library
#        startindex = content.find("dgHoldings_ctl02_lblShelf")
#        stopindex = content[startindex:].find("</span>")
#        shelf = content[startindex+27:startindex+stopindex]
#        self.shelf = filterHtml(shelf)
#        
#        startindex = content.find("dgHoldings_ctl02_lblBranchDepartment")
#        stopindex = content[startindex:].find("</span>")
#        libandsection = content[startindex+38:startindex+stopindex]
#        startindex = libandsection.find('&nbsp;')
#        startindex = libandsection.find('&nbsp;', startindex + 6)
#        
#        self.section = libandsection[startindex+6:]
        
        #Get library specific data
        startindex = content.find("lblBranchDepartment")
        finalstop = content.find("</table>", startindex)

        found = False
        self.shelves = []
        
        while((startindex >= 0) and (startindex < finalstop)):
            #Get library
            libandsection = _getTextTag(content, startindex)
            delimiter = libandsection.find('&nbsp')
            library = libandsection[:delimiter]
            
            if((reqlibrary is None) or (library == reqlibrary)):
                #Get section
                delimiter = libandsection.rfind(';')
                self.section = libandsection[delimiter + 1:]
                    
                #Get shelf
                startindex = content.find("lblShelf", startindex)
                shelf = _getTextTag(content, startindex)
                shelf = filterHtml(shelf)
                self.shelves.append(shelf)

                #Get availability
                startindex = content.find("lblAvailable", startindex)
                self.available = _getTextTag(content, startindex)
                found = True

            startindex = content.find("lblBranchDepartment", startindex + 1)

        if(not found):
            raise CouldNotReadBookError('Book not present at library ' + reqlibrary)

        # Extract the books subjects
        self.subjects = []
        
        startindex = content.find(u"Ämnesord")
        startindex = content.find("<td", startindex)
        finalstop = content.find("</td>", startindex)
        startindex = content.find("<a", startindex)
        
        while((startindex >= 0) and (startindex < finalstop)):
            startindex = content.find(">", startindex)
            stopindex = content.find("<", startindex)
            subject = content[startindex + 1:stopindex]
            subject = subject.strip(subjectstrip)
            self.subjects.append(subject)
            startindex = content.find("<a", stopindex)

#        print(self.title + ' has the following subjects:\n')
#        
#        for i in self.subjects:
#            print('  ' + i)

def harvestBookInfo(url, reqlibrary):
    """Harvest a book from an url. Will throw a CouldNotReadBookError
    if reqlibrary is not None and the book is not available at that library.
    
    Arguments
    url -- an url pointing to the book data
    reqlibrary -- if not None, the book must be available at this library
    
    """
    try:
        page = urllib.urlopen(url)
    except IOError:
        raise CouldNotReadBookError('Could not read url ' + self._url)

    content = page.read()
    content = unicode(content, 'utf8')
    page.close()    

    return BookInfo(content, reqlibrary)

#Test code
if __name__ == "__main__":
    bi = harvestBookInfo(r'http://bib.kommunen.varberg.se/opac/show_holdings.aspx?paging=false&bokid=135403', 'Varbergs bibliotek')
    
    print(bi.title.encode('utf-8') + ':')
    
    print('  Section ' + bi.section.encode('utf-8'))
    #print('  Shelf ' + bi.shelf.encode('utf-8'))
    print('  Availability ' + bi.available.encode('utf-8'))
    
    print('  Subjects:')

    for i in bi.subjects:
        print('    ' + i)
