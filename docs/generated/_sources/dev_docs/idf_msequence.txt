
Idf\_MSequence - Syntactic Sugar work
=====================================


Underlying Data structure of again
----------------------------------


Let us open a small idf file and look at the underlying data structure.

::

    # assume we have open an IDF file called idf
    # let us add three construction objects to it
    idf.newidfobject('construction'.upper(), Name='C1')
    idf.newidfobject('construction'.upper(), Name='C2')
    idf.newidfobject('construction'.upper(), Name='C3')
    constructions = idf.idfobjects['construction'.upper()]
    print constructions


::

    [
    CONSTRUCTION,             
        C1;                       !- Name
    , 
    CONSTRUCTION,             
        C2;                       !- Name
    , 
    CONSTRUCTION,             
        C3;                       !- Name
    ]


We know that constructions us just syntactic sugar around the underlying
data structure. Let us call the underlying data structure
*real\_constructions*

::

    # set real_constructions
    real_constructions = = idf.model.dt['construction'.upper()]
    print real_constructions


::

    [['CONSTRUCTION', 'C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]


::

    real_constructions -> the underlying data structure
    constructions -> syntactic sugar for real_constructions


So any changes made in constructions should reflected in constructions.
Let us test this out.

::

    constructions[0].Name = 'New C1'
    print constructions


::

    [
    CONSTRUCTION,             
        New C1;                   !- Name
    , 
    CONSTRUCTION,             
        C2;                       !- Name
    , 
    CONSTRUCTION,             
        C3;                       !- Name
    ]


::

    print real_constructions


::

    [['CONSTRUCTION', 'New C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]


Even though we made the change only in *constructions*, we can see the
changes in both *constructions* and *real\_constructions*. ``Ep_Bunch``
takes care of this for us.

::

    print 'type for constructions', type(constructions)


::

    type for constructions <type 'list'>


since constructions is a list, we can do all the list operations on it.
Let us try some of them:

::
    
    constructions.pop(0)
    

::

    CONSTRUCTION,             
        New C1;                   !- Name    


::

    print constructions    


::

    [
    CONSTRUCTION,             
        C2;                       !- Name
    , 
    CONSTRUCTION,             
        C3;                       !- Name
    ]


That makes sense. We poped the first item in the list and now we have
only two items.

Is this change reflected in real\_constructions ?

::

    print real_constructions


::

    [['CONSTRUCTION', 'New C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]


Dammit !! Why not ?

We still have 3 items in real\_constructions and 2 items in
constructions

::

    print 'type for constructions', type(constructions)
    print 'id of constructions', id(constructions)
    print 'type for real_constructions', type(constructions)
    print 'id of real_constructions', id(real_constructions)


::

    type for constructions <type 'list'>
    id of constructions 4576898440
    type for real_constructions <type 'list'>
    id of real_constructions 4535436208


-  Both ``constructions`` and ``real_constructions`` are lists.
-  But looking at their ids, it is clear that they are two different
   lists.
-  poping an item in one list will not pop it in the other list :-(


-  In ``constructions[0].Name =`` ``"New C1"`` we see changes to an item
   within ``constructions`` is reflected within ``real_constructions``
-  ``EpBunch`` takes care of that connection
-  We are having problems with the list functions.
-  we see that pop() does not work for us
-  similarly the results of append(), insert(), sort() and reverse() in
   ``constructions`` will not be reflected in ``real_constructions``

This is how it works in eppy version 0.5

We need to fix this. Now we describe how this problem was fixed.

``constructions`` should be a list-like wrapper around
``real_constructions``. Python has an excellent data structure called
``collections.MutableSequence`` that works perfectly for this. Alex
Martelli has a great discussion of this in this stackoverflow thread
`Overriding append method after inheriting from a Python
List <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>`__

-  So we make a class ``eppy.idf_msequence.Idf_MSequence`` that inherits
   form ``collections.MutableSequence``
-  ``constructions`` is now an instance of
   ``eppy.idf_msequence.Idf_MSequence``
-  reading the above stackoverflow thread and the code wihtin
   ``eppy.idf_msequence.Idf_MSequence`` should show you how it works
-  version of eppy higher than 0.5 will use
   ``eppy.idf_msequence.Idf_MSequence``

Let us take a look at how it works (in all versions of eppy newer than
0.5):

.. code:: python

    # using eppy version greater than 0.5
    import sys
    # pathnameto_eppy = 'c:/eppy'
    pathnameto_eppy = '../../../'
    sys.path.append(pathnameto_eppy)
    from eppy import modeleditor
    from eppy.modeleditor import IDF
    iddfile = "../../../eppy/resources/iddfiles/Energy+V7_2_0.idd"
    fname1 = "../../../eppy/resources/idffiles/V_7_2/smallfile.idf"
    IDF.setiddname(iddfile)
    idf = IDF(fname1)
    
    idf.newidfobject('construction'.upper(), Name='C1')
    idf.newidfobject('construction'.upper(), Name='C2')
    idf.newidfobject('construction'.upper(), Name='C3')
    constructions = idf.idfobjects['construction'.upper()]
.. code:: python

    print constructions

.. parsed-literal::

    [
    CONSTRUCTION,             
        C1;                       !- Name
    , 
    CONSTRUCTION,             
        C2;                       !- Name
    , 
    CONSTRUCTION,             
        C3;                       !- Name
    ]


.. code:: python

    real_constructions = idf.model.dt['construction'.upper()]
    print real_constructions

.. parsed-literal::

    [['CONSTRUCTION', 'C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]


Shall we test ``pop(0)`` here ?

.. code:: python

    constructions.pop(0)



.. parsed-literal::

    
    CONSTRUCTION,             
        C1;                       !- Name




.. code:: python

    print constructions

.. parsed-literal::

    [
    CONSTRUCTION,             
        C2;                       !- Name
    , 
    CONSTRUCTION,             
        C3;                       !- Name
    ]


.. code:: python

    print real_constructions

.. parsed-literal::

    [['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]


Awesome !!! both ``constructions`` and ``real_constructions`` have the
same number of items

.. code:: python

    print type(constructions)
    print type(real_constructions)

.. parsed-literal::

    <class 'eppy.idf_msequence.Idf_MSequence'>
    <type 'list'>


what kind of sorcery is this. How did that work. How does
``Idf.Msequence`` do this magic ? Let us look at that
`link <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>`__
in stackoverflow. The question raised in stackovverflow is:

*I want to create a list that can only accept certain types. As such,
I'm trying to inherit from a list in Python, and overriding the append()
method like so:* and there is a sample code after this.

Alex Martelli responds:

*Not the best approach! Python lists have so many mutating methods that
you'd have to be overriding a bunch (and would probably forget some).*

*Rather, wrap a list, inherit from collections.MutableSequence, and add
your checks at the very few "choke point" methods on which
MutableSequence relies to implement all others.* Alex's code follows
after this point. In ``eppy.idf_msequence`` I have included Alex's code.

Stop here and read through the `stackoverflow
link <http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>`__

Well ... you don't really have to. It does go off on some tangents
unrelated to what we do in eppy.

The strategy in ``eppy.idf_msequence.Idf_MSequence`` is to have two
lists, list1 and list2. To play with this I made a simple class
``TwoLists``. Here ``TwoLists`` acts just like a list. Any operation
list operation on ``TwoLists`` will result in a similar operation on
both list1 and list2. ``TwoLists`` is not used in eppy, I simply use it
to flesh out how ``MutableSequence`` can be used. I am going to play
with ``TwoLists`` here to show you how cool it is :-)

.. code:: python

    from eppy.idf_msequence import TwoLists
    twolists = TwoLists()
    print twolists

.. parsed-literal::

    list1 = [], list2 = []


.. code:: python

    twolists.append(5)
    print twolists

.. parsed-literal::

    list1 = [5], list2 = ['r_5']


.. code:: python

    twolists.append(dict(a=15))
    print twolists

.. parsed-literal::

    list1 = [5, {'a': 15}], list2 = ['r_5', "r_{'a': 15}"]


.. code:: python

    twolists.insert(1, 42)
    print twolists

.. parsed-literal::

    list1 = [5, 42, {'a': 15}], list2 = ['r_5', 'r_42', "r_{'a': 15}"]


.. code:: python

    twolists.pop(-1)



.. parsed-literal::

    {'a': 15}



.. code:: python

    print twolists

.. parsed-literal::

    list1 = [5, 42], list2 = ['r_5', 'r_42']


Isn't that neat !! ``Idf_MSequence`` works in a similar way. Out of
sheer laziness I am going to let you figure it out on your own. (ignore
``Idf_MSequence_old``, since that went in the wrong direction)

.. code:: python

    