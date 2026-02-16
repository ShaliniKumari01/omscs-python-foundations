def word_frequency(text: str) -> dict[str, int]:
    freq: dict[str, int] = {}
    current: list[str] = []

    for ch in text.lower():
        if ch.isalnum():
            current.append(ch)
        else:
            if current:
                w = "".join(current)
                freq[w] = freq.get(w, 0) + 1
                current = []

    if current:  # flush last word
        w = "".join(current)
        freq[w] = freq.get(w, 0) + 1

    return freq


if __name__ == "__main__":
    sample = "To be, or not to be: that is the question."
    print("Input:", sample)
    print("Output:", word_frequency(sample))
