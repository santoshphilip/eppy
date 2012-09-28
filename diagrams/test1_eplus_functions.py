"""further py.test for eplus_functions.py"""

from StringIO import StringIO
import sys
sys.path.append('../EPlusInputcode')

import iddV6_0
from EPlusCode.EPlusInterfaceFunctions import readidf

import eplus_functions
import idd_fields
import pytest

    