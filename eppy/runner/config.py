# Copyright (c) 2015 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""
Config parameters for eppy.runner. Ideally we would have these set
automatically by looking for them on the filesystem.

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os


EPLUS_HOME = 'C:\EnergyPlusV8-3-0'
EPLUS_WEATHER = os.path.join(EPLUS_HOME, 'WeatherData')
EPLUS_EXE = os.path.join(EPLUS_HOME, 'energyplus.exe')
