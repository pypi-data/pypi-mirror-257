from minimal_python_project_skeleton import increment


def test_int():
    assert increment(3) == 4


def test_float():
    assert increment(3.0) == 4.0
