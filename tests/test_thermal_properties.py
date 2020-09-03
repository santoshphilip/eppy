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

import warnings

from io import StringIO

from eppy.constructions.thermal_properties import INSIDE_FILM_R
from eppy.constructions.thermal_properties import OUTSIDE_FILM_R
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
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

expected_failure = """
  Construction,
    TestConstruction,                       !- Name
    Skyhooks;                           !- Inside Layer
    
  Boiler:HotWater,
    Skyhooks,
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

infrared_transparent = """
  Construction,
    TestConstruction,        !- Name
    TestMaterial,            !- Inside Layer
    InfraredTransparent,     !- Layer 2
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
  Material:InfraredTransparent,
    InfraredTransparent;     !- Name
    """

no_mass = """
  Construction,
    TestConstruction,        !- Name
    TestMaterial,            !- Inside Layer
    NoMass,                  !- Layer 2
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
  Material:NoMass,
    NoMass,                  ! Material Name
    ,                        ! Roughness
    0.1,                     ! Resistance {M**2K/W}
    ,                        ! Thermal Absorptance
    ,                        ! Solar Absorptance
    ;                        ! Visible Absorptance
    """

roof_vegetation = """
  Construction,
    TestConstruction,        !- Name
    RoofVegetation;          !- Inside Layer
    
  Material:RoofVegetation,
    RoofVegetation,          !- Name
    ,                        !- Height of Plants {m}
    ,                        !- Leaf Area Index {dimensionless}
    ,                        !- Leaf Reflectivity {dimensionless}
    ,                        !- Leaf Emissivity
    ,                        !- Minimum Stomatal Resistance {s/m}
    ,                        !- Soil Layer Name
    ,                        !- Roughness
    0.1,                     !- Thickness {m}
    0.5,                     !- Conductivity of Dry Soil {W/m-K}
    1000,                    !- Density of Dry Soil {kg/m3}
    1200,                    !- Specific Heat of Dry Soil {J/kg-K}
    ,                        !- Thermal Absorptance
    ,                        !- Solar Absorptance
    ,                        !- Visible Absorptance
    ,                        !- Saturation Volumetric Moisture Content of the Soil Layer
    ,                        !- Residual Volumetric Moisture Content of the Soil Layer
    ,                        !- Initial Volumetric Moisture Content of the Soil Layer
    ;                        !- Moisture Diffusion Calculation Method
    """


class Test_ThermalProperties(object):
    def setup_method(self, test_method):
        self.idf = IDF()

    def test_rvalue_1_layer_construction(self):
        self.idf.initreadtxt(single_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = INSIDE_FILM_R + m.Thickness / m.Conductivity + OUTSIDE_FILM_R
        assert c.rvalue == expected
        assert c.rvalue == 0.35

    def test_rvalue_fails(self):
        self.idf.initreadtxt(expected_failure)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        try:
            c.rvalue
            assert False
        except AttributeError as e:
            assert str(e) == "Skyhooks material not found in IDF"

    def test_rvalue_2_layer_construction(self):
        self.idf.initreadtxt(double_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert c.rvalue == expected
        assert c.rvalue == 0.55

    def test_rvalue_airgap_construction(self):
        self.idf.initreadtxt(air_gap)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        a = self.idf.getobject("MATERIAL:AIRGAP", "AirGap")
        expected = (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + a.Thermal_Resistance
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.rvalue, expected, places=2)
        assert almostequal(c.rvalue, 0.65, places=2)

    def test_rvalue_infraredtransparent_construction(self):
        self.idf.initreadtxt(infrared_transparent)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.rvalue, expected, places=2)
        assert almostequal(c.rvalue, 0.55, places=2)

    def test_rvalue_nomass_construction(self):
        self.idf.initreadtxt(no_mass)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        n = self.idf.getobject("MATERIAL:NOMASS", "NoMass")
        expected = (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + n.Thermal_Resistance
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.rvalue, expected, places=2)
        assert almostequal(c.rvalue, 0.65, places=2)

    def test_rvalue_roofvegetation_construction(self):
        self.idf.initreadtxt(roof_vegetation)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL:ROOFVEGETATION", "RoofVegetation")
        expected = (
            INSIDE_FILM_R + m.Thickness / m.Conductivity_of_Dry_Soil + OUTSIDE_FILM_R
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert c.rvalue == expected
            assert c.rvalue == 0.35
            # check that a UserWarning is raised
            assert issubclass(w[-1].category, UserWarning)

    def test_rvalue_material(self):
        self.idf.initreadtxt(single_layer)
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness / m.Conductivity
        assert m.rvalue == expected
        assert m.rvalue == 0.2

    def test_ufactor_1_layer_construction(self):
        self.idf.initreadtxt(single_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = 1 / (INSIDE_FILM_R + m.Thickness / m.Conductivity + OUTSIDE_FILM_R)
        assert c.ufactor == expected
        assert c.ufactor == 1 / 0.35

    def test_ufactor_2_layer_construction(self):
        self.idf.initreadtxt(double_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = 1 / (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert c.ufactor == expected
        assert c.ufactor == 1 / 0.55

    def test_ufactor_airgap_construction(self):
        self.idf.initreadtxt(air_gap)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        a = self.idf.getobject("MATERIAL:AIRGAP", "AirGap")
        expected = 1 / (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + a.Thermal_Resistance
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.ufactor, expected, places=2)
        assert almostequal(c.ufactor, 1 / 0.65, places=2)

    def test_ufactor_infraredtransparent_construction(self):
        self.idf.initreadtxt(infrared_transparent)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = 1 / (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.ufactor, expected, places=2)
        assert almostequal(c.ufactor, 1 / 0.55, places=2)

    def test_ufactor_nomass_construction(self):
        self.idf.initreadtxt(no_mass)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        n = self.idf.getobject("MATERIAL:NOMASS", "NoMass")
        expected = 1 / (
            INSIDE_FILM_R
            + m.Thickness / m.Conductivity
            + n.Thermal_Resistance
            + m.Thickness / m.Conductivity
            + OUTSIDE_FILM_R
        )
        assert almostequal(c.ufactor, expected, places=2)
        assert almostequal(c.ufactor, 1 / 0.65, places=2)

    def test_ufactor_roofvegetation_construction(self):
        self.idf.initreadtxt(roof_vegetation)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL:ROOFVEGETATION", "RoofVegetation")
        expected = 1 / (
            INSIDE_FILM_R + m.Thickness / m.Conductivity_of_Dry_Soil + OUTSIDE_FILM_R
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert c.ufactor == expected
            assert c.ufactor == 1 / 0.35
            # check that a UserWarning is raised
            assert issubclass(w[-1].category, UserWarning)

    def test_ufactor_material(self):
        self.idf.initreadtxt(single_layer)
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = 1 / (m.Thickness / m.Conductivity)
        assert m.ufactor == expected
        assert m.ufactor == 1 / 0.2

    def test_heatcapacity_1_layer_construction(self):
        self.idf.initreadtxt(single_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001
        assert c.heatcapacity == expected
        assert c.heatcapacity == 120

    def test_heatcapacity_2_layer_construction(self):
        self.idf.initreadtxt(double_layer)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        assert c.heatcapacity == expected
        assert c.heatcapacity == 240

    def test_heatcapacity_airgap_construction(self):
        self.idf.initreadtxt(air_gap)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        assert almostequal(c.heatcapacity, expected, places=2)
        assert almostequal(c.heatcapacity, 240, places=2)

    def test_heatcapacity_infraredtransparent_construction(self):
        self.idf.initreadtxt(infrared_transparent)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        assert almostequal(c.heatcapacity, expected, places=2)
        assert almostequal(c.heatcapacity, 240, places=2)

    def test_heatcapacity_nomass_construction(self):
        self.idf.initreadtxt(no_mass)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001 * 2
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert almostequal(c.heatcapacity, expected, places=2)
            assert almostequal(c.heatcapacity, 240, places=2)
            assert issubclass(w[-1].category, UserWarning)

    def test_heatcapacity_roofvegetation_construction(self):
        self.idf.initreadtxt(roof_vegetation)
        c = self.idf.getobject("CONSTRUCTION", "TestConstruction")
        m = self.idf.getobject("MATERIAL:ROOFVEGETATION", "RoofVegetation")
        expected = (
            m.Thickness * m.Specific_Heat_of_Dry_Soil * m.Density_of_Dry_Soil * 0.001
        )
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # check that a UserWarning is raised
            assert almostequal(c.heatcapacity, expected, places=2)
            assert almostequal(c.heatcapacity, 120, places=2)
            assert issubclass(w[-1].category, UserWarning)

    def test_heatcapacity_material(self):
        self.idf.initreadtxt(single_layer)
        m = self.idf.getobject("MATERIAL", "TestMaterial")
        expected = m.Thickness * m.Specific_Heat * m.Density * 0.001
        assert m.heatcapacity == expected
        assert m.heatcapacity == 120
