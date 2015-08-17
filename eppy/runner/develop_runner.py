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

import os
import shutil
import tempfile
import unittest

from eppy.modeleditor import IDF4

from eppy.runner import config
from eppy.runner.functions import run


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


class IDF5(IDF4):
    """Class to handle a run.
    """
    
    def __init__(self, idf, epw):
        """
        Parameters
        ----------
        idf : file object
            The IDF object to run.
        epw : str
            File path to the EPW file to use.
            
        """
        super(IDF4, self).__init__(idf)
        self.idf = idf
        self.epw = os.path.join(config.EPLUS_WEATHER, epw)
        
    def run(self, **kwargs):
        """
        Run an IDF file with a given EnergyPlus weather file. This is a
        wrapper for the EnergyPlus cli.
        
        Parameters
        ----------
        **kwargs
            See eppy.runner.functions.run()
            
        Returns
        -------
        Results in some form? Exit code? Path to results?
    
        """
        # get the current working directory
        cwd = os.getcwd()
        # create a temp directory for the run
        self.tmpdir = tempfile.mkdtemp()

        # write the IDF to the temp directory
        idf_path = os.path.join(self.tmpdir, 'in.idf')
        self.saveas(idf_path)
        # run EnergyPlus
        run(idf_path, self.epw, run_directory=self.tmpdir, **kwargs)
        # what to do with the results?
        # reset cwd
        os.chdir(cwd)
        shutil.rmtree('results', ignore_errors=True)
        shutil.move(self.tmpdir, 'results')

        
def find_eplus_dir():
    """Locate the directory which contains the EnergyPlus install directory.
    
    Returns
    -------
    str

    """
    pass


class TestRunner(unittest.TestCase):


    def setUp(self):
        """Get an IDF object to run
        """
        self.cwd = os.getcwd()
        outdir = os.path.join(self.cwd, 'results')
        if os.path.isdir(outdir):
            shutil.rmtree(outdir)
        iddfile = "../resources/iddfiles/Energy+V8_3_0.idd"
        fname1 = "../resources/idffiles/V8_3/smallfile.idf"
        epw = 'USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw'
        IDF5.setiddname(open(iddfile, 'r'), testing=True)
        self.idf = IDF5(open(fname1, 'r'), epw)
        
    def tearDown(self):
        """Destroy temp dir, copy outputs to check on, reset working directory.
        """
        shutil.rmtree(self.idf.tmpdir, ignore_errors=True)
        os.chdir(self.cwd)
                

    def testRun(self):
        """End to end test of idf.run function.
        """
        self.idf.run(expandobjects=False, readvars=False)

    def testRunReadVars(self):
        """End to end test of idf.run function with readvars set to True.
        """
        self.idf.run(expandobjects=False, readvars=True)
        
