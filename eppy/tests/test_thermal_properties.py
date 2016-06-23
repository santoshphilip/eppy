#==============================================================================
# # Copyright (c) 2016 Jamie Bull
# # =======================================================================
# #  Distributed under the MIT License.
# #  (See accompanying file LICENSE or copy at
# #  http://opensource.org/licenses/MIT)
# # =======================================================================
# """py.test for thermal_properties.py"""
#  
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
  
from StringIO import StringIO
  
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
  
  
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
    0.10,                     !- Thickness {m}
    0.5,    !- Conductivity {W/m-K}
    1000.0,                 !- Density {kg/m3}
    1200,    !- Specific Heat {J/kg-K}
    0.9,                     !- Thermal Absorptance
    0.6,                     !- Solar Absorptance
    0.6;                     !- Visible Absorptance
    """
  

class TestThermalProperties(object):
      
    def test_rvalue_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        rvalue = c.rvalue

    def test_rvalue_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        rvalue = m.Thickness / m.Conductivity
        assert rvalue == 0.2
        assert m.rvalue == 0.2
          
    def test_uvalue_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        rvalue = c.uvalue
        assert rvalue == 1/0.35
      
    def test_uvalue_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        uvalue = 1 / (m.Thickness / m.Conductivity)
        assert uvalue == 1/0.2
        assert m.uvalue == 1/0.2
              
    def test_heatcapacity_construction(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        c = idf.getobject('CONSTRUCTION', 'TestConstruction')
        rvalue = c.heatcapacity
        assert rvalue == 120
      
    def test_heatcapacity_material(self):
        idf = IDF()
        idf.initreadtxt(single_layer)
        m = idf.getobject('MATERIAL', 'TestMaterial')
        heatcapacity = (m.Thickness * m.Specific_Heat  * m.Density * 0.001)
        assert heatcapacity == 120
        assert m.heatcapacity == 120
