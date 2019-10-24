import os

import pytest
from six import StringIO

from eppy.modeleditor import IDF
from eppy.iddcurrent import iddcurrent
from eppy import modeleditor
from eppy.tests.test_runner import versiontuple

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(THIS_DIR, os.pardir, "resources")

IDD_FILES = os.path.join(RESOURCES_DIR, "iddfiles")
IDF_FILES = os.path.join(RESOURCES_DIR, "idffiles")
try:
    VERSION = os.environ["ENERGYPLUS_INSTALL_VERSION"]  # used in CI files
except KeyError:
    VERSION = "8-9-0"  # current default for integration tests on local system
TEST_IDF = "V{}/smallfile.idf".format(VERSION[:3].replace("-", "_"))
TEST_EPW = "USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
TEST_IDD = "Energy+V{}.idd".format(VERSION.replace("-", "_"))
TEST_OLD_IDD = "Energy+V7_2_0.idd"


@pytest.fixture()
def test_idf():
    idd_file = os.path.join(IDD_FILES, TEST_IDD)
    idf_file = os.path.join(IDF_FILES, TEST_IDF)
    modeleditor.IDF.setiddname(idd_file, testing=True)
    idf = modeleditor.IDF(idf_file, TEST_EPW)
    try:
        ep_version = idf.idd_version
        assert ep_version == versiontuple(VERSION)
    except AttributeError:
        raise
    return idf


@pytest.fixture()
def base_idf():
    iddsnippet = iddcurrent.iddtxt
    iddfhandle = StringIO(iddsnippet)
    if IDF.getiddname() == None:
        IDF.setiddname(iddfhandle)
    idftxt = ""
    idfhandle = StringIO(idftxt)
    idf = IDF(idfhandle)
    return idf


@pytest.fixture()
def building(base_idf):
    """A building fixture created from base_idf and which adds a Zone, and a
    BuildingSurface:Detailed object

    Args:
        base_idf (IDF): The Base IDF created by the :func:`base_idf` fixture.
    """
    base_idf.newidfobject("Zone".upper(), Name="West Zone", defaultvalues=True)
    base_idf.newidfobject(
        "BuildingSurface:Detailed",
        Name="West Floor",
        Zone_Name="West Zone",
        Surface_Type="Floor",
        Vertex_1_Xcoordinate=0,
        Vertex_1_Ycoordinate=0,
        Vertex_1_Zcoordinate=0,
        Vertex_2_Xcoordinate=0,
        Vertex_2_Ycoordinate=10,
        Vertex_2_Zcoordinate=0,
        Vertex_3_Xcoordinate=10,
        Vertex_3_Ycoordinate=10,
        Vertex_3_Zcoordinate=0,
        Vertex_4_Xcoordinate=10,
        Vertex_4_Ycoordinate=0,
        Vertex_4_Zcoordinate=0,
    )
    yield base_idf
