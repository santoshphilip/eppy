# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""py.test for idd_index"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


from eppy.EPlusInterfaceFunctions import iddindex

commdct = [
    [
        {
            "format": ["singleLine"],
            "group": "Simulation Parameters",
            "idfobj": "Version",
            "memo": ["Specifies the EnergyPlus version of the IDF file."],
            "unique-object": [""],
        },
        {"default": ["7.0"], "field": ["Version Identifier"], "required-field": [""]},
    ],
    [
        {
            "group": "Simulation Parameters",
            "idfobj": "Building",
            "memo": [
                "Describes parameters that are used during the simulation",
                "of the building. There are necessary correlations between the entries for",
                "this object and some entries in the Site:WeatherStation and",
                "Site:HeightVariation objects, specifically the Terrain field.",
            ],
            "min-fields": ["8"],
            "required-object": [""],
            "unique-object": [""],
        },
        {
            "default": ["NONE"],
            "field": ["Name"],
            "required-field": [""],
            "retaincase": [""],
        },
        {
            "default": ["0.0"],
            "field": ["North Axis"],
            "note": ["degrees from true North"],
            "type": ["real"],
            "units": ["deg"],
        },
    ],
    [
        {
            "format": ["vertices"],
            "group": "Thermal Zones and Surfaces",
            "idfobj": "Zone",
            "memo": ["Defines a thermal zone of the building."],
        },
        {
            "field": ["Name"],
            "reference": [
                "ZoneNames",
                "OutFaceEnvNames",
                "ZoneAndZoneListNames",
                "AirflowNetworkNodeAndZoneNames",
            ],
            "required-field": [""],
            "type": ["alpha"],
        },
        {
            "default": ["0"],
            "field": ["Direction of Relative North"],
            "type": ["real"],
            "units": ["deg"],
        },
    ],
    [
        {
            "extensible:3": [
                '-- duplicate last set of x,y,z coordinates (last 3 fields), remembering to remove ; from "inner" fields.'
            ],
            "format": ["vertices"],
            "group": "Thermal Zones and Surfaces",
            "idfobj": "BuildingSurface:Detailed",
            "memo": [
                "Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors."
            ],
            "min-fields": ["19"],
        },
        {
            "field": ["Name"],
            "reference": [
                "SurfaceNames",
                "SurfAndSubSurfNames",
                "AllHeatTranSurfNames",
                "HeatTranBaseSurfNames",
                "OutFaceEnvNames",
                "AllHeatTranAngFacNames",
                "RadGroupAndSurfNames",
                "SurfGroupAndHTSurfNames",
                "AllShadingAndHTSurfNames",
            ],
            "required-field": [""],
            "type": ["alpha"],
        },
        {
            "field": ["Surface Type"],
            "key": ["Floor", "Wall", "Ceiling", "Roof"],
            "required-field": [""],
            "type": ["choice"],
        },
    ],
    [
        {
            "format": ["vertices"],
            "group": "Thermal Zones and Surfaces",
            "idfobj": "FenestrationSurface:Detailed",
            "memo": [
                "Allows for detailed entry of subsurfaces",
                "(windows, doors, glass doors, tubular daylighting devices).",
            ],
            "min-fields": ["19"],
        },
        {
            "field": ["Name"],
            "reference": [
                "SubSurfNames",
                "SurfAndSubSurfNames",
                "AllHeatTranSurfNames",
                "OutFaceEnvNames",
                "AllHeatTranAngFacNames",
                "RadGroupAndSurfNames",
                "SurfGroupAndHTSurfNames",
                "AllShadingAndHTSurfNames",
            ],
            "required-field": [""],
            "type": ["alpha"],
        },
        {
            "field": ["Surface Type"],
            "key": [
                "Window",
                "Door",
                "GlassDoor",
                "TubularDaylightDome",
                "TubularDaylightDiffuser",
            ],
            "required-field": [""],
            "type": ["choice"],
        },
    ],
    [
        {
            "group": "Thermal Zones and Surfaces",
            "idfobj": "Wall:Exterior",
            "memo": [
                "Allows for simplified entry of exterior walls.",
                "View Factor to Ground is automatically calculated.",
            ],
        },
        {
            "field": ["Name"],
            "reference": [
                "SurfaceNames",
                "SurfAndSubSurfNames",
                "AllHeatTranSurfNames",
                "HeatTranBaseSurfNames",
                "AllHeatTranAngFacNames",
                "RadGroupAndSurfNames",
                "SurfGroupAndHTSurfNames",
                "AllShadingAndHTSurfNames",
            ],
            "required-field": [""],
            "type": ["alpha"],
        },
        {
            "field": ["Construction Name"],
            "note": ["To be matched with a construction in this input file"],
            "object-list": ["ConstructionNames"],
            "required-field": [""],
            "type": ["object-list"],
        },
    ],
    [
        {
            "group": "Thermal Zones and Surfaces",
            "idfobj": "Window",
            "memo": ["Allows for simplified entry of Windows."],
        },
        {
            "field": ["Name"],
            "reference": [
                "SubSurfNames",
                "SurfAndSubSurfNames",
                "AllHeatTranSurfNames",
                "OutFaceEnvNames",
                "AllHeatTranAngFacNames",
                "RadGroupAndSurfNames",
                "SurfGroupAndHTSurfNames",
                "AllShadingAndHTSurfNames",
            ],
            "required-field": [""],
            "type": ["alpha"],
        },
        {
            "field": ["Construction Name"],
            "note": ["To be matched with a construction in this input file"],
            "object-list": ["ConstructionNames"],
            "required-field": [""],
            "type": ["object-list"],
        },
    ],
]


def test_makename2refdct():
    """py.test for makename2refdct"""
    # do a simple test
    thedata = (
        (
            {"ZONE": ["Z1", "Z2"]},
            [[{"idfobj": "zone"}, {"field": ["Name"], "reference": ["Z1", "Z2"]}]],
        ),  # expected, simpledct
        (
            {"ZONE": ["Z1", "Z2"], "WALL": ["W1", "W2"]},
            [
                [{"idfobj": "zone"}, {"field": ["Name"], "reference": ["Z1", "Z2"]}],
                [{"idfobj": "wall"}, {"field": ["Name"], "reference": ["W1", "W2"]}],
            ],
        ),  # expected, simpledct
        (
            {"ZONE": ["Z1", "Z2"], "WALL": ["W1", "W2"]},
            [
                [{"idfobj": "zone"}, {"field": ["Name"], "reference": ["Z1", "Z2"]}],
                [{"idfobj": "wall"}, {"field": ["Name"], "reference": ["W1", "W2"]}],
                [],  # put in random stuff
            ],
        ),  # expected, simpledct
        (
            {"WALL": ["W1", "W2"]},
            [
                [{"idfobj": "zone"}, {"field": ["notName"], "reference": ["Z1", "Z2"]}],
                [{"idfobj": "wall"}, {"field": ["Name"], "reference": ["W1", "W2"]}],
                [],  # put in random stuff
            ],
        ),  # expected, simpledct
        (
            {},
            [
                [{"idfobj": "zone"}, {"field": ["notName"], "reference": ["Z1", "Z2"]}],
                [{"idfobj": "wall"}, {"field": ["Name"], "noreference": ["W1", "W2"]}],
                [],  # put in random stuff
            ],
        ),  # expected, simpledct
    )
    for expected, simpledct in thedata:
        result = iddindex.makename2refdct(simpledct)
        assert result == expected
    # the test with real data
    expected = {
        "ZONE": [
            "ZoneNames",
            "OutFaceEnvNames",
            "ZoneAndZoneListNames",
            "AirflowNetworkNodeAndZoneNames",
        ],
        "WINDOW": [
            "SubSurfNames",
            "SurfAndSubSurfNames",
            "AllHeatTranSurfNames",
            "OutFaceEnvNames",
            "AllHeatTranAngFacNames",
            "RadGroupAndSurfNames",
            "SurfGroupAndHTSurfNames",
            "AllShadingAndHTSurfNames",
        ],
        "WALL:EXTERIOR": [
            "SurfaceNames",
            "SurfAndSubSurfNames",
            "AllHeatTranSurfNames",
            "HeatTranBaseSurfNames",
            "AllHeatTranAngFacNames",
            "RadGroupAndSurfNames",
            "SurfGroupAndHTSurfNames",
            "AllShadingAndHTSurfNames",
        ],
        "FENESTRATIONSURFACE:DETAILED": [
            "SubSurfNames",
            "SurfAndSubSurfNames",
            "AllHeatTranSurfNames",
            "OutFaceEnvNames",
            "AllHeatTranAngFacNames",
            "RadGroupAndSurfNames",
            "SurfGroupAndHTSurfNames",
            "AllShadingAndHTSurfNames",
        ],
        "BUILDINGSURFACE:DETAILED": [
            "SurfaceNames",
            "SurfAndSubSurfNames",
            "AllHeatTranSurfNames",
            "HeatTranBaseSurfNames",
            "OutFaceEnvNames",
            "AllHeatTranAngFacNames",
            "RadGroupAndSurfNames",
            "SurfGroupAndHTSurfNames",
            "AllShadingAndHTSurfNames",
        ],
    }
    result = iddindex.makename2refdct(commdct)
    assert result == expected


def test_makeref2namesdct():
    """pytest for makeref2namesdct"""
    thedata = (
        (
            {
                "wall": ["surface", "surfandsubsurf"],
                "roof": ["surface", "surfandsubsurf"],
                "window": ["surfandsubsurf", "subsurf"],
                "skylight": ["surfandsubsurf", "subsurf"],
                "zone": ["zname"],
            },
            {
                "surface": set(["wall", "roof"]),
                "subsurf": set(["window", "skylight"]),
                "surfandsubsurf": set(["wall", "roof", "window", "skylight"]),
                "zname": set(["zone"]),
            },
        ),  # name2refdct, expected
        (
            {
                "ZONE": [
                    "ZoneNames",
                    "OutFaceEnvNames",
                    "ZoneAndZoneListNames",
                    "AirflowNetworkNodeAndZoneNames",
                ],
                "WINDOW": [
                    "SubSurfNames",
                    "SurfAndSubSurfNames",
                    "AllHeatTranSurfNames",
                    "OutFaceEnvNames",
                    "AllHeatTranAngFacNames",
                    "RadGroupAndSurfNames",
                    "SurfGroupAndHTSurfNames",
                    "AllShadingAndHTSurfNames",
                ],
                "WALL:EXTERIOR": [
                    "SurfaceNames",
                    "SurfAndSubSurfNames",
                    "AllHeatTranSurfNames",
                    "HeatTranBaseSurfNames",
                    "AllHeatTranAngFacNames",
                    "RadGroupAndSurfNames",
                    "SurfGroupAndHTSurfNames",
                    "AllShadingAndHTSurfNames",
                ],
                "FENESTRATIONSURFACE:DETAILED": [
                    "SubSurfNames",
                    "SurfAndSubSurfNames",
                    "AllHeatTranSurfNames",
                    "OutFaceEnvNames",
                    "AllHeatTranAngFacNames",
                    "RadGroupAndSurfNames",
                    "SurfGroupAndHTSurfNames",
                    "AllShadingAndHTSurfNames",
                ],
                "BUILDINGSURFACE:DETAILED": [
                    "SurfaceNames",
                    "SurfAndSubSurfNames",
                    "AllHeatTranSurfNames",
                    "HeatTranBaseSurfNames",
                    "OutFaceEnvNames",
                    "AllHeatTranAngFacNames",
                    "RadGroupAndSurfNames",
                    "SurfGroupAndHTSurfNames",
                    "AllShadingAndHTSurfNames",
                ],
            },
            {
                "AirflowNetworkNodeAndZoneNames": {"ZONE"},
                "AllHeatTranAngFacNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "AllHeatTranSurfNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "AllShadingAndHTSurfNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "HeatTranBaseSurfNames": {"BUILDINGSURFACE:DETAILED", "WALL:EXTERIOR"},
                "OutFaceEnvNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WINDOW",
                    "ZONE",
                },
                "RadGroupAndSurfNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "SubSurfNames": {"FENESTRATIONSURFACE:DETAILED", "WINDOW"},
                "SurfAndSubSurfNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "SurfGroupAndHTSurfNames": {
                    "BUILDINGSURFACE:DETAILED",
                    "FENESTRATIONSURFACE:DETAILED",
                    "WALL:EXTERIOR",
                    "WINDOW",
                },
                "SurfaceNames": {"BUILDINGSURFACE:DETAILED", "WALL:EXTERIOR"},
                "ZoneAndZoneListNames": {"ZONE"},
                "ZoneNames": {"ZONE"},
            },
        ),  # name2refdct, expected
    )
    for name2refdct, expected in thedata:
        result = iddindex.makeref2namesdct(name2refdct)
        assert result == expected


def test_ref2names2commdct():
    """py.test for ref2names2commdct"""
    thedata = (
        (
            # ------------
            [
                [
                    {"idfobj": "referedto1"},
                    {
                        "field": ["Name"],
                        "reference": ["rname11", "rname12", "rname_both"],
                    },
                ],
                [
                    {"idfobj": "referedto2"},
                    {
                        "field": ["Name"],
                        "reference": ["rname21", "rname22", "rname_both"],
                    },
                ],
                [
                    {"idfobj": "referingobj1"},
                    {"field": ["Name"]},
                    {
                        "field": ["referingfield"],
                        "type": ["object-list"],
                        "object-list": ["rname11"],
                    },
                ],
                [
                    {"idfobj": "referingobj2"},
                    {"field": ["Name"]},
                    {
                        "field": ["referingfield"],
                        "type": ["object-list"],
                        "object-list": ["rname_both"],
                    },
                ],
            ],
            # ------------
            [
                [
                    {"idfobj": "referedto1"},
                    {
                        "field": ["Name"],
                        "reference": ["rname11", "rname12", "rname_both"],
                    },
                ],
                [
                    {"idfobj": "referedto2"},
                    {
                        "field": ["Name"],
                        "reference": ["rname21", "rname22", "rname_both"],
                    },
                ],
                [
                    {"idfobj": "referingobj1"},
                    {"field": ["Name"]},
                    {
                        "field": ["referingfield"],
                        "type": ["object-list"],
                        "object-list": ["rname11"],
                        "validobjects": set(["referedto1".upper()]),
                    },
                ],
                [
                    {"idfobj": "referingobj2"},
                    {"field": ["Name"]},
                    {
                        "field": ["referingfield"],
                        "type": ["object-list"],
                        "object-list": ["rname_both"],
                        "validobjects": set(["REFEREDTO1", "REFEREDTO2"]),
                    },
                ],
            ],
        ),  # commdct, expected
    )
    for commdct, expected in thedata:
        name2refdct = iddindex.makename2refdct(commdct)
        ref2names = iddindex.makeref2namesdct(name2refdct)
        result = iddindex.ref2names2commdct(ref2names, commdct)
        for r_item, e_item in zip(result, expected):
            assert r_item == e_item
            # the test below is ensure that the embedded data is not a copy,
            # but is pointing to the set in ref2names
            for item in r_item:
                try:
                    reference = item["object-list"][0]
                    validobjects = item["validobjects"]
                    assert id(ref2names[reference]) == id(validobjects)
                except KeyError as e:
                    continue
