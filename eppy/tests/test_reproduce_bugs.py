import os
import shutil

import pytest

from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy.runner.run_functions import paths_from_version, EnergyPlusRunError

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, "resources")

IDD_FILES = os.path.join(RESOURCES_DIR, "iddfiles")
IDF_FILES = os.path.join(RESOURCES_DIR, "idffiles")


@pytest.mark.xfail
def test_reproduce_run_issue():
    """This is for use as a debugging tool.

    Add the files used in the run as reported/provided by a user.
    Make any additional changes required for reproducing/diagnosing the issue.
    """
    # update the following four lines if necessary
    ep_version = "8-9-0"
    idffile = "V8_9/smallfile.idf"
    iddfile = "Energy+V8_9_0.idd"
    epwfile = "USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"

    _, eplus_home = paths_from_version(ep_version)
    idfname = os.path.join(IDF_FILES, idffile)
    iddfile = os.path.join(IDD_FILES, iddfile)
    epwfile = os.path.join(eplus_home, "WeatherData", epwfile)
    modeleditor.IDF.setiddname(iddfile, testing=True)
    idf = IDF(idfname, epwfile)
    # make any changes to the IDF here
    try:
        # Add any additional `run` kwargs here
        # `ep_version` kwarg is required due to buggy test isolation
        idf.run(output_directory="test_dir", ep_version=ep_version)
        # Add any tests for expected/unexpected outputs here
    except Exception:
        # Add any tests for expected/unexpected exceptions here
        raise
    finally:
        shutil.rmtree("test_dir", ignore_errors=True)
