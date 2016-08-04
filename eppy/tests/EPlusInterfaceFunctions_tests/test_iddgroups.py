# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""pytest for iddgroups"""
from six import StringIO
import eppy.EPlusInterfaceFunctions.iddgroups as iddgroups

iddtxt = """!      W/m2, W or deg C
!      W/s
!      W/W
!      years
! **************************************************************************

Lead Input;

Simulation Data;

\\group G1

Version,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

Version1,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

Version2,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

\\group G2

VersionG,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

VersionG1,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

VersionG2,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier
      \\required-field
      \\default 7.0

"""

idd_commlst = [[[]],
 [[]],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']],
 [[u'unique-object', u'format singleLine'],
  [u'field Version Identifier', u'required-field', u'default 7.0']]]

idf_commdct = [[{}],
 [{}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],
 [{u'format': [u'singleLine'], u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}]]

def test_idd2groups():
    """py.test for idd2groups"""
    data = ((
        {
            'G2': ['VersionG', 'VersionG1', 'VersionG2'],
            'G1': ['Version', 'Version1', 'Version2'],
            None: ['Lead Input', 'Simulation Data']
        },
    ), # gdict
  )
    for gdict, in data:
        result = iddgroups.iddtxt2groups(iddtxt)
        assert result == gdict

def test_idd2group():
    """py.test for idd2group"""
    data = ((
        {
            'G2': ['VersionG', 'VersionG1', 'VersionG2'],
            'G1': ['Version', 'Version1', 'Version2'],
            None: ['Lead Input', 'Simulation Data']
        },
    ), # gdict
  )
    for gdict, in data:
        fhandle = StringIO(iddtxt)
        result = iddgroups.idd2group(fhandle)
        assert result == gdict

def test_iddtxt2grouplist():
    """py.test for iddtxt2grouplist"""
    data = (([(None, 'Lead Input'), (None, 'Simulation Data'), ('G1', 'Version'), ('G1', 'Version1'), ('G1', 'Version2'), ('G2', 'VersionG'), ('G2', 'VersionG1'), ('G2', 'VersionG2')], ), # glist
    ) 
    for glist, in data:
        result = iddgroups.iddtxt2grouplist(iddtxt)
        assert result == glist
        
def test_idd2grouplist():
    """py.test idd2grouplist"""
    data = (([(None, 'Lead Input'), (None, 'Simulation Data'), ('G1', 'Version'), ('G1', 'Version1'), ('G1', 'Version2'), ('G2', 'VersionG'), ('G2', 'VersionG1'), ('G2', 'VersionG2')], ), # glist
    )
    for glist, in data:
        fhandle = StringIO(iddtxt)
        result = iddgroups.idd2grouplist(fhandle)
        assert result == glist

def test_group2commlst():
    """py.test for group2commlst"""
    data = ((
    [
     [['group None', 'idfobj Lead Input']],
     [['group None', 'idfobj Simulation Data']],
     [['group G1', 'idfobj Version', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']],
     [['group G1', 'idfobj Version1', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']],
     [['group G1', 'idfobj Version2', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']],
     [['group G2', 'idfobj VersionG', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']],
     [['group G2', 'idfobj VersionG1', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']],
     [['group G2', 'idfobj VersionG2', u'unique-object', u'format singleLine'],
      [u'field Version Identifier', u'required-field', u'default 7.0']]
  ],
    ), # groupcommlst
    )
    for groupcommlst, in data:
        glist = iddgroups.iddtxt2grouplist(iddtxt)
        result = iddgroups.group2commlst(idd_commlst, glist)
        assert result == groupcommlst

(([(None, 'Lead Input'), (None, 'Simulation Data'), ('G1', 'Version'), ('G1', 'Version1'), ('G1', 'Version2'), ('G2', 'VersionG'), ('G2', 'VersionG1'), ('G2', 'VersionG2')], ), # glist
    ) 
def test_group2commdct():
    """py.test for group2commdct"""
    data = ((
    [
     [{'group':None, 'idfobj':'Lead Input'}],
     [{'group':None, 'idfobj':'Simulation Data'}],
     [{'group':'G1', 'idfobj':'Version', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G1', 'idfobj':'Version1', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G1', 'idfobj':'Version2', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG1', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG2', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}]],
       ), # groupcommdct
    )
    for groupcommdct, in data:
        glist = iddgroups.iddtxt2grouplist(iddtxt)
        result = iddgroups.group2commdct(idf_commdct, glist)
        # assert result == groupcommdct
        for r, g in zip(result, groupcommdct):
            assert r == g

def test_commdct2grouplist():
    """py.test for commdct2grouplist"""
    data = ((
    [
     [{'group':None, 'idfobj':'Lead Input'}],
     [{'group':None, 'idfobj':'Simulation Data'}],
     [{'group':'G1', 'idfobj':'Version', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G1', 'idfobj':'Version1', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G1', 'idfobj':'Version2', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG1', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}],
     [{'group':'G2', 'idfobj':'VersionG2', u'format': [u'singleLine'], u'unique-object': [u'']},
      {u'default': [u'7.0'],
       u'field': [u'Version Identifier'],
       u'required-field': [u'']}]],
    {
        'G2': ['VersionG', 'VersionG1', 'VersionG2'],
        'G1': ['Version', 'Version1', 'Version2'],
        None: ['Lead Input', 'Simulation Data']
    },
    ), # gcommdct, gdict
    )
    for gcommdct, gdict in data:
        result = iddgroups.commdct2grouplist(gcommdct)
        assert result == gdict