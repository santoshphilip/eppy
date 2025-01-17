"""multiprocessing runs

using generators instead of a list
when you are running a 100 files you have to use generators"""

import os
from eppy.modeleditor import IDF
from eppy.runner.run_functions import runIDFs

def make_eplaunch_options(idf):
    """Make options for run, so that it runs like EPLaunch on Windows"""
    idfversion = idf.idfobjects['version'][0].Version_Identifier.split('.')
    idfversion.extend([0] * (3 - len(idfversion)))
    idfversionstr = '-'.join([str(item) for item in idfversion])
    fname = idf.idfname
    options = {
        'ep_version':idfversionstr, # runIDFs needs the version number
        'output_prefix':os.path.basename(fname).split('.')[0],
        'output_suffix':'C',
        'output_directory':os.path.dirname(fname),
        'readvars':True,
        'expandobjects':True
        }
    return options




def main():
    iddfile = "C:\EnergyPlusV23-2-0\Energy+.idd"
    IDF.setiddname(iddfile)
    epwfile = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"



    # File is from the Examples Folder
    idfname1 = "temp/HVACTemplate-5ZoneBaseboardHeat.idf"
    # copy of previous file
    idfname2 = "./temp/HVACTemplate-5ZoneBaseboardHeat1.idf"


    fnames = [idfname1, idfname2]
    idfs = (IDF(fname, epwfile) for fname in fnames)
    runs = ((idf, make_eplaunch_options(idf) ) for idf in idfs)


    num_CPUs = 2
    runIDFs(runs, num_CPUs)

if __name__ == '__main__':
    main()
