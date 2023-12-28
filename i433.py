import eppy
from eppy.runner.run_functions import EnergyPlusRunError

goodfile = "goodfile.idf"
badfile = "badfile.idf"
wfile = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
goodidf = eppy.openidf(goodfile, epw=wfile)
badidf = eppy.openidf(badfile, epw=wfile)

idfs = [badidf, goodidf]
for an_idf in idfs:
    try:    
        an_idf.run(verbose='s')
        print(f"sucessfully ran {an_idf.idfname}")
    except EnergyPlusRunError as e:
        print(f"error in running {an_idf.idfname}")        
