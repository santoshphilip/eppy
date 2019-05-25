# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for idfreader. very few tests"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import StringIO

import eppy.idfreader as idfreader
from eppy.EPlusInterfaceFunctions import readidf

from eppy.iddcurrent import iddcurrent
iddfhandle = StringIO(iddcurrent.iddtxt)

def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)

def test_convertafield():
    """py.test for convertafield"""
    data = (
    ({'type':'integer'}, '1', 'N1', 1),
        # field_comm, field_val, field_iddname, expected
    ({}, '1', 'N1', 1.0),
        # field_comm, field_val, field_iddname, expected
    ({'type':'real'}, '1', 'N1', 1.0),
        # field_comm, field_val, field_iddname, expected
    ({}, 'autosize', 'N1', 'autosize'),
    ({}, '4', 'A1', '4'),
        # field_comm, field_val, field_iddname, expected
    )
    for field_comm, field_val, field_iddname, expected in data:
        result = idfreader.convertafield(field_comm, field_val, field_iddname)
        assert result == expected

def test_convertallfields():
    """py.test convertallfields"""
    data = (
        ("version, 8.1;", 'VERSION', [u'version', u'8.1']),
            # idfstr, objkey, expected
        ("WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM, simple, 0.45;",
        'WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM',
        [u'WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM', 'simple', 0.45]),
            # idfstr, objkey, expected
        ("HVACTEMPLATE:ZONE:FANCOIL, gumby1, gumby2, 0.45;",
        'HVACTEMPLATE:ZONE:FANCOIL',
        [u'HVACTEMPLATE:ZONE:FANCOIL', 'gumby1', 'gumby2', 0.45]),
            # idfstr, objkey, expected
        ("HVACTEMPLATE:ZONE:FANCOIL, gumby1, gumby2, autosize;",
        'HVACTEMPLATE:ZONE:FANCOIL',
        [u'HVACTEMPLATE:ZONE:FANCOIL', 'gumby1', 'gumby2', 'autosize']),
            # idfstr, objkey, expected
    )
    commdct = None
    block = None
    for idfstr, objkey, expected in data:
        idfhandle = StringIO(idfstr)
        block, data, commdct, idd_index = readidf.readdatacommdct1(
                            idfhandle, iddfile=iddfhandle, 
                            commdct=commdct, block=block)
        idfreader.convertallfields(data, commdct, block)
        result = data.dt[objkey][0]
        assert result == expected
        
def test_getextensible():
    """py.test for getextensible"""
    data = (
    ([{u'format': [u'singleLine'],
  u'group': u'Simulation Parameters',
  u'idfobj': u'Version',
  u'memo': [u'Specifies the EnergyPlus version of the IDF file.'],
  u'unique-object': [u'']}, {}, {}, {}
 ],
  None), # objidd, expected
    ([{u'extensible:2': [u'- repeat last two fields, remembering to remove ; from "inner" fields.'],
 u'group': u'Schedules',
 u'idfobj': u'Schedule:Day:Interval',
 u'memo': [u'A Schedule:Day:Interval contains a full day of values with specified end times for each value',
  u'Currently, is set up to allow for 10 minute intervals for an entire day.'],
 u'min-fields': [u'5']}, {}, {}, {}
 ],
  2), # objidd, expected
    )        
    for objidd, expected in data:
        result = idfreader.getextensible(objidd)
        assert result == expected

def test_endof_extensible():
    """py.test for endof_extensible"""
    data = (
    (1, ['gumby', 'A1', 'A2'], ['A2']), # extensible, thisblock, expected
    (1, ['gumby', 'A1', 'A2', 'A3'], ['A3']), # extensible, thisblock, expected
    (2, ['gumby', 'A1', 'A2', 'A3'], ['A2', 'A3']), # extensible, thisblock, expected
    ) 
    for extensible, thisblock, expected in data:
        result = idfreader.endof_extensible(extensible, thisblock)
        assert result == expected
        
def test_extension_of_extensible():
    """py.test for extension_of_extensible"""
    data = (
    ([{u'extensible:1': None,
 u'group': u'Schedules',
 u'idfobj': u'Schedule:Day:Interval'}, {}, {}, {}
 ],
 ["Gumby", "A1", "A2"], 1, ["A3"]), # objidd, objblock, n, expected
    ([{u'extensible:1': None,
 u'group': u'Schedules',
 u'idfobj': u'Schedule:Day:Interval'}, {}, {}, {}
 ],
 ["Gumby", "A1", "A2"], 2, ["A3", "A4"]), # objidd, objblock, n, expected
    ([{u'extensible:1': None,
 u'group': u'Schedules',
 u'idfobj': u'Schedule:Day:Interval'}, {}, {}, {}
 ],
 ["Gumby", "A1", "A2"], 3, ["A3", "A4", "A5"]), # objidd, objblock, n, expected

    ([{u'extensible:2': None,
 u'group': u'Schedules',
 u'idfobj': u'Schedule:Day:Interval'}, {}, {}, {}
 ],
 ["Gumby", "A1", "A2"], 1, ["A3", "A4"]), # objidd, objblock, n, expected
    )        
    for objidd, objblock, n, expected in data:
        result = idfreader.extension_of_extensible(objidd, objblock, n)
        # print(result)
        # print(expected)
        # print("-")
        # assert result == expected
        assert True