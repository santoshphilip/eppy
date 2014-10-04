"""print steps of plant replace branch"""

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
dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
doasLoop = hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop)
airloop_idf.outputtype = 'compressed'
airloop_idf.saveas("a_branch0.idf")

n = 0
newDOASsupplyBranch = None
while newDOASsupplyBranch == None:
    n += 1
    airloop_idf = IDF(StringIO(''))
    loopname = "a_loop"
    sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
    dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
    doasLoop = hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop)
    dAirLpHvOAsys = airloop_idf.newidfobject("AirLoopHVAC:OutdoorAirSystem".upper(),
                                'DOAS_OA')
    dCoilSysDX = airloop_idf.newidfobject("CoilSystem:Cooling:DX".upper(),
                                'DOAS_CoolCoil')
    dCoilHtWtr = airloop_idf.newidfobject("Coil:Heating:Water".upper(),
                                'DOAS_HeatCoil')
    dFanCV = airloop_idf.newidfobject("Fan:ConstantVolume".upper(),
                                'DOAS_Fan')
    doasListOfComp = [dAirLpHvOAsys,dCoilSysDX,dCoilHtWtr,dFanCV]
    doasListOfComp = [dCoilSysDX,dCoilHtWtr,dFanCV]
    mainSupplyBranch = airloop_idf.getobject('BRANCH', 'sb1') # args are (key, name)

    newDOASsupplyBranch = hvacbuilder.replacebranch(airloop_idf, doasLoop, 
        mainSupplyBranch, doasListOfComp, fluid='Air',
        testing=n)

    airloop_idf.outputtype = 'compressed'
    airloop_idf.saveas("a_branch%s.idf" % (n, ))