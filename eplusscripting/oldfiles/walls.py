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

"""do just walls in eplusinterface"""
# first cut in doing list comprehesion with walls


from bunch import *
import bunchhelpers

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # small file with only surfaces
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


print
print "number of surfaces =  %s" % (len(surfaces), )

walls = [surface for surface in surfaces if surface.Surface_Type == 'Wall']

print "number of walls = %s" % (len(walls), )
print "Wall names with construction"
print "-" * len("Wall names with construction")
for wall in walls:
    print wall.Name, wall.Construction_Name
print "-" * len("Wall names with construction")

heavywalls = [wall for wall in walls if wall.Construction_Name == 'PARTITION06']

print "number of heavy walls = %s" % (len(heavywalls), )
print "Wall names with construction"
print "-" * len("Heavy Wall names with construction")
for wall in heavywalls:
    print wall.Name, wall.Construction_Name
print "-" * len("Heavy Wall names with construction")

for heavywall in heavywalls:
    heavywall.Construction_Name = 'EXTWALL80'

print "heavy walls have been made light"
print "Wall names with construction"
print "-" * len("Wall names with construction")
for wall in walls:
    print wall.Name, wall.Construction_Name
print "-" * len("Wall names with construction")

