"""use epbunch"""

from EPlusInterfaceFunctions import readidf
import bunchhelpers
from bunch_subclass import EpBunch_1 as EpBunch
import iddgaps

def makeabunch(commdct, obj, obj_i):
    """make a bunch from the object"""
    objfields = [comm.get('field') for comm in commdct[obj_i]]
    objfields[0] = ['key']
    objfields = [field[0] for field in objfields]
    obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
    bobj = EpBunch(obj, obj_fields)
    return bobj

def makebunches(data, commdct):
    """make bunches with data"""
    bunchdt = {}
    dt, dtls = data.dt, data.dtls
    for obj_i, key in enumerate(dtls):
        key = key.upper()
        bunchdt[key] = []
        objs = dt[key]
        for obj in objs:
            bobj = makeabunch(commdct, obj, obj_i)
            bunchdt[key].append(bobj)
    return bunchdt

def idfreader(fname, iddfile):
    """read idf file and reutrn bunches"""
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
    # fill gaps in idd
    dt, dtls = data.dt, data.dtls
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
                skiplist=["TABLE:MULTIVARIABLELOOKUP"]) 
    iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)
    bunchdt = makebunches(data, commdct)
    return bunchdt, data, commdct

# read code
# iddfile = "../iddfiles/Energy+V6_0.idd"
# fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
# bunchdt, data, commdct = idfreader(fname, iddfile)
# 
# zones = bunchdt['zone'.upper()]
# surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()]
# currentobjs = [key for key in bunchdt.keys() if len(bunchdt[key]) > 0]
# 
# print data