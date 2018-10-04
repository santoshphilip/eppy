
IDF in modeleditor
==================


The previous section talks about EpBunch, which deals with a single
object from Energyplus. Here we put all the pieces together so that we
have the entire **IDF** file

Class IDF
---------


IDF0 is the first class that was written. As the code was refined, it
was further refined to by subclassing to IDF1, IDF2, IDF3. Finally the
following was set as IDF = IDF3

Class IDF0
----------


Some important methods in IDF0

IDF0.setiddname
~~~~~~~~~~~~~~~


This method has a decorator ``@classmethod``. This decorator makes the
method a class method. From a stackoverflow comment, I found a brief
description of when this should be used.

``"Class methods are essential when you are doing set-up or computation that precedes the creation of an actual instance, because until the instance exists you obviously cannot use the instance as the dispatch point for your method calls"``

Having said that, I am outside my comfort zone on trying to explain this
in any depth. I will simply explain what I am doing with this here.
Below is a brief explanation intent.

-  the idd file is a very large file. There is a large overhead in
   opening more than one idd file.
-  A design decision was made to use only one idd file to be used in a
   script.
-  This means that you cannot open two idf files that are of different
   version (meaning they will use different idd files)
-  You can open any number of idf file as long as they are of the same
   version (meaing, the use the same idd file)

The class method allows us to achieve the objective:

-  The class method 'setiddname', allows us to set the name of the idd
   file, before creating an instance of IDF. It is set by the statement
   ``IDF.setiddname(iddfilename)``
-  There are other class methods that make sure that this idd name
   cannot be changed.
-  An instance of the class IDF is created using the statement
   ``idf = IDF(idffilename)``. This can be done multiple times, creating
   multiple instances and they will all use the same idd file


IDF0.\ ``__init__``
~~~~~~~~~~~~~~~~~~~


IDF is initialized by passing it the idf file name. I would look like
this:

    idf1 = IDF(filename) # filename can be a file name, file handle or an StringIO

-  Once the class is initialized, it will read the idf file.
-  If this the first time the class is inititalized, the idd file set by
   ``setiddname()`` will be read too.
-  the idd file is read only once and then same copy is used.


IDF0.read
~~~~~~~~~


The read function is called when the class IDF is initialized. The read
function calls routines from the original EPlusInterface program to do
the actual read. The read get the values for the following variables:

-  idfobjects
-  model.dt
-  model.dtls
-  idd\_info

The functions within EPlusInterface are not documented here. I wrote
them in 2004 and I have no idea how I did them. they have been working
really well with some minor updates. I don't intent to poke at that code
yet.

Other IDF methods
-----------------


The other functions in IDF0, IDF1, IDF2 and IDF3 not too complicated. It
should be possible to understand them by reading the code.

Sometime in the future, these functions will be documented later in more
detail
