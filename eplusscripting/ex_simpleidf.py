"""use pyenergyplus to ook at a simple file"""

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_2_0.idd"
fname = "../idffiles/V_7_2/smallfile.idf"
 

model, to_print, ignorethis = idfreader(fname, iddfile)
