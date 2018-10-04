Eppy Functions
==============

This Document is a work in progress

The most commonly used eppy functions are gathered here.


IDF functions:

- idf = IDF(fname) # fname or fhandle
- idf.printidf
- idf1.idfobjects['BUILDING']
- idf.save
- idf.saveas
- idf.newidfobject
- idf.copyidfobject
- idf.newidfobject
- idf.removeidfobject
- idf.popidfobject
- idf.copyidfobject

idfobjects function:

- building.Name
- surface azimuth
- surface tilt
- surface area
- building.getrange("Loads_Convergence_Tolerance_Value")
- building.checkrange("Loads_Convergence_Tolerance_Value")
- building.fieldnames

Other Functions:

- area = modeleditor.zonearea(idf, zone.Name)
- volume = modeleditor.zonevolume(idf, zone.Name)
- json_functions.updateidf(idf1, json_str)
- idf_helpers.getidfobjectlist
- idf_helpers.copyidfintoidf
