# Copyright (c) 2016 Jamie Bull
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
import platform
import pydoc
import shutil
from subprocess import CalledProcessError
from subprocess import check_call
import tempfile

try:
    import multiprocessing as mp
except ImportError:
    pass


def install_paths(version):
    """Get the install paths for EnergyPlus executable and weather files.
    """
    if platform.system() == 'Windows':
        eplus_home = "C:/EnergyPlusV{version}".format(**locals())
        eplus_exe = os.path.join(eplus_home, 'energyplus.exe')
    elif platform.system() == "Linux":
        eplus_home = "/usr/local/EnergyPlus-{version}".format(**locals())
        eplus_exe = os.path.join(eplus_home, 'energyplus')
    else:
        eplus_home = "/Applications/EnergyPlus-{version}".format(**locals())
        eplus_exe = os.path.join(eplus_home, 'energyplus')

    eplus_weather = os.path.join(eplus_home, 'WeatherData')

    return eplus_exe, eplus_weather


def wrapped_help_text(wrapped_func):
    """Decorator to pass through the documentation from a wrapped function.
    """
    def decorator(wrapper_func):
        """The decorator.

        Parameters
        ----------
        f : callable
            The wrapped function.

        """
        wrapper_func.__doc__ = ('This method wraps the following method:\n\n' +
                                pydoc.text.document(wrapped_func))
        return wrapper_func
    return decorator


def runIDFs(jobs_list, processors=1):
    """Wrapper for run() to be used when running IDF5 runs in parallel.

    Parameters
    ----------
    jobs_list : list
        A list made up of an IDF5 object and a kwargs dict (see .

    processors : int, optional
        Number of processors to run on (default: 1). If 0 is passed then
        the process will run on all CPUs, -1 means one less than all CPUs, etc.

    """
    if processors <= 0:
        processors = max(1, mp.cpu_count() - processors)

    shutil.rmtree("multi_runs", ignore_errors=True)
    os.mkdir("multi_runs")

    processed_runs = []
    for i, item in enumerate(jobs_list):
        idf = item[0]
        epw = idf.epw
        kwargs = item[1]
        idf_dir = os.path.join('multi_runs', 'idf_%i' % i)
        os.mkdir(idf_dir)
        idf_path = os.path.join(idf_dir, 'in.idf')
        idf.saveas(idf_path)
        processed_runs.append([[idf_path, epw], kwargs])

    try:
        pool = mp.Pool(processors)
        pool.map(multirunner, processed_runs)
        pool.close()
    except NameError:
        # multiprocessing not present so pass the jobs one at a time
        for job in processed_runs:
            multirunner([job])
    shutil.rmtree("multi_runs", ignore_errors=True)


def multirunner(args):
    """Wrapper for run() to be used when running IDF and EPW runs in parallel.

    Parameters
    ----------
    args : list
        A list made up of a two-item list (IDF and EPW) and a kwargs dict.

    """
    run(*args[0], **args[1])


def run(idf=None, weather=None, output_directory='', annual=False,
        design_day=False, idd=None, epmacro=False, expandobjects=False,
        readvars=False, output_prefix=None, output_suffix=None, version=False,
        verbose='v', ep_version=None):
    """
    Wrapper around the EnergyPlus command line interface.

    Parameters
    ----------
    idf : str
        Full or relative path to the IDF file to be run, or an IDF object.

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

    output_prefix : str, optional
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

    ep_version: str
        EnergyPlus version, used to find install directory. Required if run() is
        called with an IDF file path rather than an IDF object.

    Returns
    -------
    str : status

    Raises
    ------
    CalledProcessError

    AttributeError
        If no ep_version parameter is passed when calling with an IDF file path
        rather than an IDF object.


    """
    args = locals().copy()
    # get unneeded params out of args ready to pass the rest to energyplus.exe
    verbose = args.pop('verbose')
    idf = args.pop('idf')
    try:
        idf_path = os.path.abspath(idf.idfname)
    except AttributeError:
        idf_path = os.path.abspath(idf)
    ep_version = args.pop('ep_version')
    # get version from IDF object or by parsing the IDF file for it
    if not ep_version:
        try:
            ep_version = '-'.join(str(x) for x in idf.idd_version[:3])
        except AttributeError:
            raise AttributeError(
                "The ep_version must be set when passing an IDF path. \
                Alternatively, use IDF.run()")
    eplus_exe_path, eplus_weather_path = install_paths(ep_version)
    if version:
        # just get EnergyPlus version number and return
        cmd = [eplus_exe_path, '--version']
        check_call(cmd)
        return

    # convert paths to absolute paths if required
    if os.path.isfile(args['weather']):
        args['weather'] = os.path.abspath(args['weather'])
    else:
        args['weather'] = os.path.join(eplus_weather_path, args['weather'])
    args['output_directory'] = os.path.abspath(args['output_directory'])

    # store the directory we start in
    cwd = os.getcwd()
    run_dir = os.path.abspath(tempfile.mkdtemp())
    os.chdir(run_dir)

    # build a list of command line arguments
    cmd = [eplus_exe_path]
    for arg in args:
        if args[arg]:
            if isinstance(args[arg], bool):
                args[arg] = ''
            cmd.extend(['--{}'.format(arg.replace('_', '-'))])
            if args[arg] != "":
                cmd.extend([args[arg]])
    cmd.extend([idf_path])

    try:
        if verbose == 'v':
            check_call(cmd)
        elif verbose == 'q':
            check_call(cmd, stdout=open(os.devnull, 'w'))
        os.chdir(cwd)
    except CalledProcessError:
        # potentially catch contents of std out and put it in the error
        raise
    return 'OK'
