"""scripting for idfdiff.py"""

import sys
import getopt

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF

# python idfdiff.py ../resources/iddfiles/Energy+V7_2_0.idd 
# python idfdiff1.py ../resources/iddfiles/Energy+V7_2_0.idd f1.idf f2.idf 


iddfile = "../resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../resources/idffiles/V_7_2/box.idf"
fname2 = "../resources/idffiles/V_7_2/box_diff.idf"
IDF.setiddname(iddfile)
idf1 = IDF(fname1)
idf2 = IDF(fname2)
