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
import os.path

from datamanager import DataManager, BasicManager
from cache import Cache
from vbgopacbookharvester import OpacBookItem, VarbergOpacSubjectSearchHarvester, isInYouthDepartment
from blogspotharvester import BlogspotHarvester, BlogspotItemWithIsbn, BlogspotItemWithImage
from wpharvester import WordPressItem, WordpressHarvester
from harvester import getHarvester
from itemharvester import subjectstrip
from iconitem import GetIconItems

class DataManager1(BasicManager):
    """Data manager for the first Varberg display"""
    def __init__(self, dsd, settings):
        """Initiate the data manager.

        Arguments
        dsd -- data source description
        settings -- settings
        
        """
        DataManager.__init__(self)
        cachedir = os.path.join(settings.cachedir, dsd.cacheid)
        itemarg = (cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy), settings.library)
        self._cache = Cache(cachedir, OpacBookItem, itemarg)
        
        self._harvester = getHarvester(dsd, settings, self._addandcheck)
        self._harvester.newestId = self._cache.newestId
        self._harvester.itemarg = itemarg
        self._sections = dsd.sections

        self._setup(dsd)

    def _itemIsValid(self, item):
        """Determine whether an item is valid.
        
        Argument
        item -- the item to evaluate
        
        """
        return item.valid and (not self._itemids.has_key(item.uid)) and (item.section in self._sections)

class DataManager2Blog(BasicManager):
    """Data manager for the second Varberg display"""
    def __init__(self, dsd, settings):
        """Initiate the data manager.

        Arguments
        dsd -- data source description
        settings -- settings
        
        """
        DataManager.__init__(self)
        itemarg = (dsd.cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy))
        self._cache = Cache(dsd.cachedir, WordPressItem, itemarg)
        
        self._harvester = WordpressHarvester(dsd, self._addandcheck)
        self._harvester.newestId = self._cache.newestId
        self._harvester.itemarg = itemarg
        
        self._setup(dsd)

class DataManager4Blog(BasicManager):
    """Data manager for the fourth display (Hylte)"""
    def __init__(self, dsd, settings):
        """Initiate the data manager.

        Arguments
        dsd -- data source description
        settings -- settings
        
        """
        DataManager.__init__(self)
        itemarg = (dsd.cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy), settings.library)
        self._cache = Cache(dsd.cachedir, BlogspotItemWithImage, itemarg)
        
        self._harvester = BlogspotHarvester(dsd, self._addandcheck, BlogspotItemWithImage)
        self._harvester.newestId = self._cache.newestId
        self._harvester.itemarg = itemarg
        
        self._setup(dsd)

class SubjectDataManager(DataManager):
    """Superclass of the data managers of the third Varberg display. This data 
    manaager also handles a set of subjects; all items belong to one or more
    subject. This class also implements the Observable design pattern. 
    
    """
    def __init__(self, dir, dsd, settings):
        """Initiate the data manager.

        Arguments
        dir -- directory containing the subject icons
        dsd -- data source description
        settings -- settings
        
        """
        DataManager.__init__(self)
        self._harvester.newestId = self._cache.newestId
        self._items = self._cache.items
        self._newestId = self._cache.newestId

        self._historylength = dsd.maxcount
        self.interval = dsd.interval
        
        self._itemids = dict()
        self._sorteditems = dict()
        self._allitems = dict()
        self._subjectobservers = []
        self.subjectindex = 0
        self.subjecticons = GetIconItems(dir, settings)
        self.subjects = []
       
        for i in settings.subjects:
            subject = i.strip(subjectstrip)
            self._itemids[subject] = dict()
            self._sorteditems[subject] = []
            self.subjects.append(subject)

        self._initialUpdate()
        self._setsubject()

    def prev(self):
        """Select previous subject."""
        self.subjectindex -= 1

        if(self.subjectindex < 0):
           self.subjectindex = len(self.subjects) - 1

        self._setsubject()
    
    def next(self):
        """Select next subject."""
        self.subjectindex += 1
        
        if(self.subjectindex >= len(self.subjects)):
            self.subjectindex = 0
    
        self._setsubject()
    
    def addSubjectObserver(self, observer):
        """Add observer
        
        Argument
        observer -- the observer to add
        
        """
        self._subjectobservers.append(observer)
        
    def notifySubjectObservers(self):
        """Notify all observers."""
        for i in self._subjectobservers:
            i.notify(self)
            
    def _setupUpdate(self):
        """Prepare an update."""
        self._maxitemcount = self._historylength * len(self.subjects)
        self._itemstoadd = self._maxitemcount
        self._added = dict()
        self._newitems = dict()
        
        for i in self.subjects:
            self._added[i] = 0
            self._newitems[i] = []

    def _processItems(self, newestId):
        """Process the items in this data manager. 
        
        Arguments
        newestId -- the id of the most recently harvested item
        
        """
        garbage = []
        updatecache = False
        updateObservers = False

        self._modifyNewItems()

        #Adjust the lists if something was added during the update        
        if(self._itemstoadd < self._maxitemcount):
            updatecache = True
            updateObservers = True
            
            for i in self.subjects:
                currentlist = self._newitems[i]
                currentlist.extend(self._sorteditems[i])
                garbage.extend(currentlist[self._historylength:])
                self._sorteditems[i] = currentlist[:self._historylength]
                
                for j in self._sorteditems[i]:
                    if(not j in self._allitems):
                        self._allitems[j] = ''
    
            for i in garbage:
                if(not i in self._allitems):
                    #Remove item from all subject lists
                    subjects = list(set(self.subjects) & set(i.subjects))
                    
                    for j in subjects:                    
                        self._itemids[j].pop(i.uid)

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
        if(not self._filterItem(item)):
            return False
        
        dirty = False
        
        for i in self.subjects:
            if(self._subjectInItem(i, item)):
                if(self._added[i] < self._historylength):
                    if(not self._itemids[i].has_key(item.uid)):
                        self._itemids[i][item.uid] = ''
                        dirty = True
                        self._added[i] += 1
                        self._newitems[i].append(item)
                        self._itemstoadd -= 1
                        item.loadData()
    
                        if(self.isDone(i)):
                            return True

        if(not dirty):
            item.cleanup()
            
        return False

    def _modifyNewItems(self):
        """"Modify newly harvested items
        
        This function does nothing
        
        """
        pass

    def isDone(self, subject):
        """Return true if the update is complete
        
        Argument
        subject -- the current subject (not used in this function)
        
        """
        return (self._itemstoadd <= 0)

    def _subjectInItem(self, subject, item):
        """Check if a subject is among the subjects of an item
        
        Arguments
        subject -- the subject
        item-- the item
        
        """
        return subject.encode('utf-8').upper() in map(lambda str : str.encode('utf-8').upper(), item.subjects)

    def _setsubject(self):
        """Set the currently active subject in a synchronized way and notify the observers."""
        self._lock.acquire()
        self.subject = self.subjects[self.subjectindex]
        self._lock.release()

        self._setItems()
        self.notifySubjectObservers()

    def _assignItems(self):
        """Set the items of this data manager to the items of the currently active subject."""
        self._items = list(self._sorteditems[self.subject])

class DataManager3Blog(SubjectDataManager):
    """Data manager for the blog of the third Varberg display"""
    def __init__(self, dir, dsd, settings):
        """Initiate the data manager.

        Arguments
        dir -- directory containing the subject icons
        dsd -- data source description
        settings -- settings
        
        """
        itemarg = (dsd.cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy), settings.library, 
                   settings.booksearchprefix, settings.booksearchsuffix)
        self._cache = Cache(dsd.cachedir, BlogspotItemWithIsbn, itemarg)
        self._harvester = BlogspotHarvester(dsd, self._addandcheck, BlogspotItemWithIsbn)
        self._harvester.itemarg = itemarg

        SubjectDataManager.__init__(self, dir, dsd, settings)

    def _itemIsValid(self, item):
        """Determine whether an item is valid.
        
        Argument
        item -- the item to evaluate
        
        """
        return item.valid

class DataManager3New(SubjectDataManager):
    """Data manager for the list of new books of the third Varberg display"""
    def __init__(self, dir, dsd, settings):
        """Initiate the data manager.

        Arguments
        dir -- directory containing the subject icons
        dsd -- data source description
        settings -- settings
        
        """
        itemarg = (dsd.cachedir, (settings.previewx, settings.previewy), 
                   (settings.smallpreviewx, settings.smallpreviewy), settings.library)
        self._cache = Cache(dsd.cachedir, OpacBookItem, itemarg)
        #TBD Debug
        dsd.cacheid = 'Skylt3nytt'
        self._harvester = VarbergOpacSubjectSearchHarvester(dsd, settings, self._addandcheck)
        self._harvester.itemarg = itemarg
        self._library = settings.library

        SubjectDataManager.__init__(self, dir, dsd, settings)

    def _modifyNewItems(self):
        """"Modify newly harvested items
        
        Replace the item's subjects with the subject it has been added to. 
        This is done because the subject is not harvested from the item; 
        instead it comes from the search from which the item was harvested. 

        """
        for i in self.subjects:
            currentlist = self._newitems[i]
            
            for item in currentlist:
                item.subjects = [i]

    def isDone(self, subject):
        """Return true if the update is complete
        
        Argument
        subject -- the current subject

        """
        #If the harvester is updating, we are doing one update for each subject 
        #and therefore we are done with one of the updates when the subject is filled 
        if(self._harvester.doesUpdate):
            return (self._added[subject] >= self._historylength)
        #... otherwise (e.g. during cache load), we have to compare against all subjects
        else:
            return (self._itemstoadd <= 0)

    def _subjectInItem(self, subject, item):
        """Check if a subject is among the subjects of an item
        
        Arguments
        subject -- the subject
        item-- the item
        
        """
        #If the harvester is updating, the subject is only known in the harvester... 
        if(self._harvester.doesUpdate):
            return (subject == self._harvester.currentSubject)
        #... otherwise (e.g. during cache load), the subject is stored in the item
        else:
            return subject.encode('utf-8').upper() in map(lambda str : str.encode('utf-8').upper(), item.subjects)

    def _itemIsValid(self, item):
        """Determine whether an item is valid.

        Argument
        item -- the item to evaluate
        
        """
        return item.valid and isInYouthDepartment(item.shelf)
