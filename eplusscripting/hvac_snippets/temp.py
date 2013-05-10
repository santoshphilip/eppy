"""py.test for hvacbuilder"""
import sys
import os
sys.path.append('../')
from modeleditor import IDF
from StringIO import StringIO

iddname = "../../iddfiles/Energy+V6_0.idd"
idfname = "h.idf"

import snippet
iddtxt = snippet.iddtxt
idftxt = snippet.idftxt

IDF.setiddname(StringIO(iddtxt))
IDF.setiddname(iddname)
idf = IDF(StringIO(idftxt))

# IDF.setiddname(StringIO(iddtxt))
idf = IDF(StringIO(idftxt))

idf.printidf()


# from modeleditor import IDF
# from StringIO import StringIO
# iddname = "../iddfiles/Energy+V6_0.idd"
# idfname = "./hvac_snippets/h.idf"
# IDF.setiddname(iddname)
# idf = IDF(idfname)
