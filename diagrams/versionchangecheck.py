"""run this to see if version change affects any of the functions.
check if the name of the critical object has changed
check if field names in critical object has changed."""

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
# import utils
# 
# idd1 = "../iddfiles/Energy+V1_1.idd"
# idd2 = "../iddfiles/Energy+V6_0.idd"
# fname = "../idffiles/blank.idf"
# data1, commdct1 = readidf.readdatacommdct(fname, iddfile=idd1)
# data2, commdct2 = readidf.readdatacommdct(fname, iddfile=idd2)
# 
# key = 'plant loop'.upper()
# data1.dt[key]
# data2.dt[key]

# So a generic compare that will give a text output - showing the diffs
# do the unit testing using a small text snippet. 
# (write it out as a file, use it and delete it)

# update readdatacommdct to take file object and test.




