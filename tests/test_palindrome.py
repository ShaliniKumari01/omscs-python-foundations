from exercises.strings.palindrome import is_palindrome


def test_palindrome_simple():
    assert is_palindrome("racecar") is True
    assert is_palindrome("Shalini") is False


def test_palindrome_normalized():
    assert is_palindrome("A man, a plan, a canal: Panama") is True
    assert is_palindrome("No 'x' in Nixon") is True
