# Copyright (c) 2012 Santosh Philip

"""pytest for idfreader. very few tests"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.idfreader as idfreader
from StringIO import StringIO

def test_iddversiontuple():
    """py.test for iddversiontuple"""
    iddtxt = """stuff 9.8.4
    other stuff"""
    fhandle = StringIO(iddtxt)
    result = idfreader.iddversiontuple(fhandle)
    assert result == (9, 8, 4)
