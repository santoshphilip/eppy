"""make a new node"""

from idfreader import makebunches
from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

dt = data.dt
dtls = data.dtls
key = 'zone'.upper()
zn = dt[key][0] # first zone
copyofzn = list(zn) # copies a list
dt['zone'.upper()].append(copyofzn)
bunchdt = makebunches(data, commdct) # push data into bunchdt
zones = bunchdt['zone'.upper()] # list of all the zones

key_i = dtls.index(key)
key_comm = commdct[key_i]
newnode = [comm.get('default', [''])[0] for comm in key_comm]
newnode[0] = key
