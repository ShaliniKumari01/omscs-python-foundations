from __future__ import annotations

import argparse
from mini_apps.log_analyzer.analyzer import analyze_file, write_csv, LEVELS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="log_analyzer", description="Analyze a log file (counts + top errors).")
    parser.add_argument("path", help="Path to a .log file")
    parser.add_argument("--top", type=int, default=5, help="How many top ERROR messages to show (default: 5)")
    parser.add_argument("--csv", dest="csv_path", default=None, help="Optional output CSV path")

    args = parser.parse_args(argv)

    report = analyze_file(args.path, top_n=args.top)

    print(f"File: {args.path}")
    print(f"Total lines: {report.total_lines}")
    print(f"Parsed lines: {report.parsed_lines}")
    print("Level counts:")
    for lvl in LEVELS:
        print(f"  {lvl:<5} {report.level_counts.get(lvl, 0)}")

    print(f"Top {args.top} errors:")
    if not report.top_errors:
        print("  (none)")
    else:
        for msg, count in report.top_errors:
            print(f"  {count:>3}  {msg}")

    if args.csv_path:
        write_csv(args.csv_path, report)
        print(f"Wrote CSV: {args.csv_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())