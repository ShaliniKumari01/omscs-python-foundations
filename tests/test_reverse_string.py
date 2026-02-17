from exercises.basics.reverse_string import reverse_string


def test_reverse_string_basic():
    assert reverse_string("Shalini") == "inilahS"


def test_reverse_string_empty():
    assert reverse_string("") == ""


def test_reverse_string_spaces():
    assert reverse_string("a b") == "b a"
