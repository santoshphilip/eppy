# Copyright (c) 2015 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from StringIO import StringIO
import unittest

from eppy.modeleditor import IDF


class ActiveRuns(object):
    """
    This should be multiprocessing-enabled, perhaps an extension of `pool`
    which keeps track of active runs. It should therefore be a singleton since
    only one pool should exist for a system.
    
    This really belongs in a supervisor module but for practicalities of
    development let's keep it here.
    
    """
    
    def __init__(self):
        pass


def run(idf, epw):
    """
    Run and IDF file with a given EnergyPlus weather file. If this is added
    as a method by an IDF instance from the main part of Eppy then it should be
    possible to run this using idf.run('my_weather.epw') since the IDF will be
    passed as the first parameter (e.g. self).
    
    Parameters
    ----------
    idf : eppy.IDF
        The IDF file to be run.
    epw : str
        Path to an EPW file.
    
    Returns
    -------
    Results in some form? Exit code? Path to results?

    """
    # create a temp directory for the run
    # write the IDF to the temp directory
    # run EnergyPlus
    # what to do with the results?


def find_eplus_dir():
    """Locate the directory which contains the EnergyPlus install directory.
    
    Returns
    -------
    str

    """
    pass


class TestRunner(unittest.TestCase):


    def setUp(self):
        """get an IDF object to run
        """
        idftxt = """
            Version,8.1;
            Timestep,4;
            Building,None,0.0000000E+00,Suburbs,0.04,0.40,FullInteriorAndExterior,25,6;
            GlobalGeometryRules,UpperLeftCorner,CounterClockWise,World;
            Site:Location,DENVER_STAPLETON_CO_USA_WMO_724690,39.77,-104.87,-7.00,1611.00;
            SizingPeriod:DesignDay,DENVER_STAPLETON Ann Htg 99.6% Condns DB, 12, 21, WinterDesignDay, -20, 0.0, , , Wetbulb, -20, , , , , 83411., 2.3, 180, No, No, No, ASHRAEClearSky, , , , , 0.00;
            SizingPeriod:DesignDay,DENVER_STAPLETON Ann Clg .4% Condns DB=>MWB, 7, 21, SummerDesignDay, 34.1, 15.2, , , Wetbulb, 15.8, , , , , 83411., 4, 120, No, No, No, ASHRAEClearSky, , , , , 1.00;
            RunPeriod,, 1, 1, 12, 31, Tuesday, Yes, Yes, No, Yes, Yes;
            SimulationControl,No, No, No, Yes, No;
            Output:Variable,*,Site Diffuse Solar Radiation Rate per Area,Timestep;
            """
        IDF.setiddname('./eppy/resources/iddfiles/Energy+V8_1_0.idd')
        self.idf = IDF(StringIO(idftxt))
    
    def tearDown(self):
        """destroy temp dir
        """

    def testRun(self):
        """end to end test of idf.run function
        """
        self.idf.run('')
