# Copyright (c) 2016 Santosh Philip
# =======================================================================
#  Distributed under the MIT License.
#  (See accompanying file LICENSE or copy at
#  http://opensource.org/licenses/MIT)
# =======================================================================
"""integration tests for eppy"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from itertools import product
import os
import shutil
import sys

from eppy.modeleditor import IDF
from eppy.pytest_helpers import IDD_FILES
from eppy.pytest_helpers import INTEGRATION_FILES
from eppy.pytest_helpers import PATH_TO_EPPY
from eppy.pytest_helpers import do_integration_tests
import pytest


sys.path.append(PATH_TO_EPPY)


def getversion(idf):
    """return the version number"""
    versions = idf.idfobjects["VERSION"]
    return versions[0].Version_Identifier


def setversion(idf, newversion):
    """set the version number"""
    versions = idf.idfobjects["VERSION"]
    versions[0].Version_Identifier = newversion


@pytest.mark.skipif(
    not do_integration_tests(), reason="$EPPY_INTEGRATION env var not set"
)
class TestModeleditorIntegration:
    def setup(self):
        """Set the IDD and file paths, and make a copy of the original file."""
        iddfile = os.path.join(IDD_FILES, "Energy+V7_2_0.idd")
        IDF.setiddname(iddfile, testing=True)

        self.origfile = os.path.join(INTEGRATION_FILES, "origfile.idf")

        # set tempfile names
        self.startfile = os.path.join(INTEGRATION_FILES, "startfile.idf")
        self.saveasfile = os.path.join(INTEGRATION_FILES, "saveas.idf")
        self.copyfile = os.path.join(INTEGRATION_FILES, "savecopy.idf")

        # make a copy of test file
        shutil.copy(self.origfile, self.startfile)

    def teardown(self):
        """Clear up temp files so we don't accidentally check against them."""
        tempfiles = [self.startfile, self.saveasfile, self.copyfile]
        for f in tempfiles:
            try:
                os.remove(f)
            except OSError:
                pass

    def test_version_number(self):
        """Test opening an IDF file and checking version number.

        Fails if the version number is not the expected starting version number.

        """
        idf = IDF(self.startfile)

        result = getversion(idf)
        expected = "7.3"

        assert result == expected

    def test_save(self):
        """Test save with a changed version number.

        Fails if the version number has not been changed.

        """
        idf = IDF(self.startfile)
        setversion(idf, "7.4")
        idf.save()
        idf2 = IDF(self.startfile)
        assert idf is not idf2  # be sure we don't just have an in-memory copy

        result = getversion(idf2)
        expected = "7.4"

        assert result == expected

    def test_save_as(self):
        """Test saveas with a changed filename.

        IDF.saveas(fname) changes the filename. The next save should save with
        new name.

        Fails if the filename isn't changed on the file with the new name.
        """
        idf = IDF(self.startfile)
        idf.saveas(self.saveasfile)  # sets the new filename
        setversion(idf, "7.4")
        idf.save()  # should also save with the new filename
        idf2 = IDF(self.saveasfile)

        result = getversion(idf2)
        expected = "7.4"

        assert result == expected

    def test_save_copy(self):
        """Test savecopy with a new filename.

        IDF.savecopy(fname) doesn't change the filename. The next save should
        save with the original name.

        Fails if on a following save, the copy is changed.

        """
        idf = IDF(self.startfile)
        idf.savecopy(self.copyfile)
        setversion(idf, "7.5")
        idf.save()
        idf2 = IDF(self.copyfile)

        result = getversion(idf2)
        expected = "7.3"  # unchanged since version was changed after savecopy

        assert result == expected

        idf3 = IDF(self.startfile)
        result = getversion(idf3)
        expected = "7.5"  # should be changed in the original file

        assert result == expected

    def test_lineendings(self):
        """Test lineendings are set correctly on each platform."""
        idf = IDF(self.startfile)
        idf.save(lineendings="windows")
        with open(self.startfile, "rb") as sf:
            txt = sf.read()
        print(txt.count(b"\r\n"))
        lines = txt.splitlines()
        numlines = len(lines)
        assert numlines == txt.count(b"\r\n") + 1  # no CR on last line
        idf.save(lineendings="unix")
        with open(self.origfile, "rb") as of:
            txt = of.read()
        lines = txt.splitlines()
        numlines = len(lines)
        assert numlines == txt.count(b"\n") + 1  # no CR on last line

    def test_save_with_lineendings_and_encodings(self):
        """
        Test the IDF.save() function with combinations of encodings and line
        endings.

        """
        idf = IDF(self.startfile)
        lineendings = ("windows", "unix", "default")
        encodings = ("ascii", "latin-1", "UTF-8")

        for le, enc in product(lineendings, encodings):
            idf.save(lineendings=le, encoding=enc)

            with open(self.startfile, "rb") as sf:
                result = sf.read()
            if le == "windows":
                assert b"\r\n" in result
            elif le == "unix":
                assert b"\r\n" not in result
            elif le == "default":
                assert os.linesep.encode(enc) in result
