
Underlying Data Structure of eppy
=================================


As described in previous sections, eppy was built on EplusInterface

Let us open a small **idf** file to explore the data structure

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
    pathnameto_eppy = '../../../'
    sys.path.append(pathnameto_eppy)
.. code:: python

    from eppy import modeleditor
    from eppy.modeleditor import IDF
    iddfile = "../../../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    fname1 = "../../../eppy/resources/idffiles/V_7_2/dev1.idf"
    
    IDF.setiddname(iddfile)
    idf1 = IDF(fname1)
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
    
    MATERIAL:AIRGAP,          
        F04 Wall air space resistance,    !- Name
        0.15;                     !- Thermal Resistance
    
    MATERIAL:AIRGAP,          
        F05 Ceiling air space resistance,    !- Name
        0.18;                     !- Thermal Resistance
    


Original Data Structure in EPlusInterface
-----------------------------------------


The original data structure in EPlusInterface was stupidly simple and
robust. In fact attributes **stupidly simple** and **robust** seem to go
together. Eppy evolved in such a way that this data structure is still
retained. The rest of eppy is simply `syntactic
sugar <http://en.wikipedia.org/wiki/Syntactic_sugar>`__ for this data
structure.

from:
https://www.princeton.edu/~achaney/tmve/wiki100k/docs/Syntactic\_sugar.html
*"Syntactic sugar is a computer science term that refers to syntax
within a programming language that is designed to make things easier to
read or to express, while alternative ways of expressing them exist.
Syntactic sugar"*

Let us take a look at this data structure. If we open an idf file with
eppy we can explore the original data structure that comes from
EPlusInterface.

**Note** The variable names are not very intuitive at this level. I did
not know what I was doing when I wrote this code and now we are stuck
with it

There are three varaibles that hold all the data we need. They are:

-  ``idf1.model.dtls``
-  ``idf1.model.dt``
-  ``idf1.idd_info``


.. code:: python

    dtls = idf1.model.dtls # names of all the idf objects
    dt = idf1.model.dt # the idf model
    idd_info = idf1.idd_info # all the idd data
idf1.model.dtls - Overview
~~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    dtls = idf1.model.dtls # names of all the idf objects
    print type(dtls)

.. parsed-literal::

    <type 'list'>


.. code:: python

    # dtls is a list
    print dtls[:10] # print the first ten items

.. parsed-literal::

    ['LEAD INPUT', 'SIMULATION DATA', 'VERSION', 'SIMULATIONCONTROL', 'BUILDING', 'SHADOWCALCULATION', 'SURFACECONVECTIONALGORITHM:INSIDE', 'SURFACECONVECTIONALGORITHM:OUTSIDE', 'HEATBALANCEALGORITHM', 'HEATBALANCESETTINGS:CONDUCTIONFINITEDIFFERENCE']


.. code:: python

    print len(dtls) # print the numer of items in the list

.. parsed-literal::

    683


Couple of points to note about ``dtls``:

-  **dtls** is a list of all the names of the Energyplus objects.
-  This list is extracted from the the **idd** file
-  the list is in the same order as the objects in the **idd** file


idf1.model.dt - Overview
~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    dt = idf1.model.dt # the idf model
    print type(dt)

.. parsed-literal::

    <type 'dict'>


.. code:: python

    # print 10 of the keys
    print dt.keys()[:10]

.. parsed-literal::

    ['ZONEHVAC:OUTDOORAIRUNIT', 'TABLE:TWOINDEPENDENTVARIABLES', 'ENERGYMANAGEMENTSYSTEM:INTERNALVARIABLE', 'AVAILABILITYMANAGER:NIGHTCYCLE', 'GROUNDHEATTRANSFER:SLAB:BLDGPROPS', 'GENERATOR:MICROTURBINE', 'SHADING:BUILDING:DETAILED', 'EVAPORATIVECOOLER:INDIRECT:RESEARCHSPECIAL', 'ZONEHVAC:PACKAGEDTERMINALAIRCONDITIONER', 'CONSTRUCTION:WINDOWDATAFILE']


.. code:: python

    # dt is a dict
    number_of_keys = len(dt.keys())
    print number_of_keys

.. parsed-literal::

    683


-  The keys of **dt** are names of the objects (note that they are in
   capitals)
-  Items in a python dict are unordered. So the keys may be in any order
-  **dtls** will give us these names in the same order as they are in
   the idd file.
-  so use **dtls** if you want the keys in an order

We'll look at **dt** in further detail later

idf1.idd\_info - Overview
~~~~~~~~~~~~~~~~~~~~~~~~~


.. code:: python

    idd_info = idf1.idd_info # all the idd data
    print type(idd_info)

.. parsed-literal::

    <type 'list'>


.. code:: python

    print len(idd_info) # number of items in the list

.. parsed-literal::

    683


.. code:: python

    # print the first three items
    idd_info[:3]



.. parsed-literal::

    [[{}],
     [{}],
     [{'format': ['singleLine'], 'unique-object': ['']},
      {'default': ['7.0'],
       'field': ['Version Identifier'],
       'required-field': ['']}]]



.. code:: python

    # print the first three items in seperate lines
    for i, item in enumerate(idd_info[:3]):
        print "%s. %s" % (i, item)

.. parsed-literal::

    0. [{}]
    1. [{}]
    2. [{'unique-object': [''], 'format': ['singleLine']}, {'default': ['7.0'], 'field': ['Version Identifier'], 'required-field': ['']}]


That does not make much sense. Below is the first 3 items from the idd
file ::

    Lead Input;
    
    Simulation Data;
    
    \group Simulation Parameters
    
    Version,
          \unique-object
          \format singleLine
      A1 ; \field Version Identifier
          \required-field
          \default 7.0


-  If you compare the text file with the sturcture of idd\_info, you can
   start to see the similarities
-  Note that the idd\_info does not have the object name.
-  This was an unfortunate design decision that we are stuck with now
   :-(.
-  We need to jump through some hoops to get to an item in idd\_info


.. code:: python

    # the object "VERSION" is the third item in idd_info
    # to get to "VERSION" we need to find it's location in the list
    # we use "dtls" to do this
    location_of_version = dtls.index("version".upper())
    print location_of_version

.. parsed-literal::

    2


.. code:: python

    # print idd_info of "VERSION"
    idd_info[location_of_version]



.. parsed-literal::

    [{'format': ['singleLine'], 'unique-object': ['']},
     {'default': ['7.0'], 'field': ['Version Identifier'], 'required-field': ['']}]



**NOTE:**

-  the idd file is very large and uses a lot of memory when pulled into
   idd\_info
-  only one copy of idd\_info is kept when eppy is running.
-  This is the reason, eppy throws an exception when you try to set the
   idd file when it has already been set


idf1.model.dt - in detail
~~~~~~~~~~~~~~~~~~~~~~~~~


Let us look at a specific object, say **MATERIAL:AIRGAP** in
idf1.model.dt

.. code:: python

    dt = idf1.model.dt
.. code:: python

    airgaps = dt['MATERIAL:AIRGAP'.upper()]
    print type(airgaps)

.. parsed-literal::

    <type 'list'>


.. code:: python

    airgaps



.. parsed-literal::

    [['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15],
     ['MATERIAL:AIRGAP', 'F05 Ceiling air space resistance', 0.18]]



A snippet of the **idf** text file shows this ::

    MATERIAL:AIRGAP,
        F04 Wall air space resistance,    !- Name
        0.15;                     !- Thermal Resistance
    
    MATERIAL:AIRGAP,
        F05 Ceiling air space resistance,    !- Name
        0.18;                     !- Thermal Resistance

Notice the following things about idf1.model.dt:

-  The idf model is held within a dict.
-  the keys in the dict are names of the IDF objects in caps, such as
   BUILDING, VERSION, CONSTRUCTION, MATERIAL:AIRGAP etc.
-  The values in the dict are lists
-  the list contains lists. This means that **airgaps** can contain more
   than one airgap.
-  So airgaps = [airgap1, airgap2, ... ].
-  where, airgaps1 = [Type\_of\_Object, field1, field2, field3, .... ]
-  In airgaps1, all types have been converted. Note that "Thermal
   Resistance" is a float and not a string


What about an Energyplus object that does not exist in the idf file ?

.. code:: python

    roofs = dt['ROOF']
    print roofs

.. parsed-literal::

    []


You get an empty list, meaning there are no roof items within roofs

idf1.idd\_info - in detail
~~~~~~~~~~~~~~~~~~~~~~~~~~


Let us find the idd\_info for airgaps

.. code:: python

    location_of_airgaps = dtls.index("material:airgap".upper())
    print location_of_airgaps

.. parsed-literal::

    50


.. code:: python

    idd_airgaps = idd_info[location_of_airgaps]
    idd_airgaps



.. parsed-literal::

    [{'memo': ['Air Space in Opaque Construction'], 'min-fields': ['2']},
     {'field': ['Name'],
      'reference': ['MaterialName'],
      'required-field': [''],
      'type': ['alpha']},
     {'field': ['Thermal Resistance'],
      'minimum>': ['0'],
      'type': ['real'],
      'units': ['m2-K/W']}]



Compare to text in idd file::

    Material:AirGap,
           \min-fields 2
           \memo Air Space in Opaque Construction
      A1 , \field Name
           \required-field
           \type alpha
           \reference MaterialName
      N1 ; \field Thermal Resistance
           \units m2-K/W
           \type real
           \minimum> 0

-  idd\_airgaps gives details about each field
-  the last field N1 says that *type = real*
-  This tells us that the text value coming from the the test file has
   to be converted to a float


Syntactic Sugar
---------------


from:
https://www.princeton.edu/~achaney/tmve/wiki100k/docs/Syntactic\_sugar.html
*"Syntactic sugar is a computer science term that refers to syntax
within a programming language that is designed to make things easier to
read or to express, while alternative ways of expressing them exist"*

Wikipedia article on `syntactic
sugar <http://en.wikipedia.org/wiki/Syntactic_sugar>`__

**All the rest of the code in eppy is simply syntactic sugar over the
data structure in model.dtls, model.dt and idd\_info**

Of course, the above statement is a gross exageration, but it gives you
a basis for understanding the code that comes later. At the end of the
day, any further code is simply a means for changing the data within
model.dt. And you need to access the data within model.dtls and
idd\_info to do so.

Bunch
~~~~~


Bunch is a great library that subclasses dict. You can see it at:

-  https://pypi.python.org/pypi/bunch/1.0.1
-  https://github.com/dsc/bunch

Let us first take a look at a dict

.. code:: python

    adict = {'a':1, 'b':2, 'c':3}
    adict



.. parsed-literal::

    {'a': 1, 'b': 2, 'c': 3}



.. code:: python

    # one would access the values in this dict by:
    print adict
    print adict['a']
    print adict['b']
    print adict['c']

.. parsed-literal::

    {'a': 1, 'c': 3, 'b': 2}
    1
    2
    3


Bunch allows us to do this with a lot less typing

.. code:: python

    from bunch import Bunch
    bunchdict = Bunch(adict)
    print bunchdict
    print bunchdict.a
    print bunchdict.b
    print bunchdict.c

.. parsed-literal::

    Bunch(a=1, b=2, c=3)
    1
    2
    3


Let us take a look at variable **airgaps** from the previous section.

.. code:: python

    airgaps



.. parsed-literal::

    [['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15],
     ['MATERIAL:AIRGAP', 'F05 Ceiling air space resistance', 0.18]]



.. code:: python

    airgap1, airgap2 = airgaps[0], airgaps[1]
.. code:: python

    airgap1



.. parsed-literal::

    ['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15]



We are going to subclass bunch so that we can do the following to
**airgap1** from the previous section:

-  airgap1.Name
-  airgap1.Thermal\_Resistance

to remind you, the text file we are reading looks like this::

    MATERIAL:AIRGAP,          
        F04 Wall air space resistance,    !- Name
        0.15;                             !- Thermal Resistance


-  We are using the field names that come from the idd file
-  A space and other illegal (illegal for python) characters are
   replaced by an underscore


It is a little tricky tring to use bunch with airgap, because:

-  airgap is a list
-  but bunch works on dicts

So we do it in the following way:

-  we make a new Bunch from the **airgap** list.
-  The Bunch is made by by doing airgap1 = Bunch( {"Name" : "F04 Wall
   air space resistance", "Thermal\_Resistance" : 0.15} )
-  This will allow us to use the dot notation we see in bunch
-  Of course if we make changes in this Bunch, the **airgap** list does
   not change
-  Ideally we would like to see the changes reflected in the **airgap**
   list
-  We subclass Bunch as EpBunch. EpBunch is designed so that changes in
   EpBunch will make changes to the **airgap** list

*Note:* Some simplifications were made in the explanations above. So
take it with a pinch of salt :-)

EpBunch
~~~~~~~


The code of EpBunch is in eppy/bunch\_subclass.py. If you look at the
code you will see The subclassing happening in the following manner:

-  Bunch -> EpBunch1 -> EpBunch2 -> ..... -> EpBunch5 , where "Bunch ->
   EpBunch" means "EpBunch subclassed from Bunch"
-  then EpBunch = EpBunch5

**Question:** Are you demented ? Why don't you just subclass Bunch ->
EpBunch ?

**Answer:** One can get demented trying to subclass from dict. This is
pretty tricky coding and testing-debugging is difficult, since we are
overriding built-in functions of dict. When you make mistakes there, the
subclassed dict just stops working, or does very strange things. So I
built it in a carefull and incremental way, fully testing before
subclassing again. Each subclass implements some functionality and the
next one implements more.

**EpBunch** is described in more detail in the next section
