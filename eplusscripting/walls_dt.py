"""walls are directly changing the data in data.dt
bunch is pointing to data in data.dt"""
# try to get bunch to point directly to data.dt

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
from bunch import *
import bunchhelpers

class BunchPlus_5(Bunch):
    def __init__(self, obj, objls, *args, **kwargs):
        super(BunchPlus_5, self).__init__(*args, **kwargs)
        self.obj = obj
        self.objls = objls
    def __setattr__(self, name, value):
        if name == 'obj' or name == 'objls':
            super(BunchPlus_5, self).__setattr__(name, value)
            return None
        else:
            if name in self['objls']:
                i = self['objls'].index(name)
                self['obj'][i] = value
        if name == '__aliases':
            self[name] = value
            return None
        try:
            origname = self['__aliases'][name]
            if origname in self['objls']:
                i = self['objls'].index(origname)
                self['obj'][i] = value
        except KeyError, e:
            if name in self['objls']:
                i = self['objls'].index(name)
                self['obj'][i] = value
    def __getattr__(self, name):
        if name == 'obj' or name == 'objls':
            return super(BunchPlus_5, self).__getattr__(name)
        else:
            if name in self['objls']:
                i = self['objls'].index(name)
                return self['obj'][i]
        if name == '__aliases':
            return super(BunchPlus_5, self).__getattr__(name)
        try:
            origname = self['__aliases'][name]
            i = self['objls'].index(origname)
            return self['obj'][i]
        except KeyError, e:
            return super(BunchPlus_5, self).__getattr__(name)


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
print wall_fields[:10]

bwall = BunchPlus_5(dwall, wall_fields)
bwall.__aliases = {'Constr':'Construction_Name', 
    'zonename':'Zone_Name',
    'afunc':'thisfunc'} 

print bwall.Name
bwall.Name = 'Gumby'
print bwall.Name
print bwall.obj

open('a.txt', 'w').write(str(data))
print "see a.txt for changed idf"

print bwall.zonename
print bwall.Constr
bwall.Constr = "Cotton Ball"
print bwall.Constr
def thisfunc():
    print 'you are in thisfunc'
bwall.afunc