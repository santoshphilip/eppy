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

commdct = [[{u'format': [u'singleLine'],
   u'group': u'Simulation Parameters',
   u'idfobj': u'Version',
   u'memo': [u'Specifies the EnergyPlus version of the IDF file.'],
   u'unique-object': [u'']},
  {u'default': [u'7.0'],
   u'field': [u'Version Identifier'],
   u'required-field': [u'']}],

 [{u'group': u'Simulation Parameters',
   u'idfobj': u'Building',
   u'memo': [u'Describes parameters that are used during the simulation',
    u'of the building. There are necessary correlations between the entries for',
    u'this object and some entries in the Site:WeatherStation and',
    u'Site:HeightVariation objects, specifically the Terrain field.'],
   u'min-fields': [u'8'],
   u'required-object': [u''],
   u'unique-object': [u'']},
  {u'default': [u'NONE'],
   u'field': [u'Name'],
   u'required-field': [u''],
   u'retaincase': [u'']},
  {u'default': [u'0.0'],
   u'field': [u'North Axis'],
   u'note': [u'degrees from true North'],
   u'type': [u'real'],
   u'units': [u'deg']}],
    
 [{u'format': [u'vertices'],
   u'group': u'Thermal Zones and Surfaces',
   u'idfobj': u'Zone',
   u'memo': [u'Defines a thermal zone of the building.']},
  {u'field': [u'Name'],
   u'reference': [u'ZoneNames',
    u'OutFaceEnvNames',
    u'ZoneAndZoneListNames',
    u'AirflowNetworkNodeAndZoneNames'],
   u'required-field': [u''],
   u'type': [u'alpha']},
  {u'default': [u'0'],
   u'field': [u'Direction of Relative North'],
   u'type': [u'real'],
   u'units': [u'deg']},
],

 [{u'extensible:3': [u'-- duplicate last set of x,y,z coordinates (last 3 fields), remembering to remove ; from "inner" fields.'],
   u'format': [u'vertices'],
   u'group': u'Thermal Zones and Surfaces',
   u'idfobj': u'BuildingSurface:Detailed',
   u'memo': [u'Allows for detailed entry of building heat transfer surfaces. Does not include subsurfaces such as windows or doors.'],
   u'min-fields': [u'19']},
  {u'field': [u'Name'],
   u'reference': [u'SurfaceNames',
    u'SurfAndSubSurfNames',
    u'AllHeatTranSurfNames',
    u'HeatTranBaseSurfNames',
    u'OutFaceEnvNames',
    u'AllHeatTranAngFacNames',
    u'RadGroupAndSurfNames',
    u'SurfGroupAndHTSurfNames',
    u'AllShadingAndHTSurfNames'],
   u'required-field': [u''],
   u'type': [u'alpha']},
  {u'field': [u'Surface Type'],
   u'key': [u'Floor', u'Wall', u'Ceiling', u'Roof'],
   u'required-field': [u''],
   u'type': [u'choice']},
],

 [{u'format': [u'vertices'],
   u'group': u'Thermal Zones and Surfaces',
   u'idfobj': u'FenestrationSurface:Detailed',
   u'memo': [u'Allows for detailed entry of subsurfaces',
    u'(windows, doors, glass doors, tubular daylighting devices).'],
   u'min-fields': [u'19']},
  {u'field': [u'Name'],
   u'reference': [u'SubSurfNames',
    u'SurfAndSubSurfNames',
    u'AllHeatTranSurfNames',
    u'OutFaceEnvNames',
    u'AllHeatTranAngFacNames',
    u'RadGroupAndSurfNames',
    u'SurfGroupAndHTSurfNames',
    u'AllShadingAndHTSurfNames'],
   u'required-field': [u''],
   u'type': [u'alpha']},
  {u'field': [u'Surface Type'],
   u'key': [u'Window',
    u'Door',
    u'GlassDoor',
    u'TubularDaylightDome',
    u'TubularDaylightDiffuser'],
   u'required-field': [u''],
   u'type': [u'choice']},
],

[{u'group': u'Thermal Zones and Surfaces',
   u'idfobj': u'Wall:Exterior',
   u'memo': [u'Allows for simplified entry of exterior walls.',
    u'View Factor to Ground is automatically calculated.']},
  {u'field': [u'Name'],
   u'reference': [u'SurfaceNames',
    u'SurfAndSubSurfNames',
    u'AllHeatTranSurfNames',
    u'HeatTranBaseSurfNames',
    u'AllHeatTranAngFacNames',
    u'RadGroupAndSurfNames',
    u'SurfGroupAndHTSurfNames',
    u'AllShadingAndHTSurfNames'],
   u'required-field': [u''],
   u'type': [u'alpha']},
  {u'field': [u'Construction Name'],
   u'note': [u'To be matched with a construction in this input file'],
   u'object-list': [u'ConstructionNames'],
   u'required-field': [u''],
   u'type': [u'object-list']}],
  
 [{u'group': u'Thermal Zones and Surfaces',
   u'idfobj': u'Window',
   u'memo': [u'Allows for simplified entry of Windows.']},
  {u'field': [u'Name'],
   u'reference': [u'SubSurfNames',
    u'SurfAndSubSurfNames',
    u'AllHeatTranSurfNames',
    u'OutFaceEnvNames',
    u'AllHeatTranAngFacNames',
    u'RadGroupAndSurfNames',
    u'SurfGroupAndHTSurfNames',
    u'AllShadingAndHTSurfNames'],
   u'required-field': [u''],
   u'type': [u'alpha']},
  {u'field': [u'Construction Name'],
   u'note': [u'To be matched with a construction in this input file'],
   u'object-list': [u'ConstructionNames'],
   u'required-field': [u''],
   u'type': [u'object-list']}]
]

def test_makename2refdct():
    """py.test for makename2refdct"""
    # do a simple test
    thedata = (
    (
        {'ZONE':['Z1', 'Z2'], },
        [
            [{'idfobj':'zone'}, {'field':['Name'], 'reference':['Z1', 'Z2']}],
        ]
    ), # expected, simpledct
    (
        {'ZONE':['Z1', 'Z2'], 'WALL':['W1', 'W2']},
        [
            [{'idfobj':'zone'}, {'field':['Name'], 'reference':['Z1', 'Z2']}],
            [{'idfobj':'wall'}, {'field':['Name'], 'reference':['W1', 'W2']}],
        ]
    ), # expected, simpledct
    (
        {'ZONE':['Z1', 'Z2'], 'WALL':['W1', 'W2']},
        [
            [{'idfobj':'zone'}, {'field':['Name'], 'reference':['Z1', 'Z2']}],
            [{'idfobj':'wall'}, {'field':['Name'], 'reference':['W1', 'W2']}],
            [], # put in random stuff
        ]
    ), # expected, simpledct
    (
        {'WALL':['W1', 'W2']},
        [
            [{'idfobj':'zone'}, {'field':['notName'], 'reference':['Z1', 'Z2']}],
            [{'idfobj':'wall'}, {'field':['Name'], 'reference':['W1', 'W2']}],
            [], # put in random stuff
        ]
    ), # expected, simpledct
    (
        {},
        [
            [{'idfobj':'zone'}, {'field':['notName'], 'reference':['Z1', 'Z2']}],
            [{'idfobj':'wall'}, {'field':['Name'], 'noreference':['W1', 'W2']}],
            [], # put in random stuff
        ]
    ), # expected, simpledct
    )
    for expected, simpledct in thedata:            
        result = iddindex.makename2refdct(simpledct)
        assert result == expected
    # the test with real data
    expected = {
        'ZONE':[u'ZoneNames',
                u'OutFaceEnvNames',
                u'ZoneAndZoneListNames',
                u'AirflowNetworkNodeAndZoneNames'],
        'WINDOW':[u'SubSurfNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'WALL:EXTERIOR':[u'SurfaceNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'HeatTranBaseSurfNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'FENESTRATIONSURFACE:DETAILED':[u'SubSurfNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'BUILDINGSURFACE:DETAILED':[u'SurfaceNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'HeatTranBaseSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        
   }
    result = iddindex.makename2refdct(commdct)
    assert result == expected

def test_makeref2namesdct():
    """pytest for makeref2namesdct"""
    thedata = (
    (
        {
            'wall':['surface', 'surfandsubsurf'],
            'roof':['surface', 'surfandsubsurf'],
            'window':['surfandsubsurf', 'subsurf'],
            'skylight':['surfandsubsurf', 'subsurf'],
            'zone':['zname',]
        },
        {
            'surface':set(['wall', 'roof']),
            'subsurf':set(['window', 'skylight']),
            'surfandsubsurf':set(['wall', 'roof', 'window', 'skylight']),
            'zname':set(['zone']),
        }
    ), # name2refdct, expected
    (
        {
        'ZONE':[u'ZoneNames',
                u'OutFaceEnvNames',
                u'ZoneAndZoneListNames',
                u'AirflowNetworkNodeAndZoneNames'],
        'WINDOW':[u'SubSurfNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'WALL:EXTERIOR':[u'SurfaceNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'HeatTranBaseSurfNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'FENESTRATIONSURFACE:DETAILED':[u'SubSurfNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        'BUILDINGSURFACE:DETAILED':[u'SurfaceNames',
                u'SurfAndSubSurfNames',
                u'AllHeatTranSurfNames',
                u'HeatTranBaseSurfNames',
                u'OutFaceEnvNames',
                u'AllHeatTranAngFacNames',
                u'RadGroupAndSurfNames',
                u'SurfGroupAndHTSurfNames',
                u'AllShadingAndHTSurfNames'],
        
        },
        {u'AirflowNetworkNodeAndZoneNames': {'ZONE'},
         u'AllHeatTranAngFacNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'AllHeatTranSurfNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'AllShadingAndHTSurfNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'HeatTranBaseSurfNames': {'BUILDINGSURFACE:DETAILED', 'WALL:EXTERIOR'},
         u'OutFaceEnvNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WINDOW',
          'ZONE'},
         u'RadGroupAndSurfNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'SubSurfNames': {'FENESTRATIONSURFACE:DETAILED', 'WINDOW'},
         u'SurfAndSubSurfNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'SurfGroupAndHTSurfNames': {'BUILDINGSURFACE:DETAILED',
          'FENESTRATIONSURFACE:DETAILED',
          'WALL:EXTERIOR',
          'WINDOW'},
         u'SurfaceNames': {'BUILDINGSURFACE:DETAILED', 'WALL:EXTERIOR'},
         u'ZoneAndZoneListNames': {'ZONE'},
         u'ZoneNames': {'ZONE'}}
    ), # name2refdct, expected
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
    {'idfobj':'referedto1'},
    {
        'field':['Name'],
        'reference':['rname11', 'rname12', 'rname_both'],
    },
    
],

[
    {'idfobj':'referedto2'},
    {
        'field':['Name'],
        'reference':['rname21', 'rname22', 'rname_both'],
    },
    
],  

[
    {'idfobj':'referingobj1'},
    {'field':['Name']},
    {
        'field':['referingfield'],
        'type':['object-list'],
        'object-list':['rname11'],
    }
    
],  

[
    {'idfobj':'referingobj2'},
    {'field':['Name']},
    {
        'field':['referingfield'],
        'type':['object-list'],
        'object-list':['rname_both'],
    }
    
],  

],
# ------------
[
[
    {'idfobj':'referedto1'},
    {
        'field':['Name'],
        'reference':['rname11', 'rname12', 'rname_both'],
    },
    
],

[
    {'idfobj':'referedto2'},
    {
        'field':['Name'],
        'reference':['rname21', 'rname22', 'rname_both'],
    },
    
],  

[
    {'idfobj':'referingobj1'},
    {'field':['Name']},
    {
        'field':['referingfield'],
        'type':['object-list'],
        'object-list':['rname11'],
        'validobjects':set(['referedto1'.upper()]),
    }
    
],  

[
    {'idfobj':'referingobj2'},
    {'field':['Name']},
    {
        'field':['referingfield'],
        'type':['object-list'],
        'object-list':['rname_both'],
        'validobjects':set(['REFEREDTO1', 'REFEREDTO2'])
    }
    
],  
],
    ), # commdct, expected
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
                    reference = item['object-list'][0]
                    validobjects = item['validobjects']
                    assert id(ref2names[reference]) == id(validobjects)
                except KeyError as e:
                    continue
    
