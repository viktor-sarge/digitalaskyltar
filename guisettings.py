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
#Ini file identifiers
_themesection = 'Theme'
_bgcolor = 'bgcolor'
_bgimage = 'bgimage'
_softbtnimagename = 'softbuttonimage'
_softbtnactiveimagename = 'softbuttonimageactive'
_btnprevimagename = 'prevbuttonimage'
_btnnextimagename = 'nextbuttonimage'
_softbuttonfontname = 'softbuttonfontname'
_softbuttonfontstyle = 'softbuttonfontstyle'
_softbuttonfontsize = 'softbuttonfontsize'
_softbuttonfontunderline = 'softbuttonfontunderline'
_softbuttonactivefontname = 'softbuttonactivefontname'
_softbuttonactivefontstyle = 'softbuttonactivefontstyle'
_softbuttonactivefontsize = 'softbuttonactivefontsize'
_softbuttonactivefontunderline = 'softbuttonfontactiveunderline'
_softbuttonoffsetx = 'softbuttonoffsetx'
_softbuttonoffsety = 'softbuttonoffsety'
_softbuttonbgcolor = 'softbuttonbgcolor'

_dimsection = 'Dimensions'
_areamarginx = 'mainareamarginx'
_areamarginy = 'mainareamarginy'
_areacornerradius = 'mainareacornerradius'

_bottomareasection = 'BottomArea'
_yspace = 'yspace'
_bottomareamarginx = 'bottomareamarginx'
_bottomareabgcolor = 'bottomareabgcolor'

_horizontalpanelsection = 'HorizontalPanel'
_panelspace = 'panelspace'
_panelheight = 'panelheight'
_fontsize = 'fontsize'

class GuiSettings:
    """GUI related settings"""
    
    def __init__(self, inifile):
        """Read GUI related settings from an ini file
        
        Argument
        inifile -- ConfigReader containing the settings
        
        """
        self.areamarginx = inifile.getint(_dimsection, _areamarginx)
        self.areamarginy = inifile.getint(_dimsection, _areamarginy)
        self.arearadius = inifile.getint(_dimsection, _areacornerradius)
        self.bgcolor = inifile.get(_themesection, _bgcolor)
        self.bgimagename = inifile.get(_themesection, _bgimage)
        self.softbtnimagename = inifile.get(_themesection, _softbtnimagename)
        self.softbtnactiveimagename = inifile.get(_themesection, _softbtnactiveimagename)
        self.prevbuttonimagename = inifile.get(_themesection, _btnprevimagename)
        self.nextbuttonimagename = inifile.get(_themesection, _btnnextimagename)
        self.softbuttonfontname = inifile.get(_themesection, _softbuttonfontname)
        self.softbuttonfontstyle = inifile.get(_themesection, _softbuttonfontstyle)
        self.softbuttonfontsize = inifile.getint(_themesection, _softbuttonfontsize)
        self.softbuttonactivefontname = inifile.get(_themesection, _softbuttonactivefontname)
        self.softbuttonactivefontstyle = inifile.get(_themesection, _softbuttonactivefontstyle)
        self.softbuttonactivefontsize = inifile.getint(_themesection, _softbuttonactivefontsize)
        self.softbuttonoffsetx = inifile.getint(_themesection, _softbuttonoffsetx)
        self.softbuttonoffsety = inifile.getint(_themesection, _softbuttonoffsety)
        self.softbuttonbgcolor = inifile.get(_themesection, _softbuttonbgcolor)

        if(inifile.has_section(_bottomareasection)):
            self.yspace = inifile.getint(_bottomareasection, _yspace)
            self.bottomareamarginx = inifile.getint(_bottomareasection, _bottomareamarginx)
            self.bottomareabgcolor = inifile.get(_bottomareasection, _bottomareabgcolor)
            
        if(inifile.has_section(_horizontalpanelsection)):
            self.panelspace = inifile.getint(_horizontalpanelsection, _panelspace)
            self.panelheight = inifile.getint(_horizontalpanelsection, _panelheight)
