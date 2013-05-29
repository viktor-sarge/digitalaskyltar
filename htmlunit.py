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

imagekey = '@IMAGE@'
imagewidthkey = '@IMAGEWIDTH@'
imageheightkey = '@IMAGEHEIGHT@'
titlekey = '@TITLE@'
headlinekey = '@HEADLINE@'
authorkey = '@UTHOR@'
textkey = '@TEXT@'

_keywords = [imagekey, imagewidthkey, imageheightkey, imageheightkey, titlekey, 
             headlinekey, authorkey, textkey]

_htmltemplate = r"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>@TITLE@</title>
</head>
<body>
  <div style="text-align:center">
    <h1>@HEADLINE@</h1>
    <image src="@IMAGE@" width="@IMAGEWIDTH@" height="@IMAGEHEIGHT@">
  </div>
  <p>
    @TEXT@
  </p>
</body>
</html>
"""

def createHtml(defs):
    """Create an HTML document describing a book from a dictionary of keywords.
    
    Argument
    defs -- dictionary containing definitions describing a book
    
    """
#TBD Backslash problems; fix later
#    result = _htmltemplate
#    
#    for i in _keywords:
#        if(defs.has_key(i)):
#            value = defs[i]
#            result = re.sub(i, defs[i], result)

    for i in _keywords:
        if(not defs.has_key(i)):
            defs[i] = ''

    result = ur"""<!DOCTYPE html>
    <html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>""" + defs[titlekey].encode('utf8') + """</title>
    </head>
    <body>
      <div style="text-align:center">
        <h1>""" + defs[headlinekey].encode('utf8') + """</h1>
        <h3>""" + defs[authorkey].encode('utf8') + """</h3>
        
        <image src="file:///""" + defs[imagekey] + """" width=" """ + defs[imagewidthkey] + """ height=" """ + defs[imageheightkey] + """">
      </div>
      <p>
        """ + defs[textkey].encode('utf8') + """
      </p>
    </body>
    </html>
    """

    return result
