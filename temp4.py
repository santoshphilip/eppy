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
idf = IDF(fname)
# idf = eppy.openidf(fname)

idf = IDF(StringIO(""))

# em = idf.newidfobject("EnergyManagementSystem:Program")


n = 2
d1 = dict(Name="Gumby")
d2 = {f"Optical_Data_Temperature_{i}":i for i in range(1, n+1)}
d3 = {f"Window_Material_Glazing_Name_{i}":f"G{i}" for i in range(1, n+1)}
kwargs = dict()
kwargs.update(d1)
kwargs.update(d2)
kwargs.update(d3)

wm = idf.newidfobject("WindowMaterial:GlazingGroup:Thermochromic", **kwargs)
print(wm)
wm.Optical_Data_Temperature_22 = 66
wm["Optical_Data_Temperature_4"] = 33
# aval = wm["Optical_Data_Temperature_18"]
# print(aval)
print(wm)



# last idd field


op = idf.newidfobject("Output:PreprocessorMessage")
op.Preprocessor_Name = "eeeahs"
# print(op)
# op.karamna = 44
# idf.printidf()
