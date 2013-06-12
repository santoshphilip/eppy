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

"""get comfort from e+ sql file
Usage:
python get_comfort_lower.py fname func dbtId zonetempId 
python get_comfort_lower.py a.sql alldata 6 99
-
fname - energyplus sqlite file
func 
    hours = reutrns the total hours uncomfortable
    alldata = returns a csv file showing fill calcs (1st row=header)
dbtId - id of the outside air temperature in reports
zonetempId - id of the zone operative temperature in reports 
(find dbtId, zonetempId using get_varindex.py)

Test using:
python get_comfort_lower.py ./data/off.sql  alldata 6 100
python get_comfort_lower.py ./data/off.sql  hours 6 100
"""
import sys
import getopt


import eplussql
import comfort
import mycsv

help_message = '''
The help message goes here.
'''


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def comfort_fromsql(cursor, dbtId, tzoneId):
    """docstring for comfort_fromsql"""
    inmat = eplussql.get_manyvariables(cursor, [dbtId, tzoneId])
    outmat = comfort.comfort_matrix2(inmat, comfort.comfort_lower)
    return outmat
    
def comfort_headers(cursor, dbtId, tzoneId):
    """get the comfort matrix headers"""
    dbts = eplussql.get_variablename(cursor, dbtId)
    tzones = eplussql.get_variablename(cursor, tzoneId)
    unit = eplussql.get_variableunit(cursor, dbtId)
    header = [[dbts, tzones, 'tavgs', 'comfs', 'diffs'], [unit,] * 5]
    return header

    
def printalldata(cursor, dbtId, tzoneId):
    """print all the data in csv format"""
    outmat = comfort_fromsql(cursor, dbtId, tzoneId)
    header = comfort_headers(cursor, dbtId, tzoneId)
    houtmat = header + outmat
    for row in houtmat:
        print '%s,%s,%s,%s,%s' % tuple(row)

def printhours(cursor, dbtId, tzoneId):
    """print discomfort hours"""
    dbts = eplussql.get_variablename(cursor, dbtId)
    tzones = eplussql.get_variablename(cursor, tzoneId)
    outmat = comfort_fromsql(cursor, dbtId, tzoneId)
    diffs = [1 for row in outmat if row[-1] > 0]
    print "%s=%s, %s=%s, Discomfort_hours = %s  " % (dbtId, dbts, 
                                        tzoneId, tzones, sum(diffs))
    


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
        if len(args) == 4:
            fname, func, dbtId, zonetempId = args  
        cursor = eplussql.getcursor(fname) 
        if func == 'hours':
            printhours(cursor, dbtId, zonetempId)
        if func == 'alldata':
            printalldata(cursor, dbtId, zonetempId)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
