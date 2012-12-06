"""sub class bunch in steps going from data, aliases, functions"""
# TODO : go thru with a fine tooth comb. make unit tests

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf
from bunch import *
import bunchhelpers

def add2(dt):
    return dt.Name, dt.Construction_Name, dt.obj

class EpBunch_1(Bunch):
    def __init__(self, obj, objls, *args, **kwargs):
        super(EpBunch_1, self).__init__(*args, **kwargs)
        self.obj = obj
        self.objls = objls
    def __setattr__(self, name, value):
        if name == 'obj' or name == 'objls':
            super(EpBunch_1, self).__setattr__(name, value)
            return None
        else:
            if name in self['objls']:
                i = self['objls'].index(name)
                self['obj'][i] = value
    def __getattr__(self, name):
        if name == 'obj' or name == 'objls':
            return super(EpBunch_1, self).__getattr__(name)
        else:
            if name in self['objls']:
                i = self['objls'].index(name)
                return self['obj'][i]

class EpBunch_2(EpBunch_1):
    def __init__(self, obj, objls, *args, **kwargs):
        super(EpBunch_2, self).__init__(obj, objls, *args, **kwargs)
    def __setattr__(self, name, value):
        if name == '__aliases':
            self[name] = value
            return None
        try:
            origname = self['__aliases'][name]
            super(EpBunch_2, self).__setattr__(origname, value)
        except KeyError, e:
            super(EpBunch_2, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name == '__aliases':
            return super(EpBunch_2, self).__getattr__(name)
        try:
            origname = self['__aliases'][name]
            return super(EpBunch_2, self).__getattr__(origname)
        except KeyError, e:
            return super(EpBunch_2, self).__getattr__(name)
    
class EpBunch_3(EpBunch_2):
    def __init__(self, obj, objls, *args, **kwargs):
        super(EpBunch_3, self).__init__(obj, objls, *args, **kwargs)
        self['__functions'] = {}
    def __setattr__(self, name, value):
        if name == '__functions':
            self[name] = value
            return None
        try:
            origname = self['__functions'][name]
            self[origname] = value
        except KeyError, e:
            super(EpBunch_3, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name == '__functions':
            print 'it is __fnctions'
            # return super(EpBunch_3, self).__getattr__(name)
            return self['__functions']
        try:
            func = self['__functions'][name]
            return func(self)
        except KeyError, e:
            return super(EpBunch_3, self).__getattr__(name)
        
# EpBunch = EpBunch_3

def main():

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
    print wall_fields[:20]

    bwall = EpBunch(dwall, wall_fields)

    print bwall.Name
    print data.dt[wallkey][0][1]
    bwall.Name = 'Gumby'
    print bwall.Name
    print data.dt[wallkey][0][1]
    print

    # set aliases
    bwall.__aliases = {'Constr':'Construction_Name'} 

    print "wall.Construction_Name = %s" % (bwall.Construction_Name, )
    print "wall.Constr = %s" % (bwall.Constr, )
    print
    print "change wall.Constr"
    bwall.Constr = 'AnewConstr'
    print "wall.Constr = %s" % (bwall.Constr, )
    print "wall.Constr = %s" % (data.dt[wallkey][0][3], )
    print

    # add functions
    bwall.__functions = {'plus':add2} 

    print bwall.plus
    print bwall.__functions



if __name__ == '__main__':
    main()

