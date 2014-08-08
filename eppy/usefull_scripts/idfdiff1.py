# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Eppy.  If not, see <http://www.gnu.org/licenses/>.

"""do a diff between two idf files
usage:
    python idfdiff.py idd_file idf_file1 idf_file2"""
    
    
import sys
import getopt

pathnameto_eplusscripting = "../../"
sys.path.append(pathnameto_eplusscripting)

from eppy.bunch_subclass import BadEPFieldError
from eppy.modeleditor import IDF



help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def getobjname(item):
    """return obj name or blank """
    try:
        objname = item.Name
    except BadEPFieldError, e:
        objname = ' '
    return objname


def idfdiffs(idf1, idf2):
    """print the diffs between the two idfs"""
    header = "Object Key, Object Name, Field Name, %s, %s" % (idf1.idfname, 
                                                        idf2.idfname)
    print header     
    print ''                                               
    keys = idf1.model.dtls # undocumented variable

    for akey in keys:
        idfobjs1 = idf1.idfobjects[akey]
        if idfobjs1:
            import pdb; pdb.set_trace()
        idfobjs2 = idf2.idfobjects[akey]
        idfobjs1 = [(idfobj['obj'], idfobj) for idfobj in idfobjs1]
        idfobjs2 = [(idfobj['obj'], idfobj) for idfobj in idfobjs2]
        idfobjs1.sort()
        idfobjs2.sort()
        setidf1 = set([idfobj['obj'] for idfobj in idfobjs1
                                if idfobj['obj']])
        print setidf1
        # for (k1, idfobj1), (k2, idfobj2) in zip(idfobjs1, idfobjs2):
        #     for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
        #                                                 # undocumented
        #         if f1 != f2:
        #             print '%s, %s, %s, %s, %s' % (akey, getobjname(idfobj1),
        #                 idfobj1.objidd[i]['field'][0], # uncodumented var
        #                 f1, f2, )
        # # if number of objects differ
        # if len(idfobjs1) != len(idfobjs2):
        #     if len(idfobjs1) > len(idfobjs2):
        #         for k1, item in idfobjs1[-(len(idfobjs1) - len(idfobjs2)):]:
        #             print "%s, %s,  is not in %s" % (item.key.upper(),
        #                         getobjname(item), idf2.idfname,)
        #     else:
        #         for k1, item in idfobjs2[-(len(idfobjs2) - len(idfobjs1)):]:
        #             print "%s, %s,  is not in %s" % (item.key.upper(),
        #                         getobjname(item), idf1.idfname,)
                
                
 

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "ho:v", ["help", "output="])
        except getopt.error, msg:
            raise Usage(msg)
    
        # option processing
        for option, value in opts:
            if option == "-v":
                verbose = True
            if option in ("-h", "--help"):
                raise Usage(help_message)
            if option in ("-o", "--output"):
                output = value
        iddfile, fname1, fname2 = args
        IDF.setiddname(iddfile)
        idf1 = IDF(fname1)
        idf2 = IDF(fname2)

        idfdiffs(idf1, idf2)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())


# flag duplicates
# duplicates are -> set([x for x in l if l.count(x) > 1])
# - 
# find items in one list and not the other -> use sets
# compare items that are in both lists