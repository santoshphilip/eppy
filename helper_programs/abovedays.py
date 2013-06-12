# Copyright (c) 2012 Santosh Philip

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

"""get all the values above a certain bounds
---
usage:
python above.py fname ReportVariableDataDictionaryIndex abovevalue
----
change the hard coded convertc2f value (True, False) for temperature conversion
"""

import sys
import getopt


help_message = '''
The help message goes here.
'''

import eplussql
import above_functions

fname = './eplussql_test/01gh05.sql'
varindex = 70

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg



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
                
        fname, varindex, aboveval = args
        aboveval = float(aboveval)
        varname, keyvalue, varunit, 
            daysabove = above_functions.getabovedays(fname, varindex,
                                                aboveval, convertc2f=False)
        print varname, keyvalue, varunit
        for dayhr, val in  daysabove:
            print '%s, %s' % (dayhr, val)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
