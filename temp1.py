"""use minimal IDD"""

from eppy import modeleditor
from eppy.modeleditor import IDF
# iddfile = "./temp/Minimal.IDD"
# fname1 = "./temp/Minimal.idf"
iddfile = "./temp/mv.IDD"
fname1 = "./temp/mv.idf"

import pdb; pdb.set_trace()
IDF.setiddname(iddfile)
idf1 = IDF(fname1)
