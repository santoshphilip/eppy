# Copyright (c) 2012 Santosh Philip

"""clean up the docs files in this folder"""

import shutil
import os

pth = "./generated"
if os.path.exists(pth):
    shutil.rmtree(pth)
# rm -r ./generated
pth1, pth2 = "./_build/html", "./generated"
if os.path.exists(pth1):
    shutil.move(pth1, pth2)
pth = "./_build"
if os.path.exists(pth):
    shutil.rmtree(pth)
pth = "./_templates"
if os.path.exists(pth):
    shutil.rmtree(pth)
# mv ./_build/html ./generated
# rm -r _build
# rm -r _templates
