def reverse_string(text: str) -> str:
    result = ""
    for ch in text:
        result = ch + result
    return result


if __name__ == "__main__":
    sample = "Shalini"
    print("Input:", sample)
    print("Output:", reverse_string(sample))