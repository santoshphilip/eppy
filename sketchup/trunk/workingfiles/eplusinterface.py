#!/usr/local/bin/python

## EPlusInterface (EPI) - An interface for EnergyPlus
## Copyright (C) 2004 Santosh Philip
##
## This file is part of EPlusInterface.
## 
## EPlusInterface is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## EPlusInterface is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with EPlusInterface; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA 
##
##
## Santosh Philip, the author of EPlusInterface, can be contacted at the following email address:
## santosh_philip AT yahoo DOT com
## Please send all bug reports, enhancement proposals, questions and comments to that address.
## 
## VERSION: 0.005

"""GUI  for eplusinterface 
- only wxPython at the moment
- future will include PyObjC for Cocoa on the Mac"""

import os

from wxPython.wx import *
import wx

import makeidf


wildcardopen = "Text File (*.txt)|*.txt|"     \
           "All files (*.*)|*.*"

wildcardsave = "EnergyPlus File (*.idf)|*.idf|"     \
           "All files (*.*)|*.*"

class MyApp(wxApp):
    def OnInit(self):
        frame = wxFrame(NULL, -1, "EPlusInterface V0.002")
        frame.Show(true)
        self.SetTopWindow(frame)
        
        dlg = wx.FileDialog(
            frame, message="Choose a file", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcardopen, style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            fname = paths[0]
            txt = open(fname, 'r').read()
            eplustxt = makeidf.makeidf(txt) 
        dlg.Destroy()
        
        dlg = wx.FileDialog(
            frame, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="", wildcard=wildcardsave, style=wx.SAVE
            )
        if dlg.ShowModal() == wx.ID_OK:
            paths = dlg.GetPaths()
            fname = paths[0]
            open(fname, 'wb').write(eplustxt)
        dlg.Destroy()
        frame.Close()

        return true

app = MyApp(0)
app.MainLoop()
