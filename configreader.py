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
from xml.dom.minidom import parse, Document
import datetime

from varbergsettings import DataSourceDescription1

el_defcfgitem = 'DefaultConfigItem'
el_cfgitem = 'ConfigItem'
el_datasource = 'DataSource'
el_start = 'Start'
el_stop = 'Stop'

attr_year = 'Year'
attr_month = 'Month'
attr_day = 'Day'
attr_hour = 'Hour'
attr_minute = 'Minute'
attr_second = 'Second'

class Schedulable:
    """A schedulable data source which will show data described by dataSourceDescription
    starting at start, ending at stop
    
    """
    def __init__(self, xmlnode):
        self.dataSourceDescription = DataSourceDescription1(xmlnode.getElementsByTagName(el_datasource)[0])
        
        start = xmlnode.getElementsByTagName(el_start)[0]
        self.start = self._getTimeDate(start)
        stop = xmlnode.getElementsByTagName(el_stop)[0]
        self.stop = self._getTimeDate(stop)
        
    def _getTimeDate(self, xmlnode):
        year = int(xmlnode.attributes[attr_year].value)
        month = int(xmlnode.attributes[attr_month].value)
        day = int(xmlnode.attributes[attr_day].value)
        hour = int(xmlnode.attributes[attr_hour].value)
        minute = int(xmlnode.attributes[attr_minute].value)
        second = int(xmlnode.attributes[attr_second].value)
        
        return datetime.datetime(year, month, day, hour, minute, second)


class ConfigReader:
    """Reads a config xml file for the first Varberg display and stores default data sources 
    in defaults and schedulable data sources in scheds
    
    """
    
    def __init__(self, srcfile):
        xmldoc = parse(srcfile)
        
        self.defaults = []
        self.scheds = []
        
        defaults = xmldoc.documentElement.getElementsByTagName(el_defcfgitem)

        for node in defaults:
            dsd = DataSourceDescription1(node.getElementsByTagName(el_datasource)[0])
            self.defaults.append(dsd)
        
        scheds = xmldoc.documentElement.getElementsByTagName(el_cfgitem)

        for node in scheds:
            sched = Schedulable(node)
            self.scheds.append(sched)
