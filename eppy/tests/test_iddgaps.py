# Copyright (c) 2012 Santosh Philip

"""pytest for iddgaps.py"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import eppy.iddgaps as iddgaps

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
