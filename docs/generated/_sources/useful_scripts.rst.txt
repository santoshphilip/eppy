
Useful Scripts
==============

Location of the scripts
-----------------------

Here are some scripts that you may find useful. They are in the folder
"./eppy/useful\_scripts"

And now for some housekeeping before we start off

.. code:: python

    import os
    os.chdir("../eppy/useful_scripts")
    # changes directory, so we are where the scripts are located

.. code:: python

    # you would normaly install eppy by doing
    # python setup.py install
    # or
    # pip install eppy
    # or
    # easy_install eppy
    
    # if you have not done so, the following three lines are needed
    import sys
    # pathnameto_eppy = 'c:/eppy'
    pathnameto_eppy = '../../'
    sys.path.append(pathnameto_eppy) 


If you look in the folder "./eppy/useful\_scripts", you fill find the
following scripts

The scripts are:

::

    - eppy_version.py
    - idfdiff.py
    - loopdiagram.py
    - eppyreadtest_folder.py
    - eppyreadtest_file.py
        

eppy\_version.py
----------------

Many scripts will print out some help information, if you use the --help
option. Let us try that

.. code:: python

    %%bash
    # ignore the line above. It simply lets me run a command line from ipython notebook
    python eppy_version.py --help


.. parsed-literal::

    usage: eppy_version.py [-h]
    
    I print the current version of eppy. Being polite, I also say hello !
    
    optional arguments:
      -h, --help  show this help message and exit


That was useful !

Now let us try running the program

.. code:: python

    %%bash
    # ignore the line above. It simply lets me run a command line from ipython notebook
    python eppy_version.py


.. parsed-literal::

    Hello! I am  eppy version 0.4.6.4a


Redirecting output to a file
----------------------------

Most scripts will print the output to a terminal. Sometimes we want to
send the output to a file, so that we can save it for posterity. We can
do that py using ">" with the filename after that. For eppy\_version.py,
it will look like this:

python eppy_version.py > save_output.txt

Some of the following scripts will generate csv or html outputs. We can
direct the output to a file with .html extension and open it in a
browser

Compare two idf files - idfdiff.py
----------------------------------

This script will compare two idf files. The results will be displayed
printed in "csv" format or in "html" format.

You would run the script from the command line. This would be the
terminal on Mac or unix, and the dos prompt on windows. Let us look at
the help for this script, by typing:

.. code:: python

    %%bash
    # ignore the line above. It simply lets me run a command line from ipython notebook
    python idfdiff.py -h


.. parsed-literal::

    usage: idfdiff.py [-h] (--csv | --html) idd file1 file2
    
    Do a diff between two idf files. Prints the diff in csv or html file format.
    You can redirect the output to a file and open the file using as a spreadsheet
    or by using a browser
    
    positional arguments:
      idd         location of idd file = ./somewhere/eplusv8-0-1.idd
      file1       location of first with idf files = ./somewhere/f1.idf
      file2       location of second with idf files = ./somewhere/f2.idf
    
    optional arguments:
      -h, --help  show this help message and exit
      --csv
      --html


Now let us try this with two "idf" files that are slightly different. If
we open them in a file comparing software, it would look like this:

.. code:: python

    from eppy.useful_scripts import doc_images #no need to know this code, it just shows the image below
    for_images = doc_images
    for_images.display_png(for_images.filemerge) # display the image below



.. image:: useful_scripts_files/useful_scripts_21_0.png


There are 4 differences between the files. Let us see what idfdiff.py
does with the two files. We will use the --html option to print out the
diff in html format.

.. code:: python

    %%bash
    # python idfdiff.py idd file1 file2
    python idfdiff.py --html ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constructions.idf ../resources/idffiles/V_7_2/constructions_diff.idf 


.. parsed-literal::

    <html><p>file1 = ../resources/idffiles/V_7_2/constructions.idf</p><p>file2 = ../resources/idffiles/V_7_2/constructions_diff.idf</p><table border="1"><tr><th>Object Key</th><th> Object Name</th><th> Field Name</th><th> file1</th><th> file2</th></tr><tr><td>MATERIAL</td><td>F08 Metal surface</td><td></td><td>is here</td><td>not here</td></tr><tr><td>MATERIAL</td><td>F08 Metal surface haha</td><td></td><td>not here</td><td>is here</td></tr><tr><td>MATERIAL</td><td>G05 25mm wood</td><td>Conductivity</td><td>0.15</td><td>0.155</td></tr><tr><td>CONSTRUCTION</td><td>Exterior Door</td><td>Outside Layer</td><td>F08 Metal surface</td><td>F08 Metal surface haha</td></tr></table></html>


reprinting the output again for clarity:

<html><p>file1 = ../resources/idffiles/V_7_2/constructions.idf</p><p>file2 = ../resources/idffiles/V_7_2/constructions_diff.idf</p><table border="1"><tr><th>Object Key</th><th> Object Name</th><th> Field Name</th><th> file1</th><th> file2</th></tr><tr><td>MATERIAL</td><td>F08 Metal surface</td><td></td><td>not here</td><td>is here</td></tr><tr><td>MATERIAL</td><td>F08 Metal surface haha</td><td></td><td>is here</td><td>not here</td></tr><tr><td>MATERIAL</td><td>G05 25mm wood</td><td>Conductivity</td><td>0.15</td><td>0.155</td></tr><tr><td>CONSTRUCTION</td><td>Exterior Door</td><td>Outside Layer</td><td>F08 Metal surface</td><td>F08 Metal surface haha</td></tr></table></html>


It does look like html :-). We need to redirect this output to a file
and then open the file in a browser to see what it looks like. Displayed
below is the html file

.. code:: python

    from eppy.useful_scripts import doc_images #no need to know this code, it just shows the image below
    from IPython.display import HTML
    h = HTML(open(doc_images.idfdiff_path, 'r').read())
    h




.. raw:: html

    <html><p>file1 = ../resources/idffiles/V_7_2/constr.idf</p><p>file2 = ../resources/idffiles/V_7_2/constr_diff.idf</p><table border="1"><tr><th>Object Key</th><th> Object Name</th><th> Field Name</th><th> file1</th><th> file2</th></tr><tr><td>CONSTRUCTION</td><td>CLNG-1</td><td>Outside Layer</td><td>MAT-CLNG-1</td><td>MAT-CLNG-8</td></tr><tr><td>CONSTRUCTION</td><td>GARAGE-SLAB-1</td><td></td><td>is here</td><td>not here</td></tr><tr><td>CONSTRUCTION</td><td>SB-E</td><td></td><td>is here</td><td>not here</td></tr><tr><td>CONSTRUCTION</td><td>SB-U</td><td></td><td>not here</td><td>is here</td></tr><tr><td>OUTPUTCONTROL:TABLE:STYLE</td><td> </td><td>Column Separator</td><td>HTML</td><td>CSV</td></tr></table></html>




Pretty straight forward. Scroll up and look at the origin text files,
and see how idfdiff.py understands the difference

Now let us try the same thin in csv format

.. code:: python

    %%bash
    # python idfdiff.py idd file1 file2
    python idfdiff.py --csv ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/constr.idf ../resources/idffiles/V_7_2/constr_diff.idf


.. parsed-literal::

    file1 = ../resources/idffiles/V_7_2/constr.idf
    file2 = ../resources/idffiles/V_7_2/constr_diff.idf
    
    Object Key, Object Name, Field Name, file1, file2
    CONSTRUCTION,CLNG-1,Outside Layer,MAT-CLNG-1,MAT-CLNG-8
    CONSTRUCTION,GARAGE-SLAB-1,,is here,not here
    CONSTRUCTION,SB-E,,is here,not here
    CONSTRUCTION,SB-U,,not here,is here
    OUTPUTCONTROL:TABLE:STYLE, ,Column Separator,HTML,CSV


We see the same output, but now in csv format. You can redirect it to a
".csv" file and open it up as a spreadsheet

loopdiagram.py
--------------

Diagrams of HVAC loops
~~~~~~~~~~~~~~~~~~~~~~

This script will draw all the loops in an idf file. It is a bit of a
hack. So it will work on most files, but sometimes it will not :-(. But
it is pretty useful when it works.

If it does not work, send us the idf file and we'll try to fix the code

Make sure `grapphviz <http://www.research.att.com/sw/tools/graphviz/>`__
is installed for this script to work

Again, we'll have to run the script from the terminal. Let us look at
the help for this script

.. code:: python

    %%bash
    # ignore the line above. It simply lets me run a command line from ipython notebook
    python loopdiagram.py --help


.. parsed-literal::

    usage: loopdiagram.py [-h] idd file
    
    draw all the  loops in the idf file
    There are two output files saved in the same location as the idf file:
    - idf_file_location/idf_filename.dot
    - idf_file_location/idf_filename.png
    
    positional arguments:
      idd         location of idd file = ./somewhere/eplusv8-0-1.idd
      file        location of idf file = ./somewhere/f1.idf
    
    optional arguments:
      -h, --help  show this help message and exit


Pretty straightforward. Simply open png file and you will see the loop
diagram. (ignore the dot file for now. it will be documented later)

So let us try this out with and simple example file. We have a very
simple plant loop in "../resources/idffiles/V\_7\_2/plantloop.idf"

.. code:: python

    %%bash
    # ignore the line above. It simply lets me run a command line from ipython notebook
    python loopdiagram.py ../resources/iddfiles/Energy+V7_2_0.idd ../resources/idffiles/V_7_2/plantloop.idf


.. parsed-literal::

    constructing the loops
    cleaning edges
    making the diagram
    saved file: ../resources/idffiles/V_7_2/plantloop.dot
    saved file: ../resources/idffiles/V_7_2/plantloop.png


The script prints out it's progress. On larger files, this might take a
few seconds. If we open this file, it will look like the diagram below

*Note: the supply and demnd sides are not connected in the diagram, but
shown seperately for clarity*

.. code:: python

    from eppy.useful_scripts import doc_images #no need to know this code, it just shows the image below
    for_images = doc_images
    for_images.display_png(for_images.plantloop) # display the image below



.. image:: useful_scripts_files/useful_scripts_38_0.png


That diagram is not a real system. Does this script really work ?

Try it yourself. Draw the daigram for
"../resources/idffiles/V\_7\_2/5ZoneCAVtoVAVWarmestTempFlow.idf"

Names in loopdiagrams
~~~~~~~~~~~~~~~~~~~~~

-  `Designbuilder <http://www.designbuilder.co.uk>`__ is an energyplus
   editor autogenerates object names like "MyHouse:SAPZone1"
-  Note the ":" in the name.
-  Unfortunatley ":" is a reserved character when making a loop
   diagrams. (eppy uses pydot and grapphviz which has this constraint)
-  to work around this, loopdiagram will replace all ":" with a "\_\_"
-  So the names in the diagram will not match the names in your file,
   but you can make out what is going on

eppyreadtest\_folder.py
-----------------------

Not yet documented

eppyreadtest\_file.py
---------------------

Not yet documented
