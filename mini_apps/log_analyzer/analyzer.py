from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
from collections import Counter
from typing import Iterable


LEVELS = ("INFO", "WARN", "ERROR")


@dataclass(frozen=True)
class Report:
    level_counts: dict[str, int]
    top_errors: list[tuple[str, int]]
    total_lines: int
    parsed_lines: int


def parse_level(line: str) -> str | None:
    """
    Return log level if the line starts with INFO/WARN/ERROR.
    Expected format examples:
      "ERROR Payment failed user=123"
      "INFO Started job id=9"
    """
    if not line:
        return None
    
    s = line.strip()
    if not s:
        return None
    
    
    first = line.strip().split(maxsplit=1)[0].upper()
    return first if first in LEVELS else None


def extract_error_message(line: str) -> str | None:
    """
    If line starts with ERROR, return the message part after the level token.
    If message is empty, return None.
    """
    lvl = parse_level(line)
    if lvl != "ERROR":
        return None
    parts = line.strip().split(maxsplit=1)
    if len(parts) < 2:
        return None
    return parts[1].strip() or None


def analyze_lines(lines: Iterable[str], top_n: int = 5) -> Report:
    """
    Analyze an iterable of log lines.
    Returns:
      - counts of INFO/WARN/ERROR
      - top N ERROR messages
      - total_lines, parsed_lines (lines recognized with a level)
    """
    level_counter: Counter[str] = Counter()
    error_counter: Counter[str] = Counter()

    total = 0
    parsed = 0

    for raw in lines:
        total += 1
        lvl = parse_level(raw)
        if lvl is None:
            continue
        parsed += 1
        level_counter[lvl] += 1

        msg = extract_error_message(raw)
        if msg:
            error_counter[msg] += 1

    # Ensure all levels exist in output dict
    level_counts = {lvl: int(level_counter.get(lvl, 0)) for lvl in LEVELS}
    top_errors = error_counter.most_common(top_n)

    return Report(
        level_counts=level_counts,
        top_errors=top_errors,
        total_lines=total,
        parsed_lines=parsed,
    )


def analyze_file(path: str, top_n: int = 5) -> Report:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Log file not found: {path}")

    with p.open("r", encoding="utf-8", errors="replace") as f:
        return analyze_lines(f, top_n=top_n)


def write_csv(path: str, report: Report) -> None:
    """
    Write a summary CSV.

    Sections:
      - level counts
      - top errors
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)

        w.writerow(["section", "key", "value"])

        w.writerow(["meta", "total_lines", report.total_lines])
        w.writerow(["meta", "parsed_lines", report.parsed_lines])

        for lvl in LEVELS:
            w.writerow(["levels", lvl, report.level_counts.get(lvl, 0)])

        # Top errors
        if report.top_errors:
            for msg, count in report.top_errors:
                w.writerow(["top_errors", msg, count])
        else:
            w.writerow(["top_errors", "(none)", 0])