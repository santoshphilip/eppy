"""scripting for idfdiff.py"""

import idfdiff_functions

import sys
import getopt

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF

# python idfdiff.py ../resources/iddfiles/Energy+V7_2_0.idd 
# python idfdiff1.py ../resources/iddfiles/Energy+V7_2_0.idd f1.idf f2.idf 


iddfile = "../resources/iddfiles/Energy+V7_2_0.idd"
fname1 = "../resources/idffiles/V_7_2/box.idf"
fname2 = "../resources/idffiles/V_7_2/box_diff.idf"
fname1 = 'f1.idf'
fname2 = 'f2.idf'
IDF.setiddname(iddfile)
idf1 = IDF(fname1)
idf2 = IDF(fname2)

# - 
keys = idf1.model.dtls # undocumented variable
for akey in keys:
    idfobjs1 = idf1.idfobjects[akey]
    if idfobjs1:
        # check for dups
        names = [idfobj['obj'][1] for idfobj in idfobjs1]
        print names
        dups =  idfdiff_functions.find_duplicates(names)
        print dups
        print idfobj.keys()
        print idfobj['objls']
        print '----'
        if dups:
            print "*** Warning ***"
        for dup in dups:
            print "There  is more than one %s of %s=%s in first file" % (akey, 
                        idfobj['objls'][1], dup)
        if dups:
            print "The duplicates will be ignored"
            print '---------'

