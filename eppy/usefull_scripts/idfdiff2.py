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
import itertools

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
        idfobjs2 = idf2.idfobjects[akey]
        names = set([getobjname(i) for i in idfobjs1] + 
                    [getobjname(i) for i in idfobjs2])
        names = sorted(names)
        # if names:
        #     print names
        idfobjs1 = sorted(idfobjs1, key=lambda idfobj: idfobj['obj'])
        idfobjs2 = sorted(idfobjs2, key=lambda idfobj: idfobj['obj'])
        for name in names:
            n_idfobjs1 = [item for item in idfobjs1 if getobjname(item) == name]
            n_idfobjs2 = [item for item in idfobjs2 if getobjname(item) == name]
            for idfobj1, idfobj2 in itertools.izip_longest(n_idfobjs1, 
                                                          n_idfobjs2):
                if idfobj1 == None:
                    print "%s %s  is not in %s" % (idfobj2.key.upper(),
                                getobjname(idfobj2), idf1.idfname,)
                    break
                if idfobj2 == None:
                    print "%s %s  is not in %s" % (idfobj1.key.upper(),
                                getobjname(idfobj1), idf2.idfname,)
                    break

                # if idfobj1 == None or idfobj2 == None:
                #     print idfobj1
                #     print idfobj2
                #     break
                for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
                    if f1 != f2:
                        print '%s, %s, %s, %s, %s' % (akey, getobjname(idfobj1),
                            idfobj1.objidd[i]['field'][0], # uncodumented var
                            f1, f2, )
        
        # d_idfobjs1 = [(tuple(idfobj['obj'], idfobj)) for idfobj in idfobjs1]
        # d_idfobjs2 = [(tuple(idfobj['obj'], idfobj)) for idfobj in idfobjs2]

        # for (k1, idfobj1), (,idfobj2) in zip(idfobjs1, idfobjs2):
        #     for i, (f1, f2) in enumerate(zip(idfobj1.obj, idfobj2.obj)):
        #                                                 # undocumented
        #         if f1 != f2:
        #             print '%s, %s, %s, %s, %s' % (akey, getobjname(idfobj1),
        #                 idfobj1.objidd[i]['field'][0], # uncodumented var
        #                 f1, f2, )
        # # if number of objects differ
        # if len(idfobjs1) != len(idfobjs2):
        #     if len(idfobjs1) > len(idfobjs2):
        #         for item in idfobjs1[-(len(idfobjs1) - len(idfobjs2)):]:
        #             print "%s, %s,  is not in %s" % (item.key.upper(),
        #                         getobjname(item), idf2.idfname,)
        #     else:
        #         for item in idfobjs2[-(len(idfobjs2) - len(idfobjs1)):]:
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
