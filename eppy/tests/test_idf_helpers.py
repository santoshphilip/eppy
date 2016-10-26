# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for idf"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import iteritems
from six import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.pytest_helpers import almostequal
import eppy.idf_helpers as idf_helpers

iddfhandle = StringIO(iddcurrent.iddtxt)
  
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)

def test_idfobjectkeys():
    """py.test for idfobjectkeys"""
    expected = [u'LEAD INPUT',
            u'SIMULATION DATA',
            u'VERSION',
            u'SIMULATIONCONTROL',
            u'BUILDING']
    idf = IDF(StringIO(""))
    result = idf_helpers.idfobjectkeys(idf)
    assert result[:5] == expected
    