# Copyright (c) 2012 Santosh Philip

# This file is part of eppy.

# Eppy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Eppy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with eppy.  If not, see <http://www.gnu.org/licenses/>.

"""py.test for modeleditor"""
import pytest

import bunch
import idfreader
import modeleditor
import snippet

from iddcurrent import iddcurrent
iddsnippet = iddcurrent.iddtxt

idfsnippet = snippet.idfsnippet

from StringIO import StringIO
idffhandle = StringIO(idfsnippet)
iddfhandle = StringIO(iddsnippet)
bunchdt, data, commdct = idfreader.idfreader(idffhandle, iddfhandle)

def test_poptrailing():
    """py.test for poptrailing"""
    data = (([1, 2, 3, '', 56, '', '', '', ''], 
        [1, 2, 3, '', 56]), # lst, poped
        ([1, 2, 3, '', 56], 
        [1, 2, 3, '', 56]), # lst, poped
        ([1, 2, 3, 56], 
        [1, 2, 3, 56]), # lst, poped
    )

def test_extendlist():
    """py.test for extendlist"""
    data = (([1,2,3], 2, 0, [1,2,3]), # lst, i, value, nlst
    ([1,2,3], 3, 0, [1,2,3,0]), # lst, i, value, nlst
    ([1,2,3], 5, 0, [1,2,3,0,0,0]), # lst, i, value, nlst
    ([1,2,3], 7, 0, [1,2,3,0,0,0,0,0]), # lst, i, value, nlst
    )
    for lst, i, value, nlst in data:
        modeleditor.extendlist(lst, i, value=value)
        assert lst == nlst

def test_newrawobject():
    """py.test for newrawobject"""
    thedata = (('zone'.upper(), 
        ['ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate', 
            'autocalculate', 'autocalculate', '', '', 'Yes']), # key, obj
    )
    for key, obj in thedata:
        result = modeleditor.newrawobject(data, commdct, key)
        assert result == obj
        
def test_obj2bunch():
    """py.test for obj2bunch"""
    thedata = ((['ZONE', '', '0', '0', '0', '0', '1', '1', 'autocalculate', 
        'autocalculate', 'autocalculate', '', '', 'Yes']), # obj
    )
    for obj in thedata:
        key_i = data.dtls.index(obj[0].upper())
        abunch = idfreader.makeabunch(commdct, obj, key_i)
        result = modeleditor.obj2bunch(data, commdct, obj)
        assert result == abunch
    
def test_namebunch():
    """py.test for namebunch"""
    thedata = ((bunch.Bunch(dict(Name="", a=5)), 
        "yay", "yay"), # abunch, aname, thename
        (bunch.Bunch(dict(Name=None, a=5)), 
            "yay", None), # abunch, aname, thename
    )
    for abunch, aname, thename in thedata:
        result = modeleditor.namebunch(abunch, aname)
        assert result.Name == thename
        
def test_addobject():
    """py.test for addobject"""
    thedata = (
    ('ZONE', 'karamba'), # key, aname
    ('ZONE', 'None'), # key, aname
    )
    for key, aname in thedata:
        result = modeleditor.addobject(bunchdt, data, commdct, key, aname)
        assert bunchdt[key][-1].key == key # wierd, but correct :-)
        if aname:
            assert data.dt[key][-1][1] == aname
            assert bunchdt[key][-1].Name == aname
        
def test_getnamedargs():
    """py.test for getnamedargs"""
    result = dict(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(a=1, b=2, c=3)
    assert result == modeleditor.getnamedargs(dict(a=1, b=2, c=3))
    assert result == modeleditor.getnamedargs(dict(a=1, b=2), c=3)
    assert result == modeleditor.getnamedargs(dict(a=1), c=3, b=2)
    
def test_addobject1():
    """py.test for addobject"""
    thedata = (('ZONE', {'Name':'karamba'}), # key, kwargs
    )
    for key, kwargs in thedata:
        result = modeleditor.addobject1(bunchdt, data, commdct, key, kwargs)
        aname = kwargs['Name']
        assert data.dt[key][-1][1] == aname
        assert bunchdt[key][-1].Name == aname        
        
def test_getobject():
    """py.test for getobject"""
    thedata = (
        ('ZONE', 'PLENUM-1', 
            bunchdt['ZONE'][0]), # key, name, theobject
        ('ZONE', 'PLENUM-1'.lower(), 
            bunchdt['ZONE'][0]), # key, name, theobject
        ('ZONE', 'PLENUM-A', 
            None), # key, name, theobject
    )
    for key, name, theobject in thedata:
        result = modeleditor.getobject(bunchdt, key, name)
        assert result == theobject
        
def test_getobjects():
    """py.test for getobjects"""
    thedata = (
    ('ZONE', {'Name':'PLENUM-1'}, bunchdt['ZONE'][0:1]), # key, fielddict, theobjects
    )
    for key, fielddict, theobjects in thedata:
        result = modeleditor.getobjects(bunchdt, key, **fielddict)
        assert result == theobjects

def test_is_retaincase():
    """py.test for is_retaincase"""
    thedata = (
    ("BUILDING", 'Name', True), # key, fieldname, case
    ("BUILDING", 'Terrain', False), # key, fieldname, case
    )    
    for key, fieldname, case in thedata:
        idfobject = bunchdt[key][0]
        result = modeleditor.is_retaincase(bunchdt, data, commdct, 
            idfobject, fieldname)
        assert result == case

def test_equalfield():
    """py.test for equalfield"""
    thedata = (
        ("BUILDING", 0, 1, 'Name', 7, True), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, 'Name', 7, False), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'Terrain', 7, True), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'Terrain', 7, True), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 1, 'North_Axis', 7, True), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 2, 'North_Axis', 2, True), 
        # key, objindex1, objeindex2, fieldname, places, isequal
        ("BUILDING", 0, 3, 'Maximum_Number_of_Warmup_Days', 7, True), 
        ("BUILDING", 0, 3, 'Minimum_Number_of_Warmup_Days', 7, False), 
        # key, objindex1, objeindex2, fieldname, places, isequal
    )
    for key, objindex1, objindex2, fieldname, places, isequal in thedata:
        idfobject1 = bunchdt[key][objindex1]
        idfobject2 = bunchdt[key][objindex2]
        result = modeleditor.equalfield(bunchdt, data, commdct, 
            idfobject1, idfobject2, fieldname, places)
        assert result == isequal
    (key, objindex1, objeindex2, 
        fieldname, places, isequal) = ("BUILDING", 0, 1, 'Name', 7, True)
    idfobject1 = bunchdt[key][objindex1]
    idfobject2 = bunchdt["ZONE"][objindex2]
    with pytest.raises(modeleditor.NotSameObjectError):
        modeleditor.equalfield(bunchdt, data, commdct, 
            idfobject1, idfobject2, fieldname, places)
            
def test_iddofobject():
    """py.test of iddofobject"""
    thedata = (('VERSION', 
                [{'format': ['singleLine'], 'unique-object': ['']},
                {'default': ['7.0'], 'field': ['Version Identifier'], 
                'required-field': ['']}]), # key, itsidd
    )
    for key, itsidd in thedata:
        result = modeleditor.iddofobject(data, commdct, key)
        result[0].pop('memo') # memo is new in version 8.0.0
        assert result == itsidd


def test_removeextensibles():
    """py.test for removeextensibles"""
    thedata = (("BuildingSurface:Detailed".upper(), "WALL-1PF",
    ["BuildingSurface:Detailed", "WALL-1PF", "WALL", "WALL-1", "PLENUM-1", 
    "Outdoors","", "SunExposed", "WindExposed", 0.50000, '4',] ), # key, objname, rawobject
    )
    for key, objname, rawobject in thedata:
        result = modeleditor.removeextensibles(bunchdt, data, commdct, key, 
                                                objname)
        assert result.obj == rawobject
        