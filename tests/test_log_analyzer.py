from mini_apps.log_analyzer.analyzer import analyze_lines, analyze_file, write_csv


def test_analyze_lines_counts_and_top_errors():
    lines = [
        "INFO Started job id=1\n",
        "WARN Cache miss key=abc\n",
        "ERROR Payment failed user=123\n",
        "ERROR Payment failed user=123\n",
        "ERROR Timeout contacting service X\n",
        "DEBUG this line should be ignored\n",
        "\n",
    ]

    report = analyze_lines(lines, top_n=2)

    assert report.total_lines == 7
    assert report.parsed_lines == 5  # INFO/WARN/ERROR only

    assert report.level_counts["INFO"] == 1
    assert report.level_counts["WARN"] == 1
    assert report.level_counts["ERROR"] == 3

    assert report.top_errors[0] == ("Payment failed user=123", 2)
    assert report.top_errors[1] == ("Timeout contacting service X", 1)


def test_analyze_file(tmp_path):
    p = tmp_path / "app.log"
    p.write_text(
        "INFO Boot\n"
        "ERROR Boom\n"
        "ERROR Boom\n"
        "WARN Be careful\n",
        encoding="utf-8",
    )

    report = analyze_file(str(p), top_n=5)
    assert report.level_counts["INFO"] == 1
    assert report.level_counts["WARN"] == 1
    assert report.level_counts["ERROR"] == 2
    assert report.top_errors[0] == ("Boom", 2)


def test_write_csv(tmp_path):
    lines = [
        "INFO Boot\n",
        "ERROR Boom\n",
        "ERROR Boom\n",
    ]
    report = analyze_lines(lines, top_n=3)

    out = tmp_path / "report.csv"
    write_csv(str(out), report)

    content = out.read_text(encoding="utf-8").strip().splitlines()
    assert content[0] == "section,key,value"
    # Must contain level rows
    assert "levels,INFO,1" in content
    assert "levels,ERROR,2" in content
    # Must contain top error row
    assert "top_errors,Boom,2" in content