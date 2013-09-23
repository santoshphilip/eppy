
Reading outputs from E+
-----------------------


.. code:: python

    # some initial set up
    # if you have not installed epp, and only downloaded it
    # you will need the following lines
    import sys
    # pathnameto_eppy = 'c:/eppy'
    pathnameto_eppy = '../'
    sys.path.append(pathnameto_eppy) 
| So far we have been making changes to the IDF input file.
| How about looking at the outputs.

Energyplus makes nice htmlout files that look like this.

.. code:: python

    for_images.display_png(for_images.html_snippet) # display the image below


.. image:: Outputs_Tutorial_files/Outputs_Tutorial_3_0.png


| If you look at the clipping of the html file above, you see tables
with data in them.
| Eppy has functions that let you access of these tables and get the
data from any of it's cells.

| Let us say you want to find the "Net Site Energy".
| This is in table "Site and Source Energy".
| The number you want is in the third row, second column and it's value
is "47694.47"

Let us use eppy to txtract this number

.. code:: python

    from eppy import readhtml # the eppy module with functions to read the html
    fname = "../eppy/resources/outputfiles/V_7_2/5ZoneCAVtoVAVWarmestTempFlowTable_ABUPS.html" # the html file you want to read
    filehandle = open(fname, 'r').read() # get a file handle to the html file
    
    
    htables = readhtml.titletable(filehandle) # reads the tables with their titles
| If you open the python file readhtml.py and look at the function
titletable, you can see the function documentation.
| It says the following

.. code:: python

        """return a list of [(title, table), .....]
        title = previous item with a <b> tag
        table = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]"""



.. parsed-literal::

    'return a list of [(title, table), .....]\ntitle = previous item with a <b> tag\ntable = rows -> [[cell1, cell2, ..], [cell1, cell2, ..], ..]'



| The documentation says that it returns a list.
| Let us take a look inside this list. Let us look at the first item in
the list.

.. code:: python

    firstitem = htables[0]
    print firstitem

.. parsed-literal::

    (u'Site and Source Energy', [['', u'Total Energy [kWh]', u'Energy Per Total Building Area [kWh/m2]', u'Energy Per Conditioned Building Area [kWh/m2]'], [u'Total Site Energy', u'    47694.47', u'       51.44', u'       51.44'], [u'Net Site Energy', u'    47694.47', u'       51.44', u'       51.44'], [u'Total Source Energy', u'   140159.10', u'      151.16', u'      151.16'], [u'Net Source Energy', u'   140159.10', u'      151.16', u'      151.16']])


| Ughh !!! that is ugly. Hard to see what it is.
| Let us use a python module to print it pretty

.. code:: python

    import pprint
    pp = pprint.PrettyPrinter()
    pp.pprint(firstitem)

.. parsed-literal::

    (u'Site and Source Energy',
     [['',
       u'Total Energy [kWh]',
       u'Energy Per Total Building Area [kWh/m2]',
       u'Energy Per Conditioned Building Area [kWh/m2]'],
      [u'Total Site Energy', u'    47694.47', u'       51.44', u'       51.44'],
      [u'Net Site Energy', u'    47694.47', u'       51.44', u'       51.44'],
      [u'Total Source Energy', u'   140159.10', u'      151.16', u'      151.16'],
      [u'Net Source Energy', u'   140159.10', u'      151.16', u'      151.16']])


Nice. that is a little clearer

.. code:: python

    firstitem_title = firstitem[0]
    pp.pprint(firstitem_title)

.. parsed-literal::

    u'Site and Source Energy'


.. code:: python

    firstitem_table = firstitem[1]
    pp.pprint(firstitem_table)

.. parsed-literal::

    [['',
      u'Total Energy [kWh]',
      u'Energy Per Total Building Area [kWh/m2]',
      u'Energy Per Conditioned Building Area [kWh/m2]'],
     [u'Total Site Energy', u'    47694.47', u'       51.44', u'       51.44'],
     [u'Net Site Energy', u'    47694.47', u'       51.44', u'       51.44'],
     [u'Total Source Energy', u'   140159.10', u'      151.16', u'      151.16'],
     [u'Net Source Energy', u'   140159.10', u'      151.16', u'      151.16']]


| How do we get to value of "Net Site Energy".
| We know it is in the third row, second column of the table.

Easy.

.. code:: python

    thirdrow = firstitem_table[2] # we start counting with 0. So 0, 1, 2 is third row
    print thirdrow

.. parsed-literal::

    [u'Net Site Energy', u'    47694.47', u'       51.44', u'       51.44']


.. code:: python

    thirdrow_secondcolumn = thirdrow[1]
    thirdrow_secondcolumn



.. parsed-literal::

    u'    47694.47'



| the text from the html table is in unicode.
| That is why you see that weird 'u' letter.

Let us convert it to a floating point number

.. code:: python

    net_site_energy = float(thirdrow_secondcolumn)
    net_site_energy



.. parsed-literal::

    47694.47



Let us have a little fun with the tables.

Get the titles of all the tables

.. code:: python

    alltitles = [htable[0] for htable in htables]
    alltitles



.. parsed-literal::

    [u'Site and Source Energy',
     u'Site to Source Energy Conversion Factors',
     u'Building Area',
     u'End Uses',
     u'End Uses By Subcategory',
     u'Utility Use Per Conditioned Floor Area',
     u'Utility Use Per Total Floor Area',
     u'Electric Loads Satisfied',
     u'On-Site Thermal Sources',
     u'Water Source Summary',
     u'Comfort and Setpoint Not Met Summary',
     u'Comfort and Setpoint Not Met Summary']



Now let us grab the tables with the titles "Building Area" and "Site to
Source Energy Conversion Factors"

.. code:: python

    twotables = [htable for htable in htables if htable[0] in ["Building Area", "Site to Source Energy Conversion Factors"]]
    twotables



.. parsed-literal::

    [(u'Site to Source Energy Conversion Factors',
      [['', u'Site=>Source Conversion Factor'],
       [u'Electricity', u'       3.167'],
       [u'Natural Gas', u'       1.084'],
       [u'District Cooling', u'       1.056'],
       [u'District Heating', u'       3.613'],
       [u'Steam', u'       0.300'],
       [u'Gasoline', u'       1.050'],
       [u'Diesel', u'       1.050'],
       [u'Coal', u'       1.050'],
       [u'Fuel Oil #1', u'       1.050'],
       [u'Fuel Oil #2', u'       1.050'],
       [u'Propane', u'       1.050']]),
     (u'Building Area',
      [['', u'Area [m2]'],
       [u'Total Building Area', u'      927.20'],
       [u'Net Conditioned Building Area', u'      927.20'],
       [u'Unconditioned Building Area', u'        0.00']])]



| Let us leave readtables for now.
| It gives us the basic fucntionality to read any of the tables in the
html output file
