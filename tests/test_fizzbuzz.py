from exercises.loops.fizzbuzz import fizzbuzz


def test_fizzbuzz_1_to_5():
    assert fizzbuzz(5) == ["1", "2", "Fizz", "4", "Buzz"]


def test_fizzbuzz_15():
    out = fizzbuzz(15)
    assert out[14] == "FizzBuzz"  # 15th item
