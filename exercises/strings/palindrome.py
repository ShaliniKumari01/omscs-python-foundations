def is_palindrome(text: str) -> bool:
    cleaned_chars: list[str] = []
    for ch in text.lower():
        if ch.isalnum():
            cleaned_chars.append(ch)

    cleaned = "".join(cleaned_chars)
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    samples = [
        "racecar",
        "Shalini",
        "A man, a plan, a canal: Panama",
        "No 'x' in Nixon",
    ]
    for s in samples:
        print(f"{s!r} -> {is_palindrome(s)}")
