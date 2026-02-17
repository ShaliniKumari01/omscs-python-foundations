def remove_duplicates_preserve_order(items: list[int]) -> list[int]:
    seen: set[int] = set()
    result: list[int] = []

    for x in items:
        if x not in seen:
            seen.add(x)
            result.append(x)

    return result


if __name__ == "__main__":
    sample = [3, 1, 3, 2, 1, 5, 2, 2, 6]
    print("Input:", sample)
    print("Output:", remove_duplicates_preserve_order(sample))
