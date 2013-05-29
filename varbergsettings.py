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

_inicommon = 'Common'
_inidims = 'Dimensions'
_iniHorizontalPanel = 'HorizontalPanel'
_iniItemView = 'ItemView'
_iniTopLeftText = 'TopLeftText'

_iniconfig = 'configfile'
_iniprevx = 'previewx'
_iniprevy = 'previewy'
_inismallprevx = 'smallpreviewx'
_inismallprevy = 'smallpreviewy'
_inisubjects = 'Subjects'
_inisubject = 'subject'
_inilibrary = 'library'
_inimarginx = 'marginx'
_inimarginy = 'marginy'
_inifontname = 'fontname'
_inifontsize = 'fontsize'
_inifontstyle = 'fontstyle'
_iniheaderfontname = 'headerfontname'   
_iniheaderfontsize = 'headerfontsize'   
_iniheaderfontstyle = 'headerfontstyle' 
_ininormalfontname = 'normalfontname'   
_ininormalfontsize = 'normalfontsize'   
_ininormalfontstyle = 'normalfontstyle' 
_inifooterfontname = 'footerfontname'   
_inifooterfontsize = 'footerfontsize'
_inifooterfontstyle = 'footerfontstyle' 
_iniauthorfontname = 'authorfontname'   
_iniauthorfontsize = 'authorfontsize'
_iniauthorfontstyle = 'authorfontstyle'
_inileft = 'left'
_initop = 'top'
_inilinewidth = 'linewidth'
_initext = 'text'
_initextcolor = 'textcolor'
_inienableprinter = 'enableprinter'
_inibooksearchprefix = 'booksearchprefix'
_inibooksearchsuffix = 'booksearchsuffix'

_scrollbuttonsection = 'ScrollButtons'
_buttonup = 'ButtonUp'
_buttondown = 'ButtonDown'

class Settings:
    """Super class to the settings classes used for the Varberg displays. 
    This class contains properties that are common for all displays.
    
    """
    def __init__(self, inifile, inidir = None):
        """Read settings from a ConfigParser. 
        
        Arguments
        inifile -- a ConfigParser containing the settings
        
        """
        self.previewx = inifile.getint(_inidims, _iniprevx)
        self.previewy = inifile.getint(_inidims, _iniprevy)
        self.smallpreviewx = inifile.getint(_inidims, _inismallprevx)
        self.smallpreviewy = inifile.getint(_inidims, _inismallprevy)
        self.library = inifile.get(_inicommon, _inilibrary)
        
        self.headerfontname = inifile.get(_iniItemView, _iniheaderfontname)
        self.headerfontsize = inifile.getint(_iniItemView, _iniheaderfontsize)
        self.headerfontstyle = inifile.get(_iniItemView, _iniheaderfontstyle)
        self.normalfontname = inifile.get(_iniItemView, _ininormalfontname)
        self.normalfontsize = inifile.getint(_iniItemView, _ininormalfontsize)
        self.normalfontstyle = inifile.get(_iniItemView, _ininormalfontstyle)
        self.footerfontname = inifile.get(_iniItemView, _inifooterfontname)
        self.footerfontsize = inifile.getint(_iniItemView, _inifooterfontsize)
        self.footerfontstyle = inifile.get(_iniItemView, _inifooterfontstyle)

        if(inifile.has_section(_scrollbuttonsection)):
            self.scrollenabled = True
            self.buttonup =  os.path.join(inidir, inifile.get(_scrollbuttonsection, _buttonup))
            self.buttondown =  os.path.join(inidir, inifile.get(_scrollbuttonsection, _buttondown))
        else:
            self.scrollenabled = False

class Settings1(Settings):
    """This class contains settings for the first Varberg display."""
    def __init__(self, inidir, inifile):
        """Read settings from a ConfigParser. 
        
        Arguments
        inidir -- working directory
        inifile -- a ConfigParser containing the settings
        
        """
        Settings.__init__(self, inifile, inidir)
        self.configfile = os.path.join(inidir, inifile.get(_inicommon, _iniconfig))
        self.cachedir = os.path.join(inidir, inifile.get(_inicommon, _inicachedir))
        self.authorfontname = inifile.get(_iniItemView, _iniauthorfontname)
        self.authorfontsize = inifile.getint(_iniItemView, _iniauthorfontsize)
        self.authorfontstyle = inifile.get(_iniItemView, _iniauthorfontstyle)

class Settings2(Settings):
    """This class contains settings for the second Varberg display."""
    def __init__(self, inidir, inifile):
        """Read settings from a ConfigParser. 
        
        Arguments
        inidir -- working directory
        inifile -- a ConfigParser containing the settings
        
        """
        Settings.__init__(self, inifile, inidir)
        
        self.marginx = inifile.getint(_iniHorizontalPanel, _inimarginx)
        self.marginy = inifile.getint(_iniHorizontalPanel, _inimarginy)
        self.fontname =  inifile.get(_iniHorizontalPanel, _inifontname)
        self.fontsize =  inifile.getint(_iniHorizontalPanel, _inifontsize)
        self.fontstyle = inifile.get(_iniHorizontalPanel, _inifontstyle)

        self.tlfontname = inifile.get(_iniTopLeftText, _inifontname)
        self.tlfontsize = inifile.get(_iniTopLeftText, _inifontsize)
        self.tlfontstyle = inifile.get(_iniTopLeftText, _inifontstyle)
        self.tlleft = inifile.get(_iniTopLeftText, _inileft)
        self.tltop = inifile.get(_iniTopLeftText, _initop)
        self.tllinewidth = inifile.get(_iniTopLeftText, _inilinewidth)
        self.tltext = inifile.get(_iniTopLeftText, _initext)
        self.tltextcolor = inifile.get(_iniTopLeftText, _initextcolor)

_subjectlinedelimiter = '|'
class Settings3(Settings):
    """This class contains settings for the third Varberg display."""
    def __init__(self, inidir, inifile):
        """Read settings from a ConfigParser. 
        
        Arguments
        inidir -- working directory
        inifile -- a ConfigParser containing the settings
        
        """
        Settings.__init__(self, inifile, inidir)
        
        self.authorfontname = inifile.get(_iniItemView, _iniauthorfontname)
        self.authorfontsize = inifile.getint(_iniItemView, _iniauthorfontsize)
        self.authorfontstyle = inifile.get(_iniItemView, _iniauthorfontstyle)
        self.enableprinter = inifile.getboolean(_inicommon, _inienableprinter)
        self.booksearchprefix = inifile.get(_inicommon, _inibooksearchprefix)
        self.booksearchsuffix = inifile.get(_inicommon, _inibooksearchsuffix)

        self.subjects = []
        self.subjecticons = []
        ctr = 1
        option = _inisubject + str(ctr)
        
        while(inifile.has_option(_inisubjects, option)):
            subjectline = inifile.get(_inisubjects, option)
            words = subjectline.split(_subjectlinedelimiter)
            self.subjects.append(words[0])
            self.subjecticons.append(words[1])
            ctr += 1
            option = _inisubject + str(ctr)

class Settings4(Settings):
    """This class contains settings for the fourth display, the Hylte display."""
    def __init__(self, inidir, inifile):
        """Read settings from a ConfigParser. 
        
        Arguments
        inidir -- working directory
        inifile -- a ConfigParser containing the settings
        
        """
        Settings.__init__(self, inifile, inidir)
        self.authorfontname = inifile.get(_iniItemView, _iniauthorfontname)
        self.authorfontsize = inifile.getint(_iniItemView, _iniauthorfontsize)
        self.authorfontstyle = inifile.get(_iniItemView, _iniauthorfontstyle)

el_library = 'Library'
el_section = 'Section'
el_interval = 'Interval'

attr_type = 'Type'
attr_buttontext = 'ButtonText'
attr_buttonindex = 'ButtonIndex'
attr_maxcount = 'MaxCount'
attr_cachedir = 'CacheDir'
attr_link = 'Link'
attr_id = 'Id'
attr_startup = 'Startup'
attr_seconds = "Seconds"

class DataSourceDescription1:
    """Description of one data source for the first Varberg display. A data 
    source describes filtering options and a link to the data source which may 
    be a search result or an RSS feed. Data source descriptions for the first 
    display are stored in XML; the reason for doing this is to make it easier 
    to provide a variable amount of schedulable data sources. 
        
    """
    def __init__(self, xmlnode):
        """Read settings from an XML node. 
        
        Argument
        xmlnode -- the node containing the data source description
        
        """
        self.libraries = []
        self.sections = []
        
        #TBD Only read existing attributes
        self.type = xmlnode.attributes[attr_type].value
        self.buttontext = xmlnode.attributes[attr_buttontext].value
        self.buttonindex = int(xmlnode.attributes[attr_buttonindex].value)
        self.maxcount = int(xmlnode.attributes[attr_maxcount].value)
        self.cacheid = xmlnode.attributes[attr_cachedir].value
        self.link = xmlnode.attributes[attr_link].value
        self.startup = (xmlnode.attributes[attr_startup].value.upper() == 'TRUE')
        
        interval = xmlnode.getElementsByTagName(el_interval)
        
        if(interval.length > 0):
            self.interval = int(interval.item(0).attributes[attr_seconds].value)

        libs = xmlnode.getElementsByTagName(el_library)
        
        for node in libs:
            lib = node.attributes[attr_id].value
            self.libraries.append(lib)
            
        sections = xmlnode.getElementsByTagName(el_section)
        
        for node in sections:
            section = node.attributes[attr_id].value
            self.sections.append(section)
            
sBlog = 'Blog'
sNew = 'New'
_inicachedir = 'cachedir'
_iniinterval = 'interval'
_iniurl = 'url'
_inihistorylength = 'historylength'

class InifileDataSourceDescription:
    """Describes a data source for the second and third Varberg display"""

    def __init__(self, section, inidir, inifile):
        """Read settings from a ConfigParser. 
        
        Arguments
        section -- ConfigParser section containing the data
        inidir -- working directory
        inifile -- a ConfigParser containing the settings
        
        """
        self.link = inifile.get(section, _iniurl)
        self.maxcount = inifile.getint(section, _inihistorylength)
        self.cachedir = os.path.join(inidir, inifile.get(section, _inicachedir))
        self.interval = inifile.getint(section, _iniinterval)
