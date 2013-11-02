
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
        
OK. It does not let you do that and it raises an exception

So let us set the **idd** file and then open the idf file

.. code:: python

    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    IDF.setiddname(iddfile)
    idf1 = IDF(fname1)


::


    ---------------------------------------------------------------------------
    IDDAlreadySetError                        Traceback (most recent call last)

    <ipython-input-15-e0e181a1b8ca> in <module>()
          1 iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    ----> 2 IDF.setiddname(iddfile)
          3 idf1 = IDF(fname1)


    /Users/santoshphilip/Documents/coolshadow/eppy_git/eppy/eppy/modeleditor.py in setiddname(cls, arg, testing)
        389             if testing == False:
        390                 errortxt = "IDD file is set to: %s"  % (cls.iddname, )
    --> 391                 raise IDDAlreadySetError(errortxt)
        392     @classmethod
        393     def getiddname(cls):


    IDDAlreadySetError: IDD file is set to: ../eppy/resources/iddfiles/Energy+V7_2_0.idd


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

    <ipython-input-16-52df819ac489> in <module>()
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

    <ipython-input-22-a824cb1ec673> in <module>()
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


.. parsed-literal::

    
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
    Material,                 
        F08 Metal surface,        !- Name
        Smooth,                   !- Roughness
        0.0008,                   !- Thickness
        45.28,                    !- Conductivity
        7824.0,                   !- Density
        500.0;                    !- Specific Heat
    , 
    Material,                 
        I01 25mm insulation board,    !- Name
        MediumRough,              !- Roughness
        0.0254,                   !- Thickness
        0.03,                     !- Conductivity
        43.0,                     !- Density
        1210.0;                   !- Specific Heat
    , 
    Material,                 
        I02 50mm insulation board,    !- Name
        MediumRough,              !- Roughness
        0.0508,                   !- Thickness
        0.03,                     !- Conductivity
        43.0,                     !- Density
        1210.0;                   !- Specific Heat
    , 
    Material,                 
        G01a 19mm gypsum board,    !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800.0,                    !- Density
        1090.0;                   !- Specific Heat
    , 
    Material,                 
        M11 100mm lightweight concrete,    !- Name
        MediumRough,              !- Roughness
        0.1016,                   !- Thickness
        0.53,                     !- Conductivity
        1280.0,                   !- Density
        840.0;                    !- Specific Heat
    , 
    Material,                 
        F16 Acoustic tile,        !- Name
        MediumSmooth,             !- Roughness
        0.0191,                   !- Thickness
        0.06,                     !- Conductivity
        368.0,                    !- Density
        590.0;                    !- Specific Heat
    , 
    Material,                 
        M01 100mm brick,          !- Name
        MediumRough,              !- Roughness
        0.1016,                   !- Thickness
        0.89,                     !- Conductivity
        1920.0,                   !- Density
        790.0;                    !- Specific Heat
    , 
    Material,                 
        M15 200mm heavyweight concrete,    !- Name
        MediumRough,              !- Roughness
        0.2032,                   !- Thickness
        1.95,                     !- Conductivity
        2240.0,                   !- Density
        900.0;                    !- Specific Heat
    , 
    Material,                 
        M05 200mm concrete block,    !- Name
        MediumRough,              !- Roughness
        0.2032,                   !- Thickness
        1.11,                     !- Conductivity
        800.0,                    !- Density
        920.0;                    !- Specific Heat
    , 
    Material,                 
        G05 25mm wood,            !- Name
        MediumSmooth,             !- Roughness
        0.0254,                   !- Thickness
        0.15,                     !- Conductivity
        608.0,                    !- Density
        1630.0;                   !- Specific Heat
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

    
    Material,                 
        peanut butter,            !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800.0,                    !- Density
        1090.0;                   !- Specific Heat




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

    
    Version,                  
        7.2;                      !- Version Identifier
    
    SimulationControl,        
        No,                       !- Do Zone Sizing Calculation
        No,                       !- Do System Sizing Calculation
        No,                       !- Do Plant Sizing Calculation
        Yes,                      !- Run Simulation for Sizing Periods
        Yes;                      !- Run Simulation for Weather File Run Periods
    
    Building,                 
        Untitled,                 !- Name
        0.0,                      !- North Axis
        City,                     !- Terrain
        0.04,                     !- Loads Convergence Tolerance Value
        0.4,                      !- Temperature Convergence Tolerance Value
        FullInteriorAndExterior,    !- Solar Distribution
        25,                       !- Maximum Number of Warmup Days
        ;                         !- Minimum Number of Warmup Days
    
    Timestep,                 
        4;                        !- Number of Timesteps per Hour
    
    Site:Location,            
        CHICAGO_IL_USA TMY2-94846,    !- Name
        41.78,                    !- Latitude
        -87.75,                   !- Longitude
        -6.0,                     !- Time Zone
        190.0;                    !- Elevation
    
    RunPeriodControl:SpecialDays,
        New Years Day,            !- Name
        January 1,                !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Veterans Day,             !- Name
        November 11,              !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Christmas,                !- Name
        December 25,              !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Independence Day,         !- Name
        July 4,                   !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        MLK Day,                  !- Name
        3rd Monday in January,    !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Presidents Day,           !- Name
        3rd Monday in February,    !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Memorial Day,             !- Name
        Last Monday in May,       !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Labor Day,                !- Name
        1st Monday in September,    !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Columbus Day,             !- Name
        2nd Monday in October,    !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:SpecialDays,
        Thanksgiving,             !- Name
        4th Thursday in November,    !- Start Date
        1,                        !- Duration
        Holiday;                  !- Special Day Type
    
    RunPeriodControl:DaylightSavingTime,
        2nd Sunday in March,      !- Start Date
        1st Sunday in November;    !- End Date
    
    ScheduleTypeLimits,       
        Any Number;               !- Name
    
    ScheduleTypeLimits,       
        Fraction,                 !- Name
        0.0,                      !- Lower Limit Value
        1.0,                      !- Upper Limit Value
        CONTINUOUS;               !- Numeric Type
    
    ScheduleTypeLimits,       
        Temperature,              !- Name
        -60,                      !- Lower Limit Value
        200,                      !- Upper Limit Value
        CONTINUOUS;               !- Numeric Type
    
    ScheduleTypeLimits,       
        On/Off,                   !- Name
        0,                        !- Lower Limit Value
        1,                        !- Upper Limit Value
        DISCRETE;                 !- Numeric Type
    
    ScheduleTypeLimits,       
        Control Type,             !- Name
        0,                        !- Lower Limit Value
        4,                        !- Upper Limit Value
        DISCRETE;                 !- Numeric Type
    
    ScheduleTypeLimits,       
        Humidity,                 !- Name
        10,                       !- Lower Limit Value
        90,                       !- Upper Limit Value
        CONTINUOUS;               !- Numeric Type
    
    ScheduleTypeLimits,       
        Number;                   !- Name
    
    Schedule:Compact,         
        Office Lights Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays,            !- Field 2
        Until: 05:00,             !- Field 3
        0.05,                     !- Field 4
        Until: 07:00,             !- Field 5
        0.1,                      !- Field 6
        Until: 08:00,             !- Field 7
        0.3,                      !- Field 8
        Until: 17:00,             !- Field 9
        0.9,                      !- Field 10
        Until: 18:00,             !- Field 11
        0.5,                      !- Field 12
        Until: 20:00,             !- Field 13
        0.3,                      !- Field 14
        Until: 22:00,             !- Field 15
        0.2,                      !- Field 16
        Until: 23:00,             !- Field 17
        0.1,                      !- Field 18
        Until: 24:00,             !- Field 19
        0.05,                     !- Field 20
        For: SummerDesignDay,     !- Field 21
        Until: 24:00,             !- Field 22
        1.0,                      !- Field 23
        For: Saturday,            !- Field 24
        Until: 06:00,             !- Field 25
        0.05,                     !- Field 26
        Until: 08:00,             !- Field 27
        0.1,                      !- Field 28
        Until: 12:00,             !- Field 29
        0.3,                      !- Field 30
        Until: 17:00,             !- Field 31
        0.15,                     !- Field 32
        Until: 24:00,             !- Field 33
        0.05,                     !- Field 34
        For: WinterDesignDay,     !- Field 35
        Until: 24:00,             !- Field 36
        0.0,                      !- Field 37
        For: Sunday Holidays AllOtherDays,    !- Field 38
        Until: 24:00,             !- Field 39
        0.05;                     !- Field 40
    
    Schedule:Compact,         
        Office Equipment Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays,            !- Field 2
        Until: 08:00,             !- Field 3
        0.40,                     !- Field 4
        Until: 12:00,             !- Field 5
        0.90,                     !- Field 6
        Until: 13:00,             !- Field 7
        0.80,                     !- Field 8
        Until: 17:00,             !- Field 9
        0.90,                     !- Field 10
        Until: 18:00,             !- Field 11
        0.50,                     !- Field 12
        Until: 24:00,             !- Field 13
        0.40,                     !- Field 14
        For: SummerDesignDay,     !- Field 15
        Until: 24:00,             !- Field 16
        1.0,                      !- Field 17
        For: Saturday,            !- Field 18
        Until: 06:00,             !- Field 19
        0.30,                     !- Field 20
        Until: 08:00,             !- Field 21
        0.4,                      !- Field 22
        Until: 12:00,             !- Field 23
        0.5,                      !- Field 24
        Until: 17:00,             !- Field 25
        0.35,                     !- Field 26
        Until: 24:00,             !- Field 27
        0.30,                     !- Field 28
        For: WinterDesignDay,     !- Field 29
        Until: 24:00,             !- Field 30
        0.0,                      !- Field 31
        For: Sunday Holidays AllOtherDays,    !- Field 32
        Until: 24:00,             !- Field 33
        0.30;                     !- Field 34
    
    Schedule:Compact,         
        Office Occupancy Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays,            !- Field 2
        Until: 06:00,             !- Field 3
        0.0,                      !- Field 4
        Until: 07:00,             !- Field 5
        0.1,                      !- Field 6
        Until: 08:00,             !- Field 7
        0.2,                      !- Field 8
        Until: 12:00,             !- Field 9
        0.95,                     !- Field 10
        Until: 13:00,             !- Field 11
        0.5,                      !- Field 12
        Until: 17:00,             !- Field 13
        0.95,                     !- Field 14
        Until: 18:00,             !- Field 15
        0.3,                      !- Field 16
        Until: 20:00,             !- Field 17
        0.1,                      !- Field 18
        Until: 24:00,             !- Field 19
        0.05,                     !- Field 20
        For: SummerDesignDay,     !- Field 21
        Until: 06:00,             !- Field 22
        0.0,                      !- Field 23
        Until: 22:00,             !- Field 24
        1.0,                      !- Field 25
        Until: 24:00,             !- Field 26
        0.05,                     !- Field 27
        For: Saturday,            !- Field 28
        Until: 06:00,             !- Field 29
        0.0,                      !- Field 30
        Until: 08:00,             !- Field 31
        0.1,                      !- Field 32
        Until: 12:00,             !- Field 33
        0.3,                      !- Field 34
        Until: 17:00,             !- Field 35
        0.1,                      !- Field 36
        Until: 19:00,             !- Field 37
        0.0,                      !- Field 38
        Until: 24:00,             !- Field 39
        0.0,                      !- Field 40
        For: WinterDesignDay,     !- Field 41
        Until: 24:00,             !- Field 42
        0.0,                      !- Field 43
        For: Sunday Holidays AllOtherDays,    !- Field 44
        Until: 06:00,             !- Field 45
        0.0,                      !- Field 46
        Until: 18:00,             !- Field 47
        0.0,                      !- Field 48
        Until: 24:00,             !- Field 49
        0.0;                      !- Field 50
    
    Schedule:Compact,         
        Infiltration Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays SummerDesignDay,    !- Field 2
        Until: 06:00,             !- Field 3
        1.0,                      !- Field 4
        Until: 22:00,             !- Field 5
        0.0,                      !- Field 6
        Until: 24:00,             !- Field 7
        1.0,                      !- Field 8
        For: Saturday WinterDesignDay,    !- Field 9
        Until: 06:00,             !- Field 10
        1.0,                      !- Field 11
        Until: 18:00,             !- Field 12
        0.0,                      !- Field 13
        Until: 24:00,             !- Field 14
        1.0,                      !- Field 15
        For: Sunday Holidays AllOtherDays,    !- Field 16
        Until: 24:00,             !- Field 17
        1.0;                      !- Field 18
    
    Schedule:Compact,         
        Infiltration Half On Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays SummerDesignDay,    !- Field 2
        Until: 06:00,             !- Field 3
        1.0,                      !- Field 4
        Until: 22:00,             !- Field 5
        0.5,                      !- Field 6
        Until: 24:00,             !- Field 7
        1.0,                      !- Field 8
        For: Saturday WinterDesignDay,    !- Field 9
        Until: 06:00,             !- Field 10
        1.0,                      !- Field 11
        Until: 18:00,             !- Field 12
        0.5,                      !- Field 13
        Until: 24:00,             !- Field 14
        1.0,                      !- Field 15
        For: Sunday Holidays AllOtherDays,    !- Field 16
        Until: 24:00,             !- Field 17
        1.0;                      !- Field 18
    
    Schedule:Compact,         
        Infiltration Quarter On Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays SummerDesignDay,    !- Field 2
        Until: 06:00,             !- Field 3
        1.0,                      !- Field 4
        Until: 22:00,             !- Field 5
        0.25,                     !- Field 6
        Until: 24:00,             !- Field 7
        1.0,                      !- Field 8
        For: Saturday WinterDesignDay,    !- Field 9
        Until: 06:00,             !- Field 10
        1.0,                      !- Field 11
        Until: 18:00,             !- Field 12
        0.25,                     !- Field 13
        Until: 24:00,             !- Field 14
        1.0,                      !- Field 15
        For: Sunday Holidays AllOtherDays,    !- Field 16
        Until: 24:00,             !- Field 17
        1.0;                      !- Field 18
    
    Schedule:Compact,         
        Hours of Operation Schedule,    !- Name
        On/Off,                   !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays SummerDesignDay,    !- Field 2
        Until: 06:00,             !- Field 3
        0.0,                      !- Field 4
        Until: 22:00,             !- Field 5
        1.0,                      !- Field 6
        Until: 24:00,             !- Field 7
        0.0,                      !- Field 8
        For: Saturday WinterDesignDay,    !- Field 9
        Until: 06:00,             !- Field 10
        0.0,                      !- Field 11
        Until: 18:00,             !- Field 12
        1.0,                      !- Field 13
        Until: 24:00,             !- Field 14
        0.0,                      !- Field 15
        For: Sunday Holidays AllOtherDays,    !- Field 16
        Until: 24:00,             !- Field 17
        0.0;                      !- Field 18
    
    Schedule:Compact,         
        Always On,                !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: AllDays,             !- Field 2
        Until: 24:00,             !- Field 3
        1.0;                      !- Field 4
    
    Schedule:Compact,         
        Always Off,               !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: AllDays,             !- Field 2
        Until: 24:00,             !- Field 3
        0.0;                      !- Field 4
    
    Schedule:Compact,         
        Heating Setpoint Schedule,    !- Name
        Temperature,              !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays,            !- Field 2
        Until: 05:00,             !- Field 3
        15.6,                     !- Field 4
        Until: 19:00,             !- Field 5
        21.0,                     !- Field 6
        Until: 24:00,             !- Field 7
        15.6,                     !- Field 8
        For SummerDesignDay,      !- Field 9
        Until: 24:00,             !- Field 10
        15.6,                     !- Field 11
        For: Saturday,            !- Field 12
        Until: 06:00,             !- Field 13
        15.6,                     !- Field 14
        Until: 17:00,             !- Field 15
        21.0,                     !- Field 16
        Until: 24:00,             !- Field 17
        15.6,                     !- Field 18
        For: WinterDesignDay,     !- Field 19
        Until: 24:00,             !- Field 20
        21.0,                     !- Field 21
        For: Sunday Holidays AllOtherDays,    !- Field 22
        Until: 24:00,             !- Field 23
        15.6;                     !- Field 24
    
    Schedule:Compact,         
        Cooling Setpoint Schedule,    !- Name
        Temperature,              !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: Weekdays SummerDesignDay,    !- Field 2
        Until: 06:00,             !- Field 3
        30.0,                     !- Field 4
        Until: 22:00,             !- Field 5
        24.0,                     !- Field 6
        Until: 24:00,             !- Field 7
        30.0,                     !- Field 8
        For: Saturday,            !- Field 9
        Until: 06:00,             !- Field 10
        30.0,                     !- Field 11
        Until: 18:00,             !- Field 12
        24.0,                     !- Field 13
        Until: 24:00,             !- Field 14
        30.0,                     !- Field 15
        For WinterDesignDay,      !- Field 16
        Until: 24:00,             !- Field 17
        30.0,                     !- Field 18
        For: Sunday Holidays AllOtherDays,    !- Field 19
        Until: 24:00,             !- Field 20
        30.0;                     !- Field 21
    
    Schedule:Compact,         
        Office Activity Schedule,    !- Name
        Any Number,               !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: AllDays,             !- Field 2
        Until: 24:00,             !- Field 3
        120.;                     !- Field 4
    
    Schedule:Compact,         
        Office Work Eff. Schedule,    !- Name
        Fraction,                 !- Schedule Type Limits Name
        Through: 12/31,           !- Field 1
        For: AllDays,             !- Field 2
        Until: 24:00,             !- Field 3
        0.0;                      !- Field 4
    
    Schedule:Compact,         
        Office Clothing Schedule,    !- Name
        Any Number,               !- Schedule Type Limits Name
        Through: 04/30,           !- Field 1
        For: AllDays,             !- Field 2
        Until: 24:00,             !- Field 3
        1.0,                      !- Field 4
        Through: 09/30,           !- Field 5
        For: AllDays,             !- Field 6
        Until: 24:00,             !- Field 7
        0.5,                      !- Field 8
        Through: 12/31,           !- Field 9
        For: AllDays,             !- Field 10
        Until: 24:00,             !- Field 11
        1.0;                      !- Field 12
    
    Material,                 
        F08 Metal surface,        !- Name
        Smooth,                   !- Roughness
        0.0008,                   !- Thickness
        45.28,                    !- Conductivity
        7824.0,                   !- Density
        500.0;                    !- Specific Heat
    
    Material,                 
        I01 25mm insulation board,    !- Name
        MediumRough,              !- Roughness
        0.0254,                   !- Thickness
        0.03,                     !- Conductivity
        43.0,                     !- Density
        1210.0;                   !- Specific Heat
    
    Material,                 
        I02 50mm insulation board,    !- Name
        MediumRough,              !- Roughness
        0.0508,                   !- Thickness
        0.03,                     !- Conductivity
        43.0,                     !- Density
        1210.0;                   !- Specific Heat
    
    Material,                 
        peanut butter,            !- Name
        MediumSmooth,             !- Roughness
        0.019,                    !- Thickness
        0.16,                     !- Conductivity
        800.0,                    !- Density
        1090.0;                   !- Specific Heat
    
    Material,                 
        M11 100mm lightweight concrete,    !- Name
        MediumRough,              !- Roughness
        0.1016,                   !- Thickness
        0.53,                     !- Conductivity
        1280.0,                   !- Density
        840.0;                    !- Specific Heat
    
    Material,                 
        F16 Acoustic tile,        !- Name
        MediumSmooth,             !- Roughness
        0.0191,                   !- Thickness
        0.06,                     !- Conductivity
        368.0,                    !- Density
        590.0;                    !- Specific Heat
    
    Material,                 
        M01 100mm brick,          !- Name
        MediumRough,              !- Roughness
        0.1016,                   !- Thickness
        0.89,                     !- Conductivity
        1920.0,                   !- Density
        790.0;                    !- Specific Heat
    
    Material,                 
        M15 200mm heavyweight concrete,    !- Name
        MediumRough,              !- Roughness
        0.2032,                   !- Thickness
        1.95,                     !- Conductivity
        2240.0,                   !- Density
        900.0;                    !- Specific Heat
    
    Material,                 
        M05 200mm concrete block,    !- Name
        MediumRough,              !- Roughness
        0.2032,                   !- Thickness
        1.11,                     !- Conductivity
        800.0,                    !- Density
        920.0;                    !- Specific Heat
    
    Material,                 
        G05 25mm wood,            !- Name
        MediumSmooth,             !- Roughness
        0.0254,                   !- Thickness
        0.15,                     !- Conductivity
        608.0,                    !- Density
        1630.0;                   !- Specific Heat
    
    Material:AirGap,          
        F04 Wall air space resistance,    !- Name
        0.15;                     !- Thermal Resistance
    
    Material:AirGap,          
        F05 Ceiling air space resistance,    !- Name
        0.18;                     !- Thermal Resistance
    
    WindowMaterial:Glazing,   
        Clear 3mm,                !- Name
        SpectralAverage,          !- Optical Data Type
        ,                         !- Window Glass Spectral Data Set Name
        0.003,                    !- Thickness
        0.837,                    !- Solar Transmittance at Normal Incidence
        0.075,                    !- Front Side Solar Reflectance at Normal Incidence
        0.075,                    !- Back Side Solar Reflectance at Normal Incidence
        0.898,                    !- Visible Transmittance at Normal Incidence
        0.081,                    !- Front Side Visible Reflectance at Normal Incidence
        0.081,                    !- Back Side Visible Reflectance at Normal Incidence
        0.0,                      !- Infrared Transmittance at Normal Incidence
        0.84,                     !- Front Side Infrared Hemispherical Emissivity
        0.84,                     !- Back Side Infrared Hemispherical Emissivity
        0.9;                      !- Conductivity
    
    WindowMaterial:Gas,       
        Air 13mm,                 !- Name
        Air,                      !- Gas Type
        0.0127;                   !- Thickness
    
    Construction,             
        Exterior Floor,           !- Name
        I02 50mm insulation board,    !- Outside Layer
        M15 200mm heavyweight concrete;    !- Layer 2
    
    Construction,             
        Interior Floor,           !- Name
        F16 Acoustic tile,        !- Outside Layer
        F05 Ceiling air space resistance,    !- Layer 2
        M11 100mm lightweight concrete;    !- Layer 3
    
    Construction,             
        Exterior Wall,            !- Name
        M01 100mm brick,          !- Outside Layer
        M15 200mm heavyweight concrete,    !- Layer 2
        I02 50mm insulation board,    !- Layer 3
        F04 Wall air space resistance,    !- Layer 4
        peanut butter;            !- Layer 5
    
    Construction,             
        Interior Wall,            !- Name
        peanut butter,            !- Outside Layer
        F04 Wall air space resistance,    !- Layer 2
        peanut butter;            !- Layer 3
    
    Construction,             
        Exterior Roof,            !- Name
        M11 100mm lightweight concrete,    !- Outside Layer
        F05 Ceiling air space resistance,    !- Layer 2
        F16 Acoustic tile;        !- Layer 3
    
    Construction,             
        Interior Ceiling,         !- Name
        M11 100mm lightweight concrete,    !- Outside Layer
        F05 Ceiling air space resistance,    !- Layer 2
        F16 Acoustic tile;        !- Layer 3
    
    Construction,             
        Exterior Window,          !- Name
        Clear 3mm,                !- Outside Layer
        Air 13mm,                 !- Layer 2
        Clear 3mm;                !- Layer 3
    
    Construction,             
        Interior Window,          !- Name
        Clear 3mm;                !- Outside Layer
    
    Construction,             
        Exterior Door,            !- Name
        F08 Metal surface,        !- Outside Layer
        I01 25mm insulation board;    !- Layer 2
    
    Construction,             
        Interior Door,            !- Name
        G05 25mm wood;            !- Outside Layer
    
    CONSTRUCTION,             
        Interior Wall,            !- Name
        peanut butter,            !- Outside Layer
        Shiny new material object,    !- Layer 2
        peanut butter;            !- Layer 3
    
    GlobalGeometryRules,      
        UpperLeftCorner,          !- Starting Vertex Position
        Counterclockwise,         !- Vertex Entry Direction
        Absolute,                 !- Coordinate System
        Relative,                 !- Daylighting Reference Point Coordinate System
        Absolute;                 !- Rectangular Surface Coordinate System
    
    Zone,                     
        Box,                      !- Name
        0.0,                      !- Direction of Relative North
        0.288184,                 !- X Origin
        0.756604,                 !- Y Origin
        0.0,                      !- Z Origin
        ,                         !- Type
        1;                        !- Multiplier
    
    BuildingSurface:Detailed, 
        F_Surf,                   !- Name
        Floor,                    !- Surface Type
        Exterior Floor,           !- Construction Name
        Box,                      !- Zone Name
        Ground,                   !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        NoSun,                    !- Sun Exposure
        NoWind,                   !- Wind Exposure
        0.0,                      !- View Factor to Ground
        4,                        !- Number of Vertices
        5.0,                      !- Vertex 1 Xcoordinate
        6.0,                      !- Vertex 1 Ycoordinate
        0.0,                      !- Vertex 1 Zcoordinate
        5.0,                      !- Vertex 2 Xcoordinate
        0.0,                      !- Vertex 2 Ycoordinate
        0.0,                      !- Vertex 2 Zcoordinate
        0.0,                      !- Vertex 3 Xcoordinate
        0.0,                      !- Vertex 3 Ycoordinate
        0.0,                      !- Vertex 3 Zcoordinate
        0.0,                      !- Vertex 4 Xcoordinate
        6.0,                      !- Vertex 4 Ycoordinate
        0.0;                      !- Vertex 4 Zcoordinate
    
    BuildingSurface:Detailed, 
        S_Wall,                   !- Name
        Wall,                     !- Surface Type
        Exterior Wall,            !- Construction Name
        Box,                      !- Zone Name
        Outdoors,                 !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        ,                         !- View Factor to Ground
        4,                        !- Number of Vertices
        0.0,                      !- Vertex 1 Xcoordinate
        0.0,                      !- Vertex 1 Ycoordinate
        3.0,                      !- Vertex 1 Zcoordinate
        0.0,                      !- Vertex 2 Xcoordinate
        0.0,                      !- Vertex 2 Ycoordinate
        0.0,                      !- Vertex 2 Zcoordinate
        5.0,                      !- Vertex 3 Xcoordinate
        0.0,                      !- Vertex 3 Ycoordinate
        0.0,                      !- Vertex 3 Zcoordinate
        5.0,                      !- Vertex 4 Xcoordinate
        0.0,                      !- Vertex 4 Ycoordinate
        3.0;                      !- Vertex 4 Zcoordinate
    
    BuildingSurface:Detailed, 
        N_Wall,                   !- Name
        Wall,                     !- Surface Type
        Exterior Wall,            !- Construction Name
        Box,                      !- Zone Name
        Outdoors,                 !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        ,                         !- View Factor to Ground
        4,                        !- Number of Vertices
        5.0,                      !- Vertex 1 Xcoordinate
        6.0,                      !- Vertex 1 Ycoordinate
        3.0,                      !- Vertex 1 Zcoordinate
        5.0,                      !- Vertex 2 Xcoordinate
        6.0,                      !- Vertex 2 Ycoordinate
        0.0,                      !- Vertex 2 Zcoordinate
        0.0,                      !- Vertex 3 Xcoordinate
        6.0,                      !- Vertex 3 Ycoordinate
        0.0,                      !- Vertex 3 Zcoordinate
        0.0,                      !- Vertex 4 Xcoordinate
        6.0,                      !- Vertex 4 Ycoordinate
        3.0;                      !- Vertex 4 Zcoordinate
    
    BuildingSurface:Detailed, 
        R_surf,                   !- Name
        Roof,                     !- Surface Type
        Exterior Roof,            !- Construction Name
        Box,                      !- Zone Name
        Outdoors,                 !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        ,                         !- View Factor to Ground
        4,                        !- Number of Vertices
        0.0,                      !- Vertex 1 Xcoordinate
        6.0,                      !- Vertex 1 Ycoordinate
        3.0,                      !- Vertex 1 Zcoordinate
        0.0,                      !- Vertex 2 Xcoordinate
        0.0,                      !- Vertex 2 Ycoordinate
        3.0,                      !- Vertex 2 Zcoordinate
        5.0,                      !- Vertex 3 Xcoordinate
        0.0,                      !- Vertex 3 Ycoordinate
        3.0,                      !- Vertex 3 Zcoordinate
        5.0,                      !- Vertex 4 Xcoordinate
        6.0,                      !- Vertex 4 Ycoordinate
        3.0;                      !- Vertex 4 Zcoordinate
    
    BuildingSurface:Detailed, 
        W_Wall,                   !- Name
        Wall,                     !- Surface Type
        Exterior Wall,            !- Construction Name
        Box,                      !- Zone Name
        Outdoors,                 !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        ,                         !- View Factor to Ground
        4,                        !- Number of Vertices
        0.0,                      !- Vertex 1 Xcoordinate
        6.0,                      !- Vertex 1 Ycoordinate
        3.0,                      !- Vertex 1 Zcoordinate
        0.0,                      !- Vertex 2 Xcoordinate
        6.0,                      !- Vertex 2 Ycoordinate
        0.0,                      !- Vertex 2 Zcoordinate
        0.0,                      !- Vertex 3 Xcoordinate
        0.0,                      !- Vertex 3 Ycoordinate
        0.0,                      !- Vertex 3 Zcoordinate
        0.0,                      !- Vertex 4 Xcoordinate
        0.0,                      !- Vertex 4 Ycoordinate
        3.0;                      !- Vertex 4 Zcoordinate
    
    BuildingSurface:Detailed, 
        E_Wall,                   !- Name
        Wall,                     !- Surface Type
        Exterior Wall,            !- Construction Name
        Box,                      !- Zone Name
        Outdoors,                 !- Outside Boundary Condition
        ,                         !- Outside Boundary Condition Object
        SunExposed,               !- Sun Exposure
        WindExposed,              !- Wind Exposure
        ,                         !- View Factor to Ground
        4,                        !- Number of Vertices
        5.0,                      !- Vertex 1 Xcoordinate
        0.0,                      !- Vertex 1 Ycoordinate
        3.0,                      !- Vertex 1 Zcoordinate
        5.0,                      !- Vertex 2 Xcoordinate
        0.0,                      !- Vertex 2 Ycoordinate
        0.0,                      !- Vertex 2 Zcoordinate
        5.0,                      !- Vertex 3 Xcoordinate
        6.0,                      !- Vertex 3 Ycoordinate
        0.0,                      !- Vertex 3 Zcoordinate
        5.0,                      !- Vertex 4 Xcoordinate
        6.0,                      !- Vertex 4 Ycoordinate
        3.0;                      !- Vertex 4 Zcoordinate
    
    FenestrationSurface:Detailed,
        S_Window,                 !- Name
        Window,                   !- Surface Type
        Exterior Window,          !- Construction Name
        S_Wall,                   !- Building Surface Name
        ,                         !- Outside Boundary Condition Object
        ,                         !- View Factor to Ground
        ,                         !- Shading Control Name
        ,                         !- Frame and Divider Name
        ,                         !- Multiplier
        4,                        !- Number of Vertices
        1.64142641902,            !- Vertex 1 Xcoordinate
        0.0,                      !- Vertex 1 Ycoordinate
        2.264479674,              !- Vertex 1 Zcoordinate
        1.64142641902,            !- Vertex 2 Xcoordinate
        0.0,                      !- Vertex 2 Ycoordinate
        1.264479674,              !- Vertex 2 Zcoordinate
        3.64142641902,            !- Vertex 3 Xcoordinate
        0.0,                      !- Vertex 3 Ycoordinate
        1.264479674,              !- Vertex 3 Zcoordinate
        3.64142641902,            !- Vertex 4 Xcoordinate
        0.0,                      !- Vertex 4 Ycoordinate
        2.264479674;              !- Vertex 4 Zcoordinate
    
    HVACTemplate:Thermostat,  
        Constant Setpoint Thermostat,    !- Name
        ,                         !- Heating Setpoint Schedule Name
        20,                       !- Constant Heating Setpoint
        ,                         !- Cooling Setpoint Schedule Name
        25;                       !- Constant Cooling Setpoint
    
    Output:VariableDictionary,
        IDF;                      !- Key Field
    


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
