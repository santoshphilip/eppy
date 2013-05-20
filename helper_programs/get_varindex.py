# Copyright (c) 2012 Santosh Phillip

# This file is part of eplusinterface_diagrams.

# Eplusinterface_diagrams is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eplusinterface_diagrams is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eplusinterface_diagrams.  If not, see <http://www.gnu.org/licenses/>.

"""get variable index from the database
This can be used to idetify the variable index to be used in get_variableunit"""

import eplussql
import sys
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def printvarindex(fname):
    """print varindex in csv format"""
    cursor = eplussql.getcursor(fname)
    mtx = eplussql.get_varindex(cursor)
    for row in mtx:
        print "%s,%s,%s,%s" % tuple(row)
        
        
# filepath = '/Users/oompag/Dropbox/stuff/eplus' # macbook
# filepath = '/Users/santosh/Dropbox/stuff/eplus' # amore
# fname = "%s/%s" % (filepath, "00_NatVentilation10.sql")
# outname = "%s/%s" % (filepath, "00_NatVentilation10.csv")
# /Users/santosh/Dropbox/stuff/eplus/00_NatVentilation10.sql
# printvarindex(fname)  



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
                
        fname = args[0]
        printvarindex(fname)  
        
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
      