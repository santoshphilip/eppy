# Copyright (c) 2015 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Run functions for EnergyPlus.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess
import unittest

from eppy.runner import config


def run(idf='in.idf',
        weather='in.epw',
        annual=False,
        output_directory=None,
        design_day=False,
        expandobjects=True,
        epmacro=False,
        readvars=False,
        idd=None,
        output_prefix=None,
        output_suffix=None,
        help=False,
        version=False,
        ):
    """
    Wrapper around the EnergyPlus command line interface.
    
    Parameters
    ----------
    idf : str, optional
        Full or relative path to the IDF file to be run.
    weather : str, optional
        Full or relative path to the weather file.
    annual : bool, optional
        If True then force annual simulation (default: False)
    output_directory : str, optional
        Output directory path (default: current directory)
    design_day : bool, optional
        Force design-day-only simulation (default: False)
    help : bool, optional
        Display help information (default: False)
    idd : str, optional
        Input data dictionary path (default: Energy+.idd in EnergyPlus directory)
    epmacro : str, optional
        Run EPMacro prior to simulation.
    expandobjects : bool, optional
        Run ExpandObjects prior to simulation (default: False)
    readvars : bool, optional
        Run ReadVarsESO after simulation (default: False)
    output_suffix : str, optional
        Suffix style for output file names (default: L)
            L: Legacy (e.g., eplustbl.csv)
            C: Capital (e.g., eplusTable.csv)
            D: Dash (e.g., eplus-table.csv)
    output-prefix : str, optional
        Prefix for output file names (default: eplus)
    version : bool, optional
        Display version information (default: False)
    help : bool, optional
        Display help information (default: False)
        
    Returns
    -------
        EnergyPlus return code.

    """
    args = locals().copy() 

    # get the IDF name
    idf = args.pop('idf')
    
    # build a list of command line arguments
    cmd_args = []
    for arg in args:
        if args[arg]:
            if isinstance(args[arg], basestring):
                args[arg] = ' "{}"'.format(args[arg])
            elif isinstance(args[arg], bool):
                args[arg] = ''
            cmd_args.append('--{}{}'.format(arg.replace('_', '-'), args[arg]))

    # Get the path to the EnergyPlus executable
    energyplus = os.path.join(config.EPLUS_HOME, config.EPLUS_EXE)

    # build the command line interface string
    cmd = '"{}" {} "{}"'.format(energyplus, ' '.join(cmd_args), idf)

    if subprocess.check_call(cmd):
        # Should try and generate a more useful error message
        raise Exception("EnergyPlus did not complete")


class TestWrapper(unittest.TestCase):


    def setUp(self):
        """
        """
        pass
        
    def tearDown(self):
        """
        """
        pass
    
    def testCommandStrings(self):
        """end to end test of idf.run function
        """
        assert run('in.idf')
    