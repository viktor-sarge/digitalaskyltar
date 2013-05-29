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
import sys
import shutil

import varberg1
import varberg2
import varberg3
import hylte4
from download import download3
from common import getConfigParser

#Inifile constants
_ininames = ['varberg1.ini', 'varberg2.ini', 'varberg3.ini', 'hylte4.ini']
_inisection = 'Default'

_displaynames = ['1', '2', '3', '4']
_cache = 'DOWNLOAD='

def main():
    """Load the inifile and start the program."""

    inidir = os.path.dirname(os.path.abspath(sys.argv[0]))
    download = False

    if(sys.argv[1].upper() == _displaynames[0]):
        unit = varberg1
        ininame = _ininames[0]
    elif(sys.argv[1].upper() == _displaynames[1]):
        unit = varberg2
        ininame = _ininames[1]
    elif(sys.argv[1].upper() == _displaynames[2]):
        unit = varberg3
        ininame = _ininames[2]
        
        if(len(sys.argv) > 2):
            if(sys.argv[2].upper().startswith(_cache)):
                amount = sys.argv[2][len(_cache):]
                download = True
    elif(sys.argv[1].upper() == _displaynames[3]):
        unit = hylte4
        ininame = _ininames[3]
    else:
        print('Please provide a valid display number')
        return

    inifile = os.path.join(inidir, ininame)
    parser = getConfigParser(inifile)

    #Workaround for unicode in exefiles
    if hasattr(sys,"setdefaultencoding"):
        sys.setdefaultencoding("utf-8")

    if(parser is not None):
        if(download):
            if(unit == varberg3):
                download3(inidir, parser, amount)
        else:
            controller = unit.Controller(inidir, parser)
            controller.gui.root.mainloop()
    
if __name__ == "__main__":
    main()
