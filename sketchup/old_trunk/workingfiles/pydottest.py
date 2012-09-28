"""helper routines for py.test"""

def almostequals(a, b, err=9):
    """line assertNotAlmostEqual in unittest"""
    errval = 10 ** -err
    return abs(a - b) < errval
