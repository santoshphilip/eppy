####################################
running energyplus from command line
####################################



- copy all files into the working folder 
- coded for Energyplusv6-0-0 
    - for another version, do a search for Energyplusv6-0-0 and modify in source file


----

EPLUS.BAT
---------

- to run a single idf file

command

- eplus idffilename
    without idf extension

Weather file

- weather file name must be in weatherfile.txt as the first line without the extension
- the weather file should be in the weatherfiles folder of the root energyplus directory.



MEPLUS.BAT
----------

- to run multiple idf files with preprocessing routines
- set up the tasks in runlist.txt

command to run tasks

- meplus

runlist.txt structure::

    c:/Energyplusv6-0-0/mruneplus idffilename weatherfilename
    python somethin.py | c:/Energyplusv6-0-0/mruneplus idffilename1 weatherfilename
    python somethin.py | c:/Energyplusv6-0-0/mruneplus idffilename2 weatherfilename
    c:/Energyplusv6-0-0/mruneplus idffilename3 weatherfilename
    c:/Energyplusv6-0-0/mruneplus idffilename4 weatherfilename
    
this will run the following

- c:/Energyplusv6-0-0/mruneplus idffilename weatherfilename
- python somethin.py
- c:/Energyplusv6-0-0/mruneplus idffilename1 weatherfilename
- python somethin.py
- c:/Energyplusv6-0-0/mruneplus idffilename2 weatherfilename 
- c:/Energyplusv6-0-0/mruneplus idffilename3 weatherfilename
- c:/Energyplusv6-0-0/mruneplus idffilename4 weatherfilename

prerequisite:

- in c:/Energyplusv6-0-0/
    - copy runeplus.bat mruneplus.bat
    - add the following lines to the end of mruneplus.bat
        - nextbat.py
        - meplus_main.bat
- the weather file should be in the weatherfiles folder of the root energyplus directory.
            