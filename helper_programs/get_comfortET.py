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

"""get comfort from e+ sql file
Usage:
python get_comfort sqlname etcsv func zonetempId [windinc=2 comforttype-80]
python get_comfort a.sql hawaii.csv alldata 99 [2 80]
python get_comfort a.sql hawaii.csv hours 99 [2 80]
-
sqlname - energyplus sqlite file
etcsv - csv file with outside ET* (first row is header)
func 
    hours = reutrns the total hours uncomfortable
    alldata = returns a csv file showing fill calcs (1st row=header)
zonetempId - id of the zone operative temperature in reports
- optional args [windinc comforttype]
    windinc - increase discomfort temp due to wind
    comforttype - 80% or 90% (only 80 works now)
python get_comfort fname func comforttype dbtId zonetempId
python get_comfort a.sql hours 80 6  99

Test using:
python get_comfortET.py ./data/off.sql ./data/hawaii.csv alldata 100 2 80
python get_comfortET.py ./data/off.sql ./data/hawaii.csv hours 100 2 80"""
# TODO : reduce size of above sql
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

def comfort_fromsql(cursor, etrows, tzoneId, windinc, comforttype):
    """docstring for comfort_fromsql"""
    roomtemps = eplussql.get_manyvariables(cursor, [tzoneId, ])
    inmat = [et + rm for et, rm in zip(etrows, roomtemps)]
    outmat = comfort.comfort_matrix(inmat, comfort.comfortET,
            limit=comforttype, windinc=windinc)
    return outmat
    
def comfort_headers(cursor, tzoneId):
    """get the comfort matrix headers"""
    tzones = eplussql.get_variablename(cursor, tzoneId)
    unit = eplussql.get_variableunit(cursor, tzoneId)
    header = [['ET*', tzones, 'tavgs', 'comfs', 'diffs'], [unit,] * 5]
    return header

    
def printalldata(cursor, etrows, func, zonetempId, windinc, comforttype):
    """print all the data in csv format"""
    outmat = comfort_fromsql(cursor, etrows, zonetempId, windinc, comforttype)
    header = comfort_headers(cursor, zonetempId)
    houtmat = header + outmat
    for row in houtmat:
    # for row in outmat:
        print '%s,%s,%s,%s,%s' % tuple(row)

def printhours(cursor, etrows, func, zonetempId, windinc, comforttype):
    """print discomfort hours"""
    tzones = eplussql.get_variablename(cursor, zonetempId)
    key = eplussql.get_keyvalue(cursor, zonetempId)
    outmat = comfort_fromsql(cursor, etrows, zonetempId, windinc, comforttype)
    diffs = [1 for row in outmat if row[-1] < 0]
    print "%s=%s %s, Discomfort_hours = %s  " % (zonetempId, tzones, key,
                                                        sum(diffs))

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
        if len(args) == 6:
            sqlname, etcsv, func, zonetempId, windinc, comforttype = args        
        if len(args) == 5:
            sqlname, etcsv, func, zonetempId, windinc = args  
            comforttype = 80      
        if len(args) == 4:
            sqlname, etcsv, func, zonetempId = args  
            windinc, comforttype = 2, 80  
        windinc, comforttype = float(windinc), float(comforttype)
        cursor = eplussql.getcursor(sqlname) 
        etrows = mycsv.readcsv(etcsv)
        etrows.pop(0)
        etrows = [[float(cell) for cell in row] for row in etrows]
        if func == 'hours':
            printhours(cursor, etrows, func, zonetempId, windinc, comforttype)
        if func == 'alldata':
            printalldata(cursor, etrows, func, zonetempId, windinc,
                                                                comforttype)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
