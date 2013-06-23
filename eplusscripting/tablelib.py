"""routines to deal with tables in the html output files of E+
Should contain only routines that deal with html"""

# Copyright (C) 2009 Santosh Philip
# This file is part of tablediff.
# 
# tablediff is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# tablediff is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with tablediff.  If not, see <http://www.gnu.org/licenses/>.

from bs4 import BeautifulSoup, NavigableString, Tag

def nestedtable(table):
    """test if the table has nested tables"""
    if table.table.table == None:
        return False
    else:
        return True

class NotSimpleTable(Exception):
    pass
        

def is_simpletable(table):
    """test if the table has only strings in the cells"""
    tds = table('td')
    for td in tds:
        if td.contents != []:
            if len(td.contents) == 1:
                if not isinstance(td.contents[0], NavigableString):
                    return False
            else:
                return False
    return True

def table2matrix(table):
    """convert a table to a list of lists - a 2D matrix"""
    if not is_simpletable(table):
        raise NotSimpleTable, "Not able read a cell in the table as a string"
    rows = []
    for tr in table('tr'):
        row = []
        for td in tr('td'):
            try:
                row.append(td.contents[0])
            except IndexError, e:
                row.append('')
        rows.append(row)
    return rows

#=============================
# matrix operations

def equal_matrixsize(mat1, mat2):
    """return true if the mat1 and mat2 have same configuration of cells"""
    if mat1 == mat2: return True 
    if len(mat1) == len(mat2):
        for i in range(len(mat1)):
            if len(mat1[i]) == len(mat2[i]):
                pass
            else:
                return False
    else:
        return False
    return True


def gettables(soupbody):
    """from soupbody get all the tables"""
    body = soupbody
    tables = []        
    for obj in body.contents:
        try:
            if obj.name == 'table':
                tables.append(obj)
        except AttributeError, e:
            pass
    return tables
    

def flattenkey(btabledct):
    """flattens the key by bringing the header one level down into next dct"""
    decdct= {}
    for boldkey in btabledct.keys():
        for gridkey in btabledct[boldkey].keys():
            lst = [boldkey] + list(gridkey)
            newkey = tuple(lst)
            decdct[newkey] = btabledct[boldkey][gridkey]
    return decdct    

def bigsmallequal((value, isdiff)):
    """test if the value is big, small or equal, or None"""
    if isdiff == True:
        return 'big'
    if isdiff == False:
        try:
            anum = float(value)
            if anum != 0:
                return 'small'
            else:
                return 'equal'
        except ValueError, e:
            return None

def matrix2table3(table, mat, theformat='%s'):
    # TODO : unit test needed for this function
    """pushes the matrix into the table
    The matrix and table dimensions have to match. No checks are done
    returns a dictionary: {'big':n1, 'small':n2, 'equal':n3, None:n4} n1,n2.. are the sums
    The table is changed in place"""
    # TODO - test that table and matrix dimensions match
    # TODO - test that there are no nested tables
    thesum = {'big':0, 'small':0, 'equal':0, None:0, 'table_size_error':0}
    flat = []
    for row in mat:
        flat = flat + row
    alltds = table.findAll('td')
    for old, new in zip(alltds, flat):
        valuetype = bigsmallequal(new)
        thesum[valuetype] += 1 
        if valuetype:
            old['class'] = valuetype
        try:
            if isinstance(new[0], tuple):
                newval = '%s vs %s' % (new[0][0], new[0][1])
            else:
                newval = new[0]
                if valuetype != None:
                    newval = theformat % (newval,)                    
            old.contents[0].replaceWith(unicode(newval))
        except IndexError, e: # no contents to replace
            pass 
    return thesum           

def error2table(table):
    """pushes the table_size_error into the table
    The matrix and table dimensions have to match. No checks are done
    returns a dictionary: {'big':0, 'small':0, 'equal':0, None:0, 'table_size_error':1}
    The table is changed in place"""
    valuetype = 'table_size_error'
    thesum = {'big':0, 'small':0, 'equal':0, None:0, 'table_size_error':1}
    alltds = table.findAll('td')
    for td in alltds:
        td['class'] = valuetype
        try:
            td.contents[0].replaceWith(unicode(valuetype))
        except IndexError, e: # no contents to replace
            pass 
    # put in error message
    parent = table.parent
    index = parent.contents.index(table)
    themessage = 'table_size_error = The size of the tables in the files do not match'
    parent.insert(index + 1, '<em>%s</em>' % (themessage, ))
    
    return thesum           

    