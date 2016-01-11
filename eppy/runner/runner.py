# Copyright (c) 2016 Jamie Bull
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
import pydoc

from eppy.modeleditor import IDF4

from eppy.runner.run_functions import run


def wrappedHelpText(wrappedFunc):
    def decorator(f):
        f.__doc__ = ('This method wraps the following method:\n\n' +
                     pydoc.text.document(wrappedFunc))
        return f
    return decorator


class IDF5(IDF4):

    """Subclass of IDF used to carry out simulation runs.
    """

    def __init__(self, idf, epw):
        """
        Parameters
        ----------
        idf : file or file-like object
            The IDF object to run.
        epw : str
            File path to the EPW file to use.

        """
        super(IDF4, self).__init__(idf)
        self.idf = idf
        self.epw = epw

    @wrappedHelpText(run)
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
