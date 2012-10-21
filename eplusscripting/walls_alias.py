"""do just walls in eplusinterface"""
# first cut in doing list comprehesion with walls
# 2012-10-20: try to make aliases in the name space - DONE in BunchPlus_1
# 2012-10-21 add __aliases, __functions, __eplusvars to BunchEp as keys
# __aliases = {'Constr':'Construction_Name', ... } - DONE in BunchPlus_4
# write functions addaliases, addfunctions, initeplusvars
# put a test in addaliases for duplicates and non-existent


from bunch import *

class BunchPlus_1(Bunch):
    def __setattr__(self, name, value):
        if name == 'Constr':
            self['Construction_Name'] = value
        else:
            self[name] = value
    def __getattr__(self, name):
        if name == 'Constr':
            return self['Construction_Name']
        else:
            return super(BunchPlus, self).__getattr__(name)    
        
aliases = {'Constr':'Construction_Name'}
class BunchPlus_2(Bunch):
    def __setattr__(self, name, value):
        try:
            origname = aliases[name]
            self[origname] = value
        except KeyError, e:
            self[name] = value
    def __getattr__(self, name):
        try:
            origname = aliases[name]
            return self[origname]
        except KeyError, e:
            return super(BunchPlus, self).__getattr__(name)    
        
aliases = {'Constr':'Construction_Name'}

class BunchPlus_3(Bunch):
    def __setattr__(self, name, value):
        try:
            origname = aliases[name]
            self[origname] = value
        except KeyError, e:
            self[name] = value
    def __getattr__(self, name):
        try:
            origname = aliases[name]
            return self[origname]
        except KeyError, e:
            return super(BunchPlus, self).__getattr__(name)

class BunchPlus_4(Bunch):
    def __init__(self, *args, **kwargs):
        super(BunchPlus_4, self).__init__(*args, **kwargs)
        self['__aliases'] = {}
    def __setattr__(self, name, value):
        if name == '__aliases':
            self[name] = value
            return None
        try:
            origname = self['__aliases'][name]
            self[origname] = value
        except KeyError, e:
            self[name] = value
    def __getattr__(self, name):
        if name == '__aliases':
            return super(BunchPlus, self).__getattr__(name)
        try:
            origname = self['__aliases'][name]
            return self[origname]
        except KeyError, e:
            return super(BunchPlus, self).__getattr__(name)

BunchPlus = BunchPlus_4
        
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
bwalls = [BunchPlus(zip(wall_fields, wall)) for wall in walls]
for wall in bwalls:
    wall.__aliases = {'Constr':'Construction_Name'} 
surfaces = bwalls


# change all heavy walls in the project to medium walls
walls = [surface for surface in surfaces if surface.Surface_Type == 'Wall']
heavywalls = [wall for wall in walls if wall.Construction_Name == 'PARTITION06']
for heavywall in heavywalls:
    heavywall.Construction_Name = 'EXTWALL80'


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


# for w in allwalls:
#     for i in w:
#         print i
#     print '-' * 25


wall = walls[0]
print wall.Construction_Name
# print wall.Constr
wall.Constr = 'geeese'
print wall.Constr
