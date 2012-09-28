"""get comfort from e+ sql file
Usage:
python get_comfort_upper.py fname func dbtId zonetempId [windinc=0]
python get_comfort_upper.py a.sql alldata 6 99 [0]
-
fname - energyplus sqlite file
func 
    hours = reutrns the total hours uncomfortable
    alldata = returns a csv file showing fill calcs (1st row=header)
dbtId - id of the outside air temperature in reports
zonetempId - id of the zone operative temperature in reports 
(find dbtId, zonetempId using get_varindex.py)
- optional args [windinc]
    windinc - increase discomfort temp due to wind
Test using:
python get_comfort_upper.py ./data/off.sql  alldata 6 100 [0]
python get_comfort_upper.py ./data/off.sql  hours 6 100 [0]

for airspeed of 1m/s windinc = 2
python get_comfort_upper.py ./data/off.sql  alldata 6 100 2
python get_comfort_upper.py ./data/off.sql  hours 6 100 2
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

def comfort_fromsql(cursor, dbtId, tzoneId, windinc):
    """docstring for comfort_fromsql"""
    inmat = eplussql.get_manyvariables(cursor, [dbtId, tzoneId])
    outmat = comfort.comfort_matrix1(inmat, comfort.comfort_upper,
                                    windinc=windinc)
    return outmat
    
def comfort_headers(cursor, dbtId, tzoneId):
    """get the comfort matrix headers"""
    dbts = eplussql.get_variablename(cursor, dbtId)
    tzones = eplussql.get_variablename(cursor, tzoneId)
    unit = eplussql.get_variableunit(cursor, dbtId)
    header = [[dbts, tzones, 'tavgs', 'comfs', 'diffs'], [unit,] * 5]
    return header

    
def printalldata(cursor, dbtId, tzoneId, windinc):
    """print all the data in csv format"""
    outmat = comfort_fromsql(cursor, dbtId, tzoneId, windinc)
    header = comfort_headers(cursor, dbtId, tzoneId)
    houtmat = header + outmat
    for row in houtmat:
        print '%s,%s,%s,%s,%s' % tuple(row)

def printhours(cursor, dbtId, tzoneId, windinc):
    """print discomfort hours"""
    dbts = eplussql.get_variablename(cursor, dbtId)
    tzones = eplussql.get_variablename(cursor, tzoneId)
    outmat = comfort_fromsql(cursor, dbtId, tzoneId,  windinc)
    diffs = [1 for row in outmat if row[-1] < 0]
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
        if len(args) == 5:
            fname, func, dbtId, zonetempId, windinc = args  
        if len(args) == 4:
            fname, func, dbtId, zonetempId = args  
            windinc = 0
        windinc = float(windinc)
        cursor = eplussql.getcursor(fname) 
        if func == 'hours':
            printhours(cursor, dbtId, zonetempId, windinc)
        if func == 'alldata':
            printalldata(cursor, dbtId, zonetempId, windinc)
    
    except Usage, err:
        print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
        print >> sys.stderr, "\t for help use --help"
        return 2


if __name__ == "__main__":
    sys.exit(main())
