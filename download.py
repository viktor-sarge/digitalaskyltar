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
import Tkinter as tki
from cache import Cache
from blogspotharvester import BlogspotHarvester, BlogspotItemWithIsbn
from varbergsettings import Settings3, InifileDataSourceDescription, sBlog


class download3:
    """Download data to the cache directory."""
    def __init__(self, inidir, inifile, amount):
        """Commence download operation.
        
        Arguments
        inidir -- working directory
        inifile -- config file
        amount -- amount of items to download

        """
        print('Download data for display 3...')
        self._data  = []
    
        #Create dummy GUI
        root = tki.Tk()
        settings = Settings3(inidir, inifile)
        dsdblog = InifileDataSourceDescription(sBlog, inidir, inifile)   
    
        itemarg = (dsdblog.cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy), settings.library, 
                   settings.booksearchprefix, settings.booksearchsuffix)
        cache = Cache(dsdblog.cachedir, BlogspotItemWithIsbn, itemarg)
        harvester = BlogspotHarvester(dsdblog, self._addandcheck, BlogspotItemWithIsbn)
        harvester.itemarg = itemarg
        harvester.newestId = ''
        
        harvester.update(amount)
        cache.updateContents(self._data, harvester.newestId)
        print('Done!')
    
    def _addandcheck(self, item):
        """Add and check function that is passed to the BlogspotHarvester instance. 
        
        It always returns false since the amount of items to download is 
        handled in another way. 
        """
        if(item.valid):
            self._data.append(item)
            item.loadData()
            
        return False
