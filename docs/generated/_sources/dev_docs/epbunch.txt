
EpBunch
=======


:Author: Santosh Philip.

I had completely forgotten how I had written EpBunch. Spent long time
reviewing the code and even writing more unit tests to understand what
is going on.

This is not the type of coding that non-professional programmers are
likey to do. I have had the code reviewed by other people ar python
meetups. thier reaction is that the code is OK. I am not doing anythin
fundamentally wrong.

Developing and debugging this code was tricky,

Now I have to figure out how to describe it.

Magic Methods (Dunders) of Python
---------------------------------


To understand how EpBunch or Bunch is coded, one has to have an
understanding of the magic methods of Python. For a background on magic
methods, see http://www.rafekettler.com/magicmethods.html. Let us dive
straight into this with some examples

.. code:: python

    adict = dict(a=10, b=20) # create a dictionary
    print adict
    print adict['a']
    print adict['b']

.. parsed-literal::

    {'a': 10, 'b': 20}
    10
    20


What happens when we say d['a'] ?

This is where the magic methods come in. Magic methods are methods that
work behind the scenes and do some magic. So when we say d['a'], The
dict is calling the method \`\ **getitem**\ ('a')'.

Magic methods have a double underscore, called **dunder** methods for
short

Let us override that method and see what happens.

.. code:: python

    class Funnydict(dict):
        def __getitem__(self, key):
            value = super(Funnydict, self).__getitem__(key)
            return "key = %s, value = %s" % (key, value)
    
    funny = Funnydict(dict(a=10, b=20)) 
    print funny

.. parsed-literal::

    {'a': 10, 'b': 20}


As expected

.. code:: python

    print funny['a']
    print funny['b']

.. parsed-literal::

    key = a, value = 10
    key = b, value = 20


So it is true, funny['a'] does call \_\ *getitem*\ \_(a)

Let us go back to the variable **adict**

.. code:: python

    # to jog our memory
    print adict

.. parsed-literal::

    {'a': 10, 'b': 20}


.. code:: python

    # this should not work
    print adict.a

::


    ---------------------------------------------------------------------------
    AttributeError                            Traceback (most recent call last)

    <ipython-input-5-8aa7211fcb66> in <module>()
          1 # this should not work
    ----> 2 print adict.a
    

    AttributeError: 'dict' object has no attribute 'a'


What method gets called when we say **adict.a** ?

The magic method here is ``__getattr__``\ () and ``__setattr__()``.
Shall we override them and see if we can get the dot notation to work ?

.. code:: python

    class Like_bunch(dict):
        def __getattr__(self, name):
            return self[name]
        def __setattr__(self, name, value):
            self[name] = value
    
    lbunch = Like_bunch(dict(a=10, b=20))
    print lbunch

.. parsed-literal::

    {'a': 10, 'b': 20}


Works like a dict so far. How about **lbunch.a** ?

.. code:: python

    print lbunch.a
    print lbunch.b

.. parsed-literal::

    10
    20


Yipeee !!! I works

How about ``lbunch.nota = 100``

.. code:: python

    lbunch.anot = 100
    print lbunch.anot

.. parsed-literal::

    100


All good here. But don't trust the code above too much. It was simply
done as a demonstration of **dunder** methods and is not fully tested.

Eppy uses the bunch library to do something similar. You can read more
about the bunch library in the previous section.

Open an IDF file
----------------


Once again let us open a small idf file to test.

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
    


.. code:: python

    dtls = idf1.model.dtls
    dt = idf1.model.dt
    idd_info = idf1.idd_info
.. code:: python

    dt['MATERIAL:AIRGAP']



.. parsed-literal::

    [['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15],
     ['MATERIAL:AIRGAP', 'F05 Ceiling air space resistance', 0.18]]



.. code:: python

    obj_i = dtls.index('MATERIAL:AIRGAP')
    obj_idd = idd_info[obj_i]
    obj_idd



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



For the rest of this section let us look at only one airgap object

.. code:: python

    airgap = dt['MATERIAL:AIRGAP'][0]
    airgap



.. parsed-literal::

    ['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15]



Subclassing of Bunch
--------------------


Let us review our knowledge of bunch

.. code:: python

    from bunch import Bunch
    adict = {'a':1, 'b':2, 'c':3}
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


Bunch lets us use dot notation on the keys of a dictionary. We need to
find a way of making ``airgap.Name`` work. This is not straightforward
because, airgap is **list** and Bunch works on **dicts**. It would be
easy if airgap was in the form
``{'Name' : 'F04 Wall air space resistance', 'Thermal Resistance' : 0.15}``.

The rest of this section is a simplified version of how EpBunch works.

.. code:: python

    class EpBunch(Bunch):
        def __init__(self, obj, objls, objidd, *args, **kwargs):
            super(EpBunch, self).__init__(*args, **kwargs)
            self.obj = obj
            self.objls = objls
            self.objidd = objidd
The above code shows how EpBunch is initialized. Three variables are
passed to EpBunch to initialize it. They are ``obj, objls, objidd``.

.. code:: python

    obj = airgap
    objls = ['key', 'Name', 'Thermal_Resistance'] # a function extracts this from idf1.idd_info
    objidd = obj_idd
    #
    print obj
    print objls
    # let us ignore objidd for now

.. parsed-literal::

    ['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15]
    ['key', 'Name', 'Thermal_Resistance']


Now we override ``__setattr__()`` and ``__getattr__()`` in the following
way

.. code:: python

    class EpBunch(Bunch):
        def __init__(self, obj, objls, objidd, *args, **kwargs):
            super(EpBunch, self).__init__(*args, **kwargs)
            self.obj = obj
            self.objls = objls
            self.objidd = objidd
            
        def __getattr__(self, name):
            if name in ('obj', 'objls', 'objidd'):
                return super(EpBunch, self).__getattr__(name)
            i = self.objls.index(name)
            return self.obj[i]
    
        def __setattr__(self, name, value):
            if name in ('obj', 'objls', 'objidd'):
                super(EpBunch, self).__setattr__(name, value)
                return None
            i = self.objls.index(name)
            self.obj[i] = value

.. code:: python

    # Let us create a EpBunch object
    bunch_airgap = EpBunch(obj, objls, objidd)
    # Use this table to see how __setattr__ and __getattr__ work in EpBunch

    obj   = ['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15                ]
    objls = ['key',             'Name',                         'Thermal_Resistance']
    i     =   0                  1                               2

.. code:: python

    print bunch_airgap.Name
    print bunch_airgap.Thermal_Resistance

.. parsed-literal::

    F04 Wall air space resistance
    0.15


.. code:: python

    print bunch_airgap.obj

.. parsed-literal::

    ['MATERIAL:AIRGAP', 'F04 Wall air space resistance', 0.15]


Let us change some values using the dot notation

.. code:: python

    bunch_airgap.Name = 'Argon in gap'
.. code:: python

    print bunch_airgap.Name

.. parsed-literal::

    Argon in gap


.. code:: python

    print bunch_airgap.obj

.. parsed-literal::

    ['MATERIAL:AIRGAP', 'Argon in gap', 0.15]


Using the dot notation the value is changed in the list

Let us make sure it actually has done that.

.. code:: python

    idf1.model.dt['MATERIAL:AIRGAP'][0]



.. parsed-literal::

    ['MATERIAL:AIRGAP', 'Argon in gap', 0.15]



``EpBunch`` acts as a wrapper around
``idf1.model.dt['MATERIAL:AIRGAP'][0]``

In other words ``EpBunch`` is just **Syntactic Sugar** for
``idf1.model.dt['MATERIAL:AIRGAP'][0]``

Variables and Names in Python
-----------------------------


At this point your reaction may, "I don't see how all those values
changed". If such question arises in your mind, you need to read the
following:

-  `Other languages have
   'variables' <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables>`__
-  `Python has
   'names' <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#python-has-names>`__
-  Also see `Facts and myths about Python names and
   values <http://nedbatchelder.com/text/names.html>`__

This is especially important if you are experienced in other languages,
and you expect the behavior to be a little different

.. code:: python

    