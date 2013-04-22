"""py.test for class IDF0"""

from modeleditor import IDF0

def test_IDF0():
    """py.test for class IDF0"""
    assert IDF0.iddname == None
    IDF0.setiddname("gumby")
    assert IDF0.iddname == "gumby"
    IDF0.setiddname("karamba")
    assert IDF0.iddname != "karamba"
    assert IDF0.iddname == "gumby"
