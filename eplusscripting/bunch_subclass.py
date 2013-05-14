"""sub class bunch in steps going from data, aliases, functions"""
# TODO : go thru with a fine tooth comb. make unit tests

import sys
from EPlusInterfaceFunctions import readidf
from bunch import *
import bunchhelpers

class BadEPFieldError(Exception):
    pass

def somevalues(dt):
    """returns some values"""
    return dt.Name, dt.Construction_Name, dt.obj
    
def extendlist(lst, i, value=''):
    """extend the list so that you have i-th value"""
    if i < len(lst):
        pass
    else:
        lst.extend([value, ] * (i - len(lst) + 1))

class EpBunch_1(Bunch):
    """Has data in bunch"""
    def __init__(self, obj, objls, *args, **kwargs):
        super(EpBunch_1, self).__init__(*args, **kwargs)
        self.obj = obj
        self.objls = objls
    def __setattr__(self, name, value):
        if name in ('obj', 'objls'):
            super(EpBunch_1, self).__setattr__(name, value)
            return None
        elif name in self['objls']:
            i = self['objls'].index(name)
            try:
                self['obj'][i] = value
            except IndexError, e:
                extendlist(self['obj'], i)
                self['obj'][i] = value
        else:
            raise BadEPFieldError
    def __getattr__(self, name):
        if name in ('obj', 'objls'):
            return super(EpBunch_1, self).__getattr__(name)
        elif name in self['objls']:
            i = self['objls'].index(name)
            try:
                return self['obj'][i]
            except IndexError, e:
                return ''
        else:
            raise BadEPFieldError
    def __repr__(self):
        """print this as an idf snippet"""
        lines = [str(val) for val in self.obj]
        comments = [comm.replace('_', ' ') for comm in self.objls]
        lines[0] = "%s," % (lines[0], ) # comma after first line
        for i, line in enumerate(lines[1:-1]):
            lines[i + 1] = '    %s,' % (line, ) # indent and comma
        lines[-1] = '    %s;' % (lines[-1], )# ';' after last line
        lines = [line.ljust(26) for line in lines] # ljsut the lines
        filler = '%s    !- %s'
        nlines = [filler % (line, comm) for line, 
            comm in zip(lines[1:], comments[1:])]# adds comments to line
        nlines.insert(0, lines[0])# first line without comment
        s = '\n'.join(nlines)
        return '\n%s\n' % (s, )

class EpBunch_2(EpBunch_1):
    """Has data, aliases in bunch"""
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
    """Has data, aliases, functions in bunch"""
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
            # return super(EpBunch_3, self).__getattr__(name)
            return self['__functions']
        try:
            func = self['__functions'][name]
            return func(self)
        except KeyError, e:
            return super(EpBunch_3, self).__getattr__(name)
            
class EpBunch_4(EpBunch_3):
    """h implements __getitem__ and __setitem__"""
    def __init__(self, obj, objls, *args, **kwargs):
        super(EpBunch_4, self).__init__(obj, objls, *args, **kwargs)
    def __getitem__(self, key):
        if key in ('obj', 'objls', '__functions', '__aliases'):
            return super(EpBunch_4, self).__getitem__(key)
        elif key in self['objls']:
            i = self['objls'].index(key)
            try:
                return self['obj'][i]
            except IndexError, e:
                return ''
        else:
            raise BadEPFieldError
    def __setitem__(self, key, value):
        if key in ('obj', 'objls', '__functions', '__aliases'):
            super(EpBunch_4, self).__setitem__(key, value)
            return None
        elif key in self['objls']:
            i = self['objls'].index(key)
            try:
                self['obj'][i] = value
            except IndexError, e:
                extendlist(self['obj'], i)
                self['obj'][i] = value
            
        else:
            raise BadEPFieldError
        
                                
        
EpBunch = EpBunch_4

def main():

    # read code
    # iddfile = "../iddfiles/Energy+V6_0.idd"
    iddfile = "./walls.idd"
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
    bwall.__functions = {'svalues':somevalues} 

    print bwall.svalues
    print bwall.__functions



if __name__ == '__main__':
    main()

