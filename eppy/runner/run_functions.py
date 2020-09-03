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
from subprocess import CalledProcessError, check_call
import sys
import tempfile

from io import StringIO

try:
    import multiprocessing as mp
except ImportError:
    pass


def install_paths(version=None, iddname=None):
    """Get the install paths for EnergyPlus executable and weather files.

    We prefer to get the install path from the IDD name but fall back to
    getting it from the version number for backwards compatibility and to
    simplify tests.

    Parameters
    ----------
    version : str, optional
        EnergyPlus version in the format "X-X-X", e.g. "8-7-0".
    iddname : str, optional
        File path to the IDD.

    Returns
    -------
    eplus_exe : str
        Full path to the EnergyPlus executable.
    eplus_weather : str
        Full path to the EnergyPlus weather directory.

    """
    try:
        eplus_exe, eplus_home = paths_from_iddname(iddname)
    except (AttributeError, TypeError, ValueError):
        eplus_exe, eplus_home = paths_from_version(version)
    eplus_weather = os.path.join(eplus_home, "WeatherData")

    return eplus_exe, eplus_weather


def paths_from_iddname(iddname):
    """Get the EnergyPlus install directory and executable path.

    Parameters
    ----------
    iddname : str, optional
        File path to the IDD.

    Returns
    -------
    eplus_exe : str
        Full path to the EnergyPlus executable.
    eplus_home : str
        Full path to the EnergyPlus install directory.

    Raises
    ------
    AttributeError (TypeError on Windows)
        If iddname does not have a directory component (e.g. if None).
    ValueError
        If eplus_exe is not a file.

    """
    eplus_home = os.path.abspath(os.path.dirname(iddname))
    if platform.system() == "Windows":
        eplus_exe = os.path.join(eplus_home, "energyplus.exe")
    elif platform.system() == "Linux":
        eplus_exe = os.path.join(eplus_home, "energyplus")
    else:
        eplus_exe = os.path.join(eplus_home, "energyplus")
    if not os.path.isfile(eplus_exe):
        raise ValueError
    return eplus_exe, eplus_home


def paths_from_version(version):
    """Get the EnergyPlus install directory and executable path.

    Parameters
    ----------
    version : str, optional
        EnergyPlus version in the format "X-X-X", e.g. "8-7-0".

    Returns
    -------
    eplus_exe : str
        Full path to the EnergyPlus executable.
    eplus_home : str
        Full path to the EnergyPlus install directory.

    """
    if platform.system() == "Windows":
        eplus_home = "C:/EnergyPlusV{version}".format(version=version)
        eplus_exe = os.path.join(eplus_home, "energyplus.exe")
    elif platform.system() == "Linux":
        eplus_home = "/usr/local/EnergyPlus-{version}".format(version=version)
        eplus_exe = os.path.join(eplus_home, "energyplus")
    else:
        eplus_home = "/Applications/EnergyPlus-{version}".format(version=version)
        eplus_exe = os.path.join(eplus_home, "energyplus")
    return eplus_exe, eplus_home


def wrapped_help_text(wrapped_func):
    """Decorator to pass through the documentation from a wrapped function."""

    def decorator(wrapper_func):
        """The decorator.

        Parameters
        ----------
        f : callable
            The wrapped function.

        """
        wrapper_func.__doc__ = (
            "This method wraps the following method:\n\n"
            + pydoc.text.document(wrapped_func)
        )
        return wrapper_func

    return decorator


def runIDFs(jobs, processors=1):
    """Wrapper for run() to be used when running IDF5 runs in parallel.

    Parameters
    ----------
    jobs : iterable
        A list or generator made up of an IDF5 object and a kwargs dict
        (see `run_functions.run` for valid keywords).
    processors : int, optional
        Number of processors to run on (default: 1). If 0 is passed then
        the process will run on all CPUs, -1 means one less than all CPUs, etc.

    """
    if processors <= 0:
        processors = max(1, mp.cpu_count() - processors)

    shutil.rmtree("multi_runs", ignore_errors=True)
    os.mkdir("multi_runs")

    prepared_runs = (
        prepare_run(run_id, run_data) for run_id, run_data in enumerate(jobs)
    )
    try:
        pool = mp.Pool(processors)
        pool.map(multirunner, prepared_runs)
        pool.close()
    except NameError:
        # multiprocessing not present so pass the jobs one at a time
        for job in prepared_runs:
            multirunner([job])
    shutil.rmtree("multi_runs", ignore_errors=True)


def prepare_run(run_id, run_data):
    """Prepare run inputs for one of multiple EnergyPlus runs.

    :param run_id: An ID number for naming the IDF.
    :param run_data: Tuple of the IDF and keyword args to pass to EnergyPlus executable.
    :return: Tuple of the IDF path and EPW, and the keyword args.
    """
    idf, kwargs = run_data
    epw = idf.epw
    idf_dir = os.path.join("multi_runs", "idf_%i" % run_id)
    os.mkdir(idf_dir)
    idf_path = os.path.join(idf_dir, "in.idf")
    idf.saveas(idf_path)
    return (idf_path, epw), kwargs


def multirunner(args):
    """Wrapper for run() to be used when running IDF and EPW runs in parallel.

    Parameters
    ----------
    args : list
        A list made up of a two-item list (IDF and EPW) and a kwargs dict.

    """
    run(*args[0], **args[1])


def run(
    idf=None,
    weather=None,
    output_directory="",
    annual=False,
    design_day=False,
    idd=None,
    epmacro=False,
    expandobjects=False,
    readvars=False,
    output_prefix=None,
    output_suffix=None,
    version=False,
    verbose="v",
    ep_version=None,
):
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
    verbose = args.pop("verbose")
    idf = args.pop("idf")
    iddname = args.get("idd")
    if not isinstance(iddname, str):
        args.pop("idd")
    try:
        idf_path = os.path.abspath(idf.idfname)
    except AttributeError:
        idf_path = os.path.abspath(idf)
    if not os.path.isfile(idf_path):
        raise EnergyPlusRunError(
            "ERROR: Could not find input data file: {}".format(idf_path)
        )
    if not expandobjects:
        with open(idf_path, "r") as f:
            args["expandobjects"] = "HVACTEMPLATE:" in f.read().upper()
    ep_version = args.pop("ep_version")
    # get version from IDF object or by parsing the IDF file for it
    if not ep_version:
        try:
            ep_version = "-".join(str(x) for x in idf.idd_version[:3])
        except AttributeError:
            raise AttributeError(
                "The ep_version must be set when passing an IDF path. \
                Alternatively, use IDF.run()"
            )

    eplus_exe_path, eplus_weather_path = install_paths(ep_version, iddname)
    if version:
        # just get EnergyPlus version number and return
        cmd = [eplus_exe_path, "--version"]
        check_call(cmd)
        return

    # convert paths to absolute paths if required
    if os.path.isfile(args["weather"]):
        args["weather"] = os.path.abspath(args["weather"])
    else:
        args["weather"] = os.path.join(eplus_weather_path, args["weather"])
    output_dir = os.path.abspath(args["output_directory"])
    args["output_directory"] = output_dir

    # store the directory we start in
    cwd = os.getcwd()
    run_dir = os.path.abspath(tempfile.mkdtemp())
    os.chdir(run_dir)

    # build a list of command line arguments
    cmd = [eplus_exe_path]
    for arg in args:
        if args[arg]:
            if isinstance(args[arg], bool):
                args[arg] = ""
            cmd.extend(["--{}".format(arg.replace("_", "-"))])
            if args[arg] != "":
                cmd.extend([args[arg]])
    cmd.extend([idf_path])

    # send stdout to tmp filehandle to avoid issue #245
    tmp_err = StringIO()
    sys.stderr = tmp_err
    try:
        if verbose == "v":
            print("\r\n" + " ".join(cmd) + "\r\n")
            check_call(cmd)
        elif verbose == "q":
            check_call(cmd, stdout=open(os.devnull, "w"))
    except CalledProcessError:
        message = parse_error(tmp_err, output_dir)
        raise EnergyPlusRunError(message)
    finally:
        sys.stderr = sys.__stderr__
        os.chdir(cwd)
    return "OK"


def parse_error(tmp_err, output_dir):
    """Add contents of stderr and eplusout.err and put it in the exception message.

    :param tmp_err: file-like
    :param output_dir: str
    :return: str
    """
    std_err = tmp_err.getvalue()
    err_file = os.path.join(output_dir, "eplusout.err")
    if os.path.isfile(err_file):
        with open(err_file, "r") as f:
            ep_err = f.read()
    else:
        ep_err = "<File not found>"
    message = "\r\n{std_err}\r\nContents of EnergyPlus error file at {err_file}\r\n{ep_err}".format(
        **locals()
    )
    return message


class EnergyPlusRunError(Exception):
    pass
