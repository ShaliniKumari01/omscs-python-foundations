from exercises.collections.char_frequency import char_frequency


def test_char_frequency_counts():
    freq = char_frequency("mississippi")
    assert freq["m"] == 1
    assert freq["i"] == 4
    assert freq["s"] == 4
    assert freq["p"] == 2
