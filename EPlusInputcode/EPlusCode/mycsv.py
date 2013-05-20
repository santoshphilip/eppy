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

"""my csv functions
"""

from cStringIO import StringIO
import csv

class MyCsv(Exception):
    """pass"""
    pass
class BadMatrice(MyCsv):
    """pass"""
    pass
class BadInput(MyCsv):
    """pass"""
    pass

def mergehoriz(mat1, mat2):
    """paste mat2 to the right of mat1
    tested only for mat1 and mat2 of same size
    """
    if not ismatrice(mat1):
        raise BadMatrice, 'The input is not a matrice'
    if not ismatrice(mat2):
        raise BadMatrice, 'The input is not a matrice'
    if len(mat1)!=len(mat2):
        raise BadInput, 'mat1 and mat2 are not of same size'
    mmat = []
    for i in range(len(mat1)):
        row = mat1[i]+mat2[i]
        mmat.append(row)
    return mmat

def readcsv(filename):
    """read csv file fname into a matrice mat
    Also reads a string instead of a file
    """
    try:
        reader = csv.reader(open(filename,'rU'))#if it is a file
    except:
        try:
            string = StringIO(filename)
            reader = csv.reader(string)#if it is a string
        except:
            raise BadInput, 'csv source is neither a file nor a file object'
    data = []
    for line in reader:
        data.append(line)
    return data
    

def writecsv(mat, outfile=None):
    """write the matrice mat into a file fname
    """
    # if not ismatrice(mat):
    #     raise BadMatrice, 'The input is not a matrice'
    if outfile:
        writer = csv.writer(open(outfile,'wb'))
        writer.writerows(mat) 
    else:
        f = StringIO()
        writer = csv.writer(f)
        writer.writerows(mat) 
        return f.getvalue()
    

def ismatrice(mat):
    """test if the matrice mat is a csv matrice
    """
    #test for rows
    for row in mat:
        if type(row)!=list:
            return False
    #test if cell is float,int or string
    for row in mat:
        for cell in row:
            if type(cell) not in (float, int, str, unicode):
                return False
    return True

def transpose2d(mtx):
    """Transpose a 2d matrix
       [
            [1,2,3],
            [4,5,6]
            ]
        becomes
        [
            [1,4],
            [2,5],
            [3,6]
            ]
    """
    trmtx = [[] for i in mtx[0]]
    for i in range(len(mtx)):
        for j in range(len(mtx[i])):
            trmtx[j].append(mtx[i][j])
    return trmtx
##   -------------------------    
##    from python cookbook 2nd edition page 162
    # map(mtx, zip(*arr))

def getlist(fname):
    """Gets a list from a csv file
    If the csv file has only one column:
        it returns [a,b,c,d,e]
    if it has more than one column:
        it returns [[a,s],[3,r],[v,g]]
    This should work with a text file of one column
    """
    mat = readcsv(fname)
    onecolumn = True
    for row in mat:
        if len(row)!=1:
            onecolumn = False
            break
    if onecolumn:
        mat = transpose2d(mat)[0]
    return mat

def pick_and_reorder_columns(listofrows, column_indexes)   :
   """as the function name says
   from python cookbook 2nd ed. page 161
   """
   return [ [row[colindex] for colindex in column_indexes] for row in listofrows]