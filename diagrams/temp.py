"""update referenced object names
this is not working in the second example I tried
this is because the key is not referenced.
-
How to deal with non-referenced name changes
- check that it is a name
- check for duplicate name (what do you do if it is a dup ?)
- check any field that is alpha and change it if it is same name
- echo a documentation. 
"""

import sys
sys.path.append('../EPlusInputcode')
from EPlusCode.EPlusInterfaceFunctions import readidf

from EPlusCode.EPlusInterfaceFunctions import parse_idd
from EPlusCode.EPlusInterfaceFunctions import eplusdata

iddfile = "../iddfiles/Energy+V6_0.idd"
block,commlst,commdct=parse_idd.extractidddata(iddfile)
theidd=eplusdata.idd(block,2)


fname = "../idffiles/a.idf"
fname = "../idffiles/06_OneStorey_Radiant_5.idf"
data, commdct = readidf.readdatacommdct(fname, iddfile=theidd,
                            commdct=commdct)
txt = `data`
fname = 'b.idf'
open(fname, 'w').write(txt)

import eplus_functions
import idd_fields

# ---
# getreferences(key, fieldid)
key = 'zone'.upper()
key = 'AirTerminal:SingleDuct:Uncontrolled'.upper()
fieldid = 1
ikey = data.dtls.index(key)
name = commdct[ikey][fieldid]['field'][0]
if name == 'Name':
    try:
        refs = commdct[ikey][fieldid]['reference']
    except KeyError, e:
        refs = []
else:
    refs = []
print refs
# return refs
# ---
# getReferenceObjectList(refs)
# if not refs:
#     return []
keys = [key  for key in data.dt.keys() if len(data.dt[key]) > 0]
ikeys = [(data.dtls.index(key), key) for key in keys]
reflist = []
for ref in refs:
    for i, key in ikeys:
        for j, comms in enumerate(commdct[i]):
            try:
                if ref == comms['object-list'][0]:
                    reflist.append((key, j))
            except KeyError, e:
                continue
# return reflist                
# ---
# newname2references(reflist, oldname, newname)
# if not reflist:
#     return None
oldname = 'SPACE1__1'
newname = 'LOBBY'
oldname = 'SPACE8-1 CB'
newname = 'SPACE8-1 Uncontrolled'
for key, fieldid in reflist:
    for obj in data.dt[key]:
        if obj[fieldid] == oldname:
            obj[fieldid] = newname
# ---
txt = `data`
fname = 'a.idf'
open(fname, 'w').write(txt)
# ---
        