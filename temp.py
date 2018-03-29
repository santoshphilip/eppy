from eppy.easyopen import easyopen

iddname = "/Applications/EnergyPlus-8-7-0/Energy+.idd"
fname = "/Applications/EnergyPlus-8-8-0/ExampleFiles/1ZoneDataCenterCRAC_wPumpedDXCoolingCoil.idf"
fname = "/Applications/EnergyPlus-8-7-0/ExampleFiles/5ZoneAirCooled.idf"

fname = "/Applications/EnergyPlus-8-8-0/ExampleFiles/5ZoneAirCooledWithSlab.idf"
# fname = "a.idf"
fhandle = open(fname, 'r')

# txt = "  Version,8.8;"
# txt = "Zone, gumby;"
# import StringIO
# fhandle = StringIO.StringIO(txt)

idf = easyopen(fname)
# print idf.iddname
# print idf.idfname
# idf.printidf()

# from eppy import modeleditor
# from eppy.modeleditor import IDF
#
# IDF.setiddname(iddname)
# import pdb
# pdb.set_trace()
# idf = IDF(fname)
