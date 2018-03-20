# Copyright (c) 2018 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""py.test for idf_helpers.easyopen"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from eppy import modeleditor
import eppy.easyopen as easyopen
from eppy.pytest_helpers import do_integration_tests

from six import StringIO
from six.moves import reload_module as reload

@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set")
def test_easyopen():
    """py.test for easyopen"""
    data = (("  Version,8.8;", '8.8'), # txt, result
    )
    for txt, result in data:
        fhandle = StringIO(txt)
        reload(modeleditor)
        reload(easyopen)
        idf = easyopen.easyopen(fhandle)
        versions = idf.idfobjects['version'.upper()]
        version = versions[0]
        ver = version.Version_Identifier
        # reload(modeleditor)
        # reload(IDF)
        # reload(idf_helpers)
        assert result == ver
        