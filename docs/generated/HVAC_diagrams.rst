In[1]:
.. code:: python

    """HVAC diagrams"""





.. parsed-literal::
    'HVAC diagrams'


In[2]:
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
In[3]:
.. code:: python

    from eppy import modeleditor 
    from eppy.modeleditor import IDF
    iddfile = "../eppy/resources/iddfiles/Energy+V8_0_0.idd"
    fname = "../eppy/resources/idffiles/V8_0_0/5ZoneSupRetPlenRAB.idf"
    IDF.setiddname(iddfile)
In[4]:
.. code:: python

    idf = IDF(fname)
In[5]:
.. code:: python

    # idf.model
In[6]:
.. code:: python

    from eppy.EPlusInterfaceFunctions import readidf
    from eppy.ex_loopdiagram import makeairplantloop, makediagram
    
    print "readingfile"
    data, commdct = readidf.readdatacommdct(fname, iddfile=iddfile)
    print "constructing the loops"
    edges = makeairplantloop(data, commdct)
    print "making the diagram"
    g = makediagram(edges)
    dotname = "a.dot"
    pngname = "a.png"
    # dotname = '%s.dot' % (os.path.splitext(fname)[0])
    # pngname = '%s.png' % (os.path.splitext(fname)[0])
    g.write(dotname)
    g.write_png(pngname)




.. parsed-literal::

    readingfile
    constructing the loops
    making the diagram




.. parsed-literal::
    True


In[ ]:
.. code:: python

    
