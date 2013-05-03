"""try to import from another file"""

from idfreader import idfreader
import modeleditor

# 
from modeleditor import IDF1
IDF = IDF1

iddfile = "../iddfiles/Energy+V7_2_0.idd"
IDF.setiddname(iddfile)

fname1 = "../idffiles/V_7_2/smallfile.idf"
idf1 = IDF(fname1)

print idf1
idf1.idfobjects["VERSION"]





fname2 = "../idffiles/V_7_2/constructions.idf"
idf2 = IDF(fname2)
# # print idf1
# idfobject = idf1.idfobjects["version".upper()][0]

# print idf2.idfobjects["construction".upper()][0]
# idf1.addobject("ZONE")
# idf1.saveas('a.idf')

# # test addidfobject
# constr = idf2.idfobjects["construction".upper()][0]
# idf1.addidfobject(constr)
# print idf1

# # test newidfobject
# idf1.newidfobject("zone".upper())
# idf1.newidfobject("zone".upper(), "gumby")
# print idf1
 
# bunchdt1, data1, commdct = idfreader(fname1, iddfile)
# bunchdt2, data2, commdct = idfreader(fname2, iddfile)
# 
# cons1 = bunchdt1["Construction".upper()]
# cons2 = bunchdt2["Construction".upper()]
