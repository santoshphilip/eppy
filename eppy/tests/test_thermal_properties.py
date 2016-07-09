# Copyright (c) 2016 Jamie Bull
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""Tests for thermal_properties.py
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from StringIO import StringIO

from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF

from eppy.constructions.thermal_properties import INSIDE_FILM_R
from eppy.constructions.thermal_properties import OUTSIDE_FILM_R
from eppy.pytest_helpers import almostequal


iddfhandle = StringIO(iddcurrent.iddtxt)
if IDF.getiddname() == None:
    IDF.setiddname(iddfhandle)
  
single_layer = """
  Construction,
    TestConstruction,                       !- Name
    TestMaterial;                           !- Inside Layer
    
  Material,
    TestMaterial,
    Rough,                   !- Roughness
    0.10,                    !- Thickness {m}
    0.5,                     !- Conductivity {W/m-K}
    1000.0,                  !- Density {kg/m3}
    1200,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.6,                     !- Solar Absorptance
    0.6;                     !- Visible Absorptance
    """
  
double_layer = """
  Construction,
    TestConstruction,        !- Name
    TestMaterial,            !- Inside Layer
    TestMaterial;            !- Outside Layer
    
  Material,
    TestMaterial,
    Rough,                   !- Roughness
    0.10,                    !- Thickness {m}
    0.5,                     !- Conductivity {W/m-K}
    1000.0,                  !- Density {kg/m3}
    1200,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.6,                     !- Solar Absorptance
    0.6;                     !- Visible Absorptance
    """
  
air_gap = """
  Construction,
    TestConstruction,        !- Name
    TestMaterial,            !- Inside Layer
    AirGap,                  !- Layer 2
    TestMaterial;            !- Outside Layer
    
  Material,
    TestMaterial,
    Rough,                   !- Roughness
    0.10,                    !- Thickness {m}
    0.5,                     !- Conductivity {W/m-K}
    1000.0,                  !- Density {kg/m3}
    1200,                    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.6,                     !- Solar Absorptance
    0.6;                     !- Visible Absorptance
  Material:AirGap,
    AirGap,
    0.1;                     !- Thermal Resistance
    """
  

class TestThermalProperties(object):
      
    def test_rvalue_1_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = (INSIDE_FILM_R +
                    m.Thickness / m.Conductivity +
                    OUTSIDE_FILM_R)
        assert c.rvalue == expected
        assert c.rvalue == 0.35

    def test_rvalue_2_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(double_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = (INSIDE_FILM_R +
                    m.Thickness / m.Conductivity +
                    m.Thickness / m.Conductivity +
                    OUTSIDE_FILM_R)
        assert c.rvalue == expected
        assert c.rvalue == 0.55

    def test_rvalue_airgap_construction(self):
        idf = IDF()
        idf.initreadtxt(air_gap)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        a = idf.getobject('MATERIAL:AIRGAP', 'AirGap')
        expected = (INSIDE_FILM_R +
                    m.Thickness / m.Conductivity +
                    a.Thermal_Resistance +
                    m.Thickness / m.Conductivity +
                    OUTSIDE_FILM_R)
        assert almostequal(c.rvalue, expected, places=2)
        assert almostequal(c.rvalue, 0.65, places=2)

    def test_rvalue_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = m.Thickness / m.Conductivity
        assert m.rvalue == expected
        assert m.rvalue == 0.2
          
    def test_ufactor_1_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = 1 / (INSIDE_FILM_R +
                        m.Thickness / m.Conductivity + 
                        OUTSIDE_FILM_R)
        assert c.ufactor == expected
        assert c.ufactor == 1 / 0.35
      
    def test_ufactor_2_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(double_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = 1 / (INSIDE_FILM_R +
                        m.Thickness / m.Conductivity + 
                        m.Thickness / m.Conductivity + 
                        OUTSIDE_FILM_R)
        assert c.ufactor == expected
        assert c.ufactor == 1 / 0.55
      
    def test_ufactor_airgap_construction(self):
        idf = IDF()
        idf.initreadtxt(air_gap)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        a = idf.getobject('MATERIAL:AIRGAP', 'AirGap')
        expected = 1 /(INSIDE_FILM_R +
                       m.Thickness / m.Conductivity +
                       a.Thermal_Resistance +
                       m.Thickness / m.Conductivity +
                       OUTSIDE_FILM_R)
        assert almostequal(c.ufactor, expected, places=2)
        assert almostequal(c.ufactor, 1 / 0.65, places=2)

    def test_ufactor_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = 1 / (m.Thickness / m.Conductivity)
        assert m.ufactor == expected
        assert m.ufactor == 1 / 0.2
              
    def test_heatcapacity_1_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001
        assert c.heatcapacity == expected
        assert c.heatcapacity == 120
      
    def test_heatcapacity_2_layer_construction(self):
        idf = IDF()
        idf.initreadtxt(double_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        assert c.heatcapacity == expected
        assert c.heatcapacity == 240
      
    def test_heatcapacity_airgap_construction(self):
        idf = IDF()
        idf.initreadtxt(air_gap)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        m = idf.getobject('MATERIAL', 'TestMaterial')
        a = idf.getobject('MATERIAL:AIRGAP', 'AirGap')
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        assert almostequal(c.heatcapacity, expected, places=2)
        assert almostequal(c.heatcapacity, 240, places=2)

    def test_heatcapacity_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        expected = (m.Thickness * m.Specific_Heat * m.Density * 0.001)
        assert m.heatcapacity == expected
        assert m.heatcapacity == 120
