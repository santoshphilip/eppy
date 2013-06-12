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

"""read energyplus sqlite files"""

import sqlite3
from datetime import datetime
import mycsv

class VersionMismatchError(Exception):
    pass
    
class NotHourlyError(Exception):
    pass        
    

def c2f(celsius):
    """convert celsius to fahrenheit"""
    return celsius * 1.8 + 32
    
def get_eplusversion(cursor):
    """return the E+ version from the sql file"""
    sql = "SELECT EnergyPlusVersion FROM Simulations WHERE SimulationIndex = 1"
    cursor.execute(sql)
    firstrow = list(cursor)[0][0]#firstrow = EnergyPlus 6.0.0.023, 12/14/2010 8:26 PM 
    e_version = firstrow.split(',')[0]
    justnumber = e_version.split()[-1]
    return justnumber

def getcursor(fname, eplusversion='6.0.0.023', versionresponse=None, testing=False):
    """get cursor of database file fname
    the arg testing is used in py.test"""
    conn = sqlite3.connect(fname)
    cursor = conn.cursor()
    # ====== check E+ version number. if it does not match throw exception print or ignore.
    if testing == 'skipversiontest':
        return cursor
    thisversion = get_eplusversion(cursor)
    if eplusversion <= thisversion:
        message = "this module:%s is tested for ver:%s, this is ver:%s" % (__name__, eplusversion, thisversion)
        if versionresponse == 'exception':
            raise VersionMismatchError, message
        if versionresponse == 'print':
            if not testing:
                print message
            else:
                return "printed"
        if versionresponse == None:
            if not testing:
                pass
            else:
                return None
    # end E+ version number tests
    return cursor
    
def get_wfilestart(cursor):
    """return time index where variable from weatherfile run starts"""
    if checkhourly(cursor) == False:
        raise NotHourlyError, 'All reports must be hourly for this to work'
    sql = "SELECT EnvironmentPeriodIndex, EnvironmentName FROM EnvironmentPeriods WHERE EnvironmentType = 3"
    # 3 = weather file (from E+ docs)
    cursor.execute(sql)
    matrix = [index for index, name in cursor]
    weatherfilestart = (matrix[0]-1) * 24
    return weatherfilestart

def get_variables(cursor, ReportVariableDataDictionaryIndex, func=None):
    """get the list of variables for ReportVariableDataDictionaryIndex"""
    startpoint = get_wfilestart(cursor)
    sql = "SELECT TimeIndex, VariableValue FROM ReportVariableData WHERE ReportVariableDataDictionaryIndex = %s and TimeIndex > %s" % (ReportVariableDataDictionaryIndex, startpoint, )
    cursor.execute(sql)
    matrix = [VariableValue for TimeIndex, VariableValue in cursor]
    if not func:
        return matrix
    else:
        return [func(item) for item in matrix]
        
def get_variables1(cursor, ReportVariableDataDictionaryIndex, func=None, year=2012):
    """better version of get_variables"""
    sql = "SELECT EnvironmentPeriodIndex FROM EnvironmentPeriods WHERE EnvironmentType = 3"
    cursor.execute(sql)
    rows = [row for row in cursor]
    EnvironmentPeriodIndex = rows[0][0]

    sql = "SELECT TimeIndex, Month, Day, Hour, Minute FROM Time WHERE EnvironmentPeriodIndex = 3"
    cursor.execute(sql)
    trows = [row for row in cursor]
    # find year from day in a date. ???
    starttimeindex = trows[0][0]
    endtimeindex = trows[-1][0]
    
    print starttimeindex, endtimeindex

    # ReportVariableDataDictionaryIndex = 6
    sql = "SELECT rowid, TimeIndex, VariableValue FROM ReportVariableData WHERE (TimeIndex BETWEEN %s and %s) and ReportVariableDataDictionaryIndex = %s" % (starttimeindex, endtimeindex, ReportVariableDataDictionaryIndex)
    cursor.execute(sql)
    rows = [row for row in cursor]
    TimeIndexs = [TimeIndex for rowid, TimeIndex, VariableValue in rows]
    tmes = [(year, Month, Day, Hour, Minute) for TimeIndex, Month, Day, Hour, Minute in trows if TimeIndex in TimeIndexs]
    print tmes[:10]
    rows = [(rowid, tme, VariableValue) for tme, (rowid, TimeIndex, VariableValue) in zip(tmes, rows)]
    rows = [VariableValue for rowid, tme, VariableValue in rows]
    # return rows
    if not func:
        return rows
    else:
        return [func(row) for row in rows]
    

def get_manyvariables(cursor, ReportVariableDataDictionaryIndices, 
funcs=None):
    """get a matrix of variables listed in ReportVariableDataDictionaryIndices. 
    Each column in the matrix will a different variable. 
    Each variable can be modified by the corresponding func in cunction"""
    if funcs == None:
        funcs = [None] * len(ReportVariableDataDictionaryIndices)
    thevars = []
    for ind, func in zip(ReportVariableDataDictionaryIndices, funcs):
        thevars.append(get_variables(cursor, ind, func))
    return mycsv.transpose2d(thevars)
        
    
def get_variablename(cursor, ReportVariableDataDictionaryIndex):
    """get the variable name for the ReportVariableDataDictionaryIndex"""
    sql = "SELECT VariableName FROM ReportVariableDataDictionary WHERE ReportVariableDataDictionaryIndex = %s" % (ReportVariableDataDictionaryIndex, )
    cursor.execute(sql)
    matrix = [row for row in cursor]
    return matrix[0][0]
    
def get_variableunit(cursor, ReportVariableDataDictionaryIndex):
    """get the unit for the ReportVariableDataDictionaryIndex"""
    # "SELECT VariableUnits FROM ReportVariableDataDictionary WHERE ReportVariableDataDictionaryIndex = 70"
    sql = "SELECT VariableUnits FROM ReportVariableDataDictionary WHERE ReportVariableDataDictionaryIndex = %s" % (ReportVariableDataDictionaryIndex, )
    cursor.execute(sql)
    matrix = [row for row in cursor]
    return matrix[0][0]

def get_keyvalue(cursor, ReportVariableDataDictionaryIndex):
    """get the keyvalue for the ReportVariableDataDictionaryIndex"""
    # "SELECT VariableUnits FROM ReportVariableDataDictionary WHERE ReportVariableDataDictionaryIndex = 70"
    sql = "SELECT KeyValue FROM ReportVariableDataDictionary WHERE ReportVariableDataDictionaryIndex = %s" % (ReportVariableDataDictionaryIndex, )
    cursor.execute(sql)
    matrix = [row for row in cursor]
    return matrix[0][0]
    
def checkhourly(cursor):
    """check to see that all variables are hourly"""
    sql = "SELECT ReportingFrequency FROM ReportVariableDataDictionary"
    cursor.execute(sql)  
    matrix = list(cursor)
    hourlies = [row[0] for row in matrix if row[0] == u'Hourly']
    return len(hourlies) == len(matrix)

def get_varindex(cursor):
    """get variable index from the database
    This can be used to idetify the variable index to be used in get_variableunit"""
    sql = "SELECT  ReportVariableDataDictionaryIndex, KeyValue, VariableName, VariableUnits FROM ReportVariableDataDictionary"
    cursor.execute(sql)  
    mtx = list(cursor)
    mtx1 = [list(row) for row in mtx]
    return  [['Index', 'KeyValue', 'VariableName', 'VariableUnits']] + mtx1

def outofbounds(cursor, ReportVariableDataDictionaryIndex, bound, above=True):
    """count the numeber of times the variable is out of bounds"""
    bound = float(bound)
    varlist = get_variables(cursor, ReportVariableDataDictionaryIndex)
    if above:
        out = [val for val in varlist if val > bound]
    else:
        out = [val for val in varlist if val < bound]
    return len(out)
    
    
# def testhourly(cursor):
#     """test that only hourly data is reported"""
#     sql = "SELECT ReportingFrequency FROM ReportVariableDataDictionary"
#     cursor.execute(sql)
#     fulllst = list(cursor)
#     hlst = [row for row in fulllst if row[0] == "Hourly"]
#     return len(fulllst) == len(hlst)