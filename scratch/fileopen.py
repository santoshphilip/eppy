# Copyright (c) 2012 Santosh Philip

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

"""file open using Tkinter"""
# import sys
# sys.path.append('./PmwContribD_r2_0_2')

import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import ProgressDialog

class TkFileDialogExample(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        # define buttons
        Tkinter.Button(self, text='select idf file', command=self.askopenfilename).pack(**button_opt)

        # define options for opening or saving a file
        self.file_opt = options = {}
        options['defaultextension'] = '' # couldn't figure out how this works
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('idf file', '.idf')]
        options['initialdir'] = '~/'
        options['initialfile'] = '' #'myfile.txt'
        options['parent'] = root
        options['title'] = 'This is a title'

    def askopenfilename(self):

        """Returns an opened file in read mode.
        This time the dialog just returns a filename and the file is opened by your own code.
        """

        # get filename
        filename = tkFileDialog.askopenfilename(**self.file_opt)
        print filename
        tkMessageBox.showinfo("Say Hello", "Hello World")
        tkMessageBox.showinfo("Say Hello done", "Hello World done")
        # self.startDial()
        # open file on your own
        # if filename:
        #     return open(filename, 'r')


if __name__=='__main__':
    root = Tkinter.Tk()
    TkFileDialogExample(root).pack()
    root.mainloop()
