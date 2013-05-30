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
from ConfigParser import ConfigParser, NoOptionError

#TBD use the same as in hylte! 

ImageFolder = 'ImageFolder'
ConfigFolder = 'ConfigFolder'
MostRecentFolder = 'MostRecentFolder'

_section = 'Searchpaths'

_allFolders = [ImageFolder, ConfigFolder]

class SearchPathManager:
    """This class handles search paths in file dialogs"""
    def load(self, inifile):
        """Load search paths from a previously saved file; if no file exists
        all paths will be initialized to the empty string
        
        Argument
        inifile -- a file containing search paths that was created by a SearchPathManager
        
        """
        self._filename = inifile
        parser = ConfigParser()
        self._parser = parser
        self._dict = dict()
        self._dict[MostRecentFolder] = ''
        
        if(parser.read(inifile) == []):
            self._init()

        for i in _allFolders:
            try:
                self._dict[i] = self._parser.get(_section, i)
                
                if(self._dict[i] != ''):
                    self._dict[MostRecentFolder] = self._dict[i]
            except NoOptionError:
                self._dict[i] = ''

    def getPath(self, id):
        """Return the most recently accessed folder for a path
        
        Argument
        id -- specifies which path to return
        
        """
        return self._dict[id]
    
    def getFirstPath(self, paths):
        """Return the first non-empty path for a list of paths or the empty
        string if none of the paths exists
        
        Argument
        paths -- specifies which paths to look for
        
        """
        for i in paths:
            if(self._dict[i] != ''):
                return self._dict[i]
                        
        return ''

    def setPath(self, id, path):
        """Update the most recently accessed folder for a path;
        update MostRecentFolder
        
        Arguments
        id -- specifies which path to store
        path -- the path to store
        
        """
        self._dict[id] = path
        self._parser.set(_section, id, path)
        
        if(path != ''):
            self._dict[MostRecentFolder] = self._dict[id]

    def save(self):
        """Save the paths to the file specified in the call to load"""
        file = open(self._filename, 'w')
        self._parser.write(file)
        file.close()

    def _init(self):
        """Initiate the instance with empty strings for all paths"""
        self._parser.add_section(_section)
            
        for i in _allFolders:
            self._parser.set(_section, i, '')

spmanager = SearchPathManager()
