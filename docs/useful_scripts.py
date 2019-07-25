from subprocess import call
import os

# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <headingcell level=1>

# Useful Scripts

# <headingcell level=2>

# Location of the scripts

# <markdowncell>

# Here are some scripts that you may find useful. They are in the folder "./eppy/useful_scripts"

# <markdowncell>

# And now for some housekeeping before we start off

# <codecell>

import os

os.chdir("../eppy/useful_scripts")
# changes directory, so we are where the scripts are located

# <codecell>

# you would normaly install eppy by doing
# python setup.py install
# or
# pip install eppy
# or
# easy_install eppy

# if you have not done so, the following three lines are needed
import sys

# pathnameto_eppy = 'c:/eppy'
pathnameto_eppy = "../../"
sys.path.append(pathnameto_eppy)

# <markdowncell>

# If you look in the folder "./eppy/useful_scripts", you fill find the following scripts
#
# The scripts are:
#
#     - eppy_version.py
#     - idfdiff.py
#     - loopdiagram.py
#     - eppyreadtest_folder.py
#     - eppyreadtest_file.py
#

# <headingcell level=2>

# eppy_version.py

# <markdowncell>

# Many scripts will print out some help information, if you use the --help option. Let us try that

# <codecell>

# %%bash
# ignore the line above. It simply lets me run a command line from ipython notebook
os.system("python eppy_version.py --help")

# <markdowncell>

# That was useful !
#
# Now let us try running the program

# <codecell>

# %%bash
# ignore the line above. It simply lets me run a command line from ipython notebook
os.system("python eppy_version.py")

# <headingcell level=2>

# Redirecting output to a file

# <markdowncell>

# Most scripts will print the output to a terminal. Sometimes we want to send the output to a file, so that we can save it for posterity. We can do that py using ">" with the filename after that. For eppy_version.py, it will look like this:

# <rawcell>

# python eppy_version.py > save_output.txt

# <markdowncell>

# Some of the following scripts will generate csv or html outputs. We can direct the output to a file with .html extension and open it in a browser

# <headingcell level=2>

# Compare two idf files - idfdiff.py

# <markdowncell>

# This script will compare two idf files. The results will be displayed printed in "csv" format or in "html" format.

# <markdowncell>

# You would run the script from the command line. This would be the terminal on Mac or unix, and the dos prompt on windows. Let us look at the help for this script, by typing:

# <codecell>

# %%bash
# ignore the line above. It simply lets me run a command line from ipython notebook
os.system("python idfdiff.py -h")

# <markdowncell>

# Now let us try this with two "idf" files that are slightly different. If we open them in a file comparing software, it would look like this:

# <codecell>

from eppy.useful_scripts import (
    doc_images,
)  # no need to know this code, it just shows the image below

for_images = doc_images
for_images.display_png(for_images.filemerge)  # display the image below

# <markdowncell>

# There are 4 differences between the files. Let us see what idfdiff.py does with the two files. We will use the --html option to print out the diff in html format.

# <codecell>

# %%bash
# python idfdiff.py idd file1 file2
os.system(
    "python idfdiff.py --html ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constructions.idf ../resources/idffiles/V_7_2/constructions_diff.idf"
)

# <rawcell>

# reprinting the output again for clarity:
#
# <html><p>file1 = ../resources/idffiles/V_7_2/constructions.idf</p><p>file2 = ../resources/idffiles/V_7_2/constructions_diff.idf</p><table border="1"><tr><th>Object Key</th><th> Object Name</th><th> Field Name</th><th> file1</th><th> file2</th></tr><tr><td>MATERIAL</td><td>F08 Metal surface</td><td></td><td>not here</td><td>is here</td></tr><tr><td>MATERIAL</td><td>F08 Metal surface haha</td><td></td><td>is here</td><td>not here</td></tr><tr><td>MATERIAL</td><td>G05 25mm wood</td><td>Conductivity</td><td>0.15</td><td>0.155</td></tr><tr><td>CONSTRUCTION</td><td>Exterior Door</td><td>Outside Layer</td><td>F08 Metal surface</td><td>F08 Metal surface haha</td></tr></table></html>

# <markdowncell>

# It does look like html :-). We need to redirect this output to a file and then open the file  in a browser to see what it looks like. Displayed below is the html file

# <codecell>

from eppy.useful_scripts import (
    doc_images,
)  # no need to know this code, it just shows the image below
from IPython.display import HTML

h = HTML(open(doc_images.idfdiff_path, "r").read())
h

# <markdowncell>

# Pretty straight forward. Scroll up and look at the origin text files, and see how idfdiff.py understands the difference

# <markdowncell>

# Now let us try the same thin in csv format

# <codecell>

# %%bash
# python idfdiff.py idd file1 file2
os.system(
    "python idfdiff.py --csv ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff.idf"
)

# <markdowncell>

# We see the same output, but now in csv format. You can redirect it to a ".csv" file and open it up as a spreadsheet

# <headingcell level=2>

# loopdiagram.py

# <markdowncell>

# This script will draw all the loops in an idf file. It is a bit of a hack. So it will work on most files, but sometimes it will not :-(. But it is pretty useful when it works.
#
# If it does not work, send us the idf file and we'll try to fix the code
#
# Make sure [grapphviz](http://www.research.att.com/sw/tools/graphviz/) is installed for this script to work
#
# Again, we'll have to run the script from the terminal. Let us look at the help for this script

# <codecell>

# %%bash
# ignore the line above. It simply lets me run a command line from ipython notebook
os.system("python loopdiagram.py --help")

# <markdowncell>

# Pretty straightforward. Simply open png file and you will see the loop diagram. (ignore the dot file for now. it will be documented later)
#
# So let us try this out with and simple example file. We have a very simple plant loop in "../resources/idffiles/V_7_2/plantloop.idf"

# <codecell>

# %%bash
# ignore the line above. It simply lets me run a command line from ipython notebook
os.system(
    "python loopdiagram.py ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/plantloop.idf"
)

# <markdowncell>

# The script prints out it's progress. On larger files, this might take a few seconds. If we open this file, it will look like the diagram below
#
# *Note: the supply and demnd sides are not connected in the diagram, but shown seperately for clarity*

# <codecell>

from eppy.useful_scripts import (
    doc_images,
)  # no need to know this code, it just shows the image below

for_images = doc_images
for_images.display_png(for_images.plantloop)  # display the image below

# <markdowncell>

# That diagram is not a real system. Does this script really work ?
#
# Try it yourself. Draw the daigram for "../resources/idffiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlow.idf"

# <headingcell level=2>

# eppyreadtest_folder.py

# <markdowncell>

# Not yet documented

# <headingcell level=2>

# eppyreadtest_file.py

# <markdowncell>

# Not yet documented


os.chdir("../../docs")
