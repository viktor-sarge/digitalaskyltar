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
from ctypes import windll
from win32com.client import Dispatch

class VideoFrame(tki.Frame):
    def __init__(self, parent, url):
        """Initiate
        
        Arguments
        parent -- the parent Tkinter widget
        url -- a link to the web page that will be displayed        

        """
        width = parent['width']
        height = width * 9 / 16
        tki.Frame.__init__(self, parent, width = width, height = height)
        hwnd = self.winfo_id()

        #Create an instance of Internet Explorer
        windll.atl.AtlAxWinInit()
        fwnd = windll.user32.CreateWindowExA(0, 'AtlAxWin', 0, 0x50000000, 0, 0, width, height, hwnd, 0, 0, 0)
        self._ie = Dispatch('{8856F961-340A-11D0-A96B-00C04FD705A2}')
        ie_addr = int(repr(self._ie._oleobj_).split()[-1][2:-1], 16)
        windll.atl.AtlAxAttachControl(ie_addr, fwnd, 0)

        #Go to the specified web page
        self._ie.Navigate2(url)
