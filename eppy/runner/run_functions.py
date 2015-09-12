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

from subprocess import CalledProcessError
import os
import shutil
import subprocess
import tempfile

from runner.config import EPLUS_HOME
import multiprocessing as mp


EPLUS_WEATHER = os.path.join(EPLUS_HOME, 'WeatherData')
EPLUS_EXE = os.path.join(EPLUS_HOME, 'energyplus.exe')
THIS_DIR = os.path.dirname(__file__)


def runIDFs(runs_list, processors=1):
    """Wrapper for run() to be used when running IDF5 runs in parallel.
    
    Parameters
    ----------
    runs_list : list
        A list made up of an IDF5 object and a kwargs dict.
    processors : int, optional
        Number of processors to run on (default: 1). If zero is passed then
        the process will run on all CPUs.
        
    """
    if processors == 0:
        processors = mp.cpu_count()
    shutil.rmtree("multi_runs", ignore_errors=True)
    os.mkdir("multi_runs")
    processed_runs = []
    for i, item in enumerate(runs_list):
        idf = item[0]
        epw = idf.epw
        kwargs = item[1]
        idf_dir = os.path.join('multi_runs', 'idf_%i' % i)
        os.mkdir(idf_dir)
        idf_path = os.path.join(idf_dir, 'in.idf')
        idf.saveas(idf_path)
        processed_runs.append([[idf_path, epw], kwargs])
    pool = mp.Pool(processors)
    pool.map(multirunner, processed_runs)
    pool.close()
    shutil.rmtree("multi_runs", ignore_errors=True)


def multirunner(args):
    """Wrapper for run() to be used when running IDF and EPW runs in parallel.
    
    Parameters
    ----------
    args : list
        A list made up of a two-item list (IDF and EPW) and a kwargs dict.
        
    """
    run(*args[0], **args[1])
    

def run(idf,
        weather,
        output_directory='run_outputs',
        annual=False,
        design_day=False,
        idd=None,
        epmacro=False,
        expandobjects=False,
        readvars=False,
        output_prefix=None,
        output_suffix=None,
        version=False,
        verbose='v'):
    """
    Wrapper around the EnergyPlus command line interface.
    
    Parameters
    ----------
    idf : str
        Full or relative path to the IDF file to be run.
    weather : str
        Full or relative path to the weather file.
    output_directory : str, optional
        Full or relative path to an output directory (default: 'run_outputs)
    annual : bool, optional
        If True then force annual simulation (default: False)
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
    output-prefix : str, optional
        Prefix for output file names (default: eplus)
    output_suffix : str, optional
        Suffix style for output file names (default: L)
            L: Legacy (e.g., eplustbl.csv)
            C: Capital (e.g., eplusTable.csv)
            D: Dash (e.g., eplus-table.csv)
    version : bool, optional
        Display version information (default: False)
    verbose: str
        Set verbosity of runtime messages (default: v)
            v: verbose
            q: quiet
    
    Raises
    ------
    CalledProcessError
    
    """
    args = locals().copy()
    if version:
        # just get EnergyPlus version number and return
        cmd = [EPLUS_EXE, '--version']
        subprocess.check_call(cmd)
        return

    # get unneeded params out of args ready to pass the rest to energyplus.exe
    verbose = args.pop('verbose')
    idf = os.path.abspath(args.pop('idf'))
    # convert paths to absolute paths
    if os.path.isfile(args['weather']):
        args['weather'] = os.path.abspath(args['weather'])
    else:
        args['weather'] = os.path.join(EPLUS_WEATHER, args['weather'])
    args['output_directory'] = os.path.abspath(args['output_directory'])
    
    # store the directory we start in
    cwd = os.getcwd()
    run_dir = os.path.abspath(tempfile.mkdtemp())
    os.chdir(run_dir)

    # build a list of command line arguments
    cmd = [EPLUS_EXE]
    cmd.extend(dict_to_cmd(args))
    cmd.extend([idf])   
    
    try:
        if verbose == 'v':
            subprocess.check_call(cmd)
        elif verbose == 'q':
            subprocess.check_call(cmd, stdout=open(os.devnull, 'w'))
        os.chdir(cwd)
    except CalledProcessError:
        # potentially catch contents of std out and put it in the error
        raise


def dict_to_cmd(args):
    """Replace underscores with hyphens and convert boolean args to flags.
    """
    cmd = []
    for arg in args:
        if args[arg]:
            if isinstance(args[arg], bool): # just add the flag
                cmd.extend(['--{}'.format(arg.replace('_', '-'))])
            else:
                cmd.extend(['--{}'.format(arg.replace('_', '-')), args[arg]])
    return cmd


