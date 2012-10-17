"""do just walls in eplusinterface"""
# first cut in doing list comprehesion with walls


from bunch import *

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

iddfile = "./walls.idd"
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "./walls.idf" # for supply mixer and return plenum
# fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # for supply plenum
# fname = "../idffiles/VAVSingleDuctReheat.idf" # for zone mixer
# fname = "../idffiles/06_OneStorey_Radiant_5.idf" # metrovalley
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

dt = data.dt
dtls = data.dtls
wall_i = dtls.index('BuildingSurface:Detailed'.upper())
wallkey = 'BuildingSurface:Detailed'.upper()
wallfields = [comm.get('field') for comm in commdct[wall_i]]
wallfields[0] = ['key']
# wallfields = [field[0] for field in wallfields if field !=None]
wallfields = [field[0] for field in wallfields]
wall_fields = [field.replace(' ', '_') for field in wallfields]
# wallfields[:20]
# wall_fields[:20]
walls = dt[wallkey]

wall = walls[0]
bwalls = [Bunch(zip(wall_fields, wall)) for wall in walls]


# [wall.Name for wall in bwalls]
# [wall.Construction_Name for wall in bwalls]
# [(wall.Name, wall.Construction_Name) for wall in bwalls]
# [(wall.Name, wall.Construction_Name) for wall in bwalls if wall.Surface_Type == 'Roof']
# [(wall.Name, wall.Zone_Name) for wall in bwalls]

allwalls = [[wall.Name for wall in bwalls],
[wall.Construction_Name for wall in bwalls],
[(wall.Name, wall.Construction_Name) for wall in bwalls],
[(wall.Name, wall.Construction_Name) for wall in bwalls if wall.Surface_Type == 'Roof'],
[(wall.Name, wall.Zone_Name) for wall in bwalls]]


for w in allwalls:
    for i in w:
        print i
    print '-' * 25
