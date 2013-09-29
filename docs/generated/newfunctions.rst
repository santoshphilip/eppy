
New functions
=============


These are recently written functions that have not made it into the main
documentation

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

    <ipython-input-4-bcc3a85c2348> in <module>()
          2     idf1 = IDF(fname1)
          3 except Exception, e:
    ----> 4     raise e
    

    IDDNotSetError: IDD file needed to read the idf file. Set it using IDF.setidd(iddfile)


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

    <ipython-input-7-ad7cf0dbde94> in <module>()
          2     IDF.setiddname("anotheridd.idd")
          3 except Exception, e:
    ----> 4     raise e
    

    IDDAlreadySetError: IDD file is set to: ../eppy/resources/iddfiles/Energy+V7_2_0.idd


Excellent!! It rased the exception we were expecting.

Check range for fields
----------------------


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

    <ipython-input-8-35bb37b39fba> in <module>()
          4     print building.checkrange("Loads_Convergence_Tolerance_Value")
          5 except RangeError, e:
    ----> 6     raise e
    

    RangeError: Value 0.6 is not less or equal to the 'maximum' of 0.5


So the Range Check works

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

.. parsed-literal::

    
    VERSION,                  
        7.3;                      !- Version Identifier
    


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

    