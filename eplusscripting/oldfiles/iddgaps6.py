# Copyright (c) 2012 Santosh Phillip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

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
