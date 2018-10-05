import os
import shutil
from subprocess import CalledProcessError

from eppy.modeleditor import IDF
from eppy.runner.run_functions import paths_from_version

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, 'resources')

IDD_FILES = os.path.join(RESOURCES_DIR, 'iddfiles')
IDF_FILES = os.path.join(RESOURCES_DIR, 'idffiles')


def test_reproduce_i204():
    iddfile = os.path.join(IDD_FILES, "Energy+V8_9_0.idd")
    IDF.setiddname(iddfile)
    idfname = os.path.join(IDF_FILES, "V8_9/AirCooledElectricChiller.idf")
    _, eplus_home = paths_from_version("8-9-0")
    epwfile = os.path.join(eplus_home, "WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw")
    idf = IDF(idfname, epwfile)
    output_dir = "test_dir"
    try:
        idf.run(output_directory=output_dir)
        assert False, "expected error not raised"
    except CalledProcessError:
        pass
    finally:
        shutil.rmtree(output_dir, ignore_errors=True)
