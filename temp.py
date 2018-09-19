from eppy import modeleditor
from eppy.modeleditor import IDF
iddfile = "./eppy/resources/iddfiles/Energy+V7_2_0.idd"
f1 = "./eppy/resources/idffiles/V_7_2/constr.idf"
f2 = "./eppy/resources/idffiles/V_7_2/constr_diff.idf"
IDF.setiddname(iddfile)
idf1 = IDF(f1)
idf2 = IDF(f2)
from eppy.useful_scripts import idfdiff
idfdiff.idfdiffs(idf1, idf2)
