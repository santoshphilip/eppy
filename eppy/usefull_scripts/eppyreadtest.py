"""script to test idf reads.
Use this to test all the files in the example folder when a new version is released"""

import sys
# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = '../../'
sys.path.append(pathnameto_eppy)

import os
from eppy.modeleditor import IDF
import eppy.simpleread as simpleread

iddfile = '/Applications/EnergyPlus-8-1-0/Energy+.idd'
folder = '/Applications/EnergyPlus-8-1-0/ExampleFiles'

lst = os.listdir(folder)
lst = [l for l in lst if l.endswith('.idf')]


iddhandle = open(iddfile, 'r')
for i, fname in enumerate(lst): # lst[6:7] 
                                # if you want to test a specific file
    fname1 = "%s/%s" % (folder, fname)
    print fname1
    idfhandle1 = open(fname1, 'rb')
    idfhandle2 = open(fname1, 'rb')

    result = simpleread.idfreadtest(iddhandle, idfhandle1, idfhandle2, verbose=True,save=True)
    print i, result,   fname
    
    idfhandle1.close()
    idfhandle2.close()
iddhandle.close()
    