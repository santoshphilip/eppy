from eppy import modeleditor
from eppy.modeleditor import IDF
iddfile = "./somefiles/Energy+.idd"
idffile = "./somefiles/building.idf"
IDF.setiddname(iddfile)
building = IDF(idffile)
