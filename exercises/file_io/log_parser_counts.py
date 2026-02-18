def count_log_levels(lines: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {"INFO": 0, "WARN": 0, "ERROR": 0}
    for line in lines:
        line = line.strip()
        if line.startswith("INFO"):
            counts["INFO"] += 1
        elif line.startswith("WARN"):
            counts["WARN"] += 1
        elif line.startswith("ERROR"):
            counts["ERROR"] += 1
    return counts


def read_lines(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


if __name__ == "__main__":
    sample_path = "sample.log"
    sample = [
        "INFO App started\n",
        "WARN Disk is almost full\n",
        "ERROR Failed to connect\n",
        "INFO Request handled\n",
    ]
    with open(sample_path, "w", encoding="utf-8") as f:
        f.writelines(sample)

    lines = read_lines(sample_path)
    print("Counts:", count_log_levels(lines))
