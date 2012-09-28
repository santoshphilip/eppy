#!/usr/bin/env python

##TUI.py - A simple Python Textual User Interface library
##Copyright (C) 2004 Christopher Rebert
##
##This program is free software; you can redistribute it and/or
##modify it under the terms of the GNU General Public License
##as published by the Free Software Foundation; either version 2
##of the License, or (at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program; if not, write to the Free Software
##Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.


#Christopher Rebert, the author of TUI.py, can be contacted at the following email address:
#krebert AT mindspring DOT com
#Please send all bug reports, enhancement proposals, questions and comments to that address.

#VERSION: 1.3

#Planned for version 1.4: TextEditor - Help needed
#                         CellSelect
#                         Tree - Help Needed
#                         Tester

#changes made by Santosh Philip
#FileDirChooser() does not work correctly ... it has been updated

import os
from sys import stderr, platform
from os import listdir, mkdir
from os.path import exists
from time import sleep
from getpass import getpass, getuser
from dircache import annotate

__author__ = 'Christopher Rebert <krebert AT mindspring DOT com>'
__license__ = 'GNU General Public License'
__version__ = 1.3

def _PrintTitleLine(Title):
    """Prints title lines.
    
    Title - Title to print a line for.

    Intended for internal use only!"""
    
    print "="*(len(Title)+3)

def RadioButtons(Prompt, DescrObjs, Prefix=None, Mid=None):
    """Asks the user to choose one option from a group.
    
    Prompt - The string the user will be prompted with. A colon is always added to its end.
    DescrObjs - A tuple containing (Description,Object) pairs.
                Description is the string that the user will see as an option.
                Object is what will be returned if the user chooses its associated Description.
                The order is significant, as the options are presented in the order that they
                appear in DescrObjs.

    Optional:
        Prefix - The string to print along with a colon, a space, and then Mid, following the
                 title line. Both or neither must be given. If neither is given, they are not
                 printed. Default is None, meaning that Prefix and Mid won't be printed.
        Mid - See Prefix. Default is None, meaning that Mid and Prefix won't be printed."""
    
    ObjDict = {}
    Prompt += ":"
    if Mid and Prefix:
        Mid = Prefix+":"+Mid
    for Num in range(len(DescrObjs)):
        ObjDict[Num+1] = DescrObjs[Num]
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        if Mid and Prefix:
            print Mid
            print
        elif not Mid and Prefix:
            raise ValueError, "Both Prefix and Mid must be given, not just one of them"
        elif Mid and not Prefix:
            raise ValueError, "Both Prefix and Mid must be given, not just one of them"
        for Num in xrange(1, len(ObjDict)+1):
            print "["+`Num`+"]", ObjDict[Num][0]
        print
        try:
            Choice = ObjDict[int(raw_input("Enter the # of your choice: "))][1]
            print
            print
            break
        except (ValueError, KeyError, IndexError):
            print
            print
    return Choice

Menu = ListBox = Buttons = Tabs = DialogBox = RadioButtons

def CheckBoxes(Prompt, DescrObjs):
    """Asks the user to choose one or more options from a group.

    Prompt - The string the user will be prompted with. A colon is always added to its end.
    DescrObjs - A tuple containing (Description,Object) pairs.
                Description is the string that the user will see as an option.
                Object is what will be returned if the user chooses its associated Description.
                The order is significant, as the options are presented in the order that they
                appear in DescrObjs."""
    
    ObjDict = {}
    Prompt += ":"
    for Num in range(len(DescrObjs)):
        ObjDict[Num+1] = DescrObjs[Num]
    del DescrObjs
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        for Num in xrange(1, len(ObjDict)+1):
            print "["+`Num`+"]", ObjDict[Num][0]
        print
        CheckList = raw_input("Enter the #s of your choices separated by commas: ").split(",")
        print
        print
        try:
            CheckList = [ObjDict[int(Check)][1] for Check in CheckList]
            CheckList.sort()
            break
        except (KeyError, ValueError):
            continue
    return CheckList

CheckList = CheckBoxes

def ComboBox(Prompt, DescrObjs):
    """Asks the user to choose an option from a group or enter one of their own.

    Prompt - The string the user will be prompted with. A colon is always added to its end.
    DescrObjs - A tuple containing (Description,Object) pairs.
                Description is a string that the user will see as an option.
                Object is what will be returned if the user chooses its associated Description.
                The order is significant, as the options are presented in the order that they
                appear in DescrObjs."""
    
    ObjDict = {}
    Prompt += ":"
    for Num in range(len(DescrObjs)):
        ObjDict[Num+1] = DescrObjs[Num]
    Custom = len(ObjDict)+1
    ObjDict[Custom] = ("Type Your Own Option in",Custom)
    
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        for Num in xrange(1, len(ObjDict)+1):
            print "["+`Num`+"]", ObjDict[Num][0]
        print
        try:
            Choice = int(raw_input("Enter the # of your choice: "))

            if Choice == Custom:
                print
                print
                Choice = TextEntry(Prompt[:-1])
                for Val in ObjDict.values():
                    if Val[0] == Choice:
                        Choice = Val[1]
                        break
            else:
                Choice = ObjDict[Choice][1]
        
        except (ValueError, KeyError, IndexError):
            pass
        print
        print
    return Choice

def SpinBox(Prompt, Mode=0, Min=None, Max=None, Mul=None, NumObjs=None):
    """Asks the user for a number.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        Mode - Determines whether to return an int or a float, depending on what its type is.
               Default is integer.
        Min - The minimum number that the user will be allowed to enter. Default is None,
              meaning that there will be no minimum number.
        Max - The maximum number that the user will be allowed to enter. Default is None,
              meaning that there will be no maximum number.
        Mul - The number that the user enters must be a multiple of this for the number to be
              accepted. Default is None, meaning that there will be no such requirement.
        NumObjs - A tuple containing (Number,Object) pairs.
                  Object will be returned if the user chooses its associated Number. Default is
                  None, meaning that the user's number itself will be returned."""
    
    if not isinstance(Mode, int) and not isinstance(Mode, float):
        raise ValueError, "Mode should be an int or float not: "+type(Mode)
    Prompt += ":"
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        print "Min:",`Min`,
        print " Max:",`Max`,
        print " Multiple of:",`Mul`
        print
        try:
            Choice = raw_input("Enter a # that meets the requirements: ")
            if isinstance(Mode, int):
                Choice = int(Choice)
            elif isinstance(Mode, float):
                Choice = float(Choice)
        except ValueError:
            print
            print
            continue
        print
        print
        if Mul != None and Choice % Mul != 0:
            continue
        if Min == None and Max == None:
            break
        elif Min == None and New <= Max:
            break
        elif Max == None and Min <= New:
            break
        elif Min <= New <= Max:
            break
        else:
            continue
    try:
        Choice = NumObjs[Choice]
    except (KeyError, TypeError):
        pass
    return Choice

Scale = SpinBox

def TextEntry(Prompt, TextObjs=None):
    """Asks the user to enter text.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        TextObjs - A tuple containing (String,Object) pairs.
                   Object will be returned if the user inputs its associated String. Default is
                   None, meaning that the user's text itself will be returned."""

    
    Prompt += ":"
    print Prompt
    _PrintTitleLine(Prompt)
    Text = raw_input("Enter text: ")
    print
    print
    if TextObjs:
        try:
            Text = TextObjs[Text]
        except KeyError:
            pass
    return Text

TextField = TextEntry

def SecureTextEntry(Prompt, TextObjs):
    """Asks the user to enter text in a secure (if possible) way.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        TextObjs - A tuple containing (String,Object) pairs.
                   Object will be returned if the user inputs its associated String. Default is
                   None, meaning that the user's text itself will be returned."""
    
    Prompt += ":"
    print Prompt
    _PrintTitleLine(Prompt)
    print "Note: The text you enter may not be displayed at all"
    print
    Text = getpass(Prompt)
    print
    print
    if TextObjs:
        try:
            Text = TextObjs[Text]
        except KeyError:
            pass
    return Text

def UserPassPrompt(Prompt):
    """Securely asks the user for a username and password.

    Prompt - The string the user will be prompted with. A colon is always added to its end."""

    print Prompt
    _PrintTitleLine(Prompt)
    print "Note: Password may not be displayed at all"
    print
    User = raw_input("Username: ")
    Pass = getpass()
    print
    print
    return User, Pass

def PassPrompt(Prompt):
    """Securely asks the user for a password.

    Prompt - The string the user will be prompted with. A colon is always added to its end."""
    
    print Prompt
    _PrintTitleLine(Prompt)
    print "Note: Password may not be displayed at all"
    print
    Pass = getpass()
    print
    print
    return Pass

def PNDialogBox(Prompt, Type="oc", Default=True, PNObjs=None):
    """Asks the user a yes/no or ok/cancel question.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        Type - 'oc' for okay/cancel options, 'yn' for yes/no options. Default is 'oc'.
        Default - Indicates whether the default answer should be in the negative or affirmative
                  depending on whether Default is true or false. Default is true.
        PNObjs - A tuple containing (Truth,Object) pairs.
                 Object will be returned if the user selects the option implying the truth
                 value Truth. Default is None, meaning that the user's truth value itself will
                 be returned."""
    
    if Type == "oc":
        if Default:
            DescrObjs = (("Okay",True), ("Cancel",False))
        else:
            DescrObjs = (("Cancel",False), ("Okay",True))
    elif Type == "yn":
        if Default:
            DescrObjs = (("Yes",True), ("No",False))
        else:
            DescrObjs = (("No",False), ("Yes",True))
    else:
        raise ValueError, "Invalid value for Type and/or Default"
    
    Choice = RadioButtons(DescrObjs)
    if PNObjs:
        Choice = PNObjs[Choice]
    return Choice

def MessageBox(Title, Msg):
    """Displays a message.

    Title - The title of the message.
    Msg - The Message to be displayed."""
    
    print Title
    _PrintTitleLine(Title)
    print Msg, "\n"
    d = raw_input("Press Enter to Acknowledge")
    print
    print

def ErrorBox(Error):
    """Displays an error message.

    Error - The error to be displayed."""
    
    print >> stderr, "Error"
    print >> stderr, "========"
    print >> stderr, Error
    print >> stderr
    d = raw_input("Press Enter to Acknowledge")
    print
    print

def AboutBox(AppName, Description, Year, Holder, Credits):
    """Displays general program information.

    AppName - The name of the application.
    Description - A description of the application.
    Year - The year(s) the application was copywritten.
    Holder - The application's copyright owner(s).
    Credits - The credits for the application."""

    if isinstance(Year, str):
        YearLen = len(Year)
    elif isinstance(Year, int):
        YearLen = len(`Year`)
    
    if len(AppName)+len(Description)+6 > YearLen+len(Holder)+15:
        TitleLineLen = len(AppName)+len(Description)+6
    else:
        TitleLineLen = YearLen+len(Holder)+18
    
    print AppName,"-",Description
    sleep(0.5)
    print "Copyright (C)", Year, Holder
    sleep(0.5)
    _PrintTitleLine(" "*TitleLineLen)
    sleep(0.5)
    for Line in Credits.split("\n"):
        print Line
        sleep(0.5)
    print
    d = raw_input("Press Enter to Acknowledge")
    print
    print

Credits = AboutBox

def Tooltip(Tip):
    """Displays a tooltip.

    Tip - The tooltip to display."""
    
    print Tip
    sleep(3)
    print
    print

Balloon = Tooltip

def ProgressBar(Title, Percent, InProgress=None):
    """Displays a progress bar.

    Title - Title of the progress bar. Three periods are automatically added to the end.
    Percent - A number 1-100 indicating what percent of the task is done.

    Optional:
        InProgress - What part of the task is currently being performed. Three periods are
                     automatically added to the end.
    """
    
    if 0 > Percent > 100:
        raise ValueError, "Percent must be between 1-100, not "+`Percent`
    Title += "..."
    print Title
    _PrintTitleLine(Title)
    _ProgressBar(Percent)
    if InProgress:
        print "Status:", InProgress+"..."
    print
    print

Meter = ProgressBar
    
def _ProgressBar(Percent):
    """Displays an individual progress bar.

    Percent - Percent to fill the progress bar to.

    Intended for internal use only."""
    
    Bars = int(round(Percent))//5
    print "["+"*"*Bars+(20-Bars)*" "+"]",`Percent`+"%",
    if Bars == 20:
        print "Done"
    else:
        print

def Bell(Prompt):
    """Displays a message to get the user's attention.

    Prompt - The prompt to alert the user with."""
    
    Border = int(round(len(Prompt)/2.0))*"*"
    HeadLine = Border+"ATTENTION"+Border
    ScrollingText(5*(HeadLine+"\n"+Prompt+"\n"))
    d = raw_input("Press Enter to Acknowledge")
    print
    print

Alert = FlashTitleBar = Bell

def ScrollingText(Text):
    """Displays some text line by line (marquee-style). (User cannot scroll)

    Text - The text to display."""
    
    for Line in [Item for Item in Text.split("\n") if Item]:
        print Line
        sleep(0.5)
    print

Ticker = ScrollingText

def ScrolledText(Prompt, Text, Lines=5):
    """Displays text that the user can scroll through. (The text cannot be edited)

    Prompt - The string the user will be prompted with. A colon is always added to its end.
    Text - The text to be displayed.

    Optional:
        Lines - The number of lines displayed per screen. Default is 5."""

    Prompt += ":"
    LineList = Text.split("\n")
    Start = 0
    if Start+Lines > len(LineList):
        Lines = len(LineList)
    
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        
        if Start > len(LineList):
            Start = Start-len(LineList)-1
        elif Start < 0:
            Start = 0
        
        if len(LineList) > Start+Lines:
            for Slice in range(Start, Start+Lines):
                print LineList[Slice]
        else:
            for Slice in range(Start,len(LineList)):
                print LineList[Slice]

        print
        d = raw_input("Press Enter to Acknowledge")
        print
        print
        Start = RadioButtons("Choose an action",( ("Scroll Up One Screen",Start-Lines),
                                                  ("Scroll Down One Screen",Start+Lines),
                                                  ("Scroll Up One Line", Start-1),
                                                  ("Scroll Down One Line",Start+1),
                                                  ("Scroll to a Line by Line #", "n"),
                                                  ("Stop Viewing Text","e") ))
        if Start == "e":
            break
        elif Start == "n":
            Start = SpinBox("Enter line #", 1, len(LineList))-1
        if Start > len(LineList)-1:
            Start = 0
            continue
        elif Start < 0:
            Start = len(LineList)-1
            continue

def FileDirEntry(Prompt, Mode="f", Exts=()):
    """Asks the user to enter the path to a file or directory.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        Mode - 'f' or 'd' depending on whether the user is to select a file or directory.
               Default is 'f' for files.
        Exts - A tuple containing the extensions (without periods) of the types of files the
               user will be allowed to select. Default is an empty tuple for any extension."""
    
    if Mode != "f" and Mode != "d":
        raise ValueError, "Mode must be 'f' or 'd', not "+`Mode`
    Prompt += ":"
    while True:
        print Prompt
        _PrintTitleLine(Prompt)
        
        if Mode == "f":
            Prompt_ = "Enter the path to a file: "
        elif Mode == "d":
            Prompt_ = "Enter the path to a directory: "
        FileDir = raw_input(Prompt_)
        FileDir = FileDir.replace("\\","/")
        printEnvironmentError
        print
        if exists(FileDir):
            if Mode == "f" and FileDir[-1] != "/" and _FileDirNameChk(FileDir, Exts):
                try:
                    d = open(FileDir,"r")
                    d.close()
                    break
                except EnvironmentError:
                    continue
            elif Mode == "d" and FileDir[-1] == "/":
                try:
                    d = open(FileDir,"r")
                    d.close()
                    continue
                except EnvironmentError:
                    break
    return FileDir

def FileDirChooser(Prompt, Mode="f", Exts=(),startdir=os.getcwd()+'/'):
    """Asks the user to browse for a file or directory.

    Prompt - The string the user will be prompted with. A colon is always added to its end.

    Optional:
        Mode - 'f' or 'd' depending on whether the user is to select a file or directory.
               Default is 'f' for files.
        Exts - A tuple containing the extensions (without periods) of the types of files the
               user will be able to select. Default is an empty tuple for any extension."""
    
    if Mode != "f" and Mode != "d":
        raise ValueError, "Mode must be 'f' or 'd', not: "+`Mode`
    if platform.count("unix") or platform.count("linux") or platform.count("gnu")\
       or platform.count("sun"):
        Dir = startdir#~" Check if "~" works on unix
    else:
        Dir = startdir
    while True:
        Dir = Dir.replace("\\","/")
        Contents = listdir(Dir)
        annotate(Dir,Contents)
        Contents.sort()
        DescrObjs = [(Item,Item) for Item in Contents if _FileDirNameChk(Item, Exts)]
        if Dir != "/":
            DescrObjs.append(("Go Up One Directory Level",1))
        DescrObjs.append(("Create a New Subdirectory",2))
        if platform == "win32":
            DescrObjs.append(("Go to Your Desktop",3))
            DescrObjs.append(("Go to Shared Desktop",4))
            DescrObjs.append(("Go to My Documents",5))
            DescrObjs.append(("Go to C:\\",6))
            DescrObjs.append(("Go to A:\\",7))
            DescrObjs.append(("Go to Another Drive",8))
        DescrObjs.append(("Cancel",9))
        FileDir = RadioButtons(Prompt, DescrObjs, "Current Directory", Dir)
        if FileDir == 9:
            FileDir = -1
            break
        elif FileDir == 1:
            Dir = "/".join( Dir.split("/")[:-2] )+"/"
            continue
        elif FileDir == 2:
            NewDir = Dir+TextEntry("Enter a name for the new directory")+"/"
            try:
                mkdir(NewDir)
                Dir = NewDir
            except EnvironmentError:
                pass
            continue
        elif FileDir == 3:
            Dir = "/Documents and Settings/"+getuser()+"/Desktop/"
            continue
        elif FileDir == 4:
            Dir = "/Documents and Settings/All Users/Desktop/"
            continue
        elif FileDir == 5:
            Dir = "/Documents and Settings/"+getuser()+"/My Documents/"
            continue
        elif FileDir == 6:
            Dir = "C:/"
            continue
        elif FileDir == 7:
            try:
                d = listdir("A:/")
                Dir = "A:/"
            except EnvironmentError:
                pass
            continue
        elif FileDir == 8:
            NewDir = TextEntry("Enter the drive letter(s)")+":/"
            try:
                if exists(NewDir):
                    Dir = NewDir
            except WindowsError:
                pass
            continue
        elif Mode == "d" and FileDir[-1] == "/":
            Action = RadioButtons("Choose an action",( ("Browse in this Directory",1),("Select this Directory",2) ))
            if Action == 1:
                Dir = Dir+FileDir
                continue
            elif Action == 2:
                break
        elif FileDir[-1] == "/":
            Dir = Dir+FileDir
            continue
        else:
            break
    if FileDir==-1: return FileDir
    return Dir+FileDir

def _FileDirNameChk(Name, Exts):
    """Checks if a file ends in a certain extension.

    Name - Name of the file to check
    Exts - A tuple containing the allowed extensions. (Without periods)

    Intended for internal use only"""

    Status = False
    if Name[-1] == "/":
        return True
    if not Exts:
        return True
    for Extension in Exts:
        try:
            Extension = "."+Extension
            if Name[-len(Extension):] == Extension:
                Status = True
                break
        except IndexError:
            pass
    return Status

def Tips(AppName, SubtitleTips):
    """Lets the user browse through software tips.

    AppName - The name of the application to display tips for.
    SubtitleTips - A tuple containg other tuples of (Subtitle,Tip).
                   Subtitle - The title of the tip.
                   Tip - The tip itself."""
    
    Position = 0
    while True:
        print AppName, "Tips"
        _PrintTitleLine(AppName+" "*5)
        print SubtitleTips[Position][0]
        print
        print SubtitleTips[Position][1]
        print
        d = raw_input("Press Enter to Acknowledge")
        print
        print
        Action = RadioButtons("Choose an action",( ("Next Tip",1), ("Previous Tip",-1),
                                                   ("Exit",0) ))
        if Action == 1:
            Position += 1
        elif Action == -1:
            Position -= 1
        elif Action == 0:
            break
        if Position > len(SubtitleTips)-1:
            Position = 0
        elif Position < 0:
            Position = len(SubtitleTips)-1

def Help(AppName, TopicDocs, TermDefs):
    """Provides a simple user help system.
    
    AppName - Name of the application to give help for.
    TopicDocs - A tuple containing pairs of (Topic,Docs).
                Topic - A help topic.
                Docs - Documentation on Topic's topic.
    TermDefs - A dictionary of Term:Def.
               Term - The term.
               Def - Term's definition."""
    
    while True:
        Section = RadioButtons(AppName+" Help System",( ("Contents",1),("Index",2),("Search",3),
                                              ("Exit Help",-1) ))
        if Section == 1:
            _HelpContents(AppName, TopicDocs)
        elif Section == 2:
            _HelpIndex(AppName, TermDefs)
        elif Section == 3:
            _HelpSearch(AppName, TermDefs)
        elif Section == -1:
            break
        
def _HelpContents(AppName, TopicDocs):
    """A simple help contents.

    AppName - The name of the application to display a help contents for.
    TopicDocs - A tuple containing pairs of (Topic,Docs).
                Topic - A help topic.
                Docs - Documentation on Topic's topic.
    
    Intended for internal use only."""
    
    TopicDocs = [(Entry[0],(Entry[0], Entry[1])) for Entry in TopicDocs]
    TopicDocs.append(("Return to Help Menu",-1))
    while True:
        Docs = RadioButtons(AppName+" Help Contents - Choose a topic", TopicDocs)
        if Docs == -1:
            break
        print AppName+" Help Contents"
        _PrintTitleLine(AppName+" "*14)
        print Docs[0]
        print
        print Docs[1]
        print
        d = raw_input("Press Enter to Acknowledge")
        print
        print

def _HelpIndex(AppName, TermDefs):
    """A simple help index.

    AppName - The name of the application to display a help index for.

    TermDefs - A dictionary of Term:Def.
               Term - The term.
               Def - Term's definition.
    
    Intended for internal use only"""
    
    while True:
        IndexView = [(Key,(Key, TermDefs[Key])) for Key in TermDefs]
        IndexView.append(("Return to Help Menu",-1))
        WordDef = RadioButtons(AppName+" Help Index - Choose a term", IndexView)
        if WordDef == -1:
            break
        print AppName+" Help Index"
        _PrintTitleLine(AppName+" "*11)
        print WordDef[0]
        print
        print WordDef[1]
        print
        d = raw_input("Press Enter to Acknowledge")
        print
        print

def _HelpSearch(AppName, SearchDict):
    """A simple help search.

    AppName - The name of the application to display a help index for.
    TermDefs - A dictionary of Term:Def.
               Term - The term.
               Def - Term's definition.
    
    Intended for internal use only."""
    
    while True:
        Action = RadioButtons(AppName+" Help Search - Choose an action",(
            ("Search for (a) word(s)",1),("Return to Help Menu",-1) ))
        if Action == -1:
            break
        elif Action == 1:
            Words = TextEntry("Enter search terms")
            print "Now Searching, Please Wait..."
            WordList = Words.split(" ")
            WordList = [Item for Item in WordList if Item != ""]
            Results = []
            for Word in WordList:
                Word = Word.lower()
                for Key in SearchDict.keys():
                    Key = Key.lower()
                    if Key.count(Word):
                        Results.append((Key, (Key,SearchDict[Key])))
            print
            print
            if not len(Results):
                print "Sorry, no search keys matched your terms."
                print "Try again using different words, or consult the Help Index"
                print
                d = raw_input("Press Enter to Acknowledge")
                print
                print
                continue
            TitleDoc = RadioButtons(AppName+" Help Search - Choose a search result", Results,
                                    "Search query", Words)
            print AppName+" Help Search - Result"
            _PrintTitleLine(AppName+" "*21)
            print TitleDoc[0]
            print
            print TitleDoc[1]
            print
            d = raw_input("Press Enter to Continue")
            print
            print
            continue

def Tree(Prompt, TreeLeaves):#Needs to be developed
    """Placeholder for a future tree selector."""

def TextEditor(Prompt):#Needs to be developed
    """Placeholder for a future text editor."""

def CellSelect(Prompt, Table):#Needs to be developed
    """Placeholder for a future table selection."""

if __name__ == "__main__":
    Creds = """Programmed by: Christopher Rebert
Special Thanks: GvR
                PSF
                Python Developers
                IDLE Developers
                Thomas Churm

    PYTHON POWERED!!!

Thanks for using TUI.py v1.3
Check our listing on PyPI for updates."""
    AboutBox("TUI.py", "A simple Python Textual User Interface library", 2004,
             "Christopher Rebert", Creds)
