"""calculate the diffs for mathdiff.py and tablediff.py"""

import py

def dodiff(v1, v2, func=None, thelimit=0):
    """find the diff between v1 and v2. func is the function used to find the diff
    1. text diff
        a. if same, use v1 
            return (v1, False) 
        b. if diff, use v1 and mark as err
            return (v1, isdiff=False)
            or 
            return ((v1, v2), isdiff=True)
    2. perc diff
        a. if idential:
            return 0
        b. if in thelimit:
            return (diff, isdiff=False)
        c. else:
            return (diff, isdiff=True)
    3. delta diff
        a. if idential 
            return 0
        b. if in thelimit:
            return (diff, isdiff=False)
        c. else:
            return (diff, isdiff=True)
    """
    # 1
    if v1 == v2:
        try:
            f1, f2 = float(v1), float(v2) #2a and 3a
            return (0, False)
        except ValueError, e:
            return (v1, False)  #1a
    else:
        try:
            f1, f2 = float(v1), float(v2)
            if not func:
                return (f2 - f1, True)
            else:
                return func(f1, f2, thelimit) #2b, 2c, 3b, 3c
        except ValueError, e:
            return ((v1, v2), True) #1b
        
def deltdiff(v1, v2, deltdifflimit=0):
    """finds the delta diff, returns (diff, isdiff) isdiff is true if diff is over the limit"""
    diff = v2 - v1
    if abs(diff) > abs(deltdifflimit):
        isdiff = True
    else:
        isdiff = False
    return (diff, isdiff)    
    
def percdiff(v1, v2, percdifflimit=0):
    """finds the perc diff, returns (diff, isdiff) isdiff is True if diff is over the limit"""
    v1, v2 = float(v1), float(v2)
    if v1 == 0 and v2 == 0:
        return (0.0, False)
    # TODO : what to return when v1 = 0 ??
    diff = (v2 - v1) / v1 * 100
    if abs(diff) > abs(percdifflimit):
        isdiff = True
    else:
        isdiff = False
    return (diff, isdiff)    
    
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

class MatrixSizeError(Exception):
    pass    

def tablediff(table1, table2, func=None, thelimit=0):
    """return a difftable that is the difference between table1 and table2
    each cell in difftable will have the diff between corresponding cell in tabl1 and table2
    diff will be in the following format -> (thediff, isDiff) where
    thediff is the difference between the cells, isdiff is True if thediff > thelimit
    the diff is calculated using func. If func= None: thediff = cell2-cell1"""
    # TODO : check if the two tables have same dimensions
    if not equal_matrixsize(table1, table2): 
        raise MatrixSizeError, "the sizes of the two tables do not match"
    thetable = []
    for row1, row2 in zip(table1, table2):
        therow = []
        for cell1, cell2 in zip(row1, row2):
            thecell = dodiff(cell1, cell2, func, thelimit)
            therow.append(thecell)
        thetable.append(therow)
    return thetable
        
    
