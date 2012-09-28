"""functions to get items in the sql above a certain value"""

import eplussql
import date_functions

def getabove(fname, varindex, aboveval, convertc2f=False):
    """return variable name, max and min of the variable"""# TODO incorrect __doc__
    cursor = eplussql.getcursor(fname)
    # startpoint = eplussql.get_wfilestart(cursor)
    varunit = eplussql.get_variableunit(cursor, varindex)
    if convertc2f and varunit == u'C':
        func = eplussql.c2f
        varunit = u'F'
    else:
        func = None
    matrix = eplussql.get_variables(cursor, varindex, func=func)
    varname = eplussql.get_variablename(cursor, varindex)
    keyvalue = eplussql.get_keyvalue(cursor, varindex)
    abovenums = [val for val in matrix if val > aboveval]
    return varname, keyvalue, varunit, len(abovenums)
    
def getabovedays(fname, varindex, aboveval, year=2001, convertc2f=False):
    """return variable name, max and min of the variable"""
    cursor = eplussql.getcursor(fname)
    # startpoint = eplussql.get_wfilestart(cursor)
    varunit = eplussql.get_variableunit(cursor, varindex) # var units
    varname = eplussql.get_variablename(cursor, varindex) # varname
    keyvalue = eplussql.get_keyvalue(cursor, varindex) # get keyvalue
    if convertc2f and varunit == u'C': # conversion
        func = eplussql.c2f
        varunit = u'F'
    else:
        func = None
    matrix = eplussql.get_variables(cursor, varindex, func=func) # gets vars
    yhours = date_functions.yeardateshours(year) # yeardates
    matrix = zip(yhours, matrix)
    # days = split2days(matrix, hrs=24) # splits it into 24 hr blocks
    # filtering of days take place below
    # daysabove = filterdaysabove(days, aboveval)
    daysabove = date_functions.filterdays(matrix, -1, aboveval,
                                        date_functions.gt, hrs=24)
    return varname, keyvalue, varunit, daysabove
    
# fname = './eplussql_test/hup01_23_pytest.sql'
# varname, keyvalue, varunit, daysabove = getabovedays(fname, 386, 88, convertc2f=True)
# for day in daysabove:
#     for d, val in day:
#         print '%s, %s' % (d, val)