# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""do just walls in eplusinterface"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from eppy.idfreader import idfreader

iddfile = "../iddfiles/Energy+V7_0_0_036.idd"
fname = "../idffiles/V_7_0/5ZoneSupRetPlenRAB.idf"

bunchdt, data, commdct = idfreader(fname, iddfile)
surfaces = bunchdt['BUILDINGSURFACE:DETAILED'.upper()] # all the surfaces

for surface in surfaces:
    name = surface.Name
    area = surface.area
    height = surface.height
    width = surface.width
    azimuth = surface.azimuth
    tilt = surface.tilt
    print(name, area, height, width, azimuth, tilt)

