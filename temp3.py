"""start to work on issue #391"""

import eppy
import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs

fname = "./temp/mv_ext1.idf"
iddfile = "./temp/m_ext1.IDD"
# idf = eppy.openidf(fname, idd=iddfile)
from eppy.modeleditor import IDF


IDF.setiddname(iddfile)
idf = IDF(fname)
# idf = eppy.openidf(fname)

# wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", Name="Gumby", Optical_Data_Temperature_1=55, Window_Material_Glazing_Name_1="G1", Optical_Data_Temperature_2=56, Window_Material_Glazing_Name_2="G2")


i = idf.model.dtls.index("WindowMaterial:GlazingGroup:Thermochromic".upper())
# idf.idd_info[i]
# print(idf.idd_info[i][-4:])
# print(idf.idd_info[i])
