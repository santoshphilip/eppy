"""read a idf file and write it disk"""
ex_readwrite.py

from idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"
 
bunchdt, data, commdct = idfreader(fname, iddfile)

outfilename = "afile.idf"
txt = str(data)
open(outfilename, 'w').write(txt)
