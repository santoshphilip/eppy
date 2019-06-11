import pytest


@pytest.mark.parametrize("key", ["BUILDING", "Building", "building", "BuIlDiNg"])
def test_get_and_set(base_idf, key):
    idf = base_idf
    idf.newidfobject(key, Name="Building")
    buildings = idf.idfobjects["building"]
    assert len(buildings) == 1


@pytest.mark.parametrize("key", ["BUILDING", "Building", "building", "BuIlDiNg"])
def test_contains(base_idf, key):
    idf = base_idf
    idf.newidfobject(key, Name="Building")
    assert key in idf.idfobjects


@pytest.mark.parametrize("key", ["BUILDING", "Building", "building", "BuIlDiNg"])
def test_del(base_idf, key):
    idf = base_idf
    idf.newidfobject(key, Name="Building")
    assert key in idf.idfobjects
    del idf.idfobjects["building"]
    assert key not in idf.idfobjects
