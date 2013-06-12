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

"""export a list of vars to csv
---
usage:
python vars2csv.py fname var1 [var2 var3 ...]"""

import eplussql
import mycsv



import sys
import getopt


help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def vars2csv(fname, variables, convertc2f=False):
    """print the vars in csvformat"""
    matrix = []
    cursor = eplussql.getcursor(fname)
    for varindex in variables:
        varunit = eplussql.get_variableunit(cursor, varindex)
        if varunit == u'C' and convertc2f:
            func = eplussql.c2f
            varunit = u'F'
        else:
            func = None
        varlist = eplussql.get_variables(cursor, varindex, func=func)
        varname = eplussql.get_variablename(cursor, varindex)
        varkeyvalue = eplussql.get_keyvalue(cursor, varindex)
        headerandlist = [varname] + [varkeyvalue] + [varunit] + varlist
        matrix.append(headerandlist)

    matrix = mycsv.transpose2d(matrix)
    for row in matrix:
        row = [str(item) for item in row]
        print ','.join(row)

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

        fname, variables = args[0], args[1:]
        fname = '%s.sql' % (fname, )
        variables = [int(vr) for vr in variables]
        vars2csv(fname, variables, convertc2f=True)
        
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())

