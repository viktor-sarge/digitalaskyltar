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
import re
import uuid
import os.path

VideoWrapperExtension = '.htm'

_htmldata = """<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Film</title>

  </head>
  <body>
<object style="height: 390px; width: 640px">
<embed src="http://www.youtube.com/v/@ID@?version=3&feature=player_embedded&autoplay=0&rel=0&disablekb=1&modestbranding=1&controls=1" type="application/x-shockwave-flash" allowScriptAccess="always" allowfullscreen="false" 
width="640" height="360"></object>
  </body>
</html>
"""

#From google
_htmldata_old = """<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    
    <title>Film</title>

  </head>
  <body>
<object style="height: 390px; width: 640px">
<param name="movie" value="http://www.youtube.com/v/@ID@?version=3&feature=player_embedded&autoplay=1&rel=0&disablekb=1&controls=0"></param>
<param name="allowFullScreen" value="true"></param>
<param name="allowscriptaccess" value="always"></param>
<embed src="http://www.youtube.com/v/@ID@?version=3&feature=player_embedded&autoplay=1&rel=0&disablekb=1" type="application/x-shockwave-flash" allowScriptAccess="always" allowfullscreen="false" 
width="640" height="360"></object>
  </body>
</html>
"""


def createVideo(src, dir, filename):
    """Create a web page containing a video player and return its filename

    Currently only youtube videos are supported. 

    Arguments
    src -- the raw video link
    dir -- the directory where the web page will be created
    filename -- the name of the file that will be created

    """
    if(not 'youtube' in src):
        raise Exception('Only youtube videos can be shown')

    #TBD Create guid
    #filename = os.path.join(dir, str(uuid.uuid1()) + '.htm')
    filename = os.path.join(dir, filename + VideoWrapperExtension)
    
    src = src.split('?')[0]
    parts = src.split('/')
    src = parts[len(parts) - 1]
    
    content = re.sub('@ID@', src, _htmldata)
    
    file = open(filename, 'w')
    file.write(content)
    file.close()
    
    return filename
