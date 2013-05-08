"""dev work on using IDF class"""
import modeleditor
from modeleditor import IDF

iddfile = "../iddfiles/Energy+V7_2_0.idd"
IDF.setiddname(iddfile)

fname1 = "../idffiles/V_7_2/smallfile.idf"
idf1 = IDF(fname1)

# print idf1

fname2 = "../idffiles/V_7_2/constructions.idf"
idf2 = IDF(fname2)

# # test addidfobject
# constr = idf2.idfobjects["construction".upper()][0]
# print constr
# idf1.addidfobject(constr)
# print idf1

# # test newidfobject
idf1.newidfobject("ZONE")
idf1.printidf()
idf1.newidfobject("ZONE", "gumby")
idf1.printidf()
 
# for objname in dtls:
#     for obj in idf.idfobjects[objname]:
#         print obj
