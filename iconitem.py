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
import PIL.Image as Image
import PIL.ImageTk as ImageTk
import os.path
from common import resizeImage

class IconItem:
    """Class containing an icon image"""
    def __init__(self, imagename, smalldims):
        """Create IconItem.
        
        Arguments
        imagename -- the name of the image
        smalldims -- a tuple containing the maximum dimensions of the icon
        
        """
        self.smallimage = None
        
        try:
            image = Image.open(imagename)
            smallimage = resizeImage(image, smalldims[0], smalldims[1])
            self.smallimage = ImageTk.PhotoImage(smallimage)
        except IOError:
            print('Error: could not open ' + imagename)

def GetIconItems(dir, settings):
    """Load icons for all subjects in the settings.
    
    Argument
    settings -- an object containing a list of subject icons
    
    """
    result = []
    smalldims = (settings.smallpreviewx, settings.smallpreviewy)
    
    for i in settings.subjecticons:
        filename = os.path.join(dir, i)
        result.append(IconItem(filename, smalldims))
        
    return result
