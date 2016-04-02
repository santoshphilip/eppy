# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""sub class bunch in steps going from data, aliases, functions"""







import copy
from eppy.EPlusInterfaceFunctions import readidf
from munch import Munch as Bunch
# import eppy.bunchhelpers

class BadEPFieldError(Exception):
    """an exception"""
    pass

class RangeError(Exception):
    """an Exception"""
    pass


def somevalues(ddtt):
    """returns some values"""
    return ddtt.Name, ddtt.Construction_Name, ddtt.obj

def extendlist(lst, i, value=''):
    """extend the list so that you have i-th value"""
    if i < len(lst):
        pass
    else:
        lst.extend([value, ] * (i - len(lst) + 1))

class EpBunch_1(Bunch):
    """Has data in bunch"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch_1, self).__init__(*args, **kwargs)
        self.obj = obj
        self.objls = objls
        self.objidd = objidd
    def __setattr__(self, name, value):
        if name in ('obj', 'objls', 'objidd'):
            super(EpBunch_1, self).__setattr__(name, value)
            return None
        elif name in self['objls']:
            i = self['objls'].index(name)
            try:
                self['obj'][i] = value
            except IndexError:
                extendlist(self['obj'], i)
                self['obj'][i] = value
        else:
            astr = "unable to find field %s" % (name, )
            raise BadEPFieldError(astr)
    def __getattr__(self, name):
        if name in ('obj', 'objls', 'objidd'):
            return super(EpBunch_1, self).__getattr__(name)
        elif name in self['objls']:
            i = self['objls'].index(name)
            try:
                return self['obj'][i]
            except IndexError:
                return ''
        else:
            astr = "unable to find field %s" % (name, )
            raise BadEPFieldError(astr)
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
        astr = '\n'.join(nlines)
        return '\n%s\n' % (astr, )
    def __str__(self):
        """same as __repr__"""
        # needed if YAML is installed. See issue 67
        return self.__repr__()

class EpBunch_2(EpBunch_1):
    """Has data, aliases in bunch"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch_2, self).__init__(obj, objls, objidd, *args, **kwargs)
    def __setattr__(self, name, value):
        if name == '__aliases':
            self[name] = value
            return None
        try:
            origname = self['__aliases'][name]
            super(EpBunch_2, self).__setattr__(origname, value)
        except KeyError:
            super(EpBunch_2, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name == '__aliases':
            return super(EpBunch_2, self).__getattr__(name)
        try:
            origname = self['__aliases'][name]
            return super(EpBunch_2, self).__getattr__(origname)
        except KeyError:
            return super(EpBunch_2, self).__getattr__(name)

class EpBunch_3(EpBunch_2):
    """Has data, aliases, functions in bunch"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch_3, self).__init__(obj, objls, objidd, *args, **kwargs)
        self['__functions'] = {}
    def __setattr__(self, name, value):
        if name == '__functions':
            self[name] = value
            return None
        try:
            origname = self['__functions'][name]
            self[origname] = value
        except KeyError:
            super(EpBunch_3, self).__setattr__(name, value)
    def __getattr__(self, name):
        if name == '__functions':
            return self['__functions']
        try:
            func = self['__functions'][name]
            if isinstance(func, EpBunchFunctionClass):
                return func.func
            else:
                return func(self)
        except KeyError:
            return super(EpBunch_3, self).__getattr__(name)

class EpBunch_4(EpBunch_3):
    """h implements __getitem__ and __setitem__"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch_4, self).__init__(obj, objls, objidd, *args, **kwargs)
    def __getitem__(self, key):
        if key in ('obj', 'objls', 'objidd', '__functions', '__aliases'):
            return super(EpBunch_4, self).__getitem__(key)
        elif key in self['objls']:
            i = self['objls'].index(key)
            try:
                return self['obj'][i]
            except IndexError:
                return ''
        else:
            astr = "unknown field %s" % (key, )
            raise BadEPFieldError(astr)
    def __setitem__(self, key, value):
        if key in ('obj', 'objls', 'objidd', '__functions', '__aliases'):
            super(EpBunch_4, self).__setitem__(key, value)
            return None
        elif key in self['objls']:
            i = self['objls'].index(key)
            try:
                self['obj'][i] = value
            except IndexError:
                extendlist(self['obj'], i)
                self['obj'][i] = value

        else:
            astr = "unknown field %s" % (key, )
            raise BadEPFieldError(astr)


# TODO unit test
def fieldnames(bch):
    """field names"""
    return bch.objls

def fieldvalues(bch):
    """field values"""
    return bch.obj

class EpBunchFunctionClass(object):
    """Exception Object"""
    pass

class GetRange(EpBunchFunctionClass):
    def __init__(self, arg):
        self.bch = arg
    def func(self, fieldname):
        """get the ranges for this field"""
        bch = self.bch
        keys = ['maximum', 'minimum', 'maximum<', 'minimum>', 'type']
        index = bch.objls.index(fieldname)
        fielddct_orig = bch.objidd[index]
        fielddct = copy.deepcopy(fielddct_orig)
        therange = {}
        for key in keys:
            therange[key] = fielddct.setdefault(key, None)
        if therange['type']:
            therange['type'] = therange['type'][0]
        if therange['type'] == 'real':
            for key in keys[:-1]:
                if therange[key]:
                    therange[key] = float(therange[key][0])
        if therange['type'] == 'integer':
            for key in keys[:-1]:
                if therange[key]:
                    therange[key] = int(therange[key][0])
        return therange

class CheckRange(EpBunchFunctionClass):
    def __init__(self, arg):
        self.bch = arg
    # def init(self, arg):
    #     self.bch = arg
    def func(self, fieldname):
        """throw exception if the out of range"""
        bch = self.bch
        fieldvalue = bch[fieldname]
        therange = bch.getrange(fieldname)
        # keys = ['maximum', 'minimum', 'maximum<', 'minimum>']
        # index = bch.objls.index(fieldname)
        # fielddct = bch.objidd[index]
        if therange['maximum'] != None:
            if fieldvalue > therange['maximum']:
                astr = "Value %s is not less or equal to the 'maximum' of %s"
                astr = astr % (fieldvalue, therange['maximum'])
                raise RangeError(astr)
        if therange['minimum'] != None:
            if fieldvalue < therange['minimum']:
                astr = "Value %s is not greater or equal to the 'minimum' of %s"
                astr = astr % (fieldvalue, therange['minimum'])
                raise RangeError(astr)
        if therange['maximum<'] != None:
            if fieldvalue >= therange['maximum<']:
                astr = "Value %s is not less than the 'maximum<' of %s"
                astr = astr % (fieldvalue, therange['maximum<'])
                raise RangeError(astr)
        if  therange['minimum>'] != None:
            if fieldvalue <= therange['minimum>']:
                astr = "Value %s is not greater than the 'minimum>' of %s"
                astr = astr % (fieldvalue, therange['minimum>'])
                raise RangeError(astr)
        return fieldvalue

class EpBunch_5(EpBunch_4):
    """implements getrange, checkrange, fieldnames"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch_5, self).__init__(obj, objls, objidd, *args, **kwargs)
        self['__functions']['fieldnames'] = fieldnames
        self['__functions']['fieldvalues'] = fieldvalues
        self['__functions']['getrange'] = GetRange(self)
        self['__functions']['checkrange'] = CheckRange(self)


EpBunch = EpBunch_5

def main():
    """main function"""
    # read code
    # iddfile = "../iddfiles/Energy+V6_0.idd"
    iddfile = "./walls.idd"
    fname = "./walls.idf" # small file with only surfaces
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

    # setup code walls - can be generic for any object
    ddtt = data.dt
    dtls = data.dtls
    wall_i = dtls.index('BuildingSurface:Detailed'.upper())
    wallkey = 'BuildingSurface:Detailed'.upper()

    dwalls = ddtt[wallkey]
    dwall = dwalls[0]

    wallfields = [comm.get('field') for comm in commdct[wall_i]]
    wallfields[0] = ['key']
    wallfields = [field[0] for field in wallfields]
    wall_fields = [bunchhelpers.makefieldname(field) for field in wallfields]
    print(wall_fields[:20])

    bwall = EpBunch(dwall, wall_fields)

    print(bwall.Name)
    print(data.dt[wallkey][0][1])
    bwall.Name = 'Gumby'
    print(bwall.Name)
    print(data.dt[wallkey][0][1])
    print()

    # set aliases
    bwall.__aliases = {'Constr':'Construction_Name'}

    print("wall.Construction_Name = %s" % (bwall.Construction_Name, ))
    print("wall.Constr = %s" % (bwall.Constr, ))
    print()
    print ("change wall.Constr")
    bwall.Constr = 'AnewConstr'
    print("wall.Constr = %s" % (bwall.Constr, ))
    print("wall.Constr = %s" % (data.dt[wallkey][0][3], ))
    print()

    # add functions
    bwall.__functions = {'svalues':somevalues}

    print(bwall.svalues)
    print(bwall.__functions)



if __name__ == '__main__':
    main()

