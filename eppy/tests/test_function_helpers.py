from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import pytest
from six import StringIO

import eppy.function_helpers as fh
from eppy.bunch_subclass import register_epbunch_function
from eppy.iddcurrent import iddcurrent
from eppy.modeleditor import IDF
from eppy.tests.test_bunch_subclass import idftxt


class TestRegisterFunction():

    @pytest.fixture()
    def IDF(self):
        iddfhandle = StringIO(iddcurrent.iddtxt)

        if IDF.getiddname() == None:
            IDF.setiddname(iddfhandle)
        yield IDF

    @pytest.fixture()
    def idf(self, IDF):
        idfhandle = StringIO(idftxt)
        yield IDF(idfhandle)

    def test_register_function_area(self, idf):
        """Add a function that comes default with eppy"""

        @register_epbunch_function('area', keys=[
            "BuildingSurface:Detailed",
            "Wall:Detailed",
            "RoofCeiling:Detailed",
            "Floor:Detailed",
            "FenestrationSurface:Detailed",
            "Shading:Site:Detailed",
            "Shading:Building:Detailed",
            "Shading:Zone:Detailed", ])
        @property
        def area(abunch):
            return fh.area(abunch)

        surf = idf.idfobjects["BuildingSurface:Detailed".upper()][0]
        assert surf.area

    def test_register_function_conditioned_area(self, idf):
        """Add a new custom function that does not come default with eppy"""

        @register_epbunch_function('conditioned_area', keys=['Zone'])
        @property
        def conditioned_area(abunch):
            zone = abunch
            area = 0
            for surface in zone.zonesurfaces:
                if surface.tilt == 180.0:
                    part_of = int(
                        zone.Part_of_Total_Floor_Area.upper() != "NO")
                    multiplier = float(
                        zone.Multiplier if zone.Multiplier != '' else 1)

                    area += surface.area * multiplier * part_of
            return area

        zone = idf.idfobjects['Zone'.upper()][0]
        assert dir(zone)
        assert zone.conditioned_area
