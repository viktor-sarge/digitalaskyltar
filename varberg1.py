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
import itertools
import configreader

import publicdisplay
from booklistview import BooklistView, evItemSelected
from bookview import BookView
import itemview
import carouselview

import language as lng
import scheduler
import varbergsettings
from varbergdatamanager import DataManager1

_button1Id = 'button1'
_button2Id = 'button2'
_buttonIds = [_button1Id, _button2Id]
_buttonCount = 2
_viewId = 'viewer'

class Controller:
    """Set up the GUI, set up the data model, handle the events"""
    
    def __init__(self, inidir, inifile):
        """Initiate the application
        
        Arguments
        inidir -- the working directory
        inifile -- the inifile 
        
        """        
        #Initiate main GUI
        gui = publicdisplay.PublicDisplay(inifile)
        self.gui = gui
        self.gui.root.protocol("WM_DELETE_WINDOW", self._ehQuit)
        self._views = dict()
        
        #Read configuration data
        settings = varbergsettings.Settings1(inidir, inifile)
        
        #Configure harvesters
        config = configreader.ConfigReader(settings.configfile)
        self._sched = scheduler.Scheduler()       
        handlers = [self._ehButton1, self._ehButton2]
        hidden = []
        self._datamanagers = dict()
        
        if(len(config.defaults) != 2):
            raise Exception('Fatal error: there shall be ' + str(_buttonCount) + 'default button configurations')
        
        #Create default harvesters and their views
        for (dsd, id, i) in itertools.izip(config.defaults, _buttonIds, range(_buttonCount)):
            dm = DataManager1(dsd, settings)
            self._datamanagers[id] = dm
            self._sched.addUpdatable(dm)
            frame = gui.createMainAreaShape(publicdisplay.shpRoundRect, id)
            blv = BooklistView(settings.previewx, settings.previewy, frame)
            self._views[id] = blv
            gui.setupSoftbutton(handlers[i], dsd.buttontext, i)

            if(dsd.startup):
                shown = id
                index = i
            else:
                hidden.append(id)

        #Create item viewer
        frame = gui.createMainAreaShape(publicdisplay.shpRoundRect, _viewId)
        viewer = BookView(frame, gui.bgcolor, settings)
        self._views[_viewId] = viewer
        hidden.append(_viewId)

        #Create carousel view    
        self._bottomframe = gui.createBottomFrame()
        self._carouselview = carouselview.ImageCarouselView(self._bottomframe, settings.smallpreviewx, settings.smallpreviewy)
        self._bottomframe.grid_remove()

        #Set initial GUI state
        self._setupPublicDisplay(shown, hidden, index)
        
        #Start background thread
        self._sched.start()

    def _ehQuit(self):
        """Terminate the application."""
        print('Closing thread...')
        self._sched.stop()
        
        while(self._sched.isAlive()):
            print('Waiting for thread to close...')
            self._sched.join(1)
        
        print('Exit')
        self.gui.root.destroy()
        
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
        
        self._bottomframe.grid_remove()
        view = self._views[shownId]
        self.gui.removeBrowsables()
        self.gui.addBrowsable(view)
        dm = self._datamanagers[shownId]
        view.notify(dm)
        
        for i in range(2):
            self.gui.setSoftButtonState(i == index, i)

        self.gui.root.bind(evItemSelected, 
                      lambda event, arg=shownId: self._ehItemSelected(event, arg))

    def _ehItemSelected(self, event, arg):
        """Handle a click event for an item.
        
        Arguments
        event -- the event object
        arg -- the id of the source of the event
        
        """
        source = self._views[arg]
        viewer = self._views[_viewId]
        
        viewer.setContent(source.itemlist, source.selectedIndex)
        self._carouselview.setItemList(source.itemlist, source.selectedIndex)
        self.gui.removeBrowsables()
        self.gui.addBrowsable(viewer)
        self.gui.addBrowsable(self._carouselview)

        self.gui.maincanvas.itemconfig(_button1Id, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(_button2Id, state = tki.HIDDEN)
        self.gui.maincanvas.itemconfig(_viewId, state = tki.NORMAL)
        self._bottomframe.grid()

    def _ehButton1(self):
        """Event handler for the upper left button."""
        
        self._setupPublicDisplay(_button1Id, [_button2Id, _viewId], 0)
        
    def _ehButton2(self):
        """Event handler for the upper right button."""
        self._setupPublicDisplay(_button2Id, [_button1Id, _viewId], 1)
