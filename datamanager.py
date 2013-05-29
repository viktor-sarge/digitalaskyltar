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
"""This unit contains data managers that creates harvester objects and 
manages the harvested data in a synchronized way. The datamanager classes 
have the update function which makes it possible to schedule them to harvest data
at regular intervals. Some of the subclasses also implements the Observable design pattern
that facilitates a GUI update every time data has been harvested. 

"""
import thread

class DataManager:
    """The super class of all data manager classes. It should not be instantiated."""
    def __init__(self):
        """Initiate the data manager."""
        
        self._isupdated = False
        self._lock = thread.allocate_lock()
        self._observers = []

    def update(self):
        """Harvest new items and process them."""
        self._setupUpdate()
        self._harvester.update()
        self._processItems(self._harvester.newestId)

        print('Update complete!')

    def getItems(self):
        """Return all items in the data manager in a synchronized way."""
        result = []
        
        self._lock.acquire()

        if(self._isupdated):
            result = self._items
            self._isupdated = False
        else:
            result = None

        self._lock.release()

        return result
    
    def addObserver(self, obs):
        """Add an observer that will get notified when this data manager is updated

        Argument
        obs -- the observer

        """
        self._observers.append(obs)

    def notifyObservers(self):
        """Notify all observers"""
        for i in self._observers:
            i.notify(self)

    def _setItems(self):
        """Assign items to the data manager in a synchronized way."""
        self._lock.acquire()
        
        self._isupdated = True
        self._assignItems()

        self._lock.release()
        
    def _initialUpdate(self):
        """Load items from the cache."""
        #Add items from cache        
        self._setupUpdate()
        
        for i in self._cache.items:
            if(self._addandcheck(i)):
                break
            
        self._processItems(self._newestId)
        self._cache.updateContents(self._allitems, self._newestId)

    def _filterItem(self, item):
        """Check if an item is valid and return the result. Dispose invalid items.
        
        Arguments
        item -- the item to check
        
        """
        if(self._itemIsValid(item)):
            return True
        else:
            item.cleanup()
            return False

class BasicManager(DataManager):
    """Super class for some of the data managers. Do not instantiate this class."""
    def _setup(self, dsd):
        """Set up the data manager. 
        
        Arguments
        dsd -- data source description
        
        """
        self._allitems = []
        self._newestId = self._cache.newestId

        self._historylength = dsd.maxcount
        self.interval = dsd.interval

        self._itemids = dict()
        
        self._initialUpdate()

        self._setItems()

    def _assignItems(self):
        """Set the items of this data manager."""
        self._items = list(self._allitems)

    def _setupUpdate(self):
        """Prepare an update."""
        self._maxitemcount = self._historylength
        self._itemstoadd = self._maxitemcount
        self._newitems = []

    def _processItems(self, newestId):
        """Process the items in this data manager. 
        
        Arguments
        newestId -- the id of the most recently harvested item
        
        """
        updatecache = False
        updateObservers = False
        
        #Adjust the lists if something was added during the update
        if(self._itemstoadd < self._maxitemcount):
            updateObservers = True
            self._newitems.extend(self._allitems)
            garbage = self._newitems[self._historylength:]
            self._allitems = self._newitems[:self._historylength]

            for i in garbage:
                updatecache = True
                self._itemids.pop(i.uid)
                i.cleanup()

        if(self._newestId != newestId):
            updatecache = True
            self._newestId = newestId

            if(self._itemstoadd < self._maxitemcount):
                self._setItems()
        
        if(updatecache):        
            self._cache.updateContents(self._allitems, newestId)
            
        if(updateObservers):
            self.notifyObservers()

    def _addandcheck(self, item):
        """Add an item if it is ok and return the result.
        
        Argument
        item -- the item to check and possibly add
        
        """
        if(self._filterItem(item)):
            self._newitems.append(item)
            self._itemids[item.uid] = ''
            self._itemstoadd -= 1
            item.loadData()
            
            if(self._itemstoadd <= 0):
                return True

        return False

    def _itemIsValid(self, item):
        """Determine whether an item is valid.
        
        Argument
        item -- the item to evaluate
        
        """
        return item.valid
