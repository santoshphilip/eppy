"""clean file with no comments"""
from EPlusCode.EPlusInterfaceFunctions import readidf


fname = '../idffiles/a.idf'
outfile = '../idffiles/a_clean.idf'
iddfile = '../iddfiles/Energy+V6_0.idd'
data, commdct = readidf.readdatacommdct(fname, iddfile)
# - 
# move surfaces and shades    
# surfacekey = 'BuildingSurface:Detailed'.upper()
# shadekey = 'Shading:Building:Detailed'.upper()

open(outfile, 'w').write(`data`)

