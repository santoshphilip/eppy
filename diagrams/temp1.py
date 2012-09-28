"""update referenced object names
this can only replace names that are object names.

need to explore how to change node names.
node names are not object names
usage:
python 
"""

import sys
import getopt
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata
import eplus_functions


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



iddfile = "../iddfiles/Energy+V6_0.idd"
block,commlst,commdct=parse_idd.extractidddata(iddfile)
theidd=eplusdata.idd(block,2)


fname = "../idffiles/a.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=theidd,
                            commdct=commdct)
idd = eplus_functions.Idd(commdct, commlst, theidd, block)
idfw = eplus_functions.IdfWrapper(data, idd)

# ---
key = 'zone'.upper()
fieldid = 1
oldname = 'SPACE1__1'
newname = 'LOBBY'

eplus_functions.rename_name(idfw, key, oldname, newname)
txt = `data`
fname = 'a.idf'
open(fname, 'w').write(txt)

        