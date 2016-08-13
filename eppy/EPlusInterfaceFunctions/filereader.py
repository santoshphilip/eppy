# Copyright (C) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Code for reading in EnergyPlus IDF and IMF files"""

def readfile(filename):
    """Read a file, handling any decoding required.
    """
    with open(filename, 'rb') as f:
        data = f.read()
        data = data.decode('ISO-8859-2')
    return data
