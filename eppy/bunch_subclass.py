# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""sub class bunch in steps going from data, aliases, functions"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import copy
from bunch import Bunch


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


class EpBunch(Bunch):
    """Has data in bunch"""
    def __init__(self, obj, objls, objidd, *args, **kwargs):
        super(EpBunch, self).__init__(*args, **kwargs)
        self.obj = obj
        self.objls = objls
        self.objidd = objidd

    @property
    def fieldnames(self):
        """Friendly name for objls.
        """
        return self.objls

    @property
    def fieldvalues(self):
        """Friendly name for obj.
        """
        return self.obj    
    
    def checkrange(self, fieldname):
        """Check if the value for a field is within the allowed range.
        """
        cr = CheckRange(self)
        return cr.func(fieldname)
    
    def getrange(self, fieldname):
        """Get the allowed range of values for a field.
        """
        gr = GetRange(self)
        return gr.func(fieldname)
    
    def __setattr__(self, name, value):
        try:
            origname = self['__functions'][name]
            # unit test
            self[origname] = value
        except KeyError:
            pass

        try:
            name = self['__aliases'][name]
        except KeyError:
            pass

        if name in ('__functions', '__aliases'):
            self[name] = value
            return None
        elif name in ('obj', 'objls', 'objidd'):
            super(EpBunch, self).__setattr__(name, value)
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
        try:
            func = self['__functions'][name]
            if isinstance(func, EpBunchFunctionClass):
                return func.func
            else:
                return func(self)
        except KeyError:
            pass

        try:
            name = self['__aliases'][name]
        except KeyError:
            pass

        if name == '__functions':
            return self['__functions']
        elif name in ('__aliases', 'obj', 'objls', 'objidd'):
            # unit test
            return super(EpBunch, self).__getattr__(name)
        elif name in self['objls']:
            i = self['objls'].index(name)
            try:
                return self['obj'][i]
            except IndexError:
                return ''
        else:
            astr = "unable to find field %s" % (name, )
            raise BadEPFieldError(astr)
        
    def __getitem__(self, key):
        if key in ('obj', 'objls', 'objidd', '__functions', '__aliases'):
            return super(EpBunch, self).__getitem__(key)
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
            super(EpBunch, self).__setitem__(key, value)
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
        # unit test
        return self.__repr__()


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

    def func(self, fieldname):
        """throw exception if the out of range"""
        bch = self.bch
        fieldvalue = bch[fieldname]
        therange = bch.getrange(fieldname)
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
