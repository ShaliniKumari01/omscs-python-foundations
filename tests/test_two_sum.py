from exercises.dicts_sets.two_sum import two_sum

def test_two_sum_found():
    assert two_sum([2, 7, 11, 15], 9) == (0, 1)

def test_two_sum_not_found():
    assert two_sum([1, 2, 3], 10) is None
