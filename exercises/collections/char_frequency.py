def char_frequency(text: str) -> dict[str, int]:
    freq: dict[str, int] = {}

    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1

    return freq


if __name__ == "__main__":
    sample = "mississippi"
    print("Input:", sample)
    print("Output:", char_frequency(sample))
