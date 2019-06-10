"""File to hold pytest fixtures to avoid boilerplate in tests."""
import pytest
from six import StringIO

from eppy.modeleditor import IDF
from eppy.iddcurrent import iddcurrent


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
