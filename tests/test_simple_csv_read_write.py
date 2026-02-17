from exercises.file_io.simple_csv_read_write import write_people_csv, read_people_csv


def test_csv_roundtrip(tmp_path):
    path = tmp_path / "people.csv"
    rows = [("Shalini", 30), ("Avi", 35), ("Mia", 3)]

    write_people_csv(str(path), rows)
    loaded = read_people_csv(str(path))

    assert loaded == rows
