"""read and write an idf file"""

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

# write 
outfile =  "../idffiles/5ZoneSupRetPlenRAB_out.idf"
open(outfile, 'w').write(str(data))

# read code
iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

# write 
outfile =  "../idffiles/V_7_0/5ZoneSupRetPlenRAB_out.idf"
open(outfile, 'w').write(str(data))