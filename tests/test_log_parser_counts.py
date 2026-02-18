from exercises.file_io.log_parser_counts import count_log_levels

def test_count_log_levels():
    lines = [
        "INFO one\n",
        "WARN two\n",
        "ERROR three\n",
        "INFO four\n",
        "DEBUG ignored\n",
    ]
    assert count_log_levels(lines) == {"INFO": 2, "WARN": 1, "ERROR": 1}
