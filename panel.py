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

_cornerradius = 10
_denominator = 6
_bgcolor = 'white'
_linecolor = 'black'

class HorizontalPanel:
    """Container class that contains references to sub panels in a PanelManager."""
    def __init__(self, left, center, right, uid):
        """Create HorizontalPanel.
        
        Arguments
        left -- left panel
        center -- center panel
        right -- right panel
        uid -- id of the the panels
        
        """
        self.left = left
        self.center = center
        self.right = right
        self.uid = uid

class PanelManager:
    """A graphical container that contains a number of rounded panels.
    Each panel contains three sub panels called left, center and right.
    
    """
    def __init__(self, parent, canvas, dims, offset, id, settings):
        """Create the panel manager and calculate the number of panels.
        
        Arguments
        parent -- parent frame on which the panels will be created
        canvas -- parent canvas on which window object for the panels will be created
        dims -- a tuple containing width and height of the panel manager
        offset -- a tuple containing x and y coordinates for the panel manager
        id -- id and id prefix for the graphical elements drawn by the panel manager
        settings -- object containing panel height and space between panels
        
        """
        self.panels = []
        self.canvas = canvas
        
        yspace = settings.panelspace
        width = dims[0] - 2 * _cornerradius
        height = settings.panelheight

        smallwidth = width / _denominator
        largewidth = width - smallwidth * 2
        diameter = 2 * _cornerradius
        left = offset[0] + _cornerradius
        leftarcx = (left - _cornerradius, left + _cornerradius)
        
        rightarcx = (left + width - _cornerradius, left + width + _cornerradius)
        rightx = left + smallwidth + largewidth
        
        count = (dims[1] + yspace) / (height + yspace)

        for i in range(count):
            top = offset[1] + i * (height + yspace)
            bottom = top + height - 1
            uid = id + str(i)
            tags = [id, uid]

            #Create panels            
            lframe = tki.Frame(parent, width = smallwidth, height = height, bg = _bgcolor)
            canvas.create_window(left, top, window = lframe, tags = tags, anchor = tki.NW)
            lframe.grid_propagate(0)

            cframe = tki.Frame(parent, width = largewidth, height = height, bg = _bgcolor)
            canvas.create_window(left + smallwidth, top, window = cframe, tags = tags, anchor = tki.NW)
            cframe.grid_propagate(0)

            rframe = tki.Frame(parent, width = smallwidth, height = height, bg = _bgcolor)
            canvas.create_window(left + smallwidth + largewidth, top, window = rframe, tags = tags, anchor = tki.NW)
            rframe.grid_propagate(0)

            self.panels.append(HorizontalPanel(lframe, cframe, rframe, uid))
            
            #Create graphics
            #canvas.create_rectangle(left + smallwidth, top, left + smallwidth + largewidth, top + height, fill = _bgcolor, outline = _linecolor, tags = tags)
            
#            canvas.create_line(rightx, top, rightx + smallwidth, top, tags = tags)
#            canvas.create_line(rightx + smallwidth, top, rightx + smallwidth, top + height, tags = tags)
#            canvas.create_line(rightx, top + height, rightx + smallwidth, top + height, tags = tags)
#            
#            canvas.create_line(left, top, left + smallwidth, top, tags = tags)
#            canvas.create_line(left, top, left, top + height, tags = tags)
#            canvas.create_line(left, top + height, left + smallwidth, top + height, tags = tags)

            canvas.create_oval(leftarcx[0], top, leftarcx[1], top + diameter, fill = _bgcolor, outline = _bgcolor, tags = tags)
            canvas.create_rectangle(leftarcx[0], top + _cornerradius, leftarcx[0] + _cornerradius, bottom - _cornerradius, fill = _bgcolor, outline = _bgcolor, tags = tags)
            canvas.create_oval(leftarcx[0], bottom, leftarcx[1], bottom - diameter, fill = _bgcolor, outline = _bgcolor, tags = tags)

            canvas.create_oval(rightarcx[0], top, rightarcx[1], top + diameter, fill = _bgcolor, outline = _bgcolor, tags = tags)
            canvas.create_rectangle(rightarcx[0], top + _cornerradius, rightarcx[1], bottom - _cornerradius, fill = _bgcolor, outline = _bgcolor, tags = tags)
            canvas.create_oval(rightarcx[0], bottom, rightarcx[1], bottom - diameter, fill = _bgcolor, outline = _bgcolor, tags = tags)
            
            #canvas.create_arc(leftarcx[0], top, leftarcx[1], top + diameter, fill = _bgcolor, start = 90, extent = 90, tags = tags)
            #canvas.create_arc(leftarcx[0], bottom, leftarcx[1], bottom - diameter, fill = _bgcolor, start = 180, extent = 90, tags = tags)
#            canvas.create_arc(rightarcx[0], top, rightarcx[1], top + diameter, fill = _bgcolor, start = 0, extent = 90, tags = tags)
#            canvas.create_arc(rightarcx[0], bottom, rightarcx[1], bottom - diameter, fill = _bgcolor, start = 270, extent = 90, tags = tags)
