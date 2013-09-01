"""script to work with frog Imapct"""

from eppy import modeleditor
from eppy.modeleditor import IDF
iddfile = "./eppy/resources/iddfiles/Energy+V7_2_0.idd"
fname = "/Volumes/Server/Active_Projects/FROG_all/Frog15_Impact/3_Simulation/2_Energy/EnergyPlus/37_SSFUSD_systems2/37_SSFUSD_UnconditionednoVent1.idf"
IDF.setiddname(iddfile)
idf = IDF(fname)

# idf.newidfobject("HVACTemplate:Zone:IdealLoadsAirSystem".upper())
idealkey = "HVACTemplate:Zone:IdealLoadsAirSystem".upper()
idf.newidfobject(idealkey, Zone_Name="west")

# try to copy from other idf
otherfname = "/Volumes/Server/Active_Projects/FROG_all/Frog15_Impact/3_Simulation/2_Energy/EnergyPlus/37_SSFUSD_systems2/37_SSFUSD_Furnace_IdealLoads.idf"

otheridf = IDF(otherfname)

