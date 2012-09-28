"""print zonenames"""


from EPlusCode.EPlusInterfaceFunctions import readidf
from EPlusCode import mycsv

fname = '../proposed_wholebuilding/PropClassRm_23.idf'
data, commdct = readidf.readdatacommdct(fname)
#-     
zones = data.dt['ZONE']
znames = [z[1] for z in zones]
znames.sort()
for z in znames:
    print z
