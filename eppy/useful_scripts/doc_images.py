# Copyright (c) 2012 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================

"""images for documentation"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from IPython.display import Image
from IPython.display import (
    display_pretty,
    display_html,
    display_jpeg,
    display_png,
    display_json,
    display_latex,
    display_svg,
)

import os

print("---***---", os.getcwd(), "---***---")
try:
    filemerge = Image(filename="../docs/images/filemerge.png")
    plantloop = Image(filename="../docs/images/plantloop.png")
    idfdiff_path = "../docs/images/idfdiff.html"
except FileNotFoundError as e:
    filemerge = Image(filename="../../docs/images/filemerge.png")  # try block
    plantloop = Image(filename="../../docs/images/plantloop.png")
    idfdiff_path = "../../docs/images/idfdiff.html"
