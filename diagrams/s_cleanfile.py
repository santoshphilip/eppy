"""make a clean idf
usage:
python s_cleanfile.py fname.idf
    will make a file called fname_clean.idf"""

import getopt
import os
import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata

help_message = '''
The help message goes here.
'''

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg






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
                
        iddfile = "../iddfiles/Energy+V6_0.idd"
        fname = args[0]
        newname = '%s_clean.idf' % (os.path.splitext(fname)[0])
        block,commlst,commdct=parse_idd.extractidddata(iddfile)
        theidd=eplusdata.idd(block,2)
        data, commdct = readidf.readdatacommdct(fname, iddfile=theidd,
                                    commdct=commdct)

        txt = `data`
        open(newname, 'w').write(txt)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

