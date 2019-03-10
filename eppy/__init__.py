# Copyright (c) 2019 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
# -*- coding: utf-8 -*-

"""Top-level package for eppy."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = """Santosh Philip"""
__email__ = 'santosh@noemail.com'
__version__ = '0.5.48'


from six import StringIO
import eppy


def newidf(version=None):
    """open a new idf file
    
    easy way to open a new idf file for particular version. Works only id Energyplus of that version is installed. 
    
    Parameters
    ----------
    version: string
        version of the new file you want to create. Will work only if this version of Energyplus has been installed. 

    Returns
    -------
    idf
       file of type eppy.modelmake.IDF
    """  # noqa: E501
    if not version:
        version = "8.9"
    import eppy.easyopen as easyopen
    idfstring = "  Version,{};".format(str(version))
    fhandle = StringIO(idfstring)
    return easyopen.easyopen(fhandle)
