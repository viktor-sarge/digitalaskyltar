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
from common import getConfigParser
from edittab import EditTab
from edittab1 import EditTab1
from edittab2 import EditTab2
from edittab3 import EditTab3

displaytypes = ['Varberg1', 'Varberg2', 'Varberg3']
_edittabs = [EditTab1, EditTab2, EditTab3]

def getNewTab(displaytype, filename, *args):
    """Return the correct type EditTab for the specified config file
    
    Argument
    displaytype -- One of the display types listed in displaytypes
    filename -- path and name of a config file of a Varberg display
    args -- arguments to the EditTab constructor that are not used by getTab
    
    """
    classtype = _edittabs[displaytypes.index(displaytype)]
    return classtype(filename, *args)

def getTab(filename, *args):
    """Return the correct type EditTab for the specified config file
    
    Argument
    filename -- path and name of a config file of a Varberg display
    args -- arguments to the EditTab constructor that are not used by getTab
    
    """
    cfgp = getConfigParser(filename)
    
    if(cfgp.has_section('BottomArea')):
        return EditTab3(filename, *args)
    elif(cfgp.has_section('TopLeftText')):
        return EditTab2(filename, *args)
    else:
        return EditTab1(filename, *args)
