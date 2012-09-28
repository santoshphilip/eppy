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
