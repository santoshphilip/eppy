# Copyright (c) 2022 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""helpers for pytest in eppy"""


import eppy


def safeIDDreset():
    """reset the IDD for testing and catch the exception"""
    try:
        eppy.modeleditor.IDF.resetidd()
    except eppy.modeleditor.IDDResetError as e:
        pass
