Making Syntactic Sugar work
===========================

Underlying Data structure of again
----------------------------------

Let us open a small idf file and look at the underlying data structure.

.. code:: python
    
    # assume we have open an IDF file called idf
    # let us add three construction objects to it
    idf.newidfobject('construction'.upper(), Name='C1')
    idf.newidfobject('construction'.upper(), Name='C2')
    idf.newidfobject('construction'.upper(), Name='C3')
    constructions = idf.idfobjects['construction'.upper()]
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
    
We know that constructions us just syntactic sugar around the underlying data structure. Let us call the underlying data structure *real_constructions*

.. code:: python
    
    # set real_constructions
    real_constructions = = idf.model.dt['construction'.upper()]
    print real_constructions
    
.. parsed-literal::
    
    [['CONSTRUCTION', 'C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]
    
.. parsed-literal::
    
    real_constructions -> the underlying data structure
    constructions -> syntactic sugar for real_constructions
    

So any changes made in constructions should reflected in constructions. Let us test this out.    
    
.. code:: python

    constructions[0].Name = 'New C1'
    print real_constructions
    
.. parsed-literal::

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
    
.. code:: python

    print real_constructions
    
.. parsed-literal::

    [['CONSTRUCTION', 'New C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]
    
Even though we made the change only in *constructions*, we can see the changes in both *constructions* and *real_constructions*.    

.. code:: python

    print 'type for constructions', type(constructions)
    
.. parsed-literal::

    type for constructions <type 'list'>
    
since constructions is a list, we can do all the list operations on it. Let us try some of them:

.. code:: python

    constructions.pop(0)
    
.. parsed-literal::

    CONSTRUCTION,             
        New C1;                   !- Name    

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

That makes sense. We poped the first item in the list and now we have only two items.

Is this change reflected in real_constructions ?

.. code:: python

    print real_constructions
    
.. parsed-literal::

    [['CONSTRUCTION', 'New C1'], ['CONSTRUCTION', 'C2'], ['CONSTRUCTION', 'C3']]

Dammit !! Why not ?

We still have 3 items in real_constructions and 2 items in constructions    

.. code:: python

    print 'type for constructions', type(constructions)
    print 'id of constructions', id(constructions)
    print 'type for real_constructions', type(constructions)
    print 'id of real_constructions', id(real_constructions)
    
.. parsed-literal::

    type for constructions <type 'list'>
    id of constructions 4576898440
    type for real_constructions <type 'list'>
    id of real_constructions 4535436208
    
- Both `constructions` and `real_constructions` are lists. 
- But looking at their ids, it is clear that they are two different lists.
- poping an item in one list will not pop it in the other list :-(

- In `constructions[0].Name =` `"New C1"` we see changes to an item within `constructions` is reflected within `real_constructions`
- `EpBunch` takes care of that connection
- We are having problems with the list functions. 
- we see that pop() does not work for us
- similarly the results of append(), insert(), sort() and reverse() in `constructions` will not be reflected in `real_constructions` 

This is how it works in eppy version 0.5

We need to fix this. Now we describe how this problem was fixed.   

`constructions` should be a list-like wrapper around `real_constructions`. Python has an excellent data structure called `collections.MutableSequence` that works perfectly for this. Alex Martelli has a great discussion of this in this stackoverflow thread `Overriding append method after inheriting from a Python List
<http://stackoverflow.com/questions/3487434/overriding-append-method-after-inheriting-from-a-python-list>`_. 

- So we make a class `eppy.idf_msequence.Idf_MSequence` that inherits form `collections.MutableSequence`
- `constructions` is now an instance of `eppy.idf_msequence.Idf_MSequence`
- reading the above stackoverflow thread and the code wihtin `eppy.idf_msequence.Idf_MSequence` should show you how it works
- version of eppy higher than 0.5 will use `eppy.idf_msequence.Idf_MSequence`

Let us take a look at how it works (in all versions of eppy newer than 0.5):

.. code:: python

    # open a new id file and add constructions to it
    idf.newidfobject('Construction'.upper(), "C1")
    idf.newidfobject('Construction'.upper(), "C2")
    idf.newidfobject('Construction'.upper(), "C3")
    
    constructions = idf.idfobjects['construction'.upper()]
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
