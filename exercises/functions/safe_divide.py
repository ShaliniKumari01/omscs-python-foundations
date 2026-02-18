def safe_divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b


if __name__ == "__main__":
    print(safe_divide(10, 2))   # 5.0
    print(safe_divide(10, 0))   # None
