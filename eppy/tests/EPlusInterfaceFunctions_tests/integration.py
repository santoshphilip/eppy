# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
"""integration tests for EPlusInterfaceFunctions"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.EPlusInterfaceFunctions.iddgroups as iddgroups

def test_idd2group():
    """py.test for idd2group"""
    data = ((
        "./eppy/tests/EPlusInterfaceFunctions_tests/integration/iddgroups.idd",
        {
            'G2': ['VersionG', 'VersionG1', 'VersionG2'],
            'G1': ['Version', 'Version1', 'Version2'],
            None: ['Lead Input', 'Simulation Data']
        },
    ), # gdict
  )
    for fname, gdict in data:
        result = iddgroups.idd2group(fname)
        assert result == gdict
        

def test_idd2grouplist():
    """py.test idd2grouplist"""
    data = ((
        "./eppy/tests/EPlusInterfaceFunctions_tests/integration/iddgroups.idd",
        [(None, u'Lead Input'), (None, u'Simulation Data'), (u'G1', u'Version'), (u'G1', u'Version1'), (u'G1', u'Version2'), (u'G2', u'VersionG'), (u'G2', u'VersionG1'), (u'G2', u'VersionG2')], ), # glist
    ) 
    for fname, glist in data:
        result = iddgroups.idd2grouplist(fname)
        assert result == glist
        