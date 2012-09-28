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
