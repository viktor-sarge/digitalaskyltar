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

import editinput as ei
import scrollbox
import language as lng
from language import lang

_padx = 5
_pady = 5

#Common
class EditInputTheme(ei.EditInput):
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtTheme])

        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtBgImage], 'Theme', 'bgimage')
        self._subinputs.append(imageinput)
        imageinput.grid(row = 0, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtSoftBtnActive], 'Theme', 'softbuttonimageactive')
        self._subinputs.append(imageinput)
        imageinput.grid(row = 1, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtSoftBtnInactive], 'Theme', 'softbuttonimage')
        self._subinputs.append(imageinput)
        imageinput.grid(row = 2, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtPrevBtn], 'Theme', 'prevbuttonimage')
        self._subinputs.append(imageinput)
        imageinput.grid(row = 3, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtNextBtn], 'Theme', 'nextbuttonimage')
        self._subinputs.append(imageinput)
        imageinput.grid(row = 4, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtActiveFont], 'Theme', 'softbuttonactivefont')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 0, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtInactiveFont], 'Theme', 'softbuttonfont')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 1, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        colorinput =  ei.EditInputColor(self, parenttab, lang[lng.txtBgColor], 'Theme', 'bgcolor')
        self._subinputs.append(colorinput)
        colorinput.grid(row = 2, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        colorinput =  ei.EditInputColor(self, parenttab, lang[lng.txtBtnColor], 'Theme', 'softbuttonbgcolor')
        self._subinputs.append(colorinput)
        colorinput.grid(row = 3, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtBtnMargin], 'Theme', 'softbuttonoffset')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 4, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

class EditInputDimensions(ei.EditInput):
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtDimensions])

        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtMainAreaMargin], 'Dimensions', 'mainareamargin')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 0, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtImageSize], 'Dimensions', 'preview')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 1, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtThumbnailSize], 'Dimensions', 'smallpreview')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 0, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtCornerRadius], 'Dimensions', 'mainareacornerradius')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 1, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

class EditInputScrollbuttons(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtScrollButtons])
        self._enable = tki.BooleanVar()

        cb = tki.Checkbutton(self, text = lang[lng.txtUseScrollButtons], onvalue = True, offvalue = False, variable = self._enable, command = self._setDirty)
        cb.grid(row = 0, column = 0, padx = 2, pady = 2, sticky = tki.W)
        
        eii = ei.EditInputImage(self, parenttab, lang[lng.txtUpImage], 'ScrollButtons', 'ButtonUp')
        eii.grid(row = 1, column = 0, padx = 2, pady = 2, sticky = tki.W)
        self._subinputs.append(eii)

        eii = ei.EditInputImage(self, parenttab, lang[lng.txtDownImage], 'ScrollButtons', 'ButtonDown')
        eii.grid(row = 2, column = 0, padx = 2, pady = 2, sticky = tki.W)
        self._subinputs.append(eii)

    def readValue(self, configparser):
        exists = configparser.has_section('ScrollButtons')
        self._enable.set(exists)
        
        if(exists):
            ei.EditInput.readValue(self, configparser)

    def writeValue(self, configfilewriter):
        if(self._enable.get()):
            ei.EditInput.writeValue(self, configfilewriter)

class EditInputItemView(ei.EditInput):
    
    def __init__(self, parent, parenttab, authorExists = False):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtItemView])

        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtHeaderFont], 'ItemView', 'headerfont')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 0, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtTextFont], 'ItemView', 'normalfont')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 1, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtFooterFont], 'ItemView', 'footerfont')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 2, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        if(authorExists):
            fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtAuthorFont], 'ItemView', 'authorfont')
            self._subinputs.append(fontinput)
            fontinput.grid(row = 3, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

#Display 1
class EditInputCommon1(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtCommon])

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtLibrary], 'Common', 'library')
        self._subinputs.append(textinput)
        textinput.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.W)

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtCacheFolder], 'Common', 'cachedir')
        self._subinputs.append(textinput)
        textinput.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tki.W)

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtConfigFile], 'Common', 'configfile')
        self._subinputs.append(textinput)
        textinput.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = tki.W)

#Display 2
class EditInputCommon2(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtCommon])

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtLibrary], 'Common', 'library')
        self._subinputs.append(textinput)
        textinput.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.W)

class EditInputTopLeftText(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtTopLeftText])
        self.columnconfigure(2, weight = 1)

        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtFont], 'TopLeftText', 'font')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 0, column = 0, rowspan = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtInsPoint], 'TopLeftText', '', 'Left', 'Top')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 0, column = 1, rowspan = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtLineLength], 'TopLeftText', 'linewidth')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 0, column = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        colorinput =  ei.EditInputColor(self, parenttab, lang[lng.txtTextColor], 'TopLeftText', 'textcolor')
        self._subinputs.append(colorinput)
        colorinput.grid(row = 1, column = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtText], 'TopLeftText', 'text')
        self._subinputs.append(textinput)
        textinput.grid(row = 2, column = 0, columnspan = 3, padx = 5, pady = 5, sticky = tki.W)

class EditInputHorizontalPanel(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtHorizPanel])

        fontinput =  ei.EditInputFont(self, parenttab, lang[lng.txtFont], 'HorizontalPanel', 'font')
        self._subinputs.append(fontinput)
        fontinput.grid(row = 0, column = 0, rowspan = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)
        
        vectorinput =  ei.EditInputVector(self, parenttab, lang[lng.txtMargin], 'HorizontalPanel', 'margin')
        self._subinputs.append(vectorinput)
        vectorinput.grid(row = 0, column = 1, rowspan = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtPanelSpace], 'HorizontalPanel', 'panelspace')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 0, column = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtPanelHeight], 'HorizontalPanel', 'panelheight')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 1, column = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

#Display 2 and 3
class EditInputDataSource(ei.EditInput):
    
    def __init__(self, parent, parenttab, section):
        if(section.upper() == lng.txtBlog.upper()):
            desc = lang[lng.txtBlog]
        elif(section.upper() == lng.txtNew.upper()):
            desc = lang[lng.txtNew]
        else:
            desc = section
        
        ei.EditInput.__init__(self, parent, parenttab, desc)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtHistorySize], section, 'historylength')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 0, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtInterval], section, 'interval')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 0, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtHarvUrl], section, 'url')
        self._subinputs.append(textinput)
        textinput.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = tki.W)

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtCacheFolder], section, 'cachedir')
        self._subinputs.append(textinput)
        textinput.grid(row = 2, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = tki.W)

#Display 3
class EditInputBottomArea(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtBottomArea])
        self.columnconfigure(0, weight = 1)
        
        colorinput =  ei.EditInputColor(self, parenttab, lang[lng.txtBgColor], 'BottomArea', 'bottomareabgcolor')
        self._subinputs.append(colorinput)
        colorinput.grid(row = 0, column = 0, rowspan = 2, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtWidthMargin], 'BottomArea', 'bottomareamarginx')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 0, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

        scalarinput =  ei.EditInputScalar(self, parenttab, lang[lng.txtBottomAreaSpace], 'BottomArea', 'yspace')
        self._subinputs.append(scalarinput)
        scalarinput.grid(row = 1, column = 1, padx = _padx, pady = _pady, sticky = tki.NSEW)

_inisubjects = 'Subjects'
_inisubject = 'subject'
_subjectlinedelimiter = '|'

class EditInputSubject(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtSubject])
        
        self._index = -1

        textinput = ei.EditInputText(self, parenttab, lang[lng.txtSubject], _inisubjects, '', width = 32)
        self._textinput = textinput
        textinput.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.W)

        imageinput =  ei.EditInputImage(self, parenttab, lang[lng.txtSubjectIcon], _inisubjects, '')
        self._imageinput = imageinput
        imageinput.grid(row = 1, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

    def setIndex(self, index):
        self._index = index
        self['text'] = ' ' + lang[lng.txtSubject] + ' ' + str(index + 1) + ' '

    def readValue(self, configparser):
        paramname = _inisubject + str(self._index + 1)
        value = configparser.get(_inisubjects, paramname)
        (desc, sep, image) = value.partition(_subjectlinedelimiter)
        self._textinput.setValue(desc)
        self._imageinput.setValue(image)

    def writeValue(self, configfilewriter):
        paramname = _inisubject + str(self._index + 1)
        desc = self._textinput.getValue()
        image = self._imageinput.getValue()
        value = desc + _subjectlinedelimiter + image
        configfilewriter.addValue(_inisubjects, paramname, value)

class SubjectPanel(scrollbox.IndexedFrame):
    def __init__(self, parent, parenttab):
        scrollbox.IndexedFrame.__init__(self, parent)
        inputsubject = EditInputSubject(self._content, parenttab)
        self._inputsubject = inputsubject
        inputsubject.grid(row = 0, column = 0)

    def update(self):
        self._inputsubject.setIndex(self.index)
        self._inputsubject._setDirty()

    def readValue(self, configparser):
        self._inputsubject.readValue(configparser)

    def writeValue(self, configfilewriter):
        self._inputsubject.writeValue(configfilewriter)

class SubjectManager(ei.EditInput):
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtSubjects])

        self._parenttab = parenttab

        self.rowconfigure(1, weight = 1)
        b = tki.Button(self, text = lang[lng.txtAddSubject], command = self._newSubject)
        b.grid(row = 0, column = 0, padx = _padx, pady = _pady, sticky = tki.NW)
        
        sb = scrollbox.Scrollbox(parenttab, self)
        self._scrollbox = sb
        sb.grid(row = 1, column = 0, padx = _padx, pady = _pady, sticky = tki.NSEW)

    def readValue(self, configparser):
        ctr = 1
        option = _inisubject + str(ctr)
        
        while(configparser.has_option(_inisubjects, option)):
            panel = self._scrollbox.getWidget(SubjectPanel, self._parenttab)
            panel.readValue(configparser)
            ctr += 1
            option = _inisubject + str(ctr)

    def writeValue(self, configfilewriter):
        for panel in self._scrollbox.widgets:
            panel.writeValue(configfilewriter)

    def _newSubject(self):
        self._scrollbox.getWidget(SubjectPanel, self._parenttab)
        self._setDirty()

class EditInputCommon3(ei.EditInput):
    
    def __init__(self, parent, parenttab):
        ei.EditInput.__init__(self, parent, parenttab, lang[lng.txtCommon])

        textinput = ei.EditInputText(self, parenttab,  lang[lng.txtLibrary], 'Common', 'library')
        self._subinputs.append(textinput)
        textinput.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.W)

        textinput = ei.EditInputText(self, parenttab,  lang[lng.txtPrinter], 'Common', 'enableprinter')
        self._subinputs.append(textinput)
        textinput.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tki.W)
