
New functions
=============


These are recently written functions that have not made it into the main
documentation

Python Lesson: Errors and Exceptions
------------------------------------


When things go wrong in your eppy script, you get "Errors and
Exceptions".

To know more about how this works in python and eppy, take a look at
`Python: Errors and
Exceptions <http://docs.python.org/2/tutorial/errors.html>`__

Setting IDD name
----------------


When you work with Energyplus you are working with **idf** files (files
that have the extension \*.idf). There is another file that is very
important, called the **idd** file. This is the file that defines all
the objects in Energyplus. Esch version of Energyplus has a different
**idd** file.

So eppy needs to know which **idd** file to use. Only one **idd** file
can be used in a script or program. This means that you cannot change
the **idd** file once you have selected it. Of course you have to first
select an **idd** file before eppy can work.

If you use eppy and break the above rules, eppy will raise an exception.
So let us use eppy incorrectly and make eppy raise the exception, just
see how that happens.

First let us try to open an **idf** file without setting an **idd**
file.

.. code:: python

    from eppy import modeleditor 
    from eppy.modeleditor import IDF
    fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
Now let us open file fname1 without setting the **idd** file

.. code:: python

    try:
        idf1 = IDF(fname1)
    except Exception, e:
        raise e

::


    ---------------------------------------------------------------------------
    IDDNotSetError                            Traceback (most recent call last)

    <ipython-input-7-bcc3a85c2348> in <module>()
          2     idf1 = IDF(fname1)
          3 except Exception, e:
    ----> 4     raise e
    

    IDDNotSetError: IDD file needed to read the idf file. Set it using IDF.setiddname(iddfile)


OK. It does not let you do that and it raises an exception

So let us set the **idd** file and then open the idf file

.. code:: python

    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    IDF.setiddname(iddfile)
    idf1 = IDF(fname1)
That worked without raising an exception

Now let us try to change the **idd** file. Eppy should not let you do
this and should raise an exception.

.. code:: python

    try:
        IDF.setiddname("anotheridd.idd")
    except Exception, e:
        raise e    

::


    ---------------------------------------------------------------------------
    IDDAlreadySetError                        Traceback (most recent call last)

    <ipython-input-9-ad7cf0dbde94> in <module>()
          2     IDF.setiddname("anotheridd.idd")
          3 except Exception, e:
    ----> 4     raise e
    

    IDDAlreadySetError: IDD file is set to: ../eppy/resources/iddfiles/Energy+V7_2_0.idd


Excellent!! It raised the exception we were expecting.

Check range for fields
----------------------


The fields of idf objects often have a range of legal values. The
following functions will let you discover what that range is and test if
your value lies within that range

demonstrate two new functions:

-  EpBunch.getrange(fieldname) # will return the ranges for that field
-  EpBunch.checkrange(fieldname) # will throw an exception if the value
   is outside the range


.. code:: python

    from eppy import modeleditor 
    from eppy.modeleditor import IDF
    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
.. code:: python

    # IDF.setiddname(iddfile)# idd ws set further up in this page
    idf1 = IDF(fname1)
.. code:: python

    building = idf1.idfobjects['building'.upper()][0]
    print building

.. parsed-literal::

    
    BUILDING,                 
        Empire State Building,    !- Name
        30.0,                     !- North Axis
        City,                     !- Terrain
        0.04,                     !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullExterior,             !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        6;                        !- Minimum Number of Warmup Days
    


.. code:: python

    print building.getrange("Loads_Convergence_Tolerance_Value")

.. parsed-literal::

    {'maximum<': None, 'minimum': None, 'type': 'real', 'maximum': 0.5, 'minimum>': 0.0}


.. code:: python

    print building.checkrange("Loads_Convergence_Tolerance_Value")

.. parsed-literal::

    0.04


Let us set these values outside the range and see what happens

.. code:: python

    building.Loads_Convergence_Tolerance_Value = 0.6
    from eppy.bunch_subclass import RangeError
    try:
        print building.checkrange("Loads_Convergence_Tolerance_Value")
    except RangeError, e:
        raise e

::


    ---------------------------------------------------------------------------
    RangeError                                Traceback (most recent call last)

    <ipython-input-15-35bb37b39fba> in <module>()
          4     print building.checkrange("Loads_Convergence_Tolerance_Value")
          5 except RangeError, e:
    ----> 6     raise e
    

    RangeError: Value 0.6 is not less or equal to the 'maximum' of 0.5


So the Range Check works

Looping through all the fields in an idf object
-----------------------------------------------


We have seen how to check the range of field in the idf object. What if
you want to do a *range check* on all the fields in an idf object ? To
do this we will need a list of all the fields in the idf object. We can
do this easily by the following line

.. code:: python

    print building.fieldnames

.. parsed-literal::

    ['key', 'Name', 'North_Axis', 'Terrain', 'Loads_Convergence_Tolerance_Value', 'Temperature_Convergence_Tolerance_Value', 'Solar_Distribution', 'Maximum_Number_of_Warmup_Days', 'Minimum_Number_of_Warmup_Days']


So let us use this

.. code:: python

    for fieldname in building.fieldnames:
        print "%s = %s" % (fieldname, building[fieldname])

.. parsed-literal::

    key = BUILDING
    Name = Empire State Building
    North_Axis = 30.0
    Terrain = City
    Loads_Convergence_Tolerance_Value = 0.6
    Temperature_Convergence_Tolerance_Value = 0.4
    Solar_Distribution = FullExterior
    Maximum_Number_of_Warmup_Days = 25
    Minimum_Number_of_Warmup_Days = 6


Now let us test if the values are in the legal range. We know that
"Loads\_Convergence\_Tolerance\_Value" is out of range

.. code:: python

    from eppy.bunch_subclass import RangeError
    for fieldname in building.fieldnames:
        try:
            building.checkrange(fieldname)
            print "%s = %s #-in range" % (fieldname, building[fieldname],)
        except RangeError as e:
            print "%s = %s #-****OUT OF RANGE****" % (fieldname, building[fieldname],)

.. parsed-literal::

    key = BUILDING #-in range
    Name = Empire State Building #-in range
    North_Axis = 30.0 #-in range
    Terrain = City #-in range
    Loads_Convergence_Tolerance_Value = 0.6 #-****OUT OF RANGE****
    Temperature_Convergence_Tolerance_Value = 0.4 #-in range
    Solar_Distribution = FullExterior #-in range
    Maximum_Number_of_Warmup_Days = 25 #-in range
    Minimum_Number_of_Warmup_Days = 6 #-in range


You see, we caught the out of range value

Blank idf file
--------------


Until now in all our examples, we have been reading an idf file from
disk:

-  How do I create a blank new idf file
-  give it a file name
-  Save it to the disk

Here are the steps to do that

.. code:: python

    # some initial steps
    from eppy.modeleditor import IDF
    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    # IDF.setiddname(iddfile) # Has already been set 
    
    # - Let us first open a file from the disk
    fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
    idf_fromfilename = IDF(fname1) # initialize the IDF object with the file name
    
    idf_fromfilename.printidf()

.. parsed-literal::

    
    VERSION,                  
        7.3;                      !- Version Identifier
    
    SIMULATIONCONTROL,        
        Yes,                      !- Do Zone Sizing Calculation
        Yes,                      !- Do System Sizing Calculation
        Yes,                      !- Do Plant Sizing Calculation
        No,                       !- Run Simulation for Sizing Periods
        Yes;                      !- Run Simulation for Weather File Run Periods
    
    BUILDING,                 
        Empire State Building,    !- Name
        30.0,                     !- North Axis
        City,                     !- Terrain
        0.04,                     !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullExterior,             !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        6;                        !- Minimum Number of Warmup Days
    
    SITE:LOCATION,            
        CHICAGO_IL_USA TMY2-94846,    !- Name
        41.78,                    !- Latitude
        -87.75,                   !- Longitude
        -6.0,                     !- Time Zone
        190.0;                    !- Elevation
    


.. code:: python

    # - now let us open a file from the disk differently
    fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
    fhandle = open(fname1, 'r') # open the file for reading and assign it a file handle
    idf_fromfilehandle = IDF(fhandle) # initialize the IDF object with the file handle
    
    idf_fromfilehandle.printidf()

.. parsed-literal::

    
    VERSION,                  
        7.3;                      !- Version Identifier
    
    SIMULATIONCONTROL,        
        Yes,                      !- Do Zone Sizing Calculation
        Yes,                      !- Do System Sizing Calculation
        Yes,                      !- Do Plant Sizing Calculation
        No,                       !- Run Simulation for Sizing Periods
        Yes;                      !- Run Simulation for Weather File Run Periods
    
    BUILDING,                 
        Empire State Building,    !- Name
        30.0,                     !- North Axis
        City,                     !- Terrain
        0.04,                     !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullExterior,             !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        6;                        !- Minimum Number of Warmup Days
    
    SITE:LOCATION,            
        CHICAGO_IL_USA TMY2-94846,    !- Name
        41.78,                    !- Latitude
        -87.75,                   !- Longitude
        -6.0,                     !- Time Zone
        190.0;                    !- Elevation
    


.. code:: python

    # So IDF object can be initialized with either a file name or a file handle
    
    # - How do I create a blank new idf file  
    idftxt = "" # empty string
    from StringIO import StringIO
    fhandle = StringIO(idftxt) # we can make a file handle of a string
    idf_emptyfile = IDF(fhandle) # initialize the IDF object with the file handle
    
    idf_emptyfile.printidf()

.. parsed-literal::

    


It did not print anything. Why should it. It was empty.

What if we give it a string that was not blank

.. code:: python

    # - The string does not have to be blank
    idftxt = "VERSION, 7.3;" # Not an emplty string. has just the version number
    fhandle = StringIO(idftxt) # we can make a file handle of a string
    idf_notemptyfile = IDF(fhandle) # initialize the IDF object with the file handle
    
    idf_notemptyfile.printidf()

.. parsed-literal::

    
    VERSION,                  
        7.3;                      !- Version Identifier
    


Aha !

Now let us give it a file name

.. code:: python

    # - give it a file name
    idf_notemptyfile.idfname = "notemptyfile.idf"
    # - Save it to the disk
    idf_notemptyfile.save()
Let us confirm that the file was saved to disk

.. code:: python

    txt = open("notemptyfile.idf", 'r').read()# read the file from the disk
    print txt
Yup ! that file was saved. Let us delete it since we were just playing

.. code:: python

    import os
    os.remove("notemptyfile.idf")
Deleting idfobjects
-------------------


There are two ways of deleting idf objects. We'll show how both of them
work.

Sirst let us build up a file we can work with.

.. code:: python

    
.. code:: python

    