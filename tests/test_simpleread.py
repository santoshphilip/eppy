"""py.test for simpleread.py"""
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from io import StringIO
import eppy.simpleread as simpleread


def test_idf2txt():
    """py.test for idf2txt"""
    data = (
        (
            """
        VERSION,
            7.3;                      !- Version Identifier

        SIMULATIONCONTROL,
            Yes,                      !- Do Zone Sizing Calculation
            Yes,                      !- Do System Sizing Calculation
            Yes,                      !- Do Plant Sizing Calculation
            No,                       !- Run Simulation for Sizing Periods
            Yes;                      !- Run Simulation for Weather File Run Periods

        BUILDING,
            Empire State Building,    !- Name
            30.0,                     !- North Axis
            City,                     !- Terrain
            0.04,                     !- Loads Convergence Tolerance Value
            0.4,                      !- Temperature Convergence Tolerance Value
            FullExterior,             !- Solar Distribution
            25,                       !- Maximum Number of Warmup Days
            6;                        !- Minimum Number of Warmup Days

        SITE:LOCATION,
            CHICAGO_IL_USA TMY2-94846,    !- Name
            41.78,                    !- Latitude
            -87.75,                   !- Longitude
            -6.0,                     !- Time Zone
            190.0;                    !- Elevation
        """,
            """;

BUILDING,
Empire State Building,
30.0,
City,
0.04,
0.4,
FullExterior,
25.0,
6.0;

SIMULATIONCONTROL,
Yes,
Yes,
Yes,
No,
Yes;

SITE:LOCATION,
CHICAGO_IL_USA TMY2-94846,
41.78,
-87.75,
-6.0,
190.0;

VERSION,
7.3;
""",
        ),  # intxt, outtxt
    )
    for intxt, outtxt in data:
        result = simpleread.idf2txt(intxt)
        assert result == outtxt


def test_idfreadtest():
    """py.test for idfreadtest"""
    data = (
        (
            """!IDD_Version 7.2.0.006
Version,
      \\unique-object
      \\format singleLine
  A1 ; \\field Version Identifier

SimulationControl,
      \\unique-object
  A1, \\field Do Zone Sizing Calculation
  A2, \\field Do System Sizing Calculation
  A3, \\field Do Plant Sizing Calculation
  A4, \\field Run Simulation for Sizing Periods
  A5; \\field Run Simulation for Weather File Run Periods

Building,
       \\unique-object
  A1 , \\field Name
  N1 , \\field North Axis
  A2 , \\field Terrain
  N2 , \\field Loads Convergence Tolerance Value
  N3 , \\field Temperature Convergence Tolerance Value
  A3 , \\field Solar Distribution
  N4 , \\field Maximum Number of Warmup Days
  N5 ; \\field Minimum Number of Warmup Days

Site:Location,
       \\unique-object
  A1 , \\field Name
  N1 , \\field Latitude
  N2 , \\field Longitude
  N3 , \\field Time Zone
  N4 ; \\field Elevation

""",
            """
VERSION,
    7.3;                      !- Version Identifier

SIMULATIONCONTROL,
    Yes,                      !- Do Zone Sizing Calculation
    Yes,                      !- Do System Sizing Calculation
    Yes,                      !- Do Plant Sizing Calculation
    No,                       !- Run Simulation for Sizing Periods
    Yes;                      !- Run Simulation for Weather File Run Periods

BUILDING,
    Empire State Building,    !- Name
    30.0,                     !- North Axis
    City,                     !- Terrain
    0.04,                     !- Loads Convergence Tolerance Value
    0.4,                      !- Temperature Convergence Tolerance Value
    FullExterior,             !- Solar Distribution
    25,                       !- Maximum Number of Warmup Days
    6;                        !- Minimum Number of Warmup Days

SITE:LOCATION,
    CHICAGO_IL_USA TMY2-94846,    !- Name
    41.78,                    !- Latitude
    -87.75,                   !- Longitude
    -6.0,                     !- Time Zone
    190.0;                    !- Elevation
""",
        ),  # iddtxt, idftxt
    )
    for iddtxt, idftxt in data:
        iddhandle = StringIO(iddtxt)
        idfhandle1 = StringIO(idftxt)
        idfhandle2 = StringIO(idftxt)
        result = simpleread.idfreadtest(iddhandle, idfhandle1, idfhandle2)
        assert result == True
