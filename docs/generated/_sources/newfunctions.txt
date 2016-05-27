
New functions
=============


These are recently written functions that have not made it into the main
documentation

Python Lesson: Errors and Exceptions
------------------------------------


.. code:: python

    # you would normaly install eppy by doing
    # python setup.py install
    # or
    # pip install eppy
    # or
    # easy_install eppy
    
    # if you have not done so, uncomment the following three lines
    import sys
    # pathnameto_eppy = 'c:/eppy'
    pathnameto_eppy = '../'
    sys.path.append(pathnameto_eppy) 

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

    <ipython-input-3-44ad2b53d42c> in <module>()
          2     idf1 = IDF(fname1)
          3 except Exception, e:
    ----> 4     raise e
          5 


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

    <ipython-input-5-52df819ac489> in <module>()
          2     IDF.setiddname("anotheridd.idd")
          3 except Exception, e:
    ----> 4     raise e
          5 


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

    {u'maximum<': None, u'minimum': None, u'type': u'real', u'maximum': 0.5, u'minimum>': 0.0}


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

    <ipython-input-11-a824cb1ec673> in <module>()
          4     print building.checkrange("Loads_Convergence_Tolerance_Value")
          5 except RangeError, e:
    ----> 6     raise e
          7 


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

    [u'key', u'Name', u'North_Axis', u'Terrain', u'Loads_Convergence_Tolerance_Value', u'Temperature_Convergence_Tolerance_Value', u'Solar_Distribution', u'Maximum_Number_of_Warmup_Days', u'Minimum_Number_of_Warmup_Days']


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


.. parsed-literal::

    !- Darwin Line endings 
    
    VERSION,                  
        7.3;                      !- Version Identifier


Yup ! that file was saved. Let us delete it since we were just playing

.. code:: python

    import os
    os.remove("notemptyfile.idf")

Deleting, copying/adding and making new idfobjects
--------------------------------------------------


Making a new idf object
~~~~~~~~~~~~~~~~~~~~~~~


Let us start with a blank idf file and make some new "MATERIAL" objects
in it

.. code:: python

    # making a blank idf object
    blankstr = ""
    from StringIO import StringIO
    idf = IDF(StringIO(blankstr))

To make and add a new idfobject object, we use the function
IDF.newidfobject(). We want to make an object of type "MATERIAL"

.. code:: python

    newobject = idf.newidfobject("material".upper()) # the key for the object type has to be in upper case
                                         # .upper() makes it upper case
        
.. code:: python

    print newobject


.. parsed-literal::

    
    MATERIAL,                 
        ,                         !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    


Let us give this a name, say "Shiny new material object"

.. code:: python

    newobject.Name = "Shiny new material object"
    print newobject


.. parsed-literal::

    
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    


.. code:: python

    anothermaterial = idf.newidfobject("material".upper())
    anothermaterial.Name = "Lousy material"
    thirdmaterial = idf.newidfobject("material".upper())
    thirdmaterial.Name = "third material"
    print thirdmaterial


.. parsed-literal::

    
    MATERIAL,                 
        third material,           !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    


Let us look at all the "MATERIAL" objects

.. code:: python

    print idf.idfobjects["MATERIAL"]


.. parsed-literal::

    [
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        Lousy material,           !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        third material,           !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    ]


As we can see there are three MATERIAL idfobjects. They are:

1. Shiny new material object
2. Lousy material
3. third material


Deleting an idf object
~~~~~~~~~~~~~~~~~~~~~~


Let us remove 2. Lousy material. It is the second material in the list.
So let us remove the second material

.. code:: python

    idf.popidfobject('MATERIAL', 1) # first material is '0', second is '1'




.. parsed-literal::

    
    MATERIAL,                 
        Lousy material,           !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance




.. code:: python

    print idf.idfobjects['MATERIAL']


.. parsed-literal::

    [
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        third material,           !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    ]


You can see that the second material is gone ! Now let us remove the
first material, but do it using a different function

.. code:: python

    firstmaterial = idf.idfobjects['MATERIAL'][-1]

.. code:: python

    idf.removeidfobject(firstmaterial)

.. code:: python

    print idf.idfobjects['MATERIAL']


.. parsed-literal::

    [
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    ]


So we have two ways of deleting an idf object:

1. popidfobject -> give it the idf key: "MATERIAL", and the index number
2. removeidfobject -> give it the idf object to be deleted


Copying/Adding an idf object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Having deleted two "MATERIAL" objects, we have only one left. Let us
make a copy of this object and add it to our idf file

.. code:: python

    onlymaterial = idf.idfobjects["MATERIAL"][0]
.. code:: python

    idf.copyidfobject(onlymaterial)
.. code:: python

    print idf.idfobjects["MATERIAL"]

.. parsed-literal::

    [
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    ]


So now we have a copy of the material. You can use this method to copy
idf objects from other idf files too.

Making an idf object with named arguments
-----------------------------------------


What if we wanted to make an idf object with values for it's fields? We
can do that too.

Renaming an idf object
----------------------


.. code:: python

    gypboard = idf.newidfobject('MATERIAL', Name="G01a 19mm gypsum board",
                                Roughness="MediumSmooth",
                                Thickness=0.019,
                                Conductivity=0.16,
                                Density=800,
                                Specific_Heat=1090)
.. code:: python

    print gypboard

.. parsed-literal::

    
    MATERIAL,                 
        G01a 19mm gypsum board,    !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800,                      !- Density
        1090,                     !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    


newidfobject() also fills in the default values like "Thermal
Absorptance", "Solar Absorptance", etc.

.. code:: python

    print idf.idfobjects["MATERIAL"]

.. parsed-literal::

    [
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    , 
    MATERIAL,                 
        G01a 19mm gypsum board,    !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800,                      !- Density
        1090,                     !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    ]


Renaming an idf object
----------------------


It is easy to rename an idf object. If we want to rename the gypboard
object that we created above, we simply say:

    gypboard.Name = "a new name".


But this could create a problem. What if this gypboard is part of a
"CONSTRUCTION" object. The construction object will refer to the
gypboard by name. If we change the name of the gypboard, we should
change it in the construction object.

But there may be many constructions objects using the gypboard. Now we
will have to change it in all those construction objects. Sounds
painfull.

Let us try this with an example:

.. code:: python

    interiorwall = idf.newidfobject("CONSTRUCTION", Name="Interior Wall",
                     Outside_Layer="G01a 19mm gypsum board",
                     Layer_2="Shiny new material object",
                     Layer_3="G01a 19mm gypsum board")
    print interiorwall


.. parsed-literal::

    
    CONSTRUCTION,             
        Interior Wall,            !- Name
        G01a 19mm gypsum board,    !- Outside Layer
        Shiny new material object,    !- Layer 2
        G01a 19mm gypsum board;    !- Layer 3
    


to rename gypboard and have that name change in all the places we call
modeleditor.rename(idf, key, oldname, newname)

.. code:: python

    modeleditor.rename(idf, "MATERIAL", "G01a 19mm gypsum board", "peanut butter")



.. parsed-literal::

    
    MATERIAL,                 
        peanut butter,            !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800,                      !- Density
        1090,                     !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance




.. code:: python

    print interiorwall

.. parsed-literal::

    
    CONSTRUCTION,             
        Interior Wall,            !- Name
        peanut butter,            !- Outside Layer
        Shiny new material object,    !- Layer 2
        peanut butter;            !- Layer 3
    


Now we have "peanut butter" everywhere. At least where we need it. Let
us look at the entir idf file, just to be sure

.. code:: python

    idf.printidf()

.. parsed-literal::

    
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    
    MATERIAL,                 
        Shiny new material object,    !- Name
        ,                         !- Roughness
        ,                         !- Thickness
        ,                         !- Conductivity
        ,                         !- Density
        ,                         !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    
    MATERIAL,                 
        peanut butter,            !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800,                      !- Density
        1090,                     !- Specific Heat
        0.9,                      !- Thermal Absorptance
        0.7,                      !- Solar Absorptance
        0.7;                      !- Visible Absorptance
    
    CONSTRUCTION,             
        Interior Wall,            !- Name
        peanut butter,            !- Outside Layer
        Shiny new material object,    !- Layer 2
        peanut butter;            !- Layer 3
    


Zone area and volume
--------------------


The idf file has zones with surfaces and windows. It is easy to get the
attributes of the surfaces and windows as we have seen in the tutorial.
Let us review this once more:

.. code:: python

    from eppy import modeleditor 
    from eppy.modeleditor import IDF
    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    fname1 = "../eppy/resources/idffiles/V_7_2/box.idf"
    # IDF.setiddname(iddfile)
.. code:: python

    idf = IDF(fname1)
.. code:: python

    surfaces = idf.idfobjects["BuildingSurface:Detailed".upper()]
    surface = surfaces[0]
    print "area = %s" % (surface.area, )
    print "tilt = %s" % (surface.tilt, )
    print "azimuth = %s" % (surface.azimuth, )

.. parsed-literal::

    area = 30.0
    tilt = 180.0
    azimuth = 0.0


Can we do the same for zones ?

Not yet .. not yet. Not in this version on eppy

But we can still get the area and volume of the zone

.. code:: python

    zones = idf.idfobjects["ZONE"]
    zone = zones[0]
    area = modeleditor.zonearea(idf, zone.Name)
    volume = modeleditor.zonevolume(idf, zone.Name)
    print "zone area = %s" % (area, )
    print "zone volume = %s" % (volume, )

.. parsed-literal::

    zone area = 30.0
    zone volume = 90.0


Not as slick, but still pretty easy

Some notes on the zone area calculation:

-  area is calculated by summing up all the areas of the floor surfaces
-  if there are no floors, then the sum of ceilings and roof is taken as
   zone area
-  if there are no floors, ceilings or roof, we are out of luck. The
   function returns 0


Using JSON to update idf
------------------------


we are going to update ``idf1`` using json. First let us print the
``idf1`` before changing it, so we can see what has changed once we make
an update

.. code:: python

    idf1.printidf()

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
        0.6,                      !- Loads Convergence Tolerance Value
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

    import eppy.json_functions as json_functions
    json_str = {"idf.VERSION..Version_Identifier":8.5,
                "idf.SIMULATIONCONTROL..Do_Zone_Sizing_Calculation": "No",
                "idf.SIMULATIONCONTROL..Do_System_Sizing_Calculation": "No",
                "idf.SIMULATIONCONTROL..Do_Plant_Sizing_Calculation": "No",
                "idf.BUILDING.Empire State Building.North_Axis": 52,
                "idf.BUILDING.Empire State Building.Terrain": "Rural",
                }
    json_functions.updateidf(idf1, json_str)
.. code:: python

    idf1.printidf()

.. parsed-literal::

    
    VERSION,                  
        8.5;                      !- Version Identifier
    
    SIMULATIONCONTROL,        
        No,                       !- Do Zone Sizing Calculation
        No,                       !- Do System Sizing Calculation
        No,                       !- Do Plant Sizing Calculation
        No,                       !- Run Simulation for Sizing Periods
        Yes;                      !- Run Simulation for Weather File Run Periods
    
    BUILDING,                 
        Empire State Building,    !- Name
        52,                       !- North Axis
        Rural,                    !- Terrain
        0.6,                      !- Loads Convergence Tolerance Value
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
    


Compare the first printidf() and the second printidf().

The syntax of the json string is described below::

    idf.BUILDING.Empire State Building.Terrain": "Rural"
    
    The key fields are seperated by dots. Let us walk through each field:
    
    idf -> make a change to the idf. (in the future there may be changes that are not related to idf)
    BUILDING -> the key for object to be changed
    Empire State Building -> The name of the object. In other word - the value of the field `Name`
    Terrain -> the field to be changed
    
    "Rural" -> the new value of the field
    
    If the object does not have a `Name` field, you leave a blank between the two dots and the first object will be changed. 
    This is done for the version number change.
    
    "idf.VERSION..Version_Identifier":8.5

You can also create a new object using JSON, using the same syntax. Take
a look at this:

.. code:: python

    json_str = {"idf.BUILDING.Taj.Terrain": "Rural",}
    json_functions.updateidf(idf1, json_str)
    idf1.idfobjects['building'.upper()]



.. parsed-literal::

    [
    BUILDING,                 
        Empire State Building,    !- Name
        52,                       !- North Axis
        Rural,                    !- Terrain
        0.6,                      !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullExterior,             !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        6;                        !- Minimum Number of Warmup Days
    , 
    BUILDING,                 
        Taj,                      !- Name
        0.0,                      !- North Axis
        Rural,                    !- Terrain
        0.04,                     !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullExterior,             !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        6;                        !- Minimum Number of Warmup Days
    ]



**Note** When you us the json update function:

-  The json function expects the ``Name`` field to have a value.
-  If you try to update an object with a blank ``Name`` field, the
   results may be unexpected (undefined ? :-). So don't do this.
-  If the object has no ``Name`` field (some don't), changes are made to
   the first object in the list. Which should be fine, since usually
   there is only one item in the list
-  In any case, if the object does not exist, it is created with the
   default values


Use Case for JSON update
~~~~~~~~~~~~~~~~~~~~~~~~


If you have an eppy running on a remote server somewhere on the
internet, you can change an idf file by sending it a JSON over the
internet. This is very useful if you ever need it. If you don't need it,
you shouldn't care :-)
