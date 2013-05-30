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
from distutils.core import setup
import py2exe

#PACKAGES = [
#    'site-packages',
#]

setup(console=['admin.py'], options={"py2exe":{"dll_excludes":[ "mswsock.dll", "powrprof.dll" ]}}, 
      typelibs = [
        ('{00062FFF-0000-0000-C000-000000000046}', 0, 11, 0),
        ('{2DF8D04C-5BFA-101B-BDE5-00AA0044DE52}', 0, 2, 1),
        ('{AC0714F2-3D04-11D1-AE7D-00A0C90F26F4}', 0, 1, 0),
    ])
