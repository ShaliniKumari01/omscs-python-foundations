from __future__ import annotations


def write_people_csv(path: str, rows: list[tuple[str, int]]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write("name,age\n")
        for name, age in rows:
            f.write(f"{name},{age}\n")


def read_people_csv(path: str) -> list[tuple[str, int]]:
    people: list[tuple[str, int]] = []

    with open(path, "r", encoding="utf-8") as f:
        header = f.readline()  # consume header
        for line in f:
            line = line.strip()
            if not line:
                continue
            name, age_str = line.split(",", 1)
            people.append((name, int(age_str)))

    return people


if __name__ == "__main__":
    data = [("Shalini", 30), ("Avi", 35), ("Mia", 3)]
    path = "people.csv"  # writes into repo root when you run script

    write_people_csv(path, data)
    loaded = read_people_csv(path)

    print("Wrote:", data)
    print("Read :", loaded)
