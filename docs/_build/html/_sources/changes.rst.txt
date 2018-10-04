Changes
=======

next release
~~~~~~~~~~~~

2018-07-06
~~~~~~~~~~

- reorganized the files to use with https://github.com/audreyr/cookiecutter

2018-04-23
----------

- idf.newidfobject() has a parameter defaultvlaues=True or False. This can be toggled to set or not set the default values in the IDF file

2018-03-24
----------

- fixed a bug, where some idfobject fields stayed as strings even though they were supposed to be numbers

2018-03-21
----------

- new function easyopen(idffile) will automatically set the IDD file and open the IDF file. This has been documented in ./docs/source/newfunctions.rst

2017-12-11
----------

- Added documentation in the installation section on how to run eppy in grasshopper
- added functions to get fan power in watts, bhp and fan flow in cfm for any fan object. This has been documented in ./docs/source/newfunctions.rst

release r0.5.46
~~~~~~~~~~~~~~~

2017-12-10
----------

- documentation is now at http://eppy.readthedocs.io/en/latest/

release r0.5.45
~~~~~~~~~~~~~~~

2017-10-01
----------

- fixed a bug in the setup.py (It was not installing some required folders)
- updated documentation to include how to run Energyplus from eppy
- format of the table file was changed in E+ 8.7. 
    - readhtml is updated to be able to read the new format (it still reads the older versions)

release r0.5.44
~~~~~~~~~~~~~~~

2017-05-23
----------

- IDF.run() works with E+ version >= 8.3
    - This will run the idf file
    - documentation updated to reflect this
- Some changes made to support eppy working on grasshopper
    - more work needs to be done on this

release r0.5.43
~~~~~~~~~~~~~~~

2017-02-09
----------

fixed the bug in the setup file

release r0.5.42
~~~~~~~~~~~~~~~

2016-12-31
~~~~~~~~~~

bugfix for idfobjects with no fieldnames. Such fields are named A!, A2, A3/ N1, N2, N3 taken from the IDD file

There is a bug in the setup.py in this version

2016-11-02
----------

It is now possible to run E+ from eppy

release r0.5.41
~~~~~~~~~~~~~~~

2016-09-14
----------

bugfix in loopdiagram.py. Some cleanup by removing extra copies of loopdiagram.py

release r0.5.40
~~~~~~~~~~~~~~~

2016-09-06
----------

This is a release for python2 and python3. pip install will automatically install the correct version.

release r0.5.31
~~~~~~~~~~~~~~~

2016-09-04
----------

bugfix so that json_functions can have idf objects with names that have dots in them

release r0.5.3
~~~~~~~~~~~~~~

2016-07-21
----------

tab completion of fileds (of idfobjects) works in ipython and ipython notebook

2016-07-09
----------

added:

- construction.rfactor and material.rfactor
- construction.uvalue and material.uvalue
- construction.heatcapacity and material.heatcapacity
- the above functions do not work in all cases yet. But are still usefull

added:

- zone.zonesurfaces -> return all surfaces of the zone
- surface.subsurfaces -> will return all the subsurfaces (windows, doors etc.) that belong to the surface

added two functions that scan through the entire idf file:

- EpBunch.getreferingobjs(args)
- EpBunch.get_referenced_object(args)
- they make it possible for an idf object to scan through it's idf file and find other idf objects that are related to it (thru object-list and reference) 


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

