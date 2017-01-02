# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""pytest for iddgaps.py"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import StringIO
import eppy.iddgaps as iddgaps
from eppy.EPlusInterfaceFunctions import readidf


iddtxt = """Version,
      \\memo Specifies the EnergyPlus version of the IDF file.
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\default 8.6
      
GroundHeatTransfer:Slab:ZFACE,
         \\memo This is only needed when using manual gridding (not recommended)
         \\memo ZFACE: Z Direction cell face coordinates: m
        N1, N2, N3, N4, N5;                  \\note fields as indicated
BranchList,
 \\extensible:1 Just duplicate last field and comments (changing numbering, please)
 \\memo Branches MUST be listed in Flow order: Inlet branch, then parallel branches, then Outlet branch.
 \\memo Branches are simulated in the order listed.  Branch names cannot be duplicated within a single branch list.
   A1,  \\field Name
       \\required-field
       \\reference BranchLists
   A2, \\field Branch 1 Name
       \\begin-extensible
       \\required-field
       \\type object-list
       \\object-list Branches
   A3, \\field Branch 2 Name
       \\type object-list
       \\object-list Branches
   A4, \\field Branch 3 Name
       \\type object-list
       \\object-list Branches
  A492,A493,A494,A495,A496,A497,A498,A499,A500,A501; \\note fields as indicated

ZoneProperty:UserViewFactors:bySurfaceName,
       \\memo View factors for Surface to Surface in a zone.
       \\memo (Number of Surfaces)**2 must be entered.
       \\extensible:3 - copy last three fields, remembering to remove ;
       \\format ViewFactor
  A1,  \\field Zone Name
       \\type object-list
       \\object-list ZoneNames
  A2,  \\field From Surface 1
       \\begin-extensible
       \\type object-list
       \\object-list AllHeatTranSurfNames
  A3,  \\field To Surface 1
       \\type object-list
       \\object-list AllHeatTranSurfNames
  N1,  \\field View Factor 1
       \\note This value is the view factor value From Surface => To Surface
       \\type real
       \\maximum 1.0
  A4,  \\field From Surface 2
       \\type object-list
       \\object-list AllHeatTranSurfNames
  A5,  \\field To Surface 2
       \\type object-list
       \\object-list AllHeatTranSurfNames
  N2,  \\field View Factor 2
       \\note This value is the view factor value From Surface => To Surface
       \\type real
       \\maximum 1.0
  A42,A43,N21, \\note fields as indicated
  A44,A45,N22; \\note fields as indicated
"""

idftxt = ""

def test_cleaniddfield():
    """pytest for cleaniddfield"""
    data = ((
        {
            'field': ['Water Supply Storage Tank Name'],
            'Field': ['Water Supply Storage Tank Name'],
            'object-list': ['WaterStorageTankNames'],
            'type': ['object-list']
        },
        {
            'field': ['Water Supply Storage Tank Name'],
            'object-list': ['WaterStorageTankNames'],
            'type': ['object-list']
        }
        ), #field, newfield
           )
    for field, newfield in data:
        result = iddgaps.cleaniddfield(field)
        assert result == newfield

def test_cleancommdct():
    """py.test for cleancommdct"""
    data = ((
        [[{
            'field': ['Water Supply Storage Tank Name'],
            'Field': ['Water Supply Storage Tank Name'],
            'object-list': ['WaterStorageTankNames'],
            'type': ['object-list']
        }]],
        [[{
            'field': ['Water Supply Storage Tank Name'],
            'object-list': ['WaterStorageTankNames'],
            'type': ['object-list']
        }]]
        ), # commdct, newcommdct
           )
    for commdct, newcommdct in data:
        result = iddgaps.cleancommdct(commdct)
        assert result == newcommdct
        

def test_getfields():
    """py.test for getfields"""
    tdata = (
    (0, [{u'default': [u'8.6'],
        u'field': [u'Version Identifier']}]
    ), # index, expected
    (1, []
    ), # index, expected
    (2, [{u'field': [u'Name'],
        u'reference': [u'BranchLists'],
        u'required-field': [u'']},
        {u'begin-extensible': [u''],
        u'field': [u'Branch 1 Name'],
        u'object-list': [u'Branches'],
        u'required-field': [u''],
        u'type': [u'object-list']},
        {u'field': [u'Branch 2 Name'],
        u'object-list': [u'Branches'],
        u'type': [u'object-list']},
        {u'field': [u'Branch 3 Name'],
        u'object-list': [u'Branches'],
        u'type': [u'object-list']}]
    ), # index, expected
    )
    for index, expected in tdata:
        iddfile = StringIO.StringIO(iddtxt)
        fname = StringIO.StringIO(idftxt)
        block, data, commdct, idd_index = readidf.readdatacommdct1(
            fname,
            iddfile=iddfile,
            commdct=None,
            block=None)
        comm = commdct[index]
        result = iddgaps.getfields(comm)
        assert result == expected

def test_repeatingfieldsnames():
    """py.test for repeatingfieldsnames"""
    tdata = (
    (0, []), # index, expected
    (1, []), # index, expected
    (2, [(u'Branch %s Name', None)]), # index, expected
    (3, [(u'From Surface %s', None), 
        (u'To Surface %s', None), 
        (u'View Factor %s', None)]), # index, expected
    ) 
    for index, expected in tdata:
        iddfile = StringIO.StringIO(iddtxt)
        fname = StringIO.StringIO(idftxt)
        block, data, commdct, idd_index = readidf.readdatacommdct1(
            fname,
            iddfile=iddfile,
            commdct=None,
            block=None)
        comm = commdct[index]
        fields = iddgaps.getfields(comm)
        result = iddgaps.repeatingfieldsnames(fields)
        assert result == expected
    
def test_missingkeys_nonstandard():
    """py.test for missingkeys_nonstandard"""
    expectedbefore = [{}, {}, {}, {}, {u'note': [u'fields as indicated']}]
    expectedafter = [{u'field': [u'N1']}, {u'field': [u'N2']}, {u'field': [u'N3']}, {u'field': [u'N4']}, {u'note': [u'fields as indicated'], u'field': [u'N5']}]
    iddfile = StringIO.StringIO(iddtxt)
    fname = StringIO.StringIO(idftxt)
    block, data, commdct, idd_index = readidf.readdatacommdct1(
        fname,
        iddfile=iddfile,
        commdct=None,
        block=None)
    dtls = data.dtls
    assert commdct[1][1:] == expectedbefore
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls)
    iddgaps.missingkeys_nonstandard(block, commdct, dtls, nofirstfields)
    assert commdct[1][1:] == expectedafter

def test_missingkeys_standard():
    """py.test for missingkeys_standard"""
    expectedbefore = [[u'Name'], [u'Branch 1 Name'], [u'Branch 2 Name'], [u'Branch 3 Name']]
    expectedafter = [[u'Name'], [u'Branch 1 Name'], [u'Branch 2 Name'], [u'Branch 3 Name'], [u'Branch 4 Name'], [u'Branch 5 Name'], [u'Branch 6 Name'], [u'Branch 7 Name'], [u'Branch 8 Name'], [u'Branch 9 Name'], [u'Branch 10 Name'], [u'Branch 11 Name'], [u'Branch 12 Name'], [u'Branch 13 Name']]
    expectedresult = [u'GROUNDHEATTRANSFER:SLAB:ZFACE']
    iddfile = StringIO.StringIO(iddtxt)
    fname = StringIO.StringIO("")
    block, data, commdct, idd_index = readidf.readdatacommdct1(
        fname,
        iddfile=iddfile,
        commdct=None,
        block=None)
    dtls = data.dtls
    fieldnames = [item[u'field'] for item in commdct[2][1:]
                        if item.has_key(u'field')]
    assert fieldnames == expectedbefore
    nofirstfields = iddgaps.missingkeys_standard(commdct, dtls)
    fieldnames = [item[u'field'] for item in commdct[2][1:]
                        if item.has_key(u'field')]
    assert fieldnames == expectedafter
    assert expectedresult == nofirstfields