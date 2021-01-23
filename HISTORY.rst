=======
History
=======

Changes
~~~~~~~

release r0.5.54
~~~~~~~~~~~~~~~

2021-01-10
----------

- fixed issue #320
    - Problem: eppy.results.readhtml is very slow. Write similar function using generators
    - Solution: functions in eppy.fasthtml use lazy evaluation to get the tables quickly. This has been documented in user documentation in "Reading outputs from E+" and in "New functions"


release r0.5.53
~~~~~~~~~~~~~~~

2020-10-25
----------

- fixed issue #302
    - Problem: no documentation for multiprocessing runs
    - Solution: added documentation for multiprocessing runs in ./docs/runningeplus.ipynb



2020-09-03
----------

- Partial fix for #287 (deprecate python2)
    - removed six in most places
    - removed python2 in .travis.yml
    - removed python2 in appveyor.yml


2020-06-20
----------

- fixed issue #291
    - used cookiecutter template for eppy
    - from https://github.com/cookiecutter/cookiecutter
- eases development, because the following commands are available from ``make``::
    
    clean                remove all build, test, coverage and Python artifacts
    clean-build          remove build artifacts
    clean-pyc            remove Python file artifacts
    clean-test           remove test and coverage artifacts
    lint                 check style with flake8
    test                 run tests quickly with the default Python
    test-all             run tests on every Python version with tox
    coverage             check code coverage quickly with the default Python
    docs                 generate Sphinx HTML documentation, including API docs
    servedocs            compile the docs watching for changes
    release              package and upload a release
    dist                 builds source and wheel package
    install              install the package to the active Python's site-packages
    

2020-06-13
----------

- fixed issue #289    
    - Problem: E+ is unable to read numbers that are wider than 19 digits
    - Solution: format these numbers in scientific notation

2020-06-07
----------

- fixed issue #281
    - Problem: pytest failing in python 2
    - Solution: Set the correct version numbers in the requirements.txt file

2020-06-05
----------

- fixed issue # 283
    - surface.azimuth calculates the azimuth from the surface coordinates
    - surface.true_azimuth also include the effecto building azimuth ans zone azimuth
    



release r0.5.52
~~~~~~~~~~~~~~~

2019-09-14
----------

- fixed issue #245 
    - Error handling errors in python 3
    
2019-08-17
----------

- fixed issue #254 
   - when running a simulation:
       - Add expandobjects flag if any HVACTemplate objects are present in IDF
    
2019-08-03
----------

- fixed issue #251
    - Run black on the whole codebase.
    - Added black --check . to the Travis config for Python 3.7 on linux for master and non-master branches, to fail if formatting inconsistencies are found.

release r0.5.51
~~~~~~~~~~~~~~~

2019-07-14
----------

- updated version number in setup.py

release r0.5.50
~~~~~~~~~~~~~~~

2019-07-06
----------

- Fixed an installation bug
    - issue # 247

2019-06-11
----------

- Allows mixed cases for specifying objects:
    - issue # 242
- the code now works in the following way::    

    # you can use:
    objs = idf.idfobjects['ElectricEquipment']
    # instead of 
    objs = idf.idfobjects['ElectricEquipment'.upper()]
    
2019-06-02
----------

- Fixes the TypeError
    - 'TypeError: can only concatenate list (not "dict_keys") to list' is fixed
    - issue # 113, # 239
    

2019-05-27
----------

- fixed issue # 238
    - **Problem:** if the IDF object has more fileds than that in the IDD file, eppy will truncate the object and will give no warning.
    - **Solution:** eppy should throw an exception to warn the user that the IDF file is not readable without changing the IDD file. 
    - The exception message will the text that has to be added to the IDD file, so that it works correctly.
     

release r0.5.49
~~~~~~~~~~~~~~~

2019-05-23
----------

- idf = eppy.openidf(fname) will set idd and open the file
    - issue # 231
- idf = eppy.newidf(version="8.5") will open a blank idf file
    - issue # 231
    
2018-11-22
----------


- fanpower.bhp2pascal(bhp, cfm, fan_tot_eff)
    - issue # 228
- fanpower.watts2pascal(watts, cfm, fan_tot_eff)
    - issue # 228
- updated useful_scripts/idfdiff.py to make the IDD file optional
    - issue # 225
- idf.copyidfobject() returns the copied object
    - issue # 223
- easyopen.easyopen gives more explicit error message when idd file is not found
     - issue # 224

release r0.5.48
~~~~~~~~~~~~~~~

2018-10-03
----------

- using cookiecuter <https://github.com/audreyr/cookiecutter-pypackage> in eppy
- fixed bug in idf.run()
    - the bug resulted in the working directory changing if the run was done with an invalid idf

release r0.5.47
~~~~~~~~~~~~~~~

2018-09-25
----------

- fixed bug in useful_scripts/idfdiff.py

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

