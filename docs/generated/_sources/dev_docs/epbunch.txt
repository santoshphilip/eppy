
EpBunch
=======


:Author: Santosh Philip.

EpBunch is at the heart of what makes eppy easy to use. Specifically
Epbunch is what allows us to use the syntax ``building.Name`` and
``building.North_Axis``. Some advanced coding had to be done to make
this happen. Coding that would be easy for professional programmers, but
not for us ordinary folk :-(

Most of us who are going to be coding eppy are not professional
programmers. I was completely out of my depth when I did this coding. I
had the code reviewed by programmers who do this for a living (at python
meetups in the Bay Area). In their opinion, I was not doing anything
fundamentally wrong.

Below is a fairly long explanation, to ease you into the code. Read
through the whole thing without trying to understand every detail, just
getting a birds eye veiw of the explanation. Then read it again, you
will start to grok some of the details. All the code here is working
code, so you can experiment with it.

Magic Methods (Dunders) of Python
---------------------------------


To understand how EpBunch or Bunch is coded, one has to have an
understanding of the magic methods of Python. (For a background on magic
methods, take a look at http://www.rafekettler.com/magicmethods.html)
Let us dive straight into this with some examples

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
dict is calling the method ``__getitem__('a')``.

Magic methods have a *double underscore* "``__``\ ", called **dunder**
methods for short

Let us override that method and see what happens.

.. code:: python

    class Funnydict(dict): # we are subclassing dict here
        def __getitem__(self, key):
            value = super(Funnydict, self).__getitem__(key)
            return "key = %s, value = %s" % (key, value)
    
    funny = Funnydict(dict(a=10, b=20)) 
    print funny

.. parsed-literal::

    {'a': 10, 'b': 20}


The print worked as expected. Now let us try to print the values

.. code:: python

    print funny['a']
    print funny['b']

.. parsed-literal::

    key = a, value = 10
    key = b, value = 20


Now that worked very differently from a dict

So it is true, funny['a'] does call ``__getitem__()`` that we just wrote

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


At this point your reaction may, "I don't see how all those values in
``idf1.model.dt`` changed". If such question arises in your mind, you
need to read the following:

-  `Other languages have
   'variables' <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#other-languages-have-variables>`__
-  `Python has
   'names' <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html#python-has-names>`__
-  Also see `Facts and myths about Python names and
   values <http://nedbatchelder.com/text/names.html>`__

This is especially important if you are experienced in other languages,
and you expect the behavior to be a little different. Actually follow
and read those links in any case.

Continuing with EpBunch
-----------------------


EpBunch\_1
~~~~~~~~~~


The code for EpBunch in the earlier section will work, but has been
simplified for clarity. In file ``bunch_subclass.py`` take a look at the
class **EpBunch\_1** . This class does the first override of
``__setattr__`` and ``__getattr__``. You will see that the code is a
little more involved, dealing with edge conditions and catching
exceptions.

**EpBunch\_1** also defines ``__repr__``. This lets you print EpBunch in
a human readable format. Further research indicates that ``__str__``
should have been used to do this, not ``__repr__`` :-(

EpBunch\_2
~~~~~~~~~~


``EpBunch_2`` is subclassed from ``EpBunch_1``.

It overrides ``__setattr__`` and ``__getattr__`` to add a small
functionality that has not been documented or used. The idea was to give
the ability to shorten field names with alias. So
``building.Maximum_Number_of_Warmup_Days`` could be made into
``building.warmupdays``.

I seemed like a good idea when I wrote it. Ignore it for now, although
it may make a comeback :-)

EpBunch\_3
~~~~~~~~~~


``EpBunch_3`` is subclassed from ``EpBunch_2``.

EpBunch\_3 adds the ability to add functions to EpBunch objects. This
would allow the object to make calculations using data within the
object. So ``BuildingSurface:Detailed`` object has all the geometry data
of the object. The function 'area' will let us calculate the are of the
object even though area is not a field in ``BuildingSurface:Detailed``.

So you can call ``idf1.idfobjects["BuildingSurface:Detailed"][0].area``
and get the area of the surface.

At the moment, the functions can use only data within the object for
it's calculation. We need to extend this functionality so that
calculations can be done using data outside the object. This would be
useful in calculating the volume of a Zone. Such a calculation would
need data from the surfaces that the aone refers to.

EpBunch\_4
~~~~~~~~~~


``EpBunch_4`` is subclassed from ``EpBunch_3``.

``EpBunch_4`` overrides ``_setitem__`` and ``__getitem__``. Right now
``airgap.Name`` works. This update allows ``airgap["Name"]`` to work
correctly too

EpBunch\_5
~~~~~~~~~~


``EpBunch_5`` is subclassed from ``EpBunch_4``.

``EpBunch_5`` adds functions that allows you to call functions
``getrange`` and ``checkrange`` for a field

Finally EpBunch
~~~~~~~~~~~~~~~


``EpBunch = EpBunch_5``

Finally ``EpBunch_5`` is named as EpBunch. So the rest of the code uses
EpBunch and in effect it uses ``Epbunch_5``
