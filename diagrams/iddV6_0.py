"""iditializes the idd version 6.0
used in unit testing to save time.
the idd file will be parsed the first time it is imported"""

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata

iddfile = "../iddfiles/Energy+V6_0.idd"
block,commlst,commdct=parse_idd.extractidddata(iddfile)
theidd=eplusdata.idd(block,2)