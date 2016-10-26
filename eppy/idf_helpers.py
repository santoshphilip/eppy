# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""useful functions that should in the class IDF. 
write them here first as a development step.
If they are really useful and don't muddy waters include them in IDF
and remove them here"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import iteritems
from six import StringIO

def idfobjectkeys(idf):
    """returns the object keys in the order they were in the IDD file
    it is an ordered list of idf.idfobjects.keys() 
    keys of a dict are unordered, so idf.idfobjects.keys() will not work for this purpose"""
    return idf.model.dtls