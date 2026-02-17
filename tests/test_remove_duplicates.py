from exercises.lists_tuples.remove_duplicates_preserve_order import (
    remove_duplicates_preserve_order,
)


def test_remove_duplicates_preserve_order():
    assert remove_duplicates_preserve_order([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_remove_duplicates_empty():
    assert remove_duplicates_preserve_order([]) == []
