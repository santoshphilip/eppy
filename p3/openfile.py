"""run this in ipython and explore.
Looks like idd is being read wrong."""
import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy) 

from eppy import modeleditor 
from eppy.modeleditor import IDF
iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"

IDF.setiddname(iddfile)
idf1 = IDF(fname1)
# idf1.model.dtls
print((idf1.model.dtls[:10]))

