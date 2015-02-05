"""test for p3"""

import eppy.EPlusInterfaceFunctions.parse_idd as parse_idd
import eppy.EPlusInterfaceFunctions.eplusdata as eplusdata

iddfile = "./eppy/resources/iddfiles/Energy+V8_0_0.idd"
idfname = "./eppy/resources/idffiles/V8_0_0/5ZoneSupRetPlenRAB.idf"
block,commlst,commdct=parse_idd.extractidddata(iddfile, debug='gumby')

theidd=eplusdata.idd(block,2)
data = eplusdata.eplusdata(theidd,idfname)

# print data.dtls[:5]
