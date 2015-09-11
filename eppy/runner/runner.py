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
import tempfile

from eppy.modeleditor import IDF4
from eppy.runner import config
from eppy.runner.functions import run


class IDF5(IDF4):
    """Subclass of IDF used to carry out simulation runs.
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
        if os.path.isfile(epw):
            self.epw = os.path.abspath(epw)
        else:
            self.epw = os.path.join(config.EPLUS_WEATHER, epw)
        
    def run(self, **kwargs):
        """
        Run an IDF file with a given EnergyPlus weather file. This is a
        wrapper for the EnergyPlus command line interface.
        
        Parameters
        ----------
        **kwargs
            See eppy.runner.functions.run()
            
        """
        if 'version' in kwargs:
            # just get EnergyPlus version number and return
            run(version=kwargs['version'])
            return
        # get the current working directory
        cwd = os.getcwd()
        if 'run_directory' in kwargs:
            self.rundir = kwargs.pop('run_directory')
            os.mkdir(self.rundir)
        else:
            # create a temp directory for the run
            self.tmpdir = tempfile.mkdtemp()
            self.rundir = self.tmpdir
        # write the IDF to the temp directory
        idf_path = os.path.join(self.rundir, 'in.idf')
        self.saveas(idf_path)
        # run EnergyPlus
        if 'output_directory' not in kwargs:
            kwargs['output_directory'] = 'run_outputs'
        run(idf_path, self.epw, run_directory=self.rundir, **kwargs)
        # reset cwd
        os.chdir(cwd)
