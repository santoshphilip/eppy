"""do just walls in eplusinterface"""
# first cut in doing list comprehesion with walls
# 2012-10-20: try to make aliases in the name space - DONE in BunchPlus_1
# 2012-10-21 add __aliases, __functions, __eplusvars to BunchEp as keys
# __aliases = {'Constr':'Construction_Name', ... } - DONE in BunchPlus_4
# write functions addaliases, addfunctions, initeplusvars
# put a test in addaliases for duplicates and non-existent
#
# on original read, it would be useful to convert int and floats

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
from bunch import *
import bunchhelpers

def add2(dt):
    return dt.Name, dt.Construction_Name


class BunchPlus_4(Bunch):
    def __init__(self, *args, **kwargs):
        super(BunchPlus_4, self).__init__(*args, **kwargs)
        self['__functions'] = {}
    def __setattr__(self, name, value):
        if name == '__functions':
            self[name] = value
            return None
        try:
            origname = self['__functions'][name]
            self[origname] = value
        except KeyError, e:
            self[name] = value
    def __getattr__(self, name):
        if name == '__functions':
            return super(BunchPlus, self).__getattr__(name)
        try:
            func = self['__functions'][name]
            return func(self)
        except KeyError, e:
            return super(BunchPlus, self).__getattr__(name)

BunchPlus = BunchPlus_4        

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
surfaces = [BunchPlus(zip(wall_fields, wall)) for wall in walls]

# add functions
for surface in surfaces:
    surface.__functions = {'plus':add2} 

wall = surfaces[0]
print wall.plus
print wall.__functions
# for surface in surfaces:
#     name, construction = surface.plus
#     print name, construction

