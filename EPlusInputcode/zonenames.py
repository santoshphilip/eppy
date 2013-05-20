# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""print zonenames"""


from EPlusCode.EPlusInterfaceFunctions import readidf
from EPlusCode import mycsv

fname = '../proposed_wholebuilding/PropClassRm_23.idf'
data, commdct = readidf.readdatacommdct(fname)
#-     
zones = data.dt['ZONE']
znames = [z[1] for z in zones]
znames.sort()
for z in znames:
    print z
