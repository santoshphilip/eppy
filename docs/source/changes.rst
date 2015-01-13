Changes
=======

2015-01-06
----------

- Added a stubs folder with scripts that can be used as templates
- Developer documentation has been completed

2014-10-21
----------

- fixed a bug in script eppy/useful_scripts/loopdiagram.py

2014-10-04
----------

- There is a developer documentation section in the documentation. This is for people who will be working on the code

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

2014-08-21
----------

release r0.463
~~~~~~~~~~~~~~

- added eppy/useful_scripts/eppy_version.py
- updated documentation to match

2014-08-19
----------

release r0.462
~~~~~~~~~~~~~~

- added a script that can compare two idf files. It is documented in "Useful Scripts". The script is in 
    - eppy/usefull_scripts/idfdiff.py
- added two scripts that test if eppy works when new versions of energyplus are released. Documentation for this is not yet done. The scripts are
    - eppy/usefull_scripts/eppyreadtest_file.py
    - eppy/usefull_scripts/eppyreadtest_folder.py
- fixed a bug where eppy would not read backslashes in a path name. Some idf objects have fields that are path names. On dos/windows machines these path names have backslashes

