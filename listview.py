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
class ListView:
    """This class maintains a browsable list of items. 
    
    It should not be instantiated since it contains a member 
    self._eventgenerator that needs to be set by a subclass. It shall be set 
    to an object containing the Tkinter event_generate function. 
    
    """    
    def __init__(self, eventid):
        """Initiate the listview.
        
        Arguments
        eventid -- id of the event that will be triggered when the listview is clicked
        
        """
        self._eventid = eventid
        self._items = []
        self.itemlist = 0
        self._listindex = 0
        self._itemcount = 0
    
    def notify(self, datasrc):
        """Looks for new data and updates the display accordingly
        
        datasrc -- an object containing a method getItems() that returns a list of
                   items to display

        """
        newlist = datasrc.getItems()
        
        if(newlist is None):
            return
        
        self.itemlist = newlist
        self._listindex = 0

        self._update()
        
    def next(self):
        """Browse to next page of items"""
        self._listindex += self._itemcount
        
        if(self._listindex >= len(self.itemlist)):
            self._listindex = 0
        
        self._update()
        
    def prev(self):
        """Browse to previous page of items"""
        self._listindex -= self._itemcount
        
        if(self._listindex < 0):
            count = (len(self.itemlist) + self._itemcount - 1) / self._itemcount
            self._listindex = (count - 1) * self._itemcount

        self._update()

    def _update(self):
        """Update the contents of the listview."""
        self._items = self.itemlist[self._listindex:self._listindex + self._itemcount]

    def _ehClick(self, event):
        """Event handler for clicks."""
        index = event.widget.index
        self.selectedIndex = self._listindex + index
        self._eventgenerator.event_generate(self._eventid, when = "tail")
