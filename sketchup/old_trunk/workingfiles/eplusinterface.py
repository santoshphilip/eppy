# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

import os
from wxPython.wx import *
import wx
import makeidf


wildcardopen = "Text File (*.txt)|*.txt|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
           "All files (*.*)|*.*"

wildcardsave = "EnergyPlus File (*.idf)|*.idf|"     \
           "Compiled Python (*.pyc)|*.pyc|" \
           "SPAM files (*.spam)|*.spam|"    \
           "Egg file (*.egg)|*.egg|"        \
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
            # This returns a Python list of files that were selected.
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
            # This returns a Python list of files that were selected.
            paths = dlg.GetPaths()
            fname = paths[0]
            open(fname, 'wb').write(eplustxt)
        dlg.Destroy()
        frame.Close()

        return true

app = MyApp(0)
app.MainLoop()
