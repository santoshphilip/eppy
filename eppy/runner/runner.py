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

from eppy.modeleditor import IDF4
from eppy.runner.run_functions import run


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
        self.epw = epw
        
    def run(self, **kwargs):
        """
        Run an IDF file with a given EnergyPlus weather file. This is a
        wrapper for the EnergyPlus command line interface.
        
        Parameters
        ----------
        **kwargs
            See eppy.runner.functions.run()
            
        """
        # write the IDF to the current directory
        self.saveas('in.idf')
        # run EnergyPlus
        run('in.idf', self.epw, **kwargs)
        # remove in.idf
        os.remove('in.idf')