#!/usr/bin/python

"""
__version__ = "$Revision: 1.8 $"
__date__ = "$Date: 2005/12/17 15:20:02 $"
"""

from PythonCard import model


class Minimal(model.Background):
    def on_menuFileAbout_select(self, event):
        pass

if __name__ == '__main__':
    app = model.Application(Minimal)
    app.MainLoop()
