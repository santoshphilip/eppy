#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Santosh Philip on 2010-11-13.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg
        
def makeeplus(fname):
    """docstring for makeed2"""
    wfname = "weatherfile.txt"
    print fname
    #get the weather file
    wfiletxt = open(wfname, 'r') .read()
    wfile = wfiletxt.split()[0]
    #make the file rund2.bat
    s='c:\\Energyplusv6-0-0\\runeplus %s %s' % (fname, wfile)
    print s
    open("runeplus.bat", 'w').write(s)
            


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
        makeeplus(args[0])
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
