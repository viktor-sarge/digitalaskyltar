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
import publicdisplay
from varbergsettings import Settings3, InifileDataSourceDescription, sBlog, sNew
import scheduler
from booklistview import BooklistView, evItemSelected
from bookview import BookView
from blogview import BlogView
from varbergdatamanager import DataManager3Blog, DataManager3New
from language import lang
import language as lng
from infobar import Infobar
from carouselview import ImageCarouselView, TextCarouselView

_blogid = 'blog'
_bottomblogid = 'bottomblog'
_newbookid = 'newbooks'
_bottomnewbookid = 'bottomnewbooks'
_blogviewid = 'blogview'
_bookviewid = 'bookview'
_bottomid = 'bottom'

class Controller:
    """Set up the GUI, set up the data model, handle the events"""
    def __init__(self, inidir, inifile):
        """Initiate the application
        
        Arguments
        inidir -- the working directory
        inifile -- the inifile 
        
        """        
        settings = Settings3(inidir, inifile)
        self._settings = settings
        dsdblog = InifileDataSourceDescription(sBlog, inidir, inifile)
        dsdnew = InifileDataSourceDescription(sNew, inidir, inifile)
                
        #Initiate main GUI
        gui = publicdisplay.PublicDisplay(inifile)
        self.gui = gui
        self.gui.root.protocol("WM_DELETE_WINDOW", self._ehQuit)
        self._views = dict()
        self._datamanagers = dict()
        
        self._sched = scheduler.Scheduler()
        
        #Configure blog data manager
        dm = DataManager3Blog(inidir, dsdblog, settings)
        self._datamanagers[_blogid] = dm
        self._sched.addUpdatable(dm)
        gui.setupSoftbutton(self._ehBlog, lang[lng.txtBlog], 0)

        frame = gui.createMainAreaShape(publicdisplay.shpSmallRoundRect, _blogid)
        blogview = BooklistView(settings.previewx, settings.previewy, frame)
        self._views[_blogid] = blogview
        dm.addSubjectObserver(blogview)

        rect = gui.createMainAreaShape(publicdisplay.shpBottomRect, _bottomblogid)
        ib = Infobar(rect)
        dm.addSubjectObserver(ib)

        #Configure new book data manager
        dm = DataManager3New(inidir, dsdnew, settings)
        self._datamanagers[_newbookid] = dm
        self._sched.addUpdatable(dm)
        gui.setupSoftbutton(self._ehNew, lang[lng.txtRecentlyBought], 1)

        frame = gui.createMainAreaShape(publicdisplay.shpSmallRoundRect, _newbookid)
        blogview = BooklistView(settings.previewx, settings.previewy, frame)
        self._views[_newbookid] = blogview
        dm.addSubjectObserver(blogview)

        rect = gui.createMainAreaShape(publicdisplay.shpBottomRect, _bottomnewbookid)
        ib = Infobar(rect)
        dm.addSubjectObserver(ib)
        
        self._itemviews = dict()

        #Create blog view
        frame = gui.createMainAreaShape(publicdisplay.shpSmallRoundRect, _blogviewid)
        viewer = BlogView(frame, gui.bgcolor, settings)
        self._views[_blogviewid] = viewer
        self._itemviews[_blogid] = _blogviewid
        
        #Create book view
        frame = gui.createMainAreaShape(publicdisplay.shpSmallRoundRect, _bookviewid)
        viewer = BookView(frame, gui.bgcolor, settings)
        self._views[_bookviewid] = viewer
        self._itemviews[_newbookid] = _bookviewid
        
        #Create carousel views
        self._imagecarouselframe = gui.createBottomFrame()
        self._imagecarouselview = ImageCarouselView(self._imagecarouselframe, settings.smallpreviewx, settings.smallpreviewy)
        self._imagecarouselframe.grid_remove()
        
        self._subjectcarouselframe = gui.createBottomFrame()
        self._subjectcarouselview = ImageCarouselView(self._subjectcarouselframe, settings.smallpreviewx, settings.smallpreviewy)
        self._subjectcarouselframe.grid_remove()

        self._setupPublicDisplay(_blogid, _bottomblogid, [_newbookid, _bottomnewbookid, _blogviewid, _bookviewid], 0)
        self._sched.start()

    def _setupPublicDisplay(self, shownId, infoid, hiddenIds, index):
        """Configure the state of the GUI.
        
        Arguments
        shownId -- the id of the GUI element to show
        infoid -- id of the Infobar
        hiddenIds -- the ids of the GUI elements to hide
        index -- the index of the button that will be active
        
        """
        self._views[_blogviewid].clear()
        self.gui.maincanvas.itemconfig(shownId, state = tki.NORMAL)
        self.gui.maincanvas.itemconfig(infoid, state = tki.NORMAL)

        for id in hiddenIds:
            self.gui.maincanvas.itemconfig(id, state = tki.HIDDEN)

        self.gui.removeBrowsables()
        dm = self._datamanagers[shownId]
        self.gui.addBrowsable(dm)
        dm.notifySubjectObservers()
        self._subjectcarouselview.setItemList(dm.subjecticons, dm.subjectindex)
        self.gui.addBrowsable(self._subjectcarouselview)
        self._imagecarouselframe.grid_remove()
        self._subjectcarouselframe.grid()

        self._prevshown = shownId
        self._previnfo = infoid
        self._prevhidden = hiddenIds
        self._previndex = index

        for i in range(2):
            self.gui.setSoftButtonState(i == index, i)

        self.gui.setupSoftbutton(self._ehBlog, lang[lng.txtBlog], 0)
        self.gui.setupSoftbutton(self._ehNew, lang[lng.txtRecentlyBought], 1)

        self.gui.root.bind(evItemSelected, 
                      lambda event, arg=shownId: self._ehItemSelected(event, arg))

    def _ehStart(self):
        """Event handler for the start button."""
        self._setupPublicDisplay(self._prevshown, self._previnfo, self._prevhidden, self._previndex)

    def _ehBlog(self):
        """Event handler for the blog button."""
        self._setupPublicDisplay(_blogid, _bottomblogid, [_newbookid, _bottomnewbookid, _blogviewid, _bookviewid], 0)

    def _ehNew(self):
        """Event handler for the button labeled "new"."""
        self._setupPublicDisplay(_newbookid, _bottomnewbookid, [_blogid, _bottomblogid, _blogviewid, _bookviewid], 1)

    def _ehItemSelected(self, event, arg):
        """Handle a click event for an item.
        
        Arguments
        event -- the event object
        arg -- the id of the source of the event
        
        """
        source = self._views[arg]
        itemviewid = self._itemviews[arg]
        viewer = self._views[itemviewid]
        self._activeview = viewer
        
        viewer.setContent(source.itemlist, source.selectedIndex)
        self._imagecarouselview.setItemList(source.itemlist, source.selectedIndex)
        self.gui.removeBrowsables()
        self.gui.addBrowsable(viewer)
        self.gui.addBrowsable(self._imagecarouselview)

        self.gui.maincanvas.itemconfig(_blogid, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(_newbookid, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(itemviewid, state = tki.NORMAL)
        self._imagecarouselframe.grid()
        self._subjectcarouselframe.grid_remove()
        self.gui.setupSoftbutton(self._ehStart, lang[lng.txtStart], 0)
        
        for i in range(2):
            self.gui.setSoftButtonState(i == 0, i)
            
    def _ehQuit(self):
        """Terminate the application."""
        print('Closing thread...')
        self._sched.stop()
        
        while(self._sched.isAlive()):
            print('Waiting for thread to close...')
            self._sched.join(1)
        
        print('Exit')
        self.gui.root.destroy()
