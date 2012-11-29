import foo
from pytest_helpers import almostequal

def test_foo():
    a = 5
    answer = 1.667
    result = foo.div3(a)
    assert almostequal(answer, result, places=2) == True
