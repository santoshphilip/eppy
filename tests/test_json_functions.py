# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for json_functions"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eppy import modeleditor
from eppy.modeleditor import IDF
from io import StringIO

from eppy.iddcurrent import iddcurrent

from eppy import json_functions


# idd is read only once in this test
# if it has already been read from some other test, it will continue with
# the old reading
iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)


def test_key2elements():
    """py.test for key2elements"""
    data = (
        ("a.b.c.d", ["a", "b", "c", "d"]),  # key, elements
        ("idf.a.Name.name.c", ["idf", "a", "Name.name", "c"]),  # key, elements
        ("idf.a.'Name.name'.c", ["idf", "a", "Name.name", "c"]),  # key, elements
        ("idf.a.'Name.name.n'.c", ["idf", "a", "Name.name.n", "c"]),  # key, elements
    )
    for key, elements in data:
        result = json_functions.key2elements(key)
        # print(result)
        # print(elements)
        assert result == elements


def test_updateidf():
    """py.test for updateidf"""
    iddtxt = """!IDD_Version 8.4.0"""
    data = (
        (
            """Version,
        8.3;                     !- Version Identifier

    """,
            {"idf.version..Version_Identifier": "0.1"},
            "version",
            "Version_Identifier",
            "0.1",
        ),  # idftxt, dct, key, field, fieldval
        (
            """SimulationControl,
    No,                      !- Do Zone Sizing Calculation
    No,                      !- Do System Sizing Calculation
    No,                      !- Do Plant Sizing Calculation
    No,                      !- Run Simulation for Sizing Periods
    Yes;                     !- Run Simulation for Weather File Run Periods
    """,
            {"idf.SimulationControl..Do_Zone_Sizing_Calculation": "Yes"},
            "SimulationControl",
            "Do_Zone_Sizing_Calculation",
            "Yes",
        ),  # idftxt, dct, key, field, fieldval
        (
            """Building,
    Untitled,                !- Name
    0.0,                     !- North Axis {deg}
    City,                    !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullInteriorAndExterior, !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    ;                        !- Minimum Number of Warmup Days
    """,
            {"idf.BUilding.Untitled.Terrain": "Rural"},
            "Building",
            "Terrain",
            "Rural",
        ),  # idftxt, dct, key, field, fieldval
        # make a new object
        (
            """
    """,
            {"idf.BUilding.Taj.Terrain": "Rural"},
            "Building",
            "Terrain",
            "Rural",
        ),  # idftxt, dct, key, field, fieldval
        # make a new object with no Name field
        (
            """
    """,
            {"idf.GlobalGeometryRules..Starting_Vertex_Position": "UpperLeftCorner"},
            "GlobalGeometryRules",
            "Starting_Vertex_Position",
            "UpperLeftCorner",
        ),  # idftxt, dct, key, field, fieldval
        (
            """Building,
    Name.name,                !- Name
    0.0,                     !- North Axis {deg}
    City,                    !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullInteriorAndExterior, !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    ;                        !- Minimum Number of Warmup Days
    """,
            {"idf.BUilding.Name.name.Terrain": "Rural"},
            "Building",
            "Terrain",
            "Rural",
        ),  # idftxt, dct, key, field, fieldval
        (
            """Building,
    Name.name,                !- Name
    0.0,                     !- North Axis {deg}
    City,                    !- Terrain
    0.04,                    !- Loads Convergence Tolerance Value
    0.4,                     !- Temperature Convergence Tolerance Value {deltaC}
    FullInteriorAndExterior, !- Solar Distribution
    25,                      !- Maximum Number of Warmup Days
    ;                        !- Minimum Number of Warmup Days
    """,
            {"idf.BUilding.'Name.name'.Terrain": "Rural"},
            "Building",
            "Terrain",
            "Rural",
        ),  # idftxt, dct, key, field, fieldval
    )
    for idftxt, dct, key, field, fieldval in data:
        idfhandle = StringIO(idftxt)
        idf = IDF(idfhandle)
        json_functions.updateidf(idf, dct)
        assert idf.idfobjects[key][0][field] == fieldval
