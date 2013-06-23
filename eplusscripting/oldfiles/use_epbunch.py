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

"""use epbunch"""

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
from bunch import *
import bunchhelpers
from bunch_subclass import EpBunch_3 as EpBunch
import geometry.surface



# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

# setup code walls - can be generic for any object
dt = data.dt
dtls = data.dtls
wall_i = dtls.index('BuildingSurface:Detailed'.upper())
wallkey = 'BuildingSurface:Detailed'.upper()

dwalls = dt[wallkey]
dwall = dwalls[0]

wallfields = [comm.get('field') for comm in commdct[wall_i]]
wallfields[0] = ['key']
wallfields = [field[0] for field in wallfields]
wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]

bwall = EpBunch(dwall, wall_fields)

print wall_fields[:15]

poly = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
area = geometry.surface.area(poly)
print area