"""do a type conversion for all variables in data.dt"""
from EPlusInterfaceFunctions import readidf

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
 
def apass(a):
    return a

dt = data.dt
dtls = data.dtls
key = 'zone'.upper()
objs = dt[key]
obj = objs[0]


key_i = dtls.index(key)
key_comm = commdct[key_i]

typefunc = dict(integer=int, real=float)
types = [comm.get('type', [None])[0] for comm in key_comm]
convs = [typefunc.get(typ, apass) for typ in types]
obj = [conv(val) for val, conv in zip(obj, convs)]

