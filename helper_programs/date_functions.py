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

"""date functions"""

import datetime

def gt(a, b):
    return a > b
    
def lt(a, b):
    return a < b

def yeardates(year):
    """return the dates of a year as string"""
    days = [(datetime.date.fromordinal(i)) for i in range(1, 366)]
    return ['%s-%s-%s' % (year, d.month, d.day) for d in days]


def yeardateshours(year):
    """return date and hour of a year as a string"""
    ydays = yeardates(year)
    hrs = []
    for d in ydays:
        for i in range(1, 25):
            st = '%s hr%s:00' % (d, i)
            hrs.append(st)
    return hrs
    

def split2days(lst, hrs=24):
    """split data into 24 hour days"""
    yr = []
    for i in range(0, len(lst) / hrs):
        day = []
        for j in range(0, hrs):
            val = lst.pop(0)
            day.append(val)
        yr.append(day)
    return yr

def split2months(lst, months=None, hours=24):
    """split the data into blocks that are months of the year.
    months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    hours = hours in a day"""
    if months == None:
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = [month * hours for month in months]
    return [[lst.pop(0) for i in range(m)] for m in months]
    
def fillmonths(data, months=None, hours=24):
    """if single data item avaliable for month, fill month with it"""
    if months == None:
        months = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    months = [month * hours for month in months]
    return [[d, ] * m for d, m in zip(data, months)]
        

def filterdays(matrix, filterindex, filterval, condition, hrs=24):
    """Filter the items in the list matrix.
    The list is chopped into blocks of size hrs
    the filter happens - 
        if condition(matrix[i][filterindex], filterval) == True:
            return the entire block
    """
    days = split2days(matrix, hrs=hrs) # splits it into 24 hr blocks
    filtered = []
    for day in days:
        for row in day:
            if condition(row[filterindex], filterval):
                filtered = filtered + day
                break
    return filtered
    
def zfilterdays(matrix, filterindex, filterval, condition, hrs=24):
    """Filter the items in the list matrix.
    The list is chopped into blocks of size hrs
    the filter happens - 
        if condition(matrix[i][filterindex], filterval) == True:
            return the entire block
        else
            return block with blank rows
    """
    days = split2days(matrix, hrs=hrs) # splits it into 24 hr blocks
    filtered = []
    for day in days:
        for row in day:
            incondition = False
            if condition(row[filterindex], filterval):
                filtered = filtered + day
                incondition = True
                break
        if incondition == False:
            filtered = filtered + [[], ] * len(day)
    return filtered
    
def flattenlist(lst):
    """will flatten alist of lists"""
    return [item for sublist in lst for item in sublist]