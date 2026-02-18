from exercises.functions.safe_divide import safe_divide

def test_safe_divide_normal():
    assert safe_divide(10, 2) == 5

def test_safe_divide_zero():
    assert safe_divide(10, 0) is None
