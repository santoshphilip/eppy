"""print steps of plant replace branch"""

import sys
import os
from io import StringIO

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)


import eppy.modeleditor as modeleditor
from eppy.modeleditor import IDF
import eppy.hvacbuilder as hvacbuilder

iddfile = "../resources/iddfiles/Energy+V8_0_0.idd"
IDF.setiddname(iddfile)

idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
loopname = "p_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4'] # demand side of the loop
hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
idf.saveas("p_branch0.idf")

n = 0
newbr = None
while newbr == None:
    n += 1
    idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
    loopname = "p_loop"
    sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
    dloop = ['db0', ['db1', 'db2', 'db3'], 'db4'] # demand side of the loop
    hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
    pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')
    chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')
    pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')
    loop = idf.getobject('PLANTLOOP', 'p_loop') # args are (key, name)
    branch = idf.getobject('BRANCH', 'sb4') # args are (key, name)
    listofcomponents = [chiller, pipe1, pipe2] # the new components are connected in this order

    newbr = hvacbuilder.replacebranch1(idf, loop, branch, listofcomponents, 
        fluid='Water', debugsave=False,
        testing=n)

    idf.saveas("p_branch%s.idf" % (n, ))