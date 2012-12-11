"""how to use iddgap module"""

import sys
from pprint import pprint
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
import iddgaps

iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
commdct = iddgaps.cleancommdct(commdct)

dt = data.dt
dtls = data.dtls

nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
            skiplist=["TABLE:MULTIVARIABLELOOKUP"])
            #skipping "TABLE:MULTIVARIABLELOOKUP" because I cannot figure it.
 
iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)

# key_txt = 'VERSION'
# key_txt = 'SCHEDULE:DAY:LIST'
# key_txt = 'MATERIALPROPERTY:GLAZINGSPECTRALDATA'
# key_txt = "TABLE:MULTIVARIABLELOOKUP"    
# key_i = dtls.index(key_txt.upper())
# comm = commdct[key_i]
# print comm
