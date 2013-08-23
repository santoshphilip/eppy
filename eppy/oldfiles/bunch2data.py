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

"""do just walls in eplusinterface.
Now I need to push the walls back to data"""
# first cut in doing list comprehesion with walls


from bunch import *
import bunchhelpers

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # small file with only surfaces
fname = "../idffiles/CoolingTower.idf" 
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


# setup code walls - can be generic for any object
dt = data.dt
dtls = data.dtls
wall_i = dtls.index('BuildingSurface:Detailed'.upper())
wallkey = 'BuildingSurface:Detailed'.upper()
wallfields = [comm.get('field') for comm in commdct[wall_i]]
wallfields[0] = ['key']
wallfields = [field[0] for field in wallfields]
wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]
walls = dt[wallkey]
surfaces = [Bunch(zip(wall_fields, wall)) for wall in walls]


# make key caps
for key in dtls:
    for obj in dt[key]:
        obj[0] = key
open('a.txt', 'w').write(str(data))


bunchdt = {}
for i, key in enumerate(dtls):
    fields = [comm.get('field') for comm in commdct[i]]
    fields[0] = ['key']
    ffields = []
    for field in fields:
        if field: # breaks off where there are idd gaps
            ffields.append(field[0])
    fields = ffields
    fields = [field.replace(' ', '_') for field in fields]
    tmplst = []
    bunchdt[key] = [Bunch(zip(fields, obj)) for obj in dt[key]]
    
# push bunchdt into data
for i, key in enumerate(dtls):
    fnames = [fd['field'][0] for fd in commdct[i] if fd.has_key('field')]
    fnames = [fname.replace(' ', '_') for fname in fnames]
    dataobjs = []
    for obj in bunchdt[key]:
        dtobj = [key]
        for fname in fnames:
            try:
                dtobj.append(obj[fname])
            except KeyError, e:
                break
        dataobjs.append(dtobj)
    dt[key] = dataobjs
    
    
        
open('b.txt', 'w').write(str(data))
        