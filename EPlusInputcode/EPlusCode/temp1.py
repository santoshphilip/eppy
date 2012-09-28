# usage below
from EPlusInterfaceFunctions import readidf


fname = "5ZoneDD.idf"
fname = "../HospitalLowEnergy.idf"
data, commdct = readidf.readdatacommdct(fname)
# 
# autosizeds = getautosizeds(data, commdct)
# 
# print autosizeds
