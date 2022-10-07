"""start to work on issue #391"""

import eppy
import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs
from io import StringIO

fname = "./temp/mv_ext3.idf"
iddfile = "./temp/m_ext1.IDD"
# idf = eppy.openidf(fname, idd=iddfile)
from eppy.modeleditor import IDF


IDF.setiddname(iddfile)
# idf = IDF(fname)
# idf = eppy.openidf(fname)

idf = IDF(StringIO(""))

# em = idf.newidfobject("EnergyManagementSystem:Program")


n = 2000
d1 = dict(Name="Gumby")
d2 = {f"Optical_Data_Temperature_{i}":i for i in range(1, n+1)}
d3 = {f"Window_Material_Glazing_Name_{i}":f"G{i}" for i in range(1, n+1)}
kwargs = dict()
kwargs.update(d1)
kwargs.update(d2)
kwargs.update(d3)
# kwargs = dict(Name="Gumby", Optical_Data_Temperature_1=55, Window_Material_Glazing_Name_1="G1", Optical_Data_Temperature_2=56, Window_Material_Glazing_Name_2="G2")

# wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", Name="Gumby", Optical_Data_Temperature_1=55, Window_Material_Glazing_Name_1="G1", Optical_Data_Temperature_2=56, Window_Material_Glazing_Name_2="G2")

wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", **kwargs)
assert wm.Optical_Data_Temperature_2000 == 2000
assert wm.Window_Material_Glazing_Name_2000 == "G2000"

# print(wm)
# i = idf.model.dtls.index("WindowMaterial:GlazingGroup:Thermochromic".upper())
# idf.idd_info[i]
# print(idf.idd_info[i][-4:])
# print(idf.idd_info[i])

# idf.printidf()
