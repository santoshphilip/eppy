
Running EnergyPlus from Eppy
============================

It would be great if we could run EnergyPlus directly from our IDF
wouldn’t it?

Well here’s how we can.

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

.. code:: python

    from eppy.modeleditor import IDF
    
    iddfile = "/Applications/EnergyPlus-8-3-0/Energy+.idd"
    IDF.setiddname(iddfile)


.. code:: python

    idfname = "/Applications/EnergyPlus-8-3-0/ExampleFiles/BasicsFiles/Exercise1A.idf"
    epwfile = "/Applications/EnergyPlus-8-3-0/WeatherData/USA_IL_Chicago-OHare.Intl.AP.725300_TMY3.epw"
    
    idf = IDF(idfname, epwfile)
    idf.run()

if you are in a terminal, you will see something like this::

    
    Processing Data Dictionary
    Processing Input File
    Initializing Simulation
    Reporting Surfaces
    Beginning Primary Simulation
    Initializing New Environment Parameters
    Warming up {1}
    Warming up {2}
    Warming up {3}
    Warming up {4}
    Warming up {5}
    Warming up {6}
    Starting Simulation at 07/21 for CHICAGO_IL_USA COOLING .4% CONDITIONS DB=>MWB
    Initializing New Environment Parameters
    Warming up {1}
    Warming up {2}
    Warming up {3}
    Warming up {4}
    Warming up {5}
    Warming up {6}
    Starting Simulation at 01/21 for CHICAGO_IL_USA HEATING 99.6% CONDITIONS
    Writing final SQL reports
    EnergyPlus Run Time=00hr 00min  0.24sec


It’s as simple as that to run using the EnergyPlus defaults, but all the
EnergyPlus command line interface options are also supported.

To get a description of the options available, as well as the defaults
you can call the Python built-in help function on the IDF.run method and
it will print a full description of the options to the console.

.. code:: python

    help(idf.run)


.. parsed-literal::

    Help on method run in module eppy.modeleditor:
    
    run(self, **kwargs) method of eppy.modeleditor.IDF instance
        This method wraps the following method:
        
        run(idf=None, weather=None, output_directory=u'', annual=False, design_day=False, idd=None, epmacro=False, expandobjects=False, readvars=False, output_prefix=None, output_suffix=None, version=False, verbose=u'v', ep_version=None)
            Wrapper around the EnergyPlus command line interface.
            
            Parameters
            ----------
            idf : str
                Full or relative path to the IDF file to be run, or an IDF object.
            
            weather : str
                Full or relative path to the weather file.
            
            output_directory : str, optional
                Full or relative path to an output directory (default: 'run_outputs)
            
            annual : bool, optional
                If True then force annual simulation (default: False)
            
            design_day : bool, optional
                Force design-day-only simulation (default: False)
            
            idd : str, optional
                Input data dictionary (default: Energy+.idd in EnergyPlus directory)
            
            epmacro : str, optional
                Run EPMacro prior to simulation (default: False).
            
            expandobjects : bool, optional
                Run ExpandObjects prior to simulation (default: False)
            
            readvars : bool, optional
                Run ReadVarsESO after simulation (default: False)
            
            output_prefix : str, optional
                Prefix for output file names (default: eplus)
            
            output_suffix : str, optional
                Suffix style for output file names (default: L)
                    L: Legacy (e.g., eplustbl.csv)
                    C: Capital (e.g., eplusTable.csv)
                    D: Dash (e.g., eplus-table.csv)
            
            version : bool, optional
                Display version information (default: False)
            
            verbose: str
                Set verbosity of runtime messages (default: v)
                    v: verbose
                    q: quiet
            
            ep_version: str
                EnergyPlus version, used to find install directory. Required if run() is
                called with an IDF file path rather than an IDF object.
            
            Returns
            -------
            str : status
            
            Raises
            ------
            CalledProcessError
            
            AttributeError
                If no ep_version parameter is passed when calling with an IDF file path
                rather than an IDF object.
    


*Note 1:* idf.run() works for E+ version >= 8.3
*Note 2:* idf.run(readvars=True) has been tested only for E+ version >= 8.9. It may work with earlier versions


Running in parallel processes
-----------------------------

One of the great things about Eppy is that it allows you to set up a lot
of jobs really easily. However, it can be slow running a lot of
EnergyPlus simulations, so it’s pretty important that we can make the
most of the processing power you have available by running on multiple
CPUs.

Again this is as simple as you’d hope it would be.

You first need to create your jobs as a list of lists in the form::

    
    [[<IDF object>, <dict of command line parameters>], ...]

The example here just creates 4 identical jobs apart from the
output\_directory the results are saved in, but you would obviously want
to make each job different.

Then run the jobs on the required number of CPUs using runIDFs...

... and your results will all be in the output\_directory you specified.

Debugging and reporting problems
--------------------------------

Debugging issues with `IDF.run()` used to be difficult, since you needed to
go and hunt for the `eplusout.err` file, and the error message returned was
not at all helpful.

Now the output from EnergyPlus is returned in the error message, as well as
the location and contents of `eplusout.err`.

For example, this is the error message produced when running an IDF which contains an
"HVACTemplate:Thermostat" object without passing `expand_objects=True` to
`idf.run()`::


    E           eppy.runner.run_functions.EnergyPlusRunError:
    E           Program terminated: EnergyPlus Terminated--Error(s) Detected.
    E
    E           Contents of EnergyPlus error file at C:\Users\jamiebull1\git\eppy\eppy\tests\test_dir\eplusout.err
    E           Program Version,EnergyPlus, Version 8.9.0-40101eaafd, YMD=2018.10.14 20:49,
    E              ** Severe  ** Line: 107 You must run the ExpandObjects program for "HVACTemplate:Thermostat"
    E              **  Fatal  ** Errors occurred on processing input file. Preceding condition(s) cause termination.
    E              ...Summary of Errors that led to program termination:
    E              ..... Reference severe error count=1
    E              ..... Last severe error=Line: 107 You must run the ExpandObjects program for "HVACTemplate:Thermostat"
    E              ************* Warning:  Node connection errors not checked - most system input has not been read (see previous warning).
    E              ************* Fatal error -- final processing.  Program exited before simulations began.  See previous error messages.
    E              ************* EnergyPlus Warmup Error Summary. During Warmup: 0 Warning; 0 Severe Errors.
    E              ************* EnergyPlus Sizing Error Summary. During Sizing: 0 Warning; 0 Severe Errors.
    E              ************* EnergyPlus Terminated--Fatal Error Detected. 0 Warning; 1 Severe Errors; Elapsed Time=00hr 00min  0.16sec


When reporting any issues related to `IDF.run()`, please include the error message
as well as the code used to call the function. Also, it may help to include an IDF
and EPW which display the problem so that we can try to reproduce it.