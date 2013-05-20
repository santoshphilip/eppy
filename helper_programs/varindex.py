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

"""get the index of all the variables in the database:
The following data is got:
Index, KeyValue, VariableName, VariableUnits
---
usage:
python varindex.py fname
    fname suffix not needed
"""

import sys
import getopt

import eplussql


help_message = __doc__


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def printvarindex(fname):
    """print the var index"""
    cursor = eplussql.getcursor(fname)
    mtx1 = eplussql.get_varindex(cursor)
    mtx2 = [[str(item) for item in row] for row in mtx1]
    mtx3 = [','.join(row) for row in mtx2]
    for row in mtx3:
        print row
    

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
        sqlfname = "%s.sql" % (fname, )
        printvarindex(sqlfname)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
