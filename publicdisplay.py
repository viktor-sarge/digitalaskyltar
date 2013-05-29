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
import os.path
import sys

import PIL.Image as Image
import PIL.ImageTk as ImageTk
from guisettings import GuiSettings
from panel import PanelManager
from common import getFont
from language import lang
import language as lng

shpRoundRect = 'RoundRect'
shpRect = 'Rect'
shpSmallRoundRect = 'SmallRoundRect'
shpBottomRect = 'BottomRect'

_contentbgcolor = 'white'
_topbuttontextcolor = 'white'
_bottompadding = 20
_topbuttoncount = 2

_bottomcanvasframespace = 20
_bottomcanvasframeheight = 40

class PublicDisplay:
    """Handle the main window and the basic GUI elements"""

    def __init__(self, inifile):
        """Intiate the GUI
        
        Arguments
        inifile -- contains settings for the application
        
        """
        root = tki.Tk()
        self.root = root
        
        self._donotthrow = []
        self._softbtn = []
        self._softbtntext = ['', '']
        self._browsables = []
        self._handlers = [None, None]
        self._observables = [None, None]

        #Get dimensions
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        #Debug 
        screenwidth = min(screenwidth, max(800, screenheight * 3 / 4))

        #Set up application window
        root.overrideredirect(1)
        geom = "{}x{}+{}+{}".format(screenwidth, screenheight, 0, 0)
        print(geom)
        root.geometry(geom)
        root.columnconfigure(0, weight = 1)
        root.rowconfigure(0, weight = 1)

        settings = GuiSettings(inifile)
        self._settings = settings

        #Set theme
        self._settheme(screenwidth, screenheight)
        
        #Get dimensions for main area
        imagew = screenwidth
        self._assignDimensions()
        self._arearadius = settings.arearadius
        self._areamarginy = settings.areamarginy
        
    def createMainAreaShape(self, shape, tag, marginx = None, marginy = None):
        """Return a frame located in the specified shape in the main area
        
        Arguments
        shape -- the kind of shape to create
        tag -- the id of the rounded rectangle; use the id to show/hide it
        marginx -- optional override of the x margin
        marginy -- optional override of the y margin

        """
        self._assignDimensions(marginx, marginy)
        
        if(shape == shpRoundRect):
            return self._createRoundRect(tag)
        elif(shape == shpSmallRoundRect):
            return self._createSmallRoundRect(tag)
        elif(shape == shpRect):
            return self._createRect(tag)
        elif(shape == shpBottomRect):
            return self._createBottomRect(tag)
        else:
            raise Exception('Can\'t create shape ' + shape)

    def createBottomFrame(self):
        """Create a frame located between the two browse buttons"""
        frame = tki.Frame(self._bottomframe, width =  self._bottomrectwidth, height =  self._bottomrectheight, 
                          bg = self.bgcolor)
        frame.grid(row = 0, column = 1, padx = _bottompadding, sticky = tki.W + tki.E)
        frame.grid_propagate(0)

        return frame
    
    def createPanelManager(self, tag, marginx = None, marginy = None):
        """Return a PanelManager object
        
        Arguments
        tag -- the id of the panels; use the id to show/hide them
        marginx -- optional override of the x margin
        marginy -- optional override of the y margin
        
        """
        self._assignDimensions(marginx, marginy)
        
        return PanelManager(self.root, self.maincanvas, (self.contentwidth, self.contentheight), 
                            (self.contentleft, self.contenttop), tag, self._settings)

    def addBrowsable(self, browsable):
        """Add an object that has a prev() and a next() function"""
        self._browsables.append(browsable)
        
    def removeBrowsables(self):
        """Remove all objects added with addBrowsable"""
        self._browsables = []
        
    def drawText(self, x, y, width, text, color, font):
        """Draw a text on the display. 
        
        Arguments
        x -- x coordinate
        y -- y coordinate
        width -- maximum line lenght
        text -- the text to display
        color -- the color of the text
        font -- the font to use
                
        """        
        self.maincanvas.create_text(x, y, anchor = tki.NW, justify = tki.LEFT, text = text, width = width, 
                                    font = font, fill = color)

    def setupSoftbutton(self, handler, text, index, observable = None):
        """Setup one of the two top buttons.
        
        Arguments
        handler -- event handler for the button
        text -- the test of the button
        index -- which button to set up: 0->top left;1-> top right
        observable -- an observable object that this public display will observe; any updates will be reflected to the user 

        """
        button = self._softbtn[index]
        self._handlers[index] = handler
        button.config(text = text)
        self._softbtntext[index] = text

        if(observable is not None):
            observable.addObserver(self)

        self._observables[index] = observable

    def setSoftButtonState(self, highlighted, index, visible = True):
        """Set the state of one of the two top buttons.
        
        Arguments
        highlighted -- determines if the button is highlighted
        index -- which button to set: 0->top left;1-> top right
        visible -- determines if the button is visible
        
        """
        button = self._softbtn[index]
        
        if(not visible):
            button.grid_remove()
        else:
            button.grid()
        
        if(highlighted):
            button.config(image = self._softimageactive)
            button.config(font = self._activefont)
        else:
            button.config(image = self._softimage)
            button.config(font = self._passivefont)
            
    def notify(self, observable):
        """Gets called by any observed observable
        
        Argument
        observable -- the calling observable
        
        """
        
        try:
            index = self._observables.index(observable)
        except ValueError:
            #The calling observable is not being observed; do nothing
            return

        button = self._softbtn[index]
        button.config(text = self._softbtntext[index] + lang[lng.txtUpdated])

    def _assignDimensions(self, marginx = None, marginy = None):
        """Set the dimensions of the main area content.
        
        Arguments
        marginx -- the left and right margin
        marginy -- the top and bottom margin
        
        """
        if(marginx is None):
            marginx = self._settings.areamarginx
            
        if(marginy is None):
            marginy = self._settings.areamarginy
        
        self.contentwidth = self._mainwidth - 2 * marginx - 2 * self._settings.arearadius
        self.contentheight = self._mainheight - 2 * marginy - 2 * self._settings.arearadius
        self.contentleft = self._maincenterx - self.contentwidth / 2
        self.contenttop = self._maincentery - self.contentheight / 2

    def _createRoundRect(self, tag):
        """Return a frame located in a rounded rectangle in the middle of the screen. 
        
        Arguments
        tag -- the id of the rounded rectangle; use the id to show/hide it
        
        """
        return self._createRoundRectCommon(tag, self.contentheight)
    
    def _createSmallRoundRect(self, tag):
        """Return a frame located in a rounded rectangle in the middle of the screen; 
           space is reserved for a bottom rectangle
        
        Arguments
        tag -- the id of the rounded rectangle; use the id to show/hide it
        
        """
        height = self.contentheight - _bottomcanvasframeheight - self._settings.yspace
        return self._createRoundRectCommon(tag, height)

    def _createRect(self, tag):
        """Return a frame located in a rectangle in the middle of the screen
        
        Arguments
        tag -- the id of the rectangle; use the id to show/hide it
        
        """
        height = self.contentheight - _bottomcanvasframeheight - self._settings.yspace
        frame = tki.Frame(self.root, width = self.contentwidth, height = height, bg = _contentbgcolor)
        self.maincanvas.create_window(self._maincenterx, self.contenttop, window = frame, tags = tag, anchor = tki.N)
        frame.grid_propagate(0)
        
        print('Rect1: ' + str(self._maincenterx), str(self.contenttop), str(self.contentwidth), str(height))

        return frame

    def _createBottomRect(self, tag):
        """Return a frame located in a rectangle in the bottom of the canvas area; 
           space is reserved for a bottom rectangle
        
        Arguments
        tag -- the id of the rectangle; use the id to show/hide it
        
        """
        insy = self.contenttop + self.contentheight
        bottomwidth = self._mainwidth - 2 * self._settings.bottomareamarginx - 2 * self._settings.arearadius

        frame = tki.Frame(self.root, width = bottomwidth, height = _bottomcanvasframeheight, bg = self._settings.bottomareabgcolor)
        #frame = tki.Frame(self.root, width = self.contentwidth, height = _bottomcanvasframeheight, bg = _contentbgcolor)
        self.maincanvas.create_window(self._maincenterx, insy, window = frame, tags = tag, anchor = tki.S)
        frame.grid_propagate(0)
        
        return frame        

    def _createRoundRectCommon(self, tag, contentheight):
        """Create a frame inside a rounded rectangle.
        
        Arguments
        tag -- the id of the rounded rectangle; use the id to show/hide it
        contentheight -- the height of the frame

        """
        contentleft = self.contentleft
        contenttop = self.contenttop
        contentwidth = self.contentwidth
        arearadius = self._arearadius
        
        tophi = contenttop - arearadius
        toplo = contenttop + arearadius
        self.maincanvas.create_oval(contentleft - arearadius, tophi, contentleft + arearadius, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)
        self.maincanvas.create_rectangle(contentleft, tophi, contentleft + contentwidth, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)
        center = contentleft + contentwidth - 1
        self.maincanvas.create_oval(center - arearadius, tophi, center + arearadius, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)

        frame = tki.Frame(self.root, width = contentwidth + 2 * arearadius, height = contentheight, bg = _contentbgcolor)
        self.maincanvas.create_window(self._maincenterx, self.contenttop, window = frame, tags = tag, anchor = tki.N)
        frame.grid_propagate(0)

#        self.maincanvas.create_rectangle(contentleft - arearadius, contenttop, contentleft + contentwidth + arearadius, contenttop + contentheight, 
#                                    fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)

        tophi = contenttop + contentheight - arearadius
        toplo = contenttop + contentheight + arearadius
        self.maincanvas.create_oval(contentleft - arearadius, tophi, contentleft + arearadius, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)
        self.maincanvas.create_rectangle(contentleft, tophi, contentleft + contentwidth, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)
        center = contentleft + contentwidth - 1
        self.maincanvas.create_oval(center - arearadius, tophi, center + arearadius, toplo, fill = _contentbgcolor, outline = _contentbgcolor, tags = tag)
        
        return frame

    def _settheme(self, screenwidth, screenheight):
        """Set the theme that was specified in the inifile. 
        
        Arguments
        screenwidth -- the width of the screen
        screenheight -- the height of the screen
        
        """
        bgcolor = self._settings.bgcolor
        self.bgcolor = bgcolor
        
        self._passivefont = getFont(self._settings.softbuttonfontname, self._settings.softbuttonfontsize, 
                                    self._settings.softbuttonfontstyle)
        
        self._activefont = getFont(self._settings.softbuttonactivefontname, self._settings.softbuttonactivefontsize, 
                                    self._settings.softbuttonactivefontstyle)

        #Load images
        dirname = os.path.dirname(sys.argv[0])

        imagename = os.path.join(dirname, self._settings.softbtnimagename)
        softimage = Image.open(imagename)
        topheight = softimage.size[1]
        softimage = ImageTk.PhotoImage(softimage)
        self._softimage = softimage

        imagename = os.path.join(dirname, self._settings.softbtnactiveimagename)
        softimage = Image.open(imagename)
        topheight = softimage.size[1]
        softimage = ImageTk.PhotoImage(softimage)
        self._softimageactive = softimage

        imagename = os.path.join(dirname, self._settings.prevbuttonimagename)
        previmage = Image.open(imagename)
        prevwidth = previmage.size[0]
        bottomheight = previmage.size[1]
        previmage = ImageTk.PhotoImage(previmage)
        self._donotthrow.append(previmage)

        imagename = os.path.join(dirname, self._settings.nextbuttonimagename)
        nextimage = Image.open(imagename)
        nextwidth = nextimage.size[0]
        bottomheight = max(bottomheight, nextimage.size[1])
        nextimage = ImageTk.PhotoImage(nextimage)
        self._donotthrow.append(nextimage)

        canvasheight = (screenheight - (bottomheight + 2 * _bottompadding))
        mainareaheight = (screenheight - (topheight + 2 * self._settings.softbuttonoffsety + bottomheight + 2 * _bottompadding))
        imagename = os.path.join(dirname, self._settings.bgimagename)
        bgimage = Image.open(imagename)
        bgimage = bgimage.resize((screenwidth, canvasheight), Image.ANTIALIAS)
        bgimage = ImageTk.PhotoImage(bgimage)
        self._donotthrow.append(bgimage)
        
        #Calculate dimensions        
        canvascenterx = screenwidth / 2
        canvascentery = canvasheight / 2
        
        #Store values for later use
        self._mainwidth = screenwidth
        self._mainheight = mainareaheight
        self._maincenterx = canvascenterx
        self._maincentery = topheight + 2 * self._settings.softbuttonoffsety + mainareaheight / 2

        #Create top frame
#        topframe = tki.Frame(self.root, bg = bgcolor)
#        topframe.grid(row = 0, sticky = tki.W + tki.N + tki.E)
#        topframe.columnconfigure(0, weight = 1)
#        topframe.columnconfigure(1, weight = 1)

#        b = tki.Button(topframe, font = self._passivefont, image = self._softimage, compound = tki.CENTER, bd = 0, highlightthickness = 0,  
#                       bg = bgcolor, activebackground = bgcolor, foreground = _topbuttontextcolor, activeforeground = _topbuttontextcolor, relief = tki.FLAT)
#        self._softbtn.append(b)
#        
#        b.grid(column = 0, row = 0, sticky = tki.W)
#        b = tki.Button(topframe, font = self._passivefont, image = self._softimage, compound = tki.CENTER, bd = 0, highlightthickness = 0,  
#                       bg = bgcolor, activebackground = bgcolor, foreground = _topbuttontextcolor, activeforeground = _topbuttontextcolor)
#        self._softbtn.append(b)
#        b.grid(column = 1, row = 0, sticky = tki.E)

        #Create main canvas
        canvas = tki.Canvas(self.root, bg = bgcolor, bd = 0, highlightthickness = 0)
        self.maincanvas = canvas
        canvas.grid(row = 0, column = 0, sticky = tki.W + tki.N + tki.E + tki.S)
        canvas.create_image(canvascenterx, canvascentery, image = bgimage)
        
        #Create top buttons
        color = self._settings.softbuttonbgcolor
        frame = tki.Frame(self.root)
        canvas.create_window(self._settings.softbuttonoffsetx, self._settings.softbuttonoffsety, window = frame, anchor = tki.NW)
        b = tki.Button(frame, font = self._passivefont, image = self._softimage, compound = tki.CENTER, bd = 0, highlightthickness = 0,  
                       bg = color, activebackground = color, foreground = _topbuttontextcolor, activeforeground = _topbuttontextcolor, relief = tki.FLAT, 
                       command = lambda : self._ehButton(0))
        self._softbtn.append(b)
        b.grid()

        frame = tki.Frame(self.root)
        canvas.create_window(screenwidth - self._settings.softbuttonoffsetx, self._settings.softbuttonoffsety, window = frame, anchor = tki.NE)
        b = tki.Button(frame, font = self._passivefont, image = self._softimage, compound = tki.CENTER, bd = 0, highlightthickness = 0,  
                       bg = color, activebackground = color, foreground = _topbuttontextcolor, activeforeground = _topbuttontextcolor, 
                       command = lambda : self._ehButton(1))
        self._softbtn.append(b)
        b.grid()
        
        #Create bottom frame
        bottomframe = tki.Frame(self.root, height = 100, bg = bgcolor)
        bottomframe.grid(row = 1, sticky = tki.W + tki.E + tki.S)
        #bottomframe.columnconfigure(0, weight = 1)
        bottomframe.columnconfigure(1, weight = 1)
        bottomframe.rowconfigure(0, weight = 1)
        #bottomframe.columnconfigure(2, weight = 1)
        self._bottomframe = bottomframe
        
        self._bottomrectwidth = screenwidth - prevwidth - nextwidth - 6 * _bottompadding
        self._bottomrectheight = bottomheight

        b = tki.Button(bottomframe, image = previmage, bd = 0, highlightthickness = 0,  bg = bgcolor, 
                       activebackground = bgcolor, command = self._ehprev)
        self._btnprev  = b
        b.grid(column = 0, row = 0, padx = _bottompadding, pady = _bottompadding, sticky = tki.W)

        b = tki.Button(bottomframe, image = nextimage, bd = 0, highlightthickness = 0,  bg = bgcolor, 
                       activebackground = bgcolor, command = self._ehnext)
        self._btnnext  = b
        b.grid(column = 2, row = 0, padx = _bottompadding, pady = _bottompadding, sticky = tki.E)


    def _ehButton(self, index):
        """Handle the events of the two top buttons
        
        Argument
        index -- button index ({0, 1})

        """
        if((0 <= index) and (index < _topbuttoncount)):
            button = self._softbtn[index]
            button.config(text = self._softbtntext[index])

            if(self._handlers[index] is not None):
                self._handlers[index]()

    def _ehnext(self):
        """Handle the event of the low right (next) button."""
        for b in self._browsables:
            b.next()

    def _ehprev(self):
        """Handle the event of the low left (prev) button."""
        for b in self._browsables:
            b.prev()
