def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}  # value -> index
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return (seen[need], i)
        seen[x] = i
    return None


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9
    print("Input:", nums, "target=", target)
    print("Output:", two_sum(nums, target))  # (0, 1)
