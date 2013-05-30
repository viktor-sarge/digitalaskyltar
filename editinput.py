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
from ttk import LabelFrame, Combobox
import tkFileDialog
import tkFont
import os
import os.path
import tkColorChooser
import string
from tkMessageBox import showwarning
import shutil

import spmanager as spm
import language as lng
from language import lang

_imagefiletypes = [('All files', '*'), ('bmp', '*.bmp'), ('jpeg', '*.jpeg'), ('jpg', '*.jpg'), ('png', '*.png')]

class EditInput(tki.LabelFrame):

    def __init__(self, parent, parenttab, name):
        tki.LabelFrame.__init__(self, parent, text = ' ' + name + ' ')
        self._parenttab = parenttab
        
        self._subinputs = []

    def readValue(self, configparser):
        for sub in self._subinputs:
            sub.readValue(configparser)

    def writeValue(self, configfilewriter):
        for sub in self._subinputs:
            sub.writeValue(configfilewriter)
            
    def copyImages(self):
        for sub in self._subinputs:
            sub.copyImages()        

    def _setDirty(self, dummy = None):
        self._parenttab.setDirty()

class EditInputImage(EditInput):
    
    def __init__(self, parent, parenttab, name, section, paramname):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramname = paramname
        self._value = ''
        self._imagename = tki.StringVar()
        
        l = tki.Label(self, textvariable = self._imagename)
        l.grid(row = 0, column = 0, padx = 5, pady = 5, columnspan = 2, sticky = tki.W)
        b = tki.Button(self, text = lang[lng.txtSelectImage] + '...', command = self._select)
        b.grid(row = 1, column = 0, padx = 5, pady = 5)
        b = tki.Button(self, text = lang[lng.txtPreviewImage], command = self._preview, state = tki.DISABLED)
        self._btnPrev = b
        b.grid(row = 1, column = 1, padx = 5, pady = 5)

    def readValue(self, configparser):
        self._setImage(configparser.get(self._section, self._paramname))

    def writeValue(self, configfilewriter):
        configfilewriter.addValue(self._section, self._paramname, self._value)

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._setImage(value)
        
    def copyImages(self):
        currentfolder = os.path.dirname(self._value)
        
        if(currentfolder != '' and currentfolder != self._parenttab.path):
            newname = os.path.join(self._parenttab.path, os.path.basename(self._value))
            
            try:
                shutil.copy(self._value, newname)
            except IOError:
                showwarning('Copy Error', 'Could not copy {} to {}'.format(self._value, newname))
            else:
                self._value = os.path.basename(self._value)

    def _setImage(self, filename):
        if(os.path.dirname(filename) == self._parenttab.path):
            self._value = os.path.basename(filename)
        else:
            self._value = filename

        self._imagename.set(os.path.basename(filename))
        self._btnPrev.config(state = tki.NORMAL)

    def _select(self):
        initdir = spm.spmanager.getFirstPath([spm.ImageFolder, 
                                              spm.MostRecentFolder])

        filename = tkFileDialog.askopenfilename(initialdir = initdir, filetypes = _imagefiletypes)
        
        if(filename != ''):
            self._setImage(filename)
            spm.spmanager.setPath(spm.ImageFolder, os.path.dirname(filename))
            self._setDirty()

    def _preview(self):
        if(os.path.dirname(self._value) == ''):
            namepath = os.path.join(self._parenttab.path, self._value)
        else:
            namepath = self._value

        os.startfile(namepath)

def validateNumeric(d, newvalue, maxlength, callifok):
    if(d == '0'):
        result = True
    elif(d == '1'):
        result = len(newvalue) <= maxlength and newvalue.isdigit()
    else:
        result = False
        
    if(result):
        callifok()

    return result

_maxscalarchars = 8
_x = 'x'
_y = 'y'

class EditInputVector(EditInput):

    def __init__(self, parent, parenttab, name, section, paramprefix, xname = None, yname = None):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramprefix = paramprefix
        
        if(xname is not None):
            self._xname = xname
        else:
            self._xname = self._paramprefix + _x
        
        if(yname is not None):
            self._yname = yname
        else:
            self._yname = self._paramprefix + _y

        l = tki.Label(self, text = lang[lng.txtX])
        l.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        tcmd = (self.register(self._ehOnValidateEntry), '%d', '%P')
        e = tki.Entry(self, validate = 'key', validatecommand = tcmd, width = _maxscalarchars)
        self._ex = e
        e.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = tki.W)

        l = tki.Label(self, text = lang[lng.txtY])
        l.grid(row = 2, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        tcmd = (self.register(self._ehOnValidateEntry), '%d', '%P')
        e = tki.Entry(self, validate = 'key', validatecommand = tcmd, width = _maxscalarchars)
        self._ey = e
        e.grid(row = 3, column = 0, padx = 5, pady = 2, sticky = tki.W)

    def readValue(self, configparser):
        self._ex['validate'] = tki.NONE
        self._ex.delete(0, tki.END)
        self._ex.insert(tki.END, configparser.get(self._section, self._xname))
        self._ex['validate'] = 'key'

        self._ey['validate'] = tki.NONE
        self._ey.delete(0, tki.END)
        self._ey.insert(tki.END, configparser.get(self._section, self._yname))
        self._ey['validate'] = 'key'

    def writeValue(self, configfilewriter):
        configfilewriter.addValue(self._section, self._xname, self._ex.get())
        configfilewriter.addValue(self._section, self._yname, self._ey.get())

    def _ehOnValidateEntry(self, d, newvalue):
        return validateNumeric(d, newvalue, _maxscalarchars, self._setDirty)

class EditInputScalar(EditInput):

    def __init__(self, parent, parenttab, name, section, paramname):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramname = paramname

        tcmd = (self.register(self._ehOnValidateEntry), '%d', '%P')
        e = tki.Entry(self, validate = 'key', validatecommand = tcmd, width = _maxscalarchars)
        self._evalue = e
        e.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.NW)

    def readValue(self, configparser):
        self._evalue['validate'] = tki.NONE
        self._evalue.delete(0, tki.END)
        self._evalue.insert(tki.END, configparser.get(self._section, self._paramname))
        self._evalue['validate'] = 'key'

    def writeValue(self, configfilewriter):
        configfilewriter.addValue(self._section, self._paramname, self._evalue.get())

    def _ehOnValidateEntry(self, d, newvalue):
        return validateNumeric(d, newvalue, _maxscalarchars, self._setDirty)

_textchars = 64

class EditInputText(EditInput):

    def __init__(self, parent, parenttab, name, section, paramname, width = _textchars):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramname = paramname

        e = tki.Entry(self, width = width)
        self._evalue = e
        e.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tki.NW)

    def readValue(self, configparser):
        self._evalue.delete(0, tki.END)
        self._evalue.insert(tki.END, configparser.get(self._section, self._paramname))

    def writeValue(self, configfilewriter):
        configfilewriter.addValue(self._section, self._paramname, self._evalue.get())
        
    def getValue(self):
        return self._evalue.get()

    def setValue(self, value):
        self._evalue.delete(0, tki.END)
        self._evalue.insert(tki.END, value)

_colorlength = 6
_defcolor = '#ffffff'

class EditInputColor(EditInput):
    
    def __init__(self, parent, parenttab, name, section, paramname):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramname = paramname
        self._value = ''
        self._imagename = tki.StringVar()
        
        
        self.columnconfigure(1, weight = 1)

        l = tki.Label(self, text = lang[lng.txtColor])
        l.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        f = tki.Frame(self)
        self._fcolor = f
        f.grid(row = 0, column = 1, padx = 5, pady = 2, rowspan = 2, sticky = tki.W + tki.N + tki.E + tki.S)

        tcmd = (self.register(self._ehOnValidateEntry), '%d', '%s', '%S', '%P')
        e = tki.Entry(self, width = _colorlength + 2, validate = tki.NONE, validatecommand = tcmd)
        self._ecolor = e
        e.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        b = tki.Button(self, text = lang[lng.txtSelectColor] + '...', command = self._select)
        b.grid(row = 2, column = 0, padx = 5, pady = 2, sticky = tki.W, columnspan = 2)
        
        self._setColor(_defcolor)
        self._ecolor['validate'] = 'key'

    def readValue(self, configparser):
        self._ecolor['validate'] = tki.NONE
        self._setColor(configparser.get(self._section, self._paramname))
        self._ecolor['validate'] = 'key'

    def writeValue(self, configfilewriter):
        configfilewriter.addValue(self._section, self._paramname, '#' + self._ecolor.get())

    def _ehOnValidateEntry(self, d, s, S, newvalue):
        """Event handler for validating a text input to an entry
        
        Arguments
        d -- type of action
        s -- value of entry prior to editing
        S -- the text string being inserted or deleted, if any
        newvalue -- value of the entry if the edit is allowed

        """
        print(newvalue)

        if(d == '0'):
            result = True
        elif(d == '1'):
            result = len(newvalue) <= _colorlength and all(c in string.hexdigits for c in newvalue)
        else:
            result = False

        if(result):
            if(len(newvalue) == _colorlength):
                self._fcolor['bg'] = '#' + newvalue

            self._setDirty()

        return result

    def _setColor(self, color):
        self._fcolor['bg'] = color
        dispcolor = color[1:]
        self._ecolor.delete(0, tki.END)
        self._ecolor.insert(tki.END, dispcolor)

    def _select(self):
        (rbgtuple, hexcolor) = tkColorChooser.askcolor()
        
        if(hexcolor is not None):
            self._setColor(hexcolor)
            self._setDirty()

_name = 'name'
_size = 'size'
_style = 'style'
_sizechars = 8

class EditInputFont(EditInput):
    
    def __init__(self, parent, parenttab, name, section, paramprefix):
        EditInput.__init__(self, parent, parenttab, name)
        self._section = section
        self._paramprefix = paramprefix
        
        fontlist = list(tkFont.families())
        fontlist.sort()
        self._bvb = tki.BooleanVar()
        self._bvi = tki.BooleanVar()
        self._bvs = tki.BooleanVar()
        self._bvu = tki.BooleanVar()
        
        l = tki.Label(self, text = lang[lng.txtFontsize])
        l.grid(row = 0, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        tcmd = (self.register(self._ehOnValidateEntry), '%d', '%P')
        e = tki.Entry(self, validate = 'key', validatecommand = tcmd, width = _sizechars)
        self._esize = e
        e.grid(row = 1, column = 0, padx = 5, pady = 2, sticky = tki.W)

        l = tki.Label(self, text = lang[lng.txtFontName])
        l.grid(row = 2, column = 0, padx = 5, pady = 2, sticky = tki.W)
        
        cb = Combobox(self, values = fontlist)
        self._cbfontname = cb
        cb.grid(row = 3, column = 0, padx = 5, pady = 2, sticky = tki.W)
        cb.bind('<<ComboboxSelected>>', self._setDirty)
        cb.current(0)

        cb = tki.Checkbutton(self, text = lang[lng.txtBold], onvalue = True, offvalue = False, variable = self._bvb, command = self._setDirty)
        self._cbb = cb
        cb.grid(row = 0, column = 1, padx = 5, pady = 2, sticky = tki.W)
        
        cb = tki.Checkbutton(self, text = lang[lng.txtItalics], onvalue = True, offvalue = False, variable = self._bvi, command = self._setDirty)
        self._cbi = cb
        cb.grid(row = 1, column = 1, padx = 5, pady = 2, sticky = tki.W)

        cb = tki.Checkbutton(self, text = lang[lng.txtStrikethrough], onvalue = True, offvalue = False, variable = self._bvs, command = self._setDirty)
        self._cbs = cb
        cb.grid(row = 2, column = 1, padx = 5, pady = 2, sticky = tki.W)

        cb = tki.Checkbutton(self, text = lang[lng.txtUnderline], onvalue = True, offvalue = False, variable = self._bvu, command = self._setDirty)
        self._cbu = cb
        cb.grid(row = 3, column = 1, padx = 5, pady = 2, sticky = tki.W)
        
    def readValue(self, configparser):
        name = configparser.get(self._section, self._paramprefix + _name)
        size = configparser.get(self._section, self._paramprefix + _size)
        style = configparser.get(self._section, self._paramprefix + _style)

        if(name in self._cbfontname['values']):
            self._cbfontname.set(name)
        else:
            showwarning('Unsupported Font', 'Font {} is not available on this computer'.format(name))

        if(size.isdigit()):
            self._esize['validate'] = tki.NONE
            self._esize.delete(0, tki.END)
            self._esize.insert(tki.END, size)
            self._esize['validate'] = 'key'
        else:
            showwarning('Invalid Font Size', 'Font size {} is not a valid integer'.format(size))

        self._bvb.set('b' in style)
        self._bvi.set('i' in style)
        self._bvs.set('s' in style)
        self._bvu.set('u' in style)

    def writeValue(self, configfilewriter):
        style = ''

        if(self._bvb.get()):
            style = style + 'b'
        
        if(self._bvi.get()):
            style = style + 'i'

        if(self._bvs.get()):
            style = style + 's'

        if(self._bvu.get()):
            style = style + 'u'

        configfilewriter.addValue(self._section, self._paramprefix + _name, self._cbfontname.get())
        configfilewriter.addValue(self._section, self._paramprefix + _size, self._esize.get())
        configfilewriter.addValue(self._section, self._paramprefix + _style, style)

    def _ehOnValidateEntry(self, d, newvalue):
        return validateNumeric(d, newvalue, _sizechars, self._setDirty)

    def _check(self, dummy = None):
        self._setDirty()
