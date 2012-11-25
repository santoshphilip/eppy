"""do just walls in eplusinterface"""
# first cut in doing list comprehesion with walls


from bunch import *

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
wall_fields = [field.replace(' ', '_') for field in wallfields]
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

