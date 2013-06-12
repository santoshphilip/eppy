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

"""py.test for eplussql.py"""

import eplussql
import pytest
import mycsv

def test_c2f():
    """py.test for c2f"""
    data = ((32, 89.6), # cel, fr
        (-40, -40), # cel, fr
    )
    for cel, fr in data:
        result = eplussql.c2f(cel)
        assert result == fr
        
def test_get_eplusversion():
    """py.test for get_eplusversion"""
    data = ('./eplussql_test/eplussql.sql','6.0.0.023') #fname, version        
    fname, version = data
    cursor = eplussql.getcursor(fname)
    result = eplussql.get_eplusversion(cursor)
    assert result == version
    
def test_getcursor():
    """py.test for getcursor"""
    data = (('./eplussql_test/eplussql.sql', u'10.0.0.023', 
        'exception'), # fname, eplusversion, versionresponse
        ('./eplussql_test/eplussql.sql', u'10.0.0.023', 
            'print'), # fname, eplusversion, versionresponse
        ('./eplussql_test/eplussql.sql', u'10.0.0.023', 
            None), # fname, eplusversion, versionresponse
    )
    error = eplussql.VersionMismatchError
    testing=True
    for fname, eplusversion, versionresponse in data:
        if versionresponse == 'exception':
            with pytest.raises(error):
                eplussql.getcursor(fname, versionresponse=versionresponse, testing=testing)
        if versionresponse == 'print':
            result = eplussql.getcursor(fname, versionresponse=versionresponse, testing=testing)
            assert result == 'printed'
        if versionresponse == None:
            result = eplussql.getcursor(fname, versionresponse=versionresponse, testing=testing)
            assert result == None
                
def test_get_wfilestart():
    """py.test for get_wfilestart"""
    data = (('./eplussql_test/eplussql.sql', 2 * 24),# fname, start
    )    
    for fname, start in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_wfilestart(cursor)
        assert result == start

def test_get_variables():
    """py.test for get_variables"""
    def _double(n):
        return n * 2
    data = (('./eplussql_test/eplussql.sql', 6, None, 
            [11.1, 10.4125, 9.625] ), # fname, ReportVariableDataDictionaryIndex, func, threevars
        ('./eplussql_test/eplussql.sql', 6, _double, 
            [22.2, 20.8250, 19.250] ), # fname, ReportVariableDataDictionaryIndex, func, threevars
    )
    for fname, ReportVariableDataDictionaryIndex, func, threevars in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_variables(cursor, 
            ReportVariableDataDictionaryIndex, func)
        threeresult = result[-6:-3]
        assert threeresult == threevars
        
def test_get_variables1():
    """py.test for get_variables1"""
    def _double(n):
        return n * 2
    data = (('./eplussql_test/eplussql.sql', 6, None, 
            [11.1, 10.4125, 9.625] ), # fname, ReportVariableDataDictionaryIndex, func, threevars
        ('./eplussql_test/eplussql.sql', 6, _double, 
            [22.2, 20.8250, 19.250] ), # fname, ReportVariableDataDictionaryIndex, func, threevars
    )
    for fname, ReportVariableDataDictionaryIndex, func, threevars in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_variables1(cursor, 
            ReportVariableDataDictionaryIndex, func)
        threeresult = result[-6:-3]
        assert threeresult == threevars
        
def test_get_manyvariables():
    """py.test for get_manyvariables"""
    data = (('./eplussql_test/eplussql.sql', [6, 7], [None, None]), # fname, ReportVariableDataDictionaryIndices, funcs
    )
    for fname, ReportVariableDataDictionaryIndices, funcs in data:
        cursor = eplussql.getcursor(fname)
        thevars = []
        for ind, func in zip(ReportVariableDataDictionaryIndices, funcs):
            thevars.append(eplussql.get_variables(cursor, ind, func))
        matrix = mycsv.transpose2d(thevars)
        result = eplussql.get_manyvariables(cursor, 
            ReportVariableDataDictionaryIndices, funcs)
        assert result == matrix
        
    
def test_get_variablename():
    """py.test for get_variablename"""
    data = (('./eplussql_test/eplussql.sql', 6, 'Outdoor Dry Bulb'), # fname, ReportVariableDataDictionaryIndex, name 
    )
    for fname, ReportVariableDataDictionaryIndex, name in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_variablename(cursor, ReportVariableDataDictionaryIndex)
        assert result == name
        
def test_get_variableunit():
    """py.test for get_variablename"""
    data = (('./eplussql_test/eplussql.sql', 6, 'C'), # fname, ReportVariableDataDictionaryIndex, unit 
    )
    for fname, ReportVariableDataDictionaryIndex, unit in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_variableunit(cursor, ReportVariableDataDictionaryIndex)
        assert result == unit
        
def test_get_keyvalue():
    """py.test for get_keyvalue"""
    data = (('./eplussql_test/eplussql.sql', 6, 'Environment'), # fname, ReportVariableDataDictionaryIndex, key 
    )
    for fname, ReportVariableDataDictionaryIndex, key in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_keyvalue(cursor, ReportVariableDataDictionaryIndex)
        assert result == key
        
def test_checkhourly():
    """py.test for checkhourly"""
    data = (('./eplussql_test/eplussql.sql', True), # fname, ishourly
        ('./eplussql_test/eplussql1.sql', False), # fname, ishourly
    )
    for fname, ishourly in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.checkhourly(cursor)
        assert result == ishourly
        
def test_get_varindex():
    """py.test for get_varindex"""
    data = (('./eplussql_test/eplussql.sql',
        [['Index', 'KeyValue', 'VariableName', 'VariableUnits'],
        [6, u'Environment', u'Outdoor Dry Bulb', u'C'],
        [7, u'Environment', u'Outdoor Wet Bulb', u'C'],
        [8, u'Environment', u'Outdoor Relative Humidity', u'%']]), # fname, indexmatrix
    )        
    for fname, indexmatrix in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.get_varindex(cursor)
        assert result == indexmatrix

def test_outofbounds():
    """py.test for outofbounds"""
    data = (('./eplussql_test/eplussql.sql', 6, 14, True, 2), # fname, ReportVariableDataDictionaryIndex, bounds, above, count
        ('./eplussql_test/eplussql.sql', 6, 5, False, 2), # fname, ReportVariableDataDictionaryIndex, bounds, above, count
    )        
    for fname, ReportVariableDataDictionaryIndex, bounds, above, count in data:
        cursor = eplussql.getcursor(fname)
        result = eplussql.outofbounds(cursor, ReportVariableDataDictionaryIndex, bounds, above)
        assert result == count
        
# def test_testhourly():
#     """py.test for testhourly"""
#     data = (('./eplussql_test/nothourly.sql', False), # fname, ishourly
#         ('./eplussql_test/hourly.sql', True), # fname, ishourly
#     )        
#     for fname, ishourly in data:
#         cursor = eplussql.getcursor(fname, testing='skipversiontest')
#         result = eplussql.testhourly(cursor)
#         assert result == ishourly
        
# TODO : put the oakland weather file in check in. this can be used when the next verion comes out.    