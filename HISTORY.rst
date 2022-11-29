=======
History
=======

Changes
~~~~~~~

release r0.5.61
~~~~~~~~~~~~~~~

2022-11-26
----------

fixed issue #401
````````````````

:Problem: idf.run() does a saveas("in.idf") and does NOT go back to original name
:Solution: do saveas("ranmdomname.idf") and go back to original name


2022-11-25
----------

fixed issue #396
````````````````

:Problem: documentation "Running EnergyPlus from Eppy" needs updating
:Solution: Updated

2022-11-24
----------

fixed issue # 397
`````````````````

:Problem: runIDFs is hard to debug since temporary files are deleted
:Solution: runIDFs( ... , debug=True) will retain those files


release r0.5.60
~~~~~~~~~~~~~~~

2022-11-08
----------

issues #395, #393, #291 fixes the following problem

:Problem: eppy reads IDD file  at the start of a script and uses it to understand the structure of the IDF file. 

    - Some IDD/IDF objects have extensible fields. 
    - For example the coordinates of a surface can have a large number of coordinates points X, Y, Z.
    - The IDD file may list only 5 of these points (I just made up the number 5 to illustrate the problem)
    - The fields in the IDD file will look like this:
        - X1, Y1, Z1
        - X2, Y2, Z2
        - X3, Y3, Z3
        - X4, Y4, Z4
        - X5, Y5, Z5
    - Now, it the IDF file has 6 coordinate points for a surface, eppy will not work, since eppy trusts the IDD file and thinks that a surface can have only 5 points
    - To make this work, the IDD file would need to have X6, Y6, Z6 in it
    - If you update the the IDD file with X6, Y6, Z6 and run the eppy script again, it would work
    - Updating the IDD file is cumbersome. Can eppy work without updating the IDD file ?
    
:Solution: fixing issues #395, #393, #291 allows eppy to work without updating the IDD file. Eppy will automatically extend the extensible fields from the IDD when the IDF file has more fields than the IDD file. This modification is done in the memory of eppy and the original IDD file on disk is not touched.

2022-10-09
----------

fixed issue #395

:Problem: dunder of setattr, getattr, setitem, getitem fail for an extensible field that is not in the IDD
:Solution: updated the dunders to extend the fields in IDD that is in eppy's memory

dunder = double underscore such as `__setattr__`

2022-10-07
----------

fixed issue #393
````````````````

:Problem: idf.newidfobject() will not work if you make it with more extensible fields than there are in the IDD
:Solution: Increase the extensible fields of the IDD (in memory of eppy) to match the fields in idf.newidfobject()


fixed issue #394
````````````````

:Problem: In idf.newidfobject(self, key, aname="", ... **kwargs), aname is depreceated
:Solution: remove aname form newidfobject

2022-10-06
----------

Fixed issue #391
````````````````

:Problem: If the IDF files has more extensible fields than the IDD file for an idfobject, the read will fail
:Solution: Increase the extensible fields of the IDD (in memory) to match the IDF file. It will not change the `Energy+.idd` on the disk.

release r0.5.59
~~~~~~~~~~~~~~~

2022-05-26
----------

Fixed issue # 386
`````````````````

:Problem: surface.area (for Building:Surface:Detailed) does not work when first 3 points are linear and numpy is installed.
:Solution: This is because numpy does not throw a ZeroDivisionError but raises a RuntimeWarning. Ensure that a ZeroDivisionError is raised in geometry.surface.unit_normal

release r0.5.58
~~~~~~~~~~~~~~~


2022-05-04
----------

fixed issue #384
````````````````

:Problem: surface.area (for Building:Surface:Detailed) does not work when first 3 points are linear
:Solution: Try the other points until you hit 3 non-linear points. Area will be calculated if any points are non-linear


release r0.5.57
~~~~~~~~~~~~~~~

Date:   Thu Dec 9 22:33:17 2021 -0800
-------------------------------------

fixed issue #368
    
    :Problem: docstrings in modeleditor.py ask for of ALL_CAPS.
    :Solution: eppy no longer needs ALL_CAPS keys. Removed ALL_CAPS from docstrings

Date:   Thu Dec 9 22:25:45 2021 -0800
-------------------------------------

fixed issue #361
    
    :Problem: DeprecationWarning: Using or importing the ABCs from 'collections'
    :Solution: import from 'collections.abc'


release r0.5.56
~~~~~~~~~~~~~~~

Date:   Tue Nov 9 08:18:06 2021 -0800
-------------------------------------
    
    Introduce Silent Verbose Mode (Issue #364)

Date:   Sun Nov 7 05:58:16 2021 -0800
-------------------------------------
    
    Add function to remove all IDF object of a certain type

Date:   Sun Oct 3 17:17:05 2021 -0700
-------------------------------------
    
    Use imap when processing generator-created jobs in runIDFs


Date:   Sun Oct 3 16:26:25 2021 -0700
-------------------------------------
    
    Use output_prefix to determine error filename


Date:   Sun Oct 3 15:53:00 2021 -0700
-------------------------------------

    fixed problem: idf.run does not restore sys.stderr properly


Date:   Sat Jul 24 06:56:54 2021 -0700
--------------------------------------

    Correctly check if multiprocessing is supported

Date:   Sat Jul 24 06:08:47 2021 -0700
--------------------------------------

    made idd path absolute
	
2021-02-21
----------

fixed issue #326
````````````````

:Problem: idf = IDF(fname) will fail if isinstance(fname, filepath.Path)
:Solution: update code to read filepath.Path

fixed issue # 315
``````````````````

:Problem: idf.save uses relative path. if the dir is changed, it can save in the wrong place
:Solution: use absolute path in idf.save

release r0.5.56
~~~~~~~~~~~~~~~

2021-02-15
----------

fixed a typo in this file (HISTORY.rst)


release r0.5.55
~~~~~~~~~~~~~~~

2021-02-15
----------

- fixed issue #324

**Problem**

- The EnergyPlus objects can have legal names in the following format `Special glass <thickness is 3mm>`
-  Energyplus itself has no problems with such names
- This name turns up in the HTML output file.
    - In the HTML file the part name`<thickness is 3mm>` looks like an HTML tag.
    - The browser tries to make sense of it and fix it so that something can be displayed
    - This results in a mangled name in the HTML file as viewed in the browser

**Solution**

- Ideally this has to be fixed in Energyplus
- eppy has a stop gap fix
- eppy will ignore any tag within a cell of a table 


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

