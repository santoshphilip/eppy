"""functions to edit the E+ model"""

from idfreader import makebunches
from idfreader import idfreader
from idfreader import makeabunch
import copy

def newrawobject(data, commdct, key):
    """make a new object for key"""
    dt = data.dt
    dtls = data.dtls
    key = key.upper()

    key_i = dtls.index(key)
    key_comm = commdct[key_i]
    obj = [comm.get('default', [''])[0] for comm in key_comm]
    obj[0] = key
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

class IDF0(object):
    iddname = None
    def __init__(self, idfname):
        # TODO use file handle instead of file name
        self.idfname = idfname
        self.read()
    @classmethod
    def setiddname(cls, arg):
        # TODO use file handle instead of filename
        if cls.iddname == None:
            cls.iddname = arg
    def read(self):
        """read the idf file"""
        # TODO unit test
        # TODO : thow an exception if iddname = None
        readout = idfreader(self.idfname, self.iddname)
        self.idfobjects, self.model, self.idd_info = readout
    def __repr__(self):
        return self.model.__repr__()
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
                            
                                    
class something(IDF0):
    """docstring for something"""
    def __init__(self, arg):
        super(something, self).__init__()
        self.arg = arg
        