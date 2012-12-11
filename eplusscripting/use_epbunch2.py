"""use epbunch"""

from EPlusInterfaceFunctions import readidf
import bunchhelpers
from bunch_subclass import EpBunch_1 as EpBunch
import iddgaps


def getobjects(bunches, key_txt):
    return [item for item in bunches[key_txt.upper()]]    


# read code
iddfile = "../iddfiles/Energy+V6_0.idd"
fname = "../idffiles/5ZoneSupRetPlenRAB.idf" # small file with only surfaces
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)

dt = data.dt
dtls = data.dtls

# fill gaps in idd
nofirstfields = iddgaps.missingkeys_standard(commdct, dtls, 
            skiplist=["TABLE:MULTIVARIABLELOOKUP"]) 
iddgaps.missingkeys_nonstandard(commdct, dtls, nofirstfields)




bunchdt = {}
for obj_i, key in enumerate(dtls):
    key = key.upper()
    bunchdt[key] = []
    objs = dt[key]
    for obj in objs:
        objfields = [comm.get('field') for comm in commdct[obj_i]]
        objfields[0] = ['key']
        objfields = [field[0] for field in objfields]
        obj_fields = [bunchhelpers.makefieldname(field) for field in objfields]
        bobj = EpBunch(obj, obj_fields)
        bunchdt[key].append(bobj)

zones = [item for item in bunchdt['zone'.upper()]]
surfaces = [item for item in bunchdt['BUILDINGSURFACE:DETAILED'.upper()]]
currentobjs = [key for key in bunchdt.keys() if len(bunchdt[key]) > 0]