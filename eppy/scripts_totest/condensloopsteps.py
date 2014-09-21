"""will generate a series of files named c_loop1.idf, c_loop2.idf ...
Doing a diff between the files will show how the condenser loop is constructed"""

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

idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
loopname = "c_loop"
sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4'] # supply side of the loop
dloop = ['db0', ['db1', 'db2', 'db3'], 'db4'] # demand side of the loop
hvacbuilder.makecondenserloop(idf, loopname, sloop, dloop)
idf.saveas("c_loop.idf")

# idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
# hvacbuilder.makecondenserloop1(idf, loopname, sloop, dloop)
# idf.saveas("c_loop1.idf")


n = 0
doasLoop = None
while doasLoop == None:
    n += 1
    condensloop_idf = IDF(StringIO(''))
    doasLoop = hvacbuilder.makecondenserloop1(condensloop_idf, loopname, sloop, dloop, testing=n)
    condensloop_idf.saveas("c_loop%s.idf" % (n, ))
