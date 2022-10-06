"""start to work on issue #391"""

import eppy
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
        # 'ep_version':idfversionstr, # runIDFs needs the version number
            # idf.run does not need the above arg
            # you can leave it there and it will be fine :-)
        'output_prefix':os.path.basename(fname).split('.')[0],
        'output_suffix':'C',
        'output_directory':os.path.dirname(fname),
        'readvars':True,
        'expandobjects':True
        }
    return options



fname = "./temp/temp_runs/Minimal_reports.idf"
fname = "./temp/mv.idf"
fname = "./temp/mv_ext.idf"
iddfile = "./temp/m_ext1.IDD"
wfile = "/Applications/EnergyPlus-8-9-0/WeatherData/USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
idf = eppy.openidf(fname, idd=iddfile, epw=wfile)
# theoptions = make_eplaunch_options(idf)
# idf.run(**theoptions)

i = idf.model.dtls.index("ZoneList".upper())
# idf.idd_info[i]
# print(idf.idd_info[i][-3:])
