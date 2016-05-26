Changes
=======

2016-02-07
----------

- bug fix -> read files that have mixed line endings. Both DOS and Unix line endings

2016-02-05
----------

- idf.save(), idf.saveas(fname), idf.savecopy(fname) save with latin-1 encoding by default. Other endcondings are possible with named argument *encodings*
- all the above saves have a default named argument called *lineendings*::

    idf.save() # -> Save in the native format of the host machine
        # if you are on a unix machine, the line endings would be unix
        # if you are on a windows machine, the line endings would be DOS
    idf.save(lineendings='default') # -> same as idf.save()
    idf.save(lineendings='windows') # -> forces the lineendings to be windows
    idf.save(lineendings='unix') # -> forces the lineendings to be unix
    
2015-10-05
----------

- ``Idf_MSequence`` has been documented. This is important to developers of eppy. Users of eppy should not care :-)

2015-07-23
----------

- eppy will without numpy installed.
- if numpy is installed, it will use numpy

This would be useful in environments where numpy would not run, such as:

- jython
- rhino

release r0.5
~~~~~~~~~~~~

2015-07-12
----------

- python3 version of eppy is in ./p3/eppy
- eppy license has transitioned from GPLv3 to MIT license
- made some bugfixes to hvacbuilder.py

2015-05-30
----------

- bugfix in ./eppy/Air:useful_scripts/idfdiff.py
- added in ./eppy/Air:useful_scripts/idfdiff_missing.py
    - this displays only the missing objects in either file

2015-05-27
----------

- idf.saveas(newname) changes the idf.idfname to newname
    - so the next idf.save() will save to newname
- to retain the original idf.idfname use idf.savecopy(copyname)


2015-05-26
----------

updated the following:
- idf.save(lineendings='default')
- idf.saveas(fname, lineendings='default')

- optional argument lineendings
    - if lineendings='default', uses the line endings of the platform
    - if lineendings='windows', forces windows line endings
    - if lineendings='unix', forces unix line endings

release r0.464a
~~~~~~~~~~~~~~~

2015-01-13
----------

r0.464a released on 2015-01-13. This in alpha release of this version. There may be minor updates after review from users.

2015-01-06
----------

- Developer documentation has been completed
- Added a stubs folder with scripts that can be used as templates

2014-10-21
----------

- fixed a bug in script eppy/useful_scripts/loopdiagram.py

2014-09-01
----------

- added a script eppy/useful_scripts/loopdiagram.py::

    python loopdiagram.py --help
    
    usage: loopdiagram.py [-h] idd file

    draw all the  loops in the idf file
    There are two output files saved in the same location as the idf file:
    - idf_file_location/idf_filename.dot
    - idf_file_location/idf_filename.png

    positional arguments:
      idd         location of idd file = ./somewhere/eplusv8-0-1.idd
      file        location of idf file = ./somewhere/f1.idf

    optional arguments:
      -h, --help  show this help message and exit
      
- fixed a bug in hvacbuilder.makeplantloop and hvacbuilder.makecondenserloop

release r0.463
~~~~~~~~~~~~~~

2014-08-21
----------

- added eppy/useful_scripts/eppy_version.py
- updated documentation to match

release r0.462
~~~~~~~~~~~~~~

2014-08-19
----------

- added a script that can compare two idf files. It is documented in "Useful Scripts". The script is in 
    - eppy/usefull_scripts/idfdiff.py
- added two scripts that test if eppy works when new versions of energyplus are released. Documentation for this is not yet done. The scripts are
    - eppy/usefull_scripts/eppyreadtest_file.py
    - eppy/usefull_scripts/eppyreadtest_folder.py
- fixed a bug where eppy would not read backslashes in a path name. Some idf objects have fields that are path names. On dos/windows machines these path names have backslashes

