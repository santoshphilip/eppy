Changes
=======

2016-05-31
----------

refactored code for class IDF and class EpBunch
fixed a bug in modeleditor.newidfobject

release r0.5.2
~~~~~~~~~~~~~~

2016-05-27
----------

added ability to update idf files thru JSON messages.

2016-04-02
----------

Replaced library bunch with munch

release r0.5.1
~~~~~~~~~~~~~~

2016-02-07
----------

- bug fix -> read files that have mixed line endings. Both DOS and Unix line endings

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

