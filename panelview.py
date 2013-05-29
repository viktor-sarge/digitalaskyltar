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
from listview import ListView
from language import lang
import language as lng
from common import getFont


evPanelItemSelected = '<<ItemSelectedInPanelListView>>'

class PanelListView(ListView):
    """A ListView that displays its items in a list of horizontal panels
    provided by a panel manager.
    
    """
    def __init__(self, panelmanager, settings):
        """Create PanelListView.

        Arguments
        panelmanager -- the panel manager that has the panels on which the objects 
                        will be visualized
        settings -- settings object containing font settings
        """

        ListView.__init__(self, evPanelItemSelected)
        
        self._canvas = panelmanager.canvas
        self._eventgenerator = panelmanager.canvas
        self._fntText = getFont(settings.fontname, settings.fontsize, settings.fontstyle)
        self._itemdatatuples = []
        self._uids = []
        
        panel = panelmanager.panels[0]
        
        color = panel.center['bg']
        height = panel.center['height']
        #padding = 5
        padding = (height - 4 * settings.fontsize) / 4
        cwrap = panel.center['width'] - 2 * padding
        rwrap = panel.right['width'] - 2 * padding
        ctr = 0

        for i in panelmanager.panels:
            magazine = tki.StringVar()
            blog = tki.StringVar()
            blogexists = tki.StringVar()

            i.left.columnconfigure(0, weight = 1)
            i.left.rowconfigure(0, weight = 1)
            lblImage = tki.Label(i.left)
            lblImage.grid()

            i.center.columnconfigure(0, weight = 1)
            i.center.rowconfigure(0, weight = 1)
            i.center.rowconfigure(1, weight = 1)
            
            l = tki.Label(i.center, textvariable = magazine, font = self._fntText, wraplength = cwrap, justify="left", bg = color)
            l.grid(row = 0, column = 0, sticky = tki.W)
            #l.grid(row = 0, column = 0, padx = padding, pady = padding, sticky = tki.W)
            #l.grid(row = 0, column = 0, padx = padding, pady = padding, sticky = tki.W)
            l = tki.Label(i.center, textvariable = blog, font = self._fntText, wraplength = cwrap, justify="left", bg = color)
            l.grid(row = 1, column = 0, sticky = tki.W)
            
            i.right.columnconfigure(0, weight = 1)
            i.right.rowconfigure(0, weight = 1)
            
            
            b = tki.Button(i.right, text = lang[lng.txtShowBlogpost], font = self._fntText, bg = color)
            b.grid(row = 0, column = 0, padx = padding, pady = padding, sticky = tki.W)
            b.index = ctr
            b.bind("<ButtonRelease-1>", self._ehClick)

#            l = tki.Label(i.right, textvariable = blogexists, font = self._fntText, wraplength = rwrap, justify="left", bg = color)
#            l.grid(row = 0, column = 0, padx = padding, pady = padding, sticky = tki.W)
#            l.index = ctr
#            l.bind("<Button-1>", self._ehClick)

            ctr += 1
            self._itemdatatuples.append((magazine, blog, blogexists, lblImage))
            self._uids.append(i.uid)            
            
        self._itemcount = ctr

    def _update(self):
        """Update the contents of the PanelListView."""
        ListView._update(self)

        for (item, (magazine, blog, blogexists, lblImage), uid) in itertools.izip_longest(self._items, self._itemdatatuples, self._uids):
            if(lblImage is None):
                break
            
            if(item is None):
                self._canvas.itemconfig(uid, state = tki.HIDDEN)
            else:
                self._canvas.itemconfig(uid, state = tki.NORMAL)
                magazine.set(item.name + ' ' + item.issue)
                #blog.set(lang[lng.txtBlogpost] + ': ' + item.title)
                blog.set(item.title)
                blogexists.set(lang[lng.txtShowBlogpost])

                if(item.smallimage is not None):
                    lblImage.config(image = item.smallimage)
                    lblImage.grid()
                else:
                    lblImage.grid_remove()
