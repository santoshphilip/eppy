"""start to work on issue #391"""

import eppy
import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs

fname = "./temp/mv_ext.idf"
iddfile = "./temp/m_ext1.IDD"
# idf = eppy.openidf(fname, idd=iddfile)
from eppy.modeleditor import IDF


# from pudb import set_trace; set_trace()
IDF.setiddname(iddfile)
idf = IDF(fname)
idf.printidf()
idf.saveas("./temp/mv_ext2.idf")

# i = idf.model.dtls.index("ZoneList".upper())
# idf.idd_info[i]
# print(idf.idd_info[i][-3:])
# print(idf.idd_info[i])
