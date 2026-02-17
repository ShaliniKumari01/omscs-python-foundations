from exercises.dicts_sets.word_frequency import word_frequency


def test_word_frequency_basic():
    text = "To be, or not to be."
    freq = word_frequency(text)

    assert freq["to"] == 2
    assert freq["be"] == 2
    assert freq["or"] == 1
    assert freq["not"] == 1
