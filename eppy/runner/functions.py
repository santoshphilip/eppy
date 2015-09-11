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

from runner import config


EPLUS_HOME = 'C:\EnergyPlusV8-3-0'
EPLUS_WEATHER = os.path.join(EPLUS_HOME, 'WeatherData')
EPLUS_EXE = os.path.join(EPLUS_HOME, 'energyplus.exe')
THIS_DIR = os.path.dirname(__file__)


def run(idf='in.idf',
        weather='in.epw',
        annual=False,
        run_directory='.',
        output_directory=None,
        design_day=False,
        expandobjects=False,
        epmacro=False,
        readvars=False,
        idd=None,
        output_prefix=None,
        output_suffix=None,
        version=False,
        verbose='v'):
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
    run_directory : str
        A directory in which to run EnergyPlus. This is needed when using
        multiprocessing (default: current directory)
    output_directory : str, optional
        Output directory path (default: current directory)
    design_day : bool, optional
        Force design-day-only simulation (default: False)
    idd : str, optional
        Input data dictionary (default: Energy+.idd in EnergyPlus directory)
    epmacro : str, optional
        Run EPMacro prior to simulation (default: False).
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
    verbose: str
        Set verbosity of runtime messages (default: v)
            v: verbose
            q: quiet
            
    Raises
    ------
        CalledProcessError
    
    """
    args = locals().copy()
    # get unneeded params out of args ready to pass the rest to energyplus.exe
    idf = args.pop('idf')
    verbosity = args.pop('verbose')
    args['output_directory'] = os.path.abspath(args.pop('output_directory'))
    os.chdir(os.path.join(os.path.pardir, args.pop('run_directory')))
    # build a list of command line arguments
    cmd = [config.EPLUS_EXE]
    for arg in args:
        if args[arg]:
            if isinstance(args[arg], bool):
                # remove the True or False to just leave the flag
                cmd.extend(['--{}'.format(arg.replace('_', '-'))])
            else:
                cmd.extend(['--{}'.format(arg.replace('_', '-')), args[arg]])

    cmd.extend([idf])   

    if verbosity == 'v':
        subprocess.check_call(cmd)
    elif verbosity == 'q':
        subprocess.check_call(cmd, stdout=open(os.devnull, 'w'))

