
Plant loops and diagrams in eppy
--------------------------------


| Eppy can build up the topology of a plant loop using single pipes in a
branch.
| Once we do that the simple branch in the loop we have built can be
replaced with a more complex branch.

Let us try this out ans see how it works.

.. code:: python

    from eppy.modeleditor import IDF
    from eppy import hvacbuilder
    
    from StringIO import StringIO
    iddfile = "../eppy/resources/iddfiles/Energy+V7_0_0_036.idd"
    IDF.setiddname(iddfile)
.. code:: python

    # make the topology of the loop
    idf = IDF(StringIO('')) # makes an empty idf file in memory with no file name
    loopname = "p_loop"
    sloop = ['sb0', ['sb1', 'sb2', 'sb3'], 'sb4']
    dloop = ['db0', ['db1', 'db2', 'db3'], 'db4']
    hvacbuilder.makeplantloop(idf, loopname, sloop, dloop)
    idf.saveas("hhh1.idf")

| We have made plant loop and saved it as hhh1.idf.
| Now let us look at what the loop looks like.

| Eppy has a function that can draw the loops.
| We'll use this to view the loop diagram.

| run the following program in the shell.
| (you have to run it from the eppy/eppy folder)

python ex_loopdiagram.py hhh1.idf

| This will output a image by name hhh1.png.
| This image is shown below

.. code:: python

    for_images.display_png(for_images.plantloop1) # display the image below


.. image:: HVAC_Tutorial_files/HVAC_Tutorial_7_0.png


Let us make a new branch and replace the exisiting branch "sb0" that has
the pipe sb0\_pipe

.. code:: python

    # make a new branch chiller->pipe1-> pipe2
    pipe1 = idf.newidfobject("PIPE:ADIABATIC", 'np1')
    chiller = idf.newidfobject("Chiller:Electric".upper(), 'Central_Chiller')
    pipe2 = idf.newidfobject("PIPE:ADIABATIC", 'np2')
    
    loop = idf.getobject('PLANTLOOP', 'p_loop')
    branch = idf.getobject('BRANCH', 'sb0')
    listofcomponents = [chiller, pipe1, pipe2]
    
    newbr = hvacbuilder.replacebranch(idf, loop, branch, listofcomponents, 'Water', False)
    idf.saveas("hhh_new.idf")

.. parsed-literal::

    unknown field Connector_3_Object_Type
    unknown field Connector_3_Object_Type


| We have saved this as file "hhh\_new.idf".
| Let us draw the diagram of this file.

python ex_loopdiagram.py hhh_new.idf

.. code:: python

    reload(ex_inits)
    for_images.display_png(for_images.plantloop2) # display the image below


.. image:: HVAC_Tutorial_files/HVAC_Tutorial_12_0.png

