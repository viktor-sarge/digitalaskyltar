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
from common import getFont
from varbergsettings import Settings2, InifileDataSourceDescription, sBlog
import scheduler
from panelview import PanelListView, evPanelItemSelected
from blogview import PlainBlogView
from varbergdatamanager import DataManager2Blog
from language import lang
import language as lng

_magazineid = 'magazine'
_blogid = 'blog'
_blogviewid = 'blogview'

class Controller:
    """Set up the GUI, set up the data model, handle the events"""
    def __init__(self, inidir, inifile):
        """Initiate the application
        
        Arguments
        inidir -- the working directory
        inifile -- the inifile 
        
        """
        settings = Settings2(inidir, inifile)
        dsdblog = InifileDataSourceDescription(sBlog, inidir, inifile)

        #Initiate main GUI
        gui = publicdisplay.PublicDisplay(inifile)
        self.gui = gui
        self.gui.root.protocol("WM_DELETE_WINDOW", self._ehQuit)
        self._views = dict()
        self._datamanagers = dict()
        
        self._sched = scheduler.Scheduler()
        
        #Configure blog data manager
        dm = DataManager2Blog(dsdblog, settings)
        self._datamanagers[_blogid] = dm
        self._sched.addUpdatable(dm)
        gui.setupSoftbutton(self._ehBlog, lang[lng.txtList], 1)

        pm = gui.createPanelManager(_blogid,settings.marginx, settings.marginy)
        blogview = PanelListView(pm, settings)
        self._views[_blogid] = blogview

        #Create blog view
        frame = gui.createMainAreaShape(publicdisplay.shpRoundRect, _blogviewid)
        blogview = PlainBlogView(frame, gui.bgcolor, settings)
        self._blogview = blogview

        #The second button is always active        
        gui.setSoftButtonState(True, 1)
        #Hide the first button and display a text instead
        gui.setSoftButtonState(False, 0, False)
        gui.drawText(settings.tlleft, settings.tltop, settings.tllinewidth, settings.tltext, settings.tltextcolor, 
                     getFont(settings.tlfontname, settings.tlfontsize, settings.tlfontstyle))
        
        self._setupPublicDisplay(_blogid, [_blogviewid], 1)
        self._sched.start()

    def _setupPublicDisplay(self, shownId, hiddenIds, index):
        """Configure the state of the GUI.
        
        Arguments
        shownId -- the id of the GUI element to show
        hiddenIds -- the ids of the GUI elements to hide
        index -- the index of the button that will be active
        
        """
        self.gui.maincanvas.itemconfig(shownId, state = tki.NORMAL)
        
        for id in hiddenIds:
            self.gui.maincanvas.itemconfig(id, state = tki.HIDDEN)
        
        view = self._views[shownId]
        self.gui.removeBrowsables()
        self.gui.addBrowsable(view)
        dm = self._datamanagers[shownId]
        view.notify(dm)

        self.gui.root.bind(evPanelItemSelected, 
                      lambda event, arg=shownId: self._ehItemSelected(event, arg))

    def _ehMagazine(self):
        """Event handler for the magazine button."""
        self._setupPublicDisplay(_newbookid, _bottomnewbookid, [_blogid, _bottomblogid, _blogviewid, _bookviewid], 0)

    def _ehBlog(self):
        """Event handler for the blog button."""
        self._setupPublicDisplay(_blogid, [_magazineid, _blogviewid], 1)

    def _ehItemSelected(self, event, arg):
        """Handle a click event for an item.
        
        Arguments
        event -- the event object
        arg -- the id of the source of the event
        
        """
        source = self._views[arg]
        self._blogview.setContent(source.itemlist, source.selectedIndex)
        self.gui.removeBrowsables()
        self.gui.addBrowsable(self._blogview)

        self.gui.maincanvas.itemconfig(_blogid, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(_magazineid, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(_blogviewid, state = tki.NORMAL)

    def _ehQuit(self):
        """Terminate the application."""
        print('Closing thread...')
        self._sched.stop()
        
        while(self._sched.isAlive()):
            print('Waiting for thread to close...')
            self._sched.join(1)
        
        print('Exit')
        self.gui.root.destroy()
