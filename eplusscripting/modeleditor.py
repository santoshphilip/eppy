"""functions to edit the E+ model"""

from idfreader import makebunches
from idfreader import idfreader
from idfreader import makeabunch

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
    
def renamebunch():
    """rename this bunch and change name in all references"""
    pass
    
def addobject(bunchdt, data, commdct, key, aname=''):
    """add an object to the eplus model"""
    obj = newrawobject(data, commdct, key)
    abunch = obj2bunch(data, commdct, obj)
    namebunch(abunch, aname)
    data.dt[key].append(obj)
    bunchdt[key].append(abunch)

