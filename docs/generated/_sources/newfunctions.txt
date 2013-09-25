
New functions
=============


These are recently written functions that have not made it into the main
documentation

EpBunch.checkrange(fieldname)
-----------------------------


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
    
    from eppy import modeleditor 
    from eppy.modeleditor import IDF
    iddfile = "../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    fname1 = "../eppy/resources/idffiles/V_7_2/smallfile.idf"
.. code:: python

    IDF.setiddname(iddfile)
    idf1 = IDF(fname1)
demonstrate two new functions:

-  EpBunch.getrange(fieldname) # will return the ranges for that field
-  EpBunch.checkrange(fieldname) # will throw an exception if the value
   is outside the range


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
    print building.checkrange("Loads_Convergence_Tolerance_Value")

::


    ---------------------------------------------------------------------------
    RangeError                                Traceback (most recent call last)

    <ipython-input-13-7ec7f7f6f637> in <module>()
          1 building.Loads_Convergence_Tolerance_Value = 0.6
    ----> 2 print building.checkrange("Loads_Convergence_Tolerance_Value")
    

    /Users/santosh/Documents/coolshadow/eplus_github/eppy/eppy/bunch_subclass.pyc in checkrange(self, fieldname)
        206                 s = "Value %s is not less or equal to the 'maximum' of %s"
        207                 s = s % (fieldvalue, therange['maximum'])
    --> 208                 raise RangeError(s)
        209         if therange['minimum'] != None:
        210             if fieldvalue < therange['minimum']:


    RangeError: Value 0.6 is not less or equal to the 'maximum' of 0.5


So the Range Check works
