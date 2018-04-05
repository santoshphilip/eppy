from eppy.easyopen import easyopen

iddname = "/Applications/EnergyPlus-8-7-0/Energy+.idd"
fname = "/Applications/EnergyPlus-8-8-0/ExampleFiles/1ZoneDataCenterCRAC_wPumpedDXCoolingCoil.idf"
fname = "/Applications/EnergyPlus-8-7-0/ExampleFiles/5ZoneAirCooled.idf"

fname = "/Applications/EnergyPlus-8-8-0/ExampleFiles/5ZoneAirCooledWithSlab.idf"
# fname = "a.idf"
fhandle = open(fname, 'r')

txt = "  Version,8.8;"
# txt = "Zone, gumby;"
import StringIO
fhandle = StringIO.StringIO(txt)

idf = easyopen(fhandle)
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

# idf.printidf()
day = idf.newidfobject('DAYLIGHTING:CONTROLS', Name='SPACE1-1_daylCtrl',
    Zone_Name='SPACE1-1', 
    Daylighting_Reference_Point_1_Name='SPACE1-1_DaylRefPt1',
    Fraction_of_Zone_Controlled_by_Reference_Point_1=1,
    Illuminance_Setpoint_at_Reference_Point_1=500,
    defaultvalues=False)
print(day)    
