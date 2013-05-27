# Copyright (c) 2012 Santosh Phillip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""functions to edit the E+ model"""

from idfreader import makebunches
from idfreader import idfreader, idfreader1
from idfreader import makeabunch
import copy

def poptrailing(lst):
    """pop the trailing items in lst that are blank"""
    for i in range(len(lst)):
        if lst[-1] != '':
            break
        lst.pop(-1)
    return lst
    

def newrawobject(data, commdct, key):
    """make a new object for key"""
    dt = data.dt
    dtls = data.dtls
    key = key.upper()

    key_i = dtls.index(key)
    key_comm = commdct[key_i]
    obj = [comm.get('default', [''])[0] for comm in key_comm]
    obj[0] = key
    obj = poptrailing(obj) # remove the blank items in a repeating field. 
    return obj
    
def addthisbunch(data, commdct, thisbunch):
    """add a bunch to model.
    abunch usually comes from another idf file
    or it can be used to copy within the idf file"""
    # TODO unit test
    key = thisbunch.key.upper()
    obj = copy.copy(thisbunch.obj)
    data.dt[key].append(obj)
    obj2bunch(data, commdct, obj)
    
def obj2bunch(data, commdct, obj):
    """make a new bunch object using the data object"""
    dt = data.dt
    dtls = data.dtls
    key = obj[0].upper()
    key_i = dtls.index(key)
    abunch = makeabunch(commdct, obj, key_i)
    return abunch
    
def namebunch(abunch, aname):
    """give the bunch object a name, if it has a Name field"""
    if abunch.Name == None:
        pass
    else:
        abunch.Name = aname
    return abunch
    
def renamebunch(bunchdt, commdct, oldname, newname):
    """rename this bunch and change name in all references"""
    pass
    
def addobject(bunchdt, data, commdct, key, aname=''):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    namebunch(abunch, aname)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    return abunch

def getnamedargs(*args, **kwargs):
    """allows you to pass a dict and named args
    so you can pass ({'a':5, 'b':3}, c=8) and get
    dict(a=5, b=3, c=8)"""
    adict = {}
    for arg in args:
        if isinstance(arg, dict):
            adict.update(arg)
    adict.update(kwargs)
    return adict
    
def addobject1(bunchdt, data, commdct, key, *args, **kwargs):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)
    adict = getnamedargs(*args, **kwargs)
    for kkey, value in adict.iteritems():
        abunch[kkey] = value
    return abunch
    
def getobject(bunchdt, key, name):
    """get the object if you have the key and the name"""
    idfobjects = bunchdt[key]
    theobjs = [idfobj for idfobj in idfobjects if idfobj.Name == name]
    try:
        return theobjs[0]
    except IndexError, e:
        return None
    

class IDF0(object):
    iddname = None
    def __init__(self, idfname):
        self.idfname = idfname
        self.read()
    @classmethod
    def setiddname(cls, arg):
        if cls.iddname == None:
            cls.iddname = arg
            cls.idd_info = None
            cls.block = None
    @classmethod
    def setidd(cls, iddinfo, block):
        cls.idd_info = iddinfo
        cls.block = block
    def read(self):
        """read the idf file"""
        # TODO unit test
        # TODO : thow an exception if iddname = None
        readout = idfreader1(self.idfname, self.iddname,
                                commdct=self.idd_info, block=self.block)
        self.idfobjects, block, self.model, idd_info = readout
        self.__class__.setidd(idd_info, block)
    def save(self):
        # TODO unit test
        s = str(self.model)
        open(self.idfname, 'w').write(s)
    def saveas(self, filename):
        s = str(self.model)
        open(filename, 'w').write(s)

class IDF1(IDF0):
    def __init__(self, idfname):
        super(IDF1, self).__init__(idfname)
    def newidfobject(self, key, aname=''):
        """add a new idfobject to the model"""
        # TODO unit test
        return addobject(self.idfobjects,
                            self.model,
                            self.idd_info,
                            key, aname=aname)  
    def addidfobject(self, idfobject):
        """add idfobject to this model"""
        # TODO unit test
        addthisbunch(self.model,
                            self.idd_info,
                            idfobject)
    def getobject(self, key, name):
        """return the object given key and name"""
        return getobject(self.idfobjects, key, name)
      
class IDF2(IDF1):
    def __init__(self, idfname):
        super(IDF2, self).__init__(idfname)
    def idfstr(self):
        # print self.model.__repr__()
        st = ''
        dtls = self.model.dtls
        for objname in dtls:
            for obj in self.idfobjects[objname]:
                 st = st + obj.__repr__()
        return st
    def printidf(self):
        """print the idf"""
        s = self.idfstr()
        dtls = self.model.dtls
        for objname in dtls:
            for obj in self.idfobjects[objname]:
                 print obj
    # def __repr__(self):
    #     return self.model.__repr__()

IDF = IDF2
        
                                    
class something(IDF0):
    """docstring for something"""
    def __init__(self, arg):
        super(something, self).__init__()
        self.arg = arg
        
