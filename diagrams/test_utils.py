"""pytest for utils.py"""

import utils

def test_getiddversion():
    """py.test for getiddversion"""
    data = (("""!IDD_Version 6.0.0.023
! **************************************************************************
! This file is the Input Data Dictionary (IDD) for EnergyPlus.
""", "6.0.0.023"),# iddtxt, verison
("""!xxxxxxxx 6.0.0.023
! **************************************************************************
! This file is the Input Data Dictionary (IDD) for EnergyPlus.
""", "version not known"),# iddtxt, verison
    )
    for iddtxt, verison in data:
        result = utils.getiddversion(iddtxt)
        assert result == verison