"""will generate a series of files named a_loop1.idf, a_loop2.idf ...
Doing a diff between the files will show how the air loop is constructed"""

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

airloop_idf = IDF(StringIO(''))
loopname = "a_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
#sloop = ['sb0', ['sb1',], 'sb4'] # supply side of the loop
dloop = ['zone1', 'zone2', 'zone3'] # zones on the demand side
doasLoop = hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop)
# print "doasLoop", doasLoop
airloop_idf.saveas("a_loop.idf")

n = 0
doasLoop = None
while doasLoop == None:
    n += 1
    airloop_idf = IDF(StringIO(''))
    doasLoop = hvacbuilder.makeairloop(airloop_idf, loopname, sloop, dloop, testing=n)
    airloop_idf.saveas("a_loop%s.idf" % (n, ))
