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
from bunch_subclass import EpBunch_2 as EpBunch
import geometry.surface



# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


dt = data.dt
dtls = data.dtls

bunchdt = {}
for obj_i, key in enumerate(dtls):
    key = key.upper()
    bunchdt[key] = []
    objs = dt[key]
    for obj in objs:
        objfields = [comm.get('field') for comm in commdct[obj_i]]
        objfields[0] = ['key']
        print(key)
        print(objfields)
        objfields = [field[0] for field in objfields]
        obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
        bobj = EpBunch(obj, obj_fields)
        bunchdt[key].append(bobj)
