# Copyright (c) 2012 Santosh Philip

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




