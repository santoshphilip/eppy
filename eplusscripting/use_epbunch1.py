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
fname = "./walls.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)


# setup code walls - can be generic for any object
dt = data.dt
dtls = data.dtls
bunchdt = {}
for obj_i, key in dtls:
    
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