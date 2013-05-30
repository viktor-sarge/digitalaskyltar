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
import ConfigParser
import StringIO

class ConfigFileWriter:
    
    def __init__(self):
        self._sections = dict()
        
    def addValue(self, section, paramname, value):
        if(not self._sections.has_key(section)):
             self._sections[section] = dict()
             
        self._sections[section][paramname] = value
        
    def writeToFile(self, filename):
        cfgp = ConfigParser.ConfigParser()
        
        for section in self._sections.keys():
            cfgp.add_section(section.encode('utf-8'))

            for option in self._sections[section].keys():
                cfgp.set(section.encode('utf-8'), option.encode('utf-8'), self._sections[section][option].encode('utf-8'))

        file = open(filename, 'w')
        cfgp.write(file)
        file.close()
