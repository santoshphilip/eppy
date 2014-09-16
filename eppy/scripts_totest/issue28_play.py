"""test out issue28"""

import sys
import os
from StringIO import StringIO

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)


import eppy.modeleditor as modeleditor
from eppy.modeleditor import IDF
import eppy.hvacbuilder as hvacbuilder

iddfile = "../resources/iddfiles/Energy+V8_0_0.idd"
IDF.setiddname(iddfile)

airloop_idf = IDF(StringIO(''))
loopname = "a_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
#sloop = ['sb0', ['sb1',], 'sb4'] # supply side of the loop
dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
doasLoop = hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop)
# print "doasLoop", doasLoop
airloop_idf.saveas("a_loop.idf")


airloop_idf = IDF(StringIO(''))
loopname = "a_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
#sloop = ['sb0', ['sb1',], 'sb4'] # supply side of the loop
dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
doasLoop = hvacbuilder.makeplantloop(airloop_idf, loopname, sloop, dloop)
# print "doasLoop", doasLoop
airloop_idf.saveas("p_loop.idf")

# dAirLpHvOAsys=airloop_idf.newidfobject("AirLoopHVAC:OutdoorAirSystem".upper(),
#                             'DOAS_OA')
# dCoilSysDX = airloop_idf.newidfobject("CoilSystem:Cooling:DX".upper(),
#                             'DOAS_CoolCoil')
# dCoilHtWtr = airloop_idf.newidfobject("Coil:Heating:Water".upper(),
#                             'DOAS_HeatCoil')
# dFanCV = airloop_idf.newidfobject("Fan:ConstantVolume".upper(),
#                             'DOAS_Fan')
# doasListOfComp = [dAirLpHvOAsys,dCoilSysDX,dCoilHtWtr,dFanCV]
# doasListOfComp = [dCoilSysDX,dCoilHtWtr,dFanCV]
# mainSupplyBranch = airloop_idf.getobject('BRANCH', 'sb1') # args are (key, name)
#
# newDOASsupplyBranch = hvacbuilder.replacebranch(airloop_idf, doasLoop, mainSupplyBranch, doasListOfComp, fluid='Air')
#
# # def replacebranch(idf, loop, branch,
# #                 listofcomponents, fluid='', debugsave=False):
